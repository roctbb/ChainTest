import time
import tornado.ioloop
import tornado.web
import json
from threading import Thread
from gchain import verify, makeBlock, echo
import requests

first_block = {"number": 0, "time": time.time() // 1000, "data": "initial block", "hash": "0"}

chain = [first_block]
network = ["http://localhost:8881", "http://localhost:8882", "http://localhost:8883"]
local = "http://localhost"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(chain))


def dataObserver():
    global chain
    while True:
        data = input()
        chain.append(makeBlock(chain, data))
        print("add new block: {}".format(chain))


def updateObserver():
    global chain
    while True:
        for node in network:
            if node == local:
                continue
            try:
                result = requests.get(node)
                new_chain = result.json()
                if len(new_chain) > len(chain):
                    print("updating chain from {}".format(node))
                    print("ours: {}".format(chain))
                    print("theirs: {}".format(new_chain))
                    conflict = False
                    error = False
                    for i in range(len(chain)):
                        if new_chain[i]["number"] == chain[i]["number"] and new_chain[i]['hash'] != chain[i]['hash']:
                            print("break in {}".format(i))
                            if chain[i]["time"]+2*60 < new_chain[i]['time']:
                                error = True
                                break
                            conflict = True
                            break
                    if error:
                        print('received incorrect chain (time) from {}'.format(node))
                    if conflict:
                        buf_chain = chain[:i] + new_chain[i:]
                        non_chain = chain[i:]
                    else:
                        buf_chain = chain + new_chain[len(chain):]
                        non_chain = []
                    if not verify(buf_chain):
                        print('received incorrect chain (check) from {}'.format(node))
                    else:
                        chain = buf_chain
                        for block in non_chain:
                            chain.append(makeBlock(chain, block['data']))
                        print('updated chain from {}'.format(node))
                        print('new chain: {}'.format(chain))
                        echo(chain)
            except:
                pass
        time.sleep(3)


port = int(input("enter port:"))
local = local + ":{}".format(port)
app = tornado.web.Application([
    (r"/", MainHandler),
])
app.listen(port)

input_thread = Thread(target=dataObserver)
update_thread = Thread(target=updateObserver)

input_thread.start()
update_thread.start()
tornado.ioloop.IOLoop.current().start()
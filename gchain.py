import hashlib as hasher
import time

def verify(blockchain):
    for i in range(1, len(blockchain)):
        if blockchain[i]['number'] - 1 != blockchain[i - 1]['number']:
            return False
        sha = hasher.sha256()
        sha.update("{}{}{}{}".format(blockchain[i]['number'], blockchain[i]['time'], blockchain[i]['data'],
                                     blockchain[i - 1]['hash']).encode('utf-8'))
        hash = sha.hexdigest()
        if blockchain[i]['hash'] != hash:
            return False
    return True


def makeBlock(blockchain, data):
    previous = blockchain[-1]
    block = {}
    block["number"] = previous["number"] + 1
    block["time"] = time.time() // 1000
    block["data"] = data

    sha = hasher.sha256()
    sha.update("{}{}{}{}".format(block['number'], block['time'], block['data'], previous['hash']).encode('utf-8'))

    block["hash"] = sha.hexdigest()

    return block

def echo(chain):
    for block in chain:
        print("{} - {}".format(block["number"], block['data']))
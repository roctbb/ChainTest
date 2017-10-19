import hashlib as hasher

word = "dog"

sha256 = hasher.sha256()
for i in range(1, 1000000000):
    if i % 10000000 == 0:
        print(i)
    sha256.update("fog{}".format(i).encode('utf-8'))

    if str(sha256.hexdigest())[0:6] == "000000":
        break
print(i)
print("found {}".format(sha256.hexdigest()))


import os
import time
import datetime
import model.KeyGenerator as KeyGenerator


def body_encrypt():
    f = open('chat.txt','r')
    message = f.read()
    print(message)
    data = KeyGenerator.encrypt(message.encode('utf-8'))

    return data


def brick_hash(data):
    data_encoding = data.encode('utf-8')
    hash, signature, public_key = KeyGenerator.sign(data_encoding)
    return str(hash), signature, public_key


def brick(non, index):
    f = open('block.txt', 'a+t')
    fr = open('block.txt', 'r')
    KeyGenerator.create_key()
    sf = open('hash.txt', 'a+t')
    sfr = open('hash.txt', 'r')
    if os.stat('block.txt').st_size ==0 or os.stat('hash.txt').st_size == 0:

        dict = {
            "index" : 0,
            "previous": "0",
            "time" : datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
            "transaction_list" : body_encrypt(),
            "nonce" : non,
            "block producer" : 'miner1'
        }
        f.writelines(str(dict))
        f.writelines('\n')

        hash, signature, public_key = brick_hash(str(dict))
        sf.writelines(hash)
        sf.writelines('\n')
        print("done")

    else:
        last_dict = fr.readlines()[-1].rstrip()
        hash, signature, public_key = brick_hash(last_dict)

        last_hash = sfr.readlines()[-1].rstrip()
        if hash == last_hash:
            sign = KeyGenerator.validation(last_dict.encode('utf-8'), signature, public_key)
            if sign == True:

                dict = {
                    "index" : index,
                    "previous": last_hash,
                    "time": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    "transaction_list": body_encrypt(),
                    "nonce" : non,
                    "block producer" : 'miner1'
                }

                f.writelines(str(dict))
                f.writelines('\n')

                hash, signature, public_key = brick_hash(str(dict))

                sf.writelines(hash)
                sf.writelines('\n')

                print("done")
            else:
                print("sign error")
        else:
            print("hash error")
    return index

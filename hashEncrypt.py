import hashlib
import os
import sys

import numpy as np
from PIL import Image

sha512 = lambda text: hashlib.sha512(text.encode()).hexdigest()


def hashEncrypt(image, key):
    array = np.array(image, dtype=np.uint8)
    shape = array.shape
    array = array.flatten()
    nums = []
    hashed = key
    for i in range(len(array) // 64):
        hashed = sha512(hashed)
        nums.extend([int(hashed[i : i + 2], 16) for i in range(0, 127, 2)])
    nums.extend(
        [int(sha512(hashed)[i : i + 2], 16) for i in range(0, 127, 2)][
            : (len(array) % 64)
        ]
    )
    print(nums[:100])
    array = np.bitwise_xor(array, np.array(nums, np.uint8))
    array = np.bitwise_xor(array, np.array(nums[::-1], np.uint8))
    return Image.fromarray(array.reshape(shape))


shuffixes = ("png", "bmp")


def encryptFolder(folder, key):
    for i in os.listdir(folder):
        cur = os.path.join(folder, i)
        if not os.path.isdir(cur):
            if i.lower().split(".")[-1] == "png":
                hashEncrypt(Image.open(cur), key).save(cur)
        else:
            encryptFolder(cur, key)


if __name__ == "__main__":
    input_path = sys.argv[1]
    key = sys.argv[2]
    if not os.path.isdir(input_path):
        output_path = sys.argv[3]
        hashEncrypt(Image.open(input_path), key).save(input_path)
    else:
        encryptFolder(input_path, key)

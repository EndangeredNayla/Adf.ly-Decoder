# ============================================
# Adf.ly Decoder
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 1/29/23
# License: MIT
# ============================================
import argparse
import os
import re
import sys
import urllib.parse

from base64 import b64decode
from urllib.request import urlopen, Request


def parse_args():
    parser = argparse.ArgumentParser(
        description='Adf.ly Decoder')
    parser.add_argument('-u', '--url', type=str, required=True, metavar="url", help='Parse Adfly link and give download URL.')
    args = parser.parse_args()
    return args

def decrypt(code):
    ''' decrypt the given adf.ly encrypted ysmm '''

    zeros, ones = '', ''
    for num, letter in enumerate(code):
        if num % 2 == 0: zeros += code[num]
        else: ones = code[num] + ones

    key = list(zeros + ones)
    i=0
    while i != len(key):
        hlp=0
        if str(key[i]).isnumeric():
            for y in range(i+1,len(key)):
                if str(key[y]).isnumeric():
                    hlp=hlp+1
                    temp=int(key[i])^int(key[y])
                    if int(temp) < 10:
                        key[i]=str(temp)
                    i=y+1
                    break
        if hlp==0:
            i=i+1
    temp="".join(key)
    key=temp
    key = b64decode(key.encode("utf-8"))
    return key.decode('utf-8')

def download_manifest(url):
    if "http" not in url:
        url = "https://" + url
    req = Request(url, headers={'User-Agent': 'Chrome/91.0.4472.77'})
    data_ = urlopen(req)
    data = data_.read()
    ysmm = data.split(b"ysmm = '")[1].split(b"';")[0]
    decrypted_url = decrypt(ysmm.decode('utf-8')) # Decrypt the URL
    decrypted_url=decrypted_url[16:-16]
    decrypted_url = urllib.parse.unquote(decrypted_url)
    try:
        m = re.search ( r'&dest=(.*)', decrypted_url)
        decrypted_url = m.group(1)
    except:
        pass
    print(decrypted_url)

if __name__ == "__main__":
    download_manifest(parse_args().url)
import argparse
import os
import struct
import sys

path = os.getcwd() +'\\music'

def check_arg(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--source',
                        help='source directory',
                        required='True',
                        default='None')
    parser.add_argument('-d', '--dumpp',
                        help='show tag dump',
                        default='None')
    parser.add_argument('-g', '--genre',
                        help='genre of music',
                        default='12')

    parsed = parser.parse_args(args)
    return parsed.source, parsed.dumpp, parsed.genre

def decoding():
    mypath, dumpp, genre = check_arg(sys.argv[1:])

    music_files = os.listdir(path=path)

    for i, music in enumerate(music_files):
        with open(music, "rb+", 0) as f:
            f.seek(-1, 2)
            f.write(bytes([17]))
            f.seek(-2, 2)
            f.write(bytes([i + 1]))
            f.seek(-3, 2)
            f.write(bytes([0]))

    tags = []
    for music in music_files:
         with open(music, "rb", 0) as f:
            f.seek(-128, 2)
            tags.append(f.read(128))

    for tag in tags:
        title = (struct.unpack('30s', tag[3:33]))[0].decode('utf-8').strip()
        artist = (struct.unpack('30s', tag[33:63]))[0].decode('utf-8').strip()
        album = (struct.unpack('30s', tag[63:93]))[0].decode('utf-8').strip()
        print('[{}] - [{}] - [{}]'.format(artist, title, album))

    if (dumpp == 'yes'):
        for tag in tags:
            hexdump = ' '.join([hex(byte) for byte in tag])
            print(hexdump + '\n')

decoding()
import argparse


parser = argparse.ArgumentParser(description='Process crawler.')


parser.add_argument('-saveDir', type=str, default='./imgs/save/',
                    help='save location of pic')

parser.add_argument('-garbageDir', type=str, default='./imgs/garbage/',
                    help='save location (no need) of pic')

parser.add_argument('-saveVideoDir', type=str, default='./videos/',
                    help='save location of pic')


args = parser.parse_args()


print(args)

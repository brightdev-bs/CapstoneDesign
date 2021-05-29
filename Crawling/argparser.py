import argparse


#argparse로 매개변수 받는 코드

parser = argparse.ArgumentParser(description='Process crawler.')

parser.add_argument('-saveDir', type=str, default='./imgs/image/',
                    help='save location of pic')

parser.add_argument('-garbageDir', type=str, default='./imgs/garbage/',
                    help='save location (no need) of pic')

parser.add_argument('-saveVideoDir', type=str, default='./videos/',
                    help='save location of video')

parser.add_argument('-DBfileDir', type=str, default='./imgs/save/',
                    help='repository of pic')


args = parser.parse_args()


print(args)

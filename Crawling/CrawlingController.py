import DCImage
import getvideo


from multiprocessing import Process, Queue


if __name__ == "__main__":
    th1 = DCImage._DCImage()
    th2 =getvideo._Video()
    try:
        th1.start()
        th2.start()
    except Exception as E:
        print(e)
   
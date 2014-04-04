import pymouse
import time

if __name__ == '__main__':
    mouse = pymouse.PyMouse()
    begin = time.time()
    origin = mouse.position()
    print 't x y'
    try:
        while True:
            pos = mouse.position()
            print time.time() - begin, pos[0] - origin[0], pos[1] - origin[1]
    except KeyboardInterrupt:
        pass

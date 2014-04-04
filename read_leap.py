import os, sys
import time

this_dir = os.path.dirname(os.path.realpath(__name__))
sys.path.insert(0, os.path.join(this_dir, 'libs', 'leap'))

import Leap

class MyListener(Leap.Listener):
    """
    Basic Leap listener printing acquired data with only *nb_hands* hands and
    *nb_fingers* fingers.
    """
    def __init__(self, nb_hands, nb_fingers):
        super(MyListener, self).__init__()
        self.nb_hands = nb_hands
        self.nb_fingers = nb_fingers

    def on_init(self, controller):
        """
        Print the header of a CSV output corresponding to the read data of the
        leap motion.
        """
        nor = lambda h: 'H%d_NorX H%d_NorY H%d_NorZ' % (h, h, h)
        vel = lambda h: 'H%d_VelX H%d_VelY H%d_VelZ' % (h, h, h)
        pos = lambda h: 'H%d_PosX H%d_PosY H%d_PosZ' % (h, h, h)
        dir = lambda h: 'H%d_DirX H%d_DirY H%d_DirZ' % (h, h, h)
        cen = lambda h: 'H%d_CenX H%d_CenY H%d_CenZ' % (h, h, h)
        rad = lambda h: 'H%d_Rad' % h
        use = [nor, vel, pos, dir]
        print ' '.join(' '.join(map(lambda f: f(h), use))
                for h in xrange(self.nb_hands))

    def on_frame(self, controller):
        """
        Read data from the leap motion and print it on stdout with space as
        separator.
        """

        frame = controller.frame()

        # Limit the acquisition
        if len(frame.hands) != self.nb_hands:
            return
        if not all(len(h.fingers) == self.nb_fingers for h in frame.hands):
            return

        vec_to_str = lambda v: '%f %f %f' % (v.x, v.y, v.z)

        for h in frame.hands:
            nor = vec_to_str(h.palm_normal)
            vel = vec_to_str(h.palm_velocity)
            pos = vec_to_str(h.palm_position)
            dir = vec_to_str(h.direction)
            cen = vec_to_str(h.sphere_center)
            rad = str(h.sphere_radius)
            use = [nor, vel, pos, dir]
            print ' '.join(use)

if __name__ == '__main__':
    nb_hands = 1
    nb_fingers = 1

    ctrl = Leap.Controller()
    listener = MyListener(nb_hands, nb_fingers)
    ctrl.add_listener(listener)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        ctrl.remove_listener(listener)

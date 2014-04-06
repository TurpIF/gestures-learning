#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
this_dir = os.path.dirname(os.path.realpath(__name__))
sys.path.insert(0, os.path.join(this_dir, 'libs', 'leap'))

import Leap
import time
from sklearn import neighbors

from learner_finger import FingerMove, FingerPoint
from learner_finger import wait_move

if __name__ == '__main__':
    size = 100
    move_files = ['leap_assets/left.mv', 'leap_assets/right.mv',
                'leap_assets/up.mv', 'leap_assets/down.mv',
                'leap_assets/front.mv', 'leap_assets/back.mv',
                'leap_assets/circle.mv',
                'leap_assets/null.mv']
    moves = []
    for f_name in move_files:
        with open(f_name, 'r') as f:
            for l in f:
                moves.append(FingerMove.from_string(l))

    XY = map(lambda x: x.to_tuple(), moves)
    XY = map(lambda x: (x[1:1 + size * 9], x[0]), XY)
    X, Y = zip(*XY)

    learner = neighbors.KNeighborsClassifier(
            n_neighbors=5, weights='distance')
    predictor = learner.fit(X, Y)

    ctrl = Leap.Controller()
    while not ctrl.is_connected:
        time.sleep(0.001)

    try:
        while True:
            wait_move(ctrl)
            hist = []
            frame = ctrl.frame()
            finger = frame.hands[0].fingers[0]
            o_pos = finger.tip_position.x, \
                finger.tip_position.y, \
                finger.tip_position.z
            for _ in xrange(size):
                f_pos = finger.tip_position.x, \
                    finger.tip_position.y, \
                    finger.tip_position.z
                f_vel = finger.tip_velocity.x, \
                    finger.tip_velocity.y, \
                    finger.tip_velocity.z
                f_dir = finger.direction.x, \
                    finger.direction.y, \
                    finger.direction.z
                f_dpos = map(lambda x: x[0] - x[1], zip(f_pos, o_pos))
                point = FingerPoint(f_dpos, f_vel, f_dir)
                hist.append(point)
                time.sleep(0.005)

            X = sum(map(lambda x: list(x.to_tuple()), hist), [])
            print predictor.predict(X)[0]
    except KeyboardInterrupt:
        pass

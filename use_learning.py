#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymouse
import time
from sklearn import neighbors

from learner_mouse import Move
from learner_mouse import wait_mouse_move

if __name__ == '__main__':
    size = 100
    move_files = ['assets/left.mv', 'assets/right.mv',
                'assets/up.mv', 'assets/down.mv',
                'assets/lt_rd.mv', 'assets/rt_ld.mv',
                'assets/ld_rt.mv', 'assets/rd_lt.mv',
                'assets/circle.mv',
                'assets/a.mv', 'assets/v.mv',
                'assets/<.mv', 'assets/>.mv',
                'assets/s.mv',
                'assets/z.mv',
                'assets/null.mv']
    moves = []
    for f_name in move_files:
        with open(f_name, 'r') as f:
            for l in f:
                moves.append(Move.from_string(l))

    X = map(lambda x: x.descr[:size], moves)
    X = map(lambda x: tuple(sum(map(list, x), [])), X)
    Y = map(lambda x: x.name, moves)

    learner = neighbors.KNeighborsClassifier(
            n_neighbors=5, weights='distance')
    predictor = learner.fit(X, Y)

    mouse = pymouse.PyMouse()
    hist_origin = []
    try:
        while True:
            wait_mouse_move()
            hist_origin = []
            for _ in xrange(size):
                pos = mouse.position()
                hist_origin.append(pos)
                time.sleep(0.005)

            o = hist_origin[0]
            X = map(lambda x: (x[0] - o[0], x[1] - o[1]), hist_origin)
            X = tuple(sum(map(list, X), []))
            hist_origin = hist_origin[1:]
            print predictor.predict(X)[0]
    except KeyboardInterrupt:
        pass

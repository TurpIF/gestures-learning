#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymouse
import time
from sklearn import neighbors

from learner_mouse import Move

if __name__ == '__main__':
    size = 20
    move_files = ['assets/left.mv', 'assets/up.mv', 'assets/down.mv',
            'assets/right.mv', 'assets/null.mv']
    moves = []
    for f_name in move_files:
        with open(f_name, 'r') as f:
            for l in f:
                moves.append(Move.from_string(l))

    X = map(lambda x: x.descr[:size], moves)
    X = map(lambda x: tuple(sum(map(list, x), [])), X)
    Y = map(lambda x: x.name, moves)

    learner = neighbors.KNeighborsClassifier(weights='distance')
    predictor = learner.fit(X, Y)

    mouse = pymouse.PyMouse()
    hist_origin = []
    try:
        while True:
            pos = mouse.position()
            hist_origin.append(pos)
            if len(hist_origin) >= size:
                o = hist_origin[0]
                X = map(lambda x: (x[0] - o[0], x[1] - o[1]), hist_origin)
                X = tuple(sum(map(list, X), []))
                hist_origin = hist_origin[1:]
                print predictor.predict(X)[0]
            time.sleep(0.005)
    except KeyboardInterrupt:
        pass

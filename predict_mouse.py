#!/usr/bin/env python2
#-*- coding: utf-8 -*-
"""
Test d'apprentissage du mouvement de la souris.
Pour plus de simplicité, le mouvement n'utilisera que l'axe X (une seule
dimension) et deux mouvements seront définis : LEFT et RIGHT.

Le but est d'identifié le mouvement en moins de 3 secondes. En effectuant une
boucle à vide en Python 2 avec uniquement la lecture de la position de la
souris et l'affichage sur stdout, on remarque qu'on peut obtenir un historique
de taille 20000. Comme ce nombre est vraiment énorme, on va freiner l'exécution
manuellement d'autant plus que scikit learn doit quand même faire une
prédiction à chaque tour de boucle.

Les tests se feront avec la souris allant à peu près à vitesse constante. Les
descriptions des mouvements ne seront donc valalbles que pour un mouvement à
une vitesse spécifié. On verra plus tard si il est possible de changer
dynamiquement l'échelle temporelle des descriptions de mouvement.

Pour le mouvements LEFT la description sera la suivante :
    dx(t=0) = 0
    dx(t=1) = -1
    dx(t=2) = -2
    dx(t=3) = -3
    dx(t=4) = -4
    ...
    dx(t=T) = -T

Pour le mouvement RIGHT :
    dx(t=0) = 0
    dx(t=1) = 1
    dx(t=2) = 2
    dx(t=3) = 3
    dx(t=4) = 4
    ...
    dx(t=T) = T

Il a fallu rajouter un mouvement NULL qui s'identifie à un manque de mouvement
de la souris.
"""

import pymouse
import time
from sklearn import svm

def count_loops(t):
    """
    Count the number of loop executed in *t* seconds.
    The loop does nothing except read the position of the mouse and write it
    into stdout.
    """
    mouse = pymouse.PyMouse()
    begin = time.time()
    N = 0
    while time.time() - begin < 3:
        print mouse.position()
        N += 1
    return N

if __name__ == '__main__':
    # print count_loops(3) # ~= 20 000

    size = 20
    LEFT = map(lambda x: (-x, 0), xrange(size))
    RIGHT = map(lambda x: (x, 0), xrange(size))
    UP = map(lambda x: (0, -x), xrange(size))
    DOWN = map(lambda x: (0, x), xrange(size))
    NULL = [(0, 0) for _ in xrange(size)]
    XY = [(LEFT, 'LEFT')] \
            + [(RIGHT, 'RIGHT')] \
            + [(UP, 'UP')] \
            + [(DOWN, 'DOWN')] \
            + [(NULL, 'NULL')]
    print XY
    X, Y = zip(*XY)
    X = map(lambda x: tuple(sum(map(list, x), [])), X)
    print X
    print Y[0], X[0]
    print Y[1], X[1]
    print Y[2], X[2]

    learner = svm.LinearSVC()
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
                print predictor.predict(X)
            time.sleep(0.005)
    except KeyboardInterrupt:
        pass

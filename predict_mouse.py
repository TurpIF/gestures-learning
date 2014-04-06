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

L'ajout de la dimension Y de la souris peut se faire et les mouvements UP et
DOWN ont été intégré. Il n'est pas possible avec scikit learn d'utiliser des
tuples de tuples pour décrire un mouvement. Cad un mouvement ne peut pas être
(dM(t=0), ..., dM(t=T)) avec les dM un tuple (dx, dy) de R^2. Il faut que la
descriptions soit aplatie et ne forme qu'un tuple de réel.

L'ajout de mouvement même simple est assez compliqué à analyser finalement. Les
mouvements des diagonales sont ajoutés la prédiction devient très flou.

En mettant un historique très court (5 éléments), la détection se fait plus
rapidement et plus juste pour les mouvements très simple telle que le suivi
d'une seule direction. On s'approche de l'identification de la dérivée du
mouvement ce qui est assez aisé, en effet, à prédire dans le cas de mouvement
unidirectionnel. Cependant, il est impossible d'avoir des mouvements compliqués avec cette courte durée.
"""

import pymouse
import time
import math

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

    size = 5
    LEFT = map(lambda x: (-x, 0), xrange(size))
    RIGHT = map(lambda x: (x, 0), xrange(size))
    UP = map(lambda x: (0, -x), xrange(size))
    DOWN = map(lambda x: (0, x), xrange(size))
    CIRCLE = map(lambda x: (30 * math.cos(x * 2.0 * math.pi / size),
        30 * math.sin(x * 2.0 * math.pi / size)), xrange(size))
    LT_RD = map(lambda x: (x, x), xrange(size))
    RD_LT = map(lambda x: (-x, -x), xrange(size))
    RT_LD = map(lambda x: (-x, x), xrange(size))
    LD_RT = map(lambda x: (x, -x), xrange(size))
    NULL = [(0, 0) for _ in xrange(size)]
    XY = [(LEFT, 'LEFT')] \
            + [(RIGHT, 'RIGHT')] \
            + [(UP, 'UP')] \
            + [(DOWN, 'DOWN')] \
            + [(LT_RD, 'LT_RD')] \
            + [(RD_LT, 'RD_LT')] \
            + [(RT_LD, 'RT_LD')] \
            + [(LD_RT, 'LD_RT')] \
            + [(NULL, 'NULL')]
            # + [(CIRCLE, 'CIRCLE')] \
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
                # print predictor.decision_function(X)
                # print X
                # print predictor.transform(X)
            time.sleep(0.005)
    except KeyboardInterrupt:
        pass

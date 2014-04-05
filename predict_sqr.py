#!/usr/bin/env python2
#-*- coding: utf-8 -*-
"""
Prédiction temporelle :
Pour faire des prédictions temporelles, il faut garder une trace des données à
traiter. Plus la taille de la trace est grande, plus on peut être précis sur la
prédiction mais plus elle est lente.

Dans ce script, il s'agit de prédiction de fonctions mathématiques de base. Ce
sont des fonctions de R dans R. Pour se rapprocher de la prédiction temporelle,
on peut dire que l'ensemble de départ R est une dimension temporelle.
L'ensemble d'arrivé est R ici mais peut très bien être multidimensionnel.

Dans ce cas, on prendra bien l'ensemble d'arrivé = R et correspond à une
différence de déplacement sur un axe par rapport à la prise d'origine (t = 0).

Un mouvement est alors représenté par une fonction de déplacement dx :
    dx(t=0) dx(t=1) ... dx(t=T)
"""
from sklearn import svm
import math
import random

if __name__ == '__main__':
    f_sqr = lambda x: x*x
    f_inv = lambda x: 1.0 / x
    f_lin = lambda x: x
    f_neg = lambda x: -x
    f_exp = lambda x: math.exp(-x)
    f_rand = lambda x: random.random() * 100

    fs = [(f_sqr, 'sqr'),
            (f_inv, 'inv'),
            (f_lin, 'lin'),
            (f_neg, 'neg'),
            (f_exp, 'exp'),
            (f_rand, 'rand')]

    size_hist = 100
    pattern = lambda f: tuple(map(f, xrange(1, size_hist)))
    XY = [(pattern(f), lbl) for f, lbl in fs]
    X, Y = zip(*XY)
    learner = svm.LinearSVC()
    predictor = learner.fit(X, Y)

    N = 1000
    for _f, lbl in fs:
        f = lambda x: _f(x) + random.gauss(0, 2.0)
        X = [pattern(f) for _ in xrange(N)]
        Y = [lbl] * N
        print lbl, ':', predictor.score(X, Y)

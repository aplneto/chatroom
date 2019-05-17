#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 23:02:46 2019

@author: aplneto
"""

import threading
from time import sleep
# Exemplo de uso da biblioteca threading

def temporizador(timeout = 60):
    time = 0
    while time < timeout:
        time += 1
        print(str(time)+'s')
        sleep(1)
    print("Fim da contagem!")
    return True

def fib(num):
    if num <= 1:
        return num
    else:
        return fib(num-1) + fib(num-2)

def fibo(x):
    fib_ = [-1]*(x+1)
    for x in range(x+1):
        if x <= 1:
            fib_[x] = x
        else:
            fib_[x] = fib_[x-1] + fib_[x-2]
    return fib_[x]
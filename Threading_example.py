#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 23:02:46 2019

@author: aplneto
"""

import threading
from time import sleep
# Exemplo de uso da biblioteca threading

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

def temporizador(name = 'temporizador', timeout = 60):
    time = 0
    while time < timeout:
        print("{0}: {1}s".format(name, time))
        sleep(1)
        time += 1
    return True

def fib_to_num(num):
    for x in range(num+1):
        print("Fibonacci recursivo de {0}: {1}".format(x, fib(x)))

def fibo_to_num(num):
    for x in range(num+1):
        print("Fibonacci dinâmico de {0}: {1}".format(x, fibo(x)))

def main(num = 100, timeout = 60):
    threading.Thread(target = temporizador, args = ['Timer', timeout]).start()
    threading.Thread(target = fib_to_num, args = [num]).start()
    threading.Thread(target = fibo_to_num, args = [num]).start()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 05:46:57 2019

@author: aplneto
"""

from socket import gethostbyname, gethostname

from chat_room_client import ChatRoomClient
from chat_room_server import ChatRoomServer

check_ip = lambda: gethostbyname(gethostname())

# Variáveis globais

LOCAL_CHAT_IP = check_ip()
LOCAL_CHAT_PORT = 5500

MY_SERVER_NAME = 'My Server'
ADMIN_NAME = 'admin'
LIMIT = 10

REMOTE_CHAT_IP = 'localhost'
REMOTE_CHAT_PORT = 4400

def menu_inputs():
    ip = check_ip()
    print('Seu IP é ' + ip)
    while True:
        menu_help()
        comando = int(input('{}: '.format(ip)))
        if comando == 0:
            break
        elif comando == 1:
            cliente = entrar_na_sala()
            return cliente
        elif comando == 2:
            servidor = criar_nova_sala()
            servidor.run()
            return servidor
        elif comando == 3:
            configurar()

def menu_help():
    print("0 - Sair")
    print("1 - Juntar-se a sala existente")
    print("2 - Criar nova sala")
    print("3 - Ajustar configurações")

def entrar_na_sala():
    global LOCAL_CHAT_IP, LOCAL_CHAT_PORT, REMOTE_CHAT_IP, REMOTE_CHAT_PORT
    cliente = ChatRoomClient(LOCAL_CHAT_IP, LOCAL_CHAT_PORT)
    cliente.conectar(REMOTE_CHAT_IP, REMOTE_CHAT_PORT)
    return cliente

def criar_nova_sala():
    global MY_SERVER_NAME, ADMIN_NAME, LIMIT
    servidor = ChatRoomServer(MY_SERVER_NAME, admin_name = ADMIN_NAME,
                              limite = LIMIT)
    return servidor

def configurar():
    def conexao_remota():
        global REMOTE_CHAT_IP, REMOTE_CHAT_PORT
        REMOTE_CHAT_IP = input("Ip do servidor ao qual deseja se conectar: ")
        REMOTE_CHAT_PORT = int(input("Porta do servidor ao qual \
                                     deseja se conectar: "))
    def conexao_local():
        global LOCAL_CHAT_IP, LOCAL_CHAT_PORT, MY_SERVER_NAME
        LOCAL_CHAT_IP = input("Seu ip: ")
        LOCAL_CHAT_PORT = int(input("Porta que deseja usar: "))
    
    def meu_servidor():
        global MY_SERVER_NAME, ADMIN_NAME, LIMIT
        MY_SERVER_NAME = input("Nome do seu servidor: ")
        ADMIN_NAME = input("Nome do administrador do servidor: ")
        LIMIT = int(input("Limite máximo de participantes: "))
    print("0 - Sair")
    print("1 - Configurações locais")
    print("2 - Configurações remotas")
    print("3 - Configurações do meu Servidor")
    while True:
        comando = int(input('Comando: '))
        if comando == 0:
            break
        if comando == 1:
            conexao_remota()
            break
        elif comando == 2:
            conexao_local()
            break
        elif comando == 3:
            meu_servidor()
            break

menu_inputs()

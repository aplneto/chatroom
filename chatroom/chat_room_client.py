#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de Cliente do Chat Room

O cliente do bate-papo tenta se conectar ao servidor. Uma vez estabelecida a
conexão, as mensagens recebidas do servidor são controladas por uma thread
separada da thread principal (ver ChatRoomClient.run)

Created on Fri May 17 01:35:46 2019

@author: aplneto
"""

import socket
import threading

class ChatRoomClient(threading.Thread):
    '''Classe do Cliente do Chat Room
    
    Essa classe envia e recebe mensagens de um servidor.
    
    O console (impressão das mensagens recebidas) é controlado por uma thread
    separada do processo principal.
    
    '''
    def __init__(self, ip = 'localhost', port = 5500):
        '''Método Construtor
        
        O método construtor da classe ChatRoomClient estabele o socket pelo
        qual a comunicação com o servidor será feita.
        
        Args:
            ip (str): endereço ip associado ao socket que receberá mensagens do
                servidor.
            port (int): porta usada para comunicação com o servidor.
        
        '''
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port))
        self.__ativo = False
    
    def conectar(self, chat_ip = 'localhost', chat_port = 4400):
        '''Método de conexão com o servidor
        
        Esse método estabelece a comunicação com o servidor e inicia a thread.
        
        Args:
            chat_ip (str): endereço ip da sala de bate-papo. Por padrão
                'localhost'.
            chat_port (int): número da porta pela qual a conexão com a sala de
                bate-papo é estabelecida. Por padrão 4400.
        '''
        try:
            server_address = (chat_ip, chat_port)
            self.server.connect(server_address)
        except:
            print('Endereço Inválido!\nVerifique o endereço da sala')
        else:
            print('Use o comando \\quit para sair da sala.')
            self.start()
            while True:
                msg = input('Você: ')
                if msg.startswith('\\quit'):
                    break
                try:
                    self.server.send(msg.encode())
                except:
                    break
            
            self.server.close()
            self.__ativo = False
            
    def run(self):
        '''Método que controla o output do servidor
        
        O método do console é uma thread que controla a impressão das mensagens
        recebidas do servidor separadamente dos inputs do usuário.
        
        Args:
            servidor (socket.socket): socket de comunicação com a sala de bate-
                papo.
        '''
        self.__ativo = True
        while True:
            try:
                msg = self.server.recv(1024).decode()
            except:
                continue
            else:
                if msg:
                    if msg.startswith('\\'):
                        self.__comando(msg)
                    else:
                        print(msg)
                else:
                    break
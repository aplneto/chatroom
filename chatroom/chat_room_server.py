#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de Servidor do Chat Room

O servidor da sala de bate-papo tenta estabelecer as conexões por meio do seu
socket de entrada, criando uma thread para receber as mensagens enviadas pelos
usuários.
As mensagens recebidas de um usuário são então retransmitidas para todos os
usuários autalmente conectados a sala de bate-papo.

Created on Thu May 16 23:24:13 2019

@author: aplneto

"""

__author__ = 'Antônio Paulino'

__email__ = 'apln2@cin.ufpe.br'

import socket
import threading

#Função Auxiliar
def makethread(func):
    """Decorator que transforma uma função qualquer numa Thread
    
    Args:
        func (function): função a ser transformada em Thread
    
    Returns:
        (function) thread da função
    """
    def _thread(*args, **kwargs):
        """Decorador interno da função
        
        Args:
            *args (tuple): tupla de argumentos da função
            **kwargs (dict): dicionários de palavras-chave da função
        
        """
        pcs = threading.Thread(target = func, args = args, kwargs = kwargs)
        pcs.start()
    return _thread

class ChatRoomServer(threading.Thread):
    '''Classe ChatRoom
    
    A classe servidor controla a comunicação e fluxo da sala.
    Na classe servidor estão definidos os protocolos de comunicação.
    
    Atributes:
        ip_address (str: 'localhost'): endereço ip padrão
        port (int: 9001): valor padrão da porta do servidor
        
    '''
    ip_address = 'localhost'
    port = 4400
    def __init__(self, room_name, **kwargs):
        '''Método construtor do servidor
        
        O método construtor inicia os atributos do servidor e o socket que
        servirá como porta de entrada para a sala de bate-papo.
        
        Args:
            room_name (str): Nome da sala de bate-papo
        
        Kwargs:
            admin_name (str): nome do moderador da sala
            limite (int): quantidade limite de conexões
            
        '''
        threading.Thread.__init__(self)
        self.room_name = room_name
        self.admin = kwargs.get('admin_name', 'admin')
        self.limite = kwargs.get('limite', 0)
        self.entrada = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.entrada.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.entrada.bind((ChatRoomServer.ip_address, ChatRoomServer.port))
        self.clientes_conectados = dict()
        self.__count = 0
        self.__ativo = False
    
    @property
    def count(self):
        '''Método de Contagem
        
        Método de contagem de pessoas conectadas ao servidor
        
        Returns:
            (tuple): uma tupla que contem o total de pessoas conectadas como
                primeiro elemento e o limite da sala como segundo
        
        '''
        return (self.__count, self.limite)
    
    def run(self):
        '''Método de início
        
        O método run determina qual será o comportamento da thread.
        
        O método aceita conexões, podendo parar caso um limite seja
        estabelecido no método construtor.
        As novas conexões aceitas são inseridas numa lista de pessoas, sendo
        removidas caso a conexão seja encerrada pelo cliente, pelo servidor ou
        por algum eventual erro.
        
        '''
        self.entrada.listen()
        self.__ativo = True
        print(self.room_name + ' online!')
        while self.__ativo:
            cliente, addr = self.entrada.accept()
            if self.limite and self.limite <= self.__count:
                print(addr[0] + ' conexão recusada')
                cliente.send('A sala está loatada'.encode())
                cliente.close()
            else:
                print(addr[0] + ' conectado')
                self.__client_handler(cliente)
                self.__count += 1
    
    @makethread
    def __client_handler(self, cliente):
        '''Método de conexão de cliente
        
        Esse é o método que trada da conexão de cada cliente.
        O método envia a mensagem de boas vindas, recebe o nome de usuário do
        cliente e espera pelas mensagens enviadas do cliente para a sala de
        bate-papo.
        
        Args:
            cliente (socket.socket): a conexão pelo qual o cliente se
            comunica com o servidor.
        
        '''
        nome = self.__autenticacao(cliente)
        while True:
            try:
                msg = cliente.recv(1024).decode()
            except:
                continue
            else:
                if msg:
                    if msg.startswith('\\list'):
                        people = ', '.join(self.clientes_conectados.keys())
                        answ = "Online: {}".format(people)
                        cliente.send(answ.encode())
                    else:
                        msg_post = "{0}: {1}".format(nome, msg).encode()
                        self.broadcast(msg_post, cliente)
                else:
                    self.desconectar(cliente)
    
    def broadcast(self, msg, remetente = None):
        '''Método de broadcast das mensagens recebidas
        
        Esse método retransmite a mensagem para todos os clientes conectados
        a sala.
        
        Args:
            msg (bytes): versão binária da mensagem que será retransmitida
            remetente (socket.socket): socket do remetente.
        
        '''
        for cliente in self.clientes_conectados.values():
            if cliente != remetente:
                try:
                    cliente.send(msg)
                except:
                    cliente.close()
                    self.desconectar(cliente)
            
    def desconectar(self, cliente):
        '''Método de desconexão de clientes
        
        Quando algum socket é encerrado pelo cliente ou por algum erro, esse
        metodo fecha a conexão do lado do servidor e remove o socket do cliente
        do grupo de sockets conectados.
        
        Args:
            cliente(socket.socket): cliente a ser desconectado
        
        '''
        for nome, conn in self.clientes_conectados.items():
            if conn == cliente:
                conn.close()
                break
        if nome:
            del self.clientes_conectados[nome]
            msg = "{0} deixou a sala".format(nome)
            self.broadcast(msg.encode())
            self.__count -= 1
    
    def expulsar(self, nome_cliente):
        '''Método de remoção forçada de usuário
        
        O método de expulsão recebe o nome do cliente e, através desse nome,
        encontra e encerra a conexão, emitindo uma mensagem de aviso para todos
        os usuários informando a expulsão forçada do membro.
        
        Args:
            nome_cliente (str): nome do cliente a ser expulso
        '''
        if nome_cliente in self.clientes_conectados:
            aviso = "Você foi expulso da sala por {0}".format(self.admin)
            self.clientes_conectados[nome_cliente].send(aviso.encode())
            self.clientes_conectados[nome_cliente].close()
            del self.clientes_conectados[nome_cliente]
            msg = "{0} expulsou {1} da sala".format(self.admin, nome_cliente)
            self.broadcast(msg.encode())
            self.__count -= 1
    
    def __autenticacao(self, cliente):
        '''Método de tratamento de nome inválido
        
        Esse método verifica se o nome do usuário é valido, garantindo que
        o nome do usuário esteja válido antes de adicioná-lo ao grupo de
        usuários conectados.
        
        Args:
            cliente (socket.socket): conexão do cliente
        
        Returns:
            (str): nome válido do usuário
        '''
        welcome = "Bem-vindo a {0}!\nPor favor, escolha um nome de usuário."
        cliente.send(welcome.format(self.room_name).encode())
        while True:
            nome = cliente.recv(1024).decode()
            if nome in self.clientes_conectados:
                cliente.send('Já existe um usuário com esse nome'.encode())
            elif nome in ['admin', 'administrador', 'mod', 'moderador']:
                cliente.send('Nome inválido'.encode())
            elif nome.startswith('\\'):
                cliente.send('Nome inválido'.encode())
            else:
                break
        self.clientes_conectados[nome] = cliente
        msg = "{0} entrou na sala".format(nome)
        self.broadcast(msg.encode(), cliente)
        cliente.send("Você já pode conversar, {}\n".format(nome).encode())
        return nome
    
    def stop(self):
        '''Método de para da thread
        
        '''
        self.__ativo = False
        self.entrada.close()
    
    def __bool__(self):
        return self.__ativo

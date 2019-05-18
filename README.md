![PyPI - Python Version](https://img.shields.io/pypi/pyversions/select.svg)

# Projeto de Redes 2019.1


## Bibliotecas Principais
- [socket](https://docs.python.org/3/library/socket.html)
- [threading](https://docs.python.org/3/library/threading.html)

## Outras Bibliotecas
- [select](https://docs.python.org/3/library/select.html)

## Links Úteis
- https://blog.4linux.com.br/socket-em-python/

## Como usar?

Baixe e extraia o arquivo zip ou clone o repositório.
Entre na pasta `chatroom` e execute o módulo `menu_initializer.py`.

Você pode ajustar as configurações do script através das variáveis
globais, ou através do menu de configuração.

As variáveis `LOCAL` são os valores utilizados para IP e Porta do socket
que você está utilizando.

```python3
LOCAL_CHAT_IP = 'localhost'
LOCAL_CHAT_PORT = 5500
```

As configurações remotas são ajustadas com o endereço do servidor ao qual
você deseja se conectar. Por exemplo:

```python3
REMOTE_CHAT_IP = 'localhost'
REMOTE_CHAT_PORT = 4400
```
Lembre-se de usar números de porta diferentes caso esteja tentando conexão
cliente-servidor em scripts no mesmo computador.

As configurações acima resultariam numa tentativa de conexão a um cliente
hospedado na mesma máquina (`localhost`) na porta 4400.
Caso esteja tentanto realizar uma conexão com um servidor em uma máquina
diferente, utilize o ip e porta da máquina.
Você pode descobrir o ip da sua máquina através do comando bash `ipconfig`
no windows ou `ifconfig` no linux.

As configurações de servidor `MY_SERVER_NAME`, `ADMIN_NAME` e `LIMIT`
representam, respectivamente, o nome do seu servidor, o nome do
administrador do servidor e o limite de pessoas conectadas ao mesmo tempo.
Caso queira que sua sala não tenha limites, defina o valor LIMIT para 0.

```python3
MY_SERVER_NAME = 'My Server'
ADMIN_NAME = 'admin'
LIMIT = 10
```

As configurações de servidor são importantes apenas caso você queira
iniciar uma nova sala. Se estiver tentando se conectar à uma sala já
existente, basta definir suas configurações locais e o endereço da sala
no servidor ao qual você deseja se conectar.

Por fim, caso escolha configurar as variáveis globais direto no script,
basta executar o script e seguir os passos que desejar no menu.

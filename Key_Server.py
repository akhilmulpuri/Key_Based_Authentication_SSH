
import socket
import random

host = '192.168.1.25'
keyserver_port = 9547
# keyserver socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, keyserver_port))
s.listen(10)

# add the ip addresses of the server
server_list = ('192.168.1.13')

# public key dictionary
key_dict = dict()

def get_publickey(client_id):
    '''Get public key'''
    print('client_id is {}'.format(client_id))
    global key_dict
    return key_dict.get(client_id,None)

def client_register(ipaddr,public_key):
    '''Generate unique client id'''
    # code for generating client id
    client_id = ipaddr.replace('.','') + str(random.randint(1,1000))
    global key_dict
    key_dict[client_id] = public_key
    return client_id



while True:

    conn,addr = s.accept()

    # receive
    msg = conn.recv(2048)

    msg = msg.decode('utf-8').split(' ')
    print('The message is {}'.format(' '.join(msg)))

    if not msg:
        print('exiting ......')
        break

    # sent by server
    if msg[0] in server_list:
        val = get_publickey(msg[1])
        val = ' '.join(val)
        print('The public key is {}'.format(val))
    # sent by client
    else:
        val = client_register(msg[0],msg[1:])
        print('The client id is {}'.format(val))

    #send
    conn.send(val.encode())
    conn.close()

    




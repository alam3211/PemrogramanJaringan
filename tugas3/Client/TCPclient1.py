import socket
import json
import os
import threading


class RelativePath:
    def __init__(self):
        self.current_dir = ''

    def get_dir(self):
        return self.current_dir

    def _get_array_dir(self):
        return self.current_dir.split('/')

    def cd(self, dir):
        if dir == '..':
            array_dir = self._get_array_dir()
            self.current_dir = ''

            a_len = len(array_dir)

            for i in range(0, a_len-2):
                self.current_dir += array_dir[i]
                self.current_dir += '/'

        elif self.current_dir == '':
            self.current_dir = dir + '/'
        else:
            self.current_dir += dir + '/'


class Client(threading.Thread):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = ('127.0.0.1', 10000)
        self.sock.connect(server_addr)
        print('connected to '+str(server_addr))
        print('Command Guide \n- ls\n- get (download)\n- put (upload)\n- cd ')
        self.r_path = RelativePath()
        threading.Thread.__init__(self)

    def _ls_handler(self):
        request = {}
        request['command'] = 'ls'
        request['dir'] = self.r_path.get_dir()

        self.sock.sendall(json.dumps(request))
        response = self.sock.recv(1024)
        data = json.loads(response)

        dir_list = data['dir_list']
        print(self.r_path.get_dir()+' LS LS LS LS LS ')
        for dir in dir_list:
            dir_type = ''
            if dir['is_file'] == False:
                dir_type = 'folder'

            print('==> '+dir['name'] + '{}'.format(dir_type))

    def _get_handler(self, filename):
        request = {}
        request['command'] = 'get'
        request['path'] = self.r_path.get_dir() + filename
        self.sock.sendall(json.dumps(request))
        fd = open(filename, 'wb+', 0)
        response = self.sock.recv(1024)
        data = json.loads(response)
        if data['file_size'] is not None:
            max_size = data['file_size']
            received = 0
            while received < max_size:
                data = self.sock.recv(1024)
                received += len(data)
                fd.write(data)
        fd.close()
        print('file download {} success'.format(filename))
        print(self.r_path.get_dir())
    def _put_handler(self, filename):
        path = self.r_path.get_dir()+filename
        fd = open(filename, 'rb')
        request = {}
        request['command'] = 'put'
        request['path'] = path
        request['file_size'] = os.path.getsize(filename)
        self.sock.sendall(json.dumps(request))
        response = self.sock.recv(1024)
        if response == '--READY--':
            for data in fd:
                self.sock.sendall(data)

        self.sock.send(bytes('--END--'))
        print('file sent {} success'.format(filename))

    def run(self):
        while True:
            commands = raw_input().split(' ')
            command = commands[0]
            if command == 'ls':
                self._ls_handler()
            elif command == 'cd':
                cd_path = commands[1]
                self.r_path.cd(cd_path)
                print(self.r_path.get_dir())
            elif command == 'get':
                self._get_handler(commands[1])
            elif command == 'put':
                self._put_handler(commands[1])

if __name__=="__main__":
    Client().start()


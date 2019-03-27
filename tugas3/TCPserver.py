import socket
import sys
import os
import time
import threading
import glob
import json

class Server(threading.Thread):
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(('127.0.0.1', 10000))
		print('Waiting for connection')
		threading.Thread.__init__(self)

	def run(self):
		self.sock.listen(1)
		while True:
			conn, address = self.sock.accept()
			print('Client '+str(address)+' Connected')
			ClientHandler(conn, address).start()

class ClientHandler(threading.Thread):
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def _ls_handler(self, request):
		response = {}
		dir_list = glob.glob(request['dir']+'*')
		response['dir_list'] = map(
			lambda file_name : {'name':file_name, 'is_file' : os.path.isfile(request['dir']+file_name)},
			dir_list
		)
		self.connection.sendall(json.dumps(response))

	def _get_handler(self, request):
		fd = open(request['path'], 'rb')
		response = {}
		response['file_size'] = os.path.getsize(request['path'])
		self.connection.sendall(json.dumps(response))
		for data in fd:
			self.connection.sendall(data)
		fd.close()

	def _put_handler(self, request):
		max_size = request['file_size']
		received = 0
		fd = open(request['path'], 'wb+', 0)
		self.connection.sendall('--READY--')
		while received < max_size:
			data = self.connection.recv(1024)
			received += len(data)
			fd.write(data)

		fd.close()
		print('file sent')

	def run(self):
		while True:
			data = self.connection.recv(1024)
			request = json.loads(data)
			print(request)
			cmd = request['command']

			if cmd == 'ls':
				self._ls_handler(request)
			elif cmd == 'get':
				self._get_handler(request)
			elif cmd == 'put':
				self._put_handler(request)

if __name__=="__main__":
	Server().start()



import socket
from threading import Thread

IP = "127.0.0.1"
PORT = 8888
ADDRESS = (IP, PORT)

CONNECT = "cmd_connect"
START = "cmd_start"
FINISH = "cmd_finish"
DISCONNECT = "cmd_disconnect"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDRESS)

def sendImage(filename, ip, port):
   fp = open(filename, "rb")
   payload = fp.read()
   payload_length = len(payload)
   fp.close()
   target_address = (ip, port)
   print "Mengirimkan " + filename + ", target: " + str(ip) + ":" + str(port)
   sock.sendto("Mengirim" + " " + filename, target_address)
   for i in range((payload_length / 1024) + 1):
      chunk = []
      if (i + 1) * 1024 > payload_length:
         chunk = payload[i * 1024:payload_length]
         chunk.ljust(1024)
      else:
         chunk = payload[i * 1024:(i + 1) * 1024]
      sock.sendto(chunk, target_address)
   print "Pengiriman telah selesai" + str(ip) + ":" + str(port)
   sock.sendto("Selesai", target_address)

def listImages(ip, port):
    listimages = ["bart.png","kucing.jpg","kucingjuga.jpg","kucingbobok.jpg"]
    target_address = (ip, port)
    for x in listimages:
        sendImage(x , ip, port)
        print "Pengiriman terhadap " + str(ip) + ":" + str(port) + " telah selesai."
        sock.sendto("Diskoneksi", target_address)

def checkRequest():
   while True:
    print "Server siap, menunggu client..."
    data, address = sock.recvfrom(1024)
    if data == "Terkoneksi":
        print "Terkoneksi pada " + str(address[0]) + ":" + str(address[1])
        thread = Thread(target=listImages, args=address)
        thread.start()

while True:
   checkRequest()
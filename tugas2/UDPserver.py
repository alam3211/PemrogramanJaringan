from threading import Thread
import socket
import os, os.path
import time

IP = "127.0.0.1"
PORT = 8888
ADDRESS = (IP, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDRESS)

def sendImage(filename, ip, port):
   fp = open(filename, "rb")
   payload = fp.read()
   payload_length = len(payload)
   fp.close()
   target_address = (ip, port)
   print "Melakukan pengiriman untuk file : " + filename + ", target: " + str(ip) + ":" + str(port)
   sock.sendto("Mengirim" + " " + filename, target_address)
   for i in payload:
      sock.sendto(i, target_address)
   print "Pengiriman ke " + str(ip) + ":" + str(port) + " selesai"
   sock.sendto("Selesai", target_address)

def setupImages(ip, port):
   target_address = (ip, port)
   listImages = ["bart.png","kucing.jpg","kucingjuga.jpg","kucingbobok.jpg"]
   for x in listImages:
    sendImage(x, ip, port)
   print "Melakukan diskoneksi" + str(ip) + ":" + str(port)
   sock.sendto("Diskoneksi", target_address)

def checkRequest():
   while True:
      data, address = sock.recvfrom(2048)
      if data == "Terhubung":
         print "Telah terhubung dengan " + str(address[0]) + ":" + str(address[1])
         thread = Thread(target=setupImages, args=address)
         thread.start()

while True:
   checkRequest()
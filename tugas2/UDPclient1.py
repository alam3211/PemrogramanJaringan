import socket

IP = "127.0.0.1"
PORT = 8888
ADDRESS = (IP, PORT)

CONNECT = "cmd_connect"
START = "cmd_start"
FINISH = "cmd_finish"
DISCONNECT = "cmd_disconnect"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fp = None
filename = ""

print "Send command: cmd_connect"
sock.sendto("Menyambung" , ADDRESS)

while True:
    data, address = sock.recvfrom(1024)
    if data == "Mengirim":
        filename = "_" + str_data[10:].strip()
        print "Mengirimkan gambar " + filename
        fp = open(filename, "wb+")
    elif data == "Selesai":
        print "Pengiriman gambar selesai " + filename
        fp.close()
    elif data == "Diskoneksi":
        print "Koneksi dengan server telah diputus"
        break
    else:
        fp.write(data)
import socket

IP = "127.0.0.1"
PORT = 8888
ADDRESS = (IP, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fp = None
filename = ""

print "Send command: cmd_connect"
sock.sendto("Terhubung", ADDRESS)

while True:
    data, address = sock.recvfrom(2048)
    str_data = str(data)
    if str_data[:8] == "Mengirim":
        filename = "copy of " + str_data[9:].strip()
        print "Mengirim gambar " + filename
        fp = open(filename, "wb+")
    elif str_data[:7] == "Selesai":
        print "Pengiriman selesai " + filename
        fp.close()
    elif str_data[:10] == "Diskoneksi":
        print "Memutus koneksi"
        break
    else:
        fp.write(data)
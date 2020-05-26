import socket
from threading import *
import database
import time
import match
import inventario

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        msg = self.sock.recv(10000).decode()
        if msg == '':
            print('Cliente cerrado')
        else:
            print('Mensaje recibido:', msg)
            dividido = msg.split(",")
            if len(dividido) == 1:
                #Hacer que recibido un imei lo busque y devuelva. Si no encuentra, crear y devolver
                a = database.buscar_imei_ultimo(("".join(dividido)))
                if a is False:
                    mensaje = str.encode("NewPhone")
                else:
                    mensaje = str.encode(",".join(a))
                self.sock.send(mensaje)
                self.sock.close()
            elif len(dividido) == 2:
                lista = database.buscar_imei(dividido[1])
                for a in range(len(lista)):
                    lista[a] = ",".join(lista[a])
                lista = "&".join(lista)
                a = str.encode(lista)
                self.sock.send(a)
                self.sock.close()
                print(a)

            # Aca es cuando se recibe un telefono para matcheo
            elif len(dividido) == 3:
                marca = dividido[1]
                modelo = dividido[2]
                lista = match.matcheo(marca, modelo)
                for a in range(len(lista)):
                    lista[a] = ','.join(lista[a])
                lista = "&".join(lista)

                a = str.encode(lista)
                self.sock.send(a)
                self.sock.close()
                print(a)

            # Aca recibe un imei y devuelve el mensaje de telefonos para sacar repuestos
            if len(dividido) == 4:
                telefono = database.buscar_imei_ultimo(dividido[-1])
                mensaje = match.es_reparable(telefono,1)
                a = str.encode(mensaje)
                self.sock.send(a)
                self.sock.close()
                print(a)

            elif len(dividido) == 5:
                database.eliminar(str(dividido[4]))
                a = str.encode("ok")
                self.sock.send(a)
                self.sock.close()


            elif len(dividido) == 6:
                mensaje = inventario.buscar_repuestos(dividido[0], dividido[1])
                a = str.encode(mensaje)
                self.sock.send(a)
                self.sock.close()
            elif len(dividido) == 7:
                inventario.guardar_repuestos(dividido[0])
                a = str.encode("ok")
                self.sock.send(a)
                self.sock.close()
            else:
                database.data_entry(dividido)
                a = str.encode("Ok")
                self.sock.send(a)
                self.sock.close()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 42069
serversocket.bind((host, port))

serversocket.listen(5)
print('Servidor iniciado, esperando...')
while 1:
    clientsocket, address = serversocket.accept()
    print('Anadido')
    client(clientsocket, address)

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

            # Hacer que recibido un imei lo busque y devuelva. Si no encuentra, crear y devolver
            if len(dividido) == 1:
                b = database.buscar_imei_ultimo(("".join(dividido)))
                if b is False:
                    a = str.encode("NewPhone")
                else:
                    a = str.encode(",".join(b))

            #
            elif len(dividido) == 2 and dividido[0] == "2":
                lista = database.buscar_imei(dividido[1])
                for a in range(len(lista)):
                    lista[a] = ",".join(lista[a])
                lista = "&".join(lista)
                a = str.encode(lista)

            # Aca es cuando se recibe un telefono para matcheo
            elif len(dividido) == 3 and dividido[0] == "3":
                marca = dividido[1]
                modelo = dividido[2]
                lista = match.matcheo(marca, modelo)
                for a in range(len(lista)):
                    lista[a] = ','.join(lista[a])
                lista = "&".join(lista)
                a = str.encode(lista)

            # Aca recibe un imei y devuelve el mensaje de telefonos para sacar repuestos
            elif len(dividido) == 2 and dividido[0] == "4":
                telefono = database.buscar_imei_ultimo(dividido[1])
                mensaje = match.es_reparable(telefono, 1)
                a = str.encode(mensaje)

            # Eliminar telefono con cierto imei
            elif len(dividido) == 2 and dividido[0] == "5":
                database.eliminar(str(dividido[1]))
                a = str.encode("ok")

            # Enviar a la aplicacion todos los repuestos de una marca y modelo
            elif len(dividido) == 3 and dividido[0] == "6":
                mensaje = inventario.buscar_repuestos(dividido[1], dividido[2])
                a = str.encode(mensaje)

            # Guardar listado actualizado de repuestos
            elif len(dividido) == 2 and dividido[0] == "7":
                inventario.guardar_repuestos(dividido[1])
                a = str.encode("ok")

            # Meter datos del telefono
            else:
                database.data_entry(dividido)
                a = str.encode("Ok")

            self.sock.send(a)
            self.sock.close()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 42070
serversocket.bind((host, port))

serversocket.listen(5)
print('Servidor iniciado, esperando...')
while 1:
    clientsocket, address = serversocket.accept()
    print('Anadido')
    client(clientsocket, address)

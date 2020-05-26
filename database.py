import sqlite3
import csv
import os.path
import mysql.connector
import database2
from datetime import datetime


def conector():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "administrador",
        database = "database"
    )
    mycursor = mydb.cursor()

    return mydb, mycursor


def obtener_ultima_id():
    conexion, cursor = conector()
    cursor.execute("SELECT * FROM CELULAR")
    celulares = cursor.fetchall()
    ultima = 0
    for a in celulares:
        if int(a[0]) > ultima:
            ultima = int(a[0])

    conexion.close()
    return ultima


def data_entry(telefono):
    conexion, cursor = conector()
    imei = telefono[0]
    if buscar_imei_ultimo(imei) is False:
        version = 1
        idtel = str(obtener_ultima_id()+1)
    else:
        version = str(int(buscar_imei_ultimo(imei)[-1]) + 1)
        idtel = buscar_imei_ultimo(imei)[0]
    telefono.insert(0, idtel)
    telefono.append(version)
    telefono[4] = str(datetime.now()).split(" ")[0]

    sentencia = '''INSERT INTO CELULAR 
                    (ID, IMEI,Marca,Modelo,Fecha,Revisor,GB,Color,Estetica,Carcasa,CamaraTrasera,CamaraDelantera,PinCarga,Auriculares,ParlanteFrontal,ParlanteTrasero,SensorProx,Bateria,BateriaPorcentaje,Wifi,Bluetooth,Vidrio,Modulo,Traslucido,Otros,Estado,Lugar,Liberar,PortaSim,Microfono,Botones,Tactil,version) 
                    VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    cursor.execute(sentencia, telefono)
    conexion.commit()
    conexion.close()

    database2.ultima_version(telefono)

    if(telefono[25] == "Vendido"):

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="administrador",
            database="ultimavers_db"
        )
        mycursor = mydb.cursor()
        conexion, cursor = mydb, mycursor

        sentencia = '''INSERT INTO VENTAS 
                        (ID, IMEI,Marca,Modelo,Fecha,Revisor,GB,Color,Estetica,Carcasa,CamaraTrasera,CamaraDelantera,PinCarga,Auriculares,ParlanteFrontal,ParlanteTrasero,SensorProx,Bateria,BateriaPorcentaje,Wifi,Bluetooth,Vidrio,Modulo,Traslucido,Otros,Estado,Lugar,Liberar,PortaSim,Microfono,Botones,Tactil,version) 
                        VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cursor.execute(sentencia, telefono)
        conexion.commit()
        conexion.close()



def buscar_imei(imei):
    #Busca todas las versiones de un telefono por su IMEI
    conexion, cursor = conector()
    cursor.execute("SELECT * FROM CELULAR")
    celulares = cursor.fetchall()
    lista = []
    for a in celulares:
        if a[1] == str(imei):
            lista.append(a)
    conexion.close()
    return lista


def buscar_imei_ultimo(imei):
    #Busca la ultima version de un telefono segun su imei
    todos = buscar_imei("".join(imei))
    if len(todos) == 0:
        return False
    retornar = todos[0]
    for a in todos:
        if int(a[-1]) > int(retornar[-1]):
            retornar = a
    return retornar

def eliminar(imei):
    telefono = list(buscar_imei_ultimo(imei))
    database2.eliminar(imei)
    conexion, cursor = conector()
    cursor.execute("DELETE FROM CELULAR WHERE IMEI = '" + imei + "'")
    conexion.commit()
    conexion.close()

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "administrador",
        database = "ultimavers_db"
    )

    mycursor = mydb.cursor()
    conexion, cursor = mydb, mycursor
    cursor.execute("DELETE FROM VENTAS WHERE IMEI = '" + imei + "'")
    conexion.commit()
    conexion.close()

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "administrador",
        database = "database"
    )
    mycursor = mydb.cursor()
    conexion, cursor = mydb, mycursor
    sentencia = '''INSERT INTO Eliminados 
                    (ID, IMEI,Marca,Modelo,Fecha,Revisor,GB,Color,Estetica,Carcasa,CamaraTrasera,CamaraDelantera,PinCarga,Auriculares,ParlanteFrontal,ParlanteTrasero,SensorProx,Bateria,BateriaPorcentaje,Wifi,Bluetooth,Vidrio,Modulo,Traslucido,Otros,Estado,Lugar,Liberar,PortaSim,Microfono,Botones,Tactil,version) 
                    VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

    telefono[4] = str(datetime.now()).split(" ")[0]
    cursor.execute(sentencia, telefono)
    conexion.commit()
    conexion.close()










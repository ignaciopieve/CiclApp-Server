import sqlite3
import csv
import os.path
import mysql.connector

def conector():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "administrador",
        database = "ultimavers_db"
    )
    mycursor = mydb.cursor()

    return mydb, mycursor


def ultima_version(telefono):
    conexion, cursor = conector()
    eliminar(telefono[1])

    sentencia = '''INSERT INTO CELULAR 
                    (ID, IMEI,Marca,Modelo,Fecha,Revisor,GB,Color,Estetica,Carcasa,CamaraTrasera,CamaraDelantera,PinCarga,Auriculares,ParlanteFrontal,ParlanteTrasero,SensorProx,Bateria,BateriaPorcentaje,Wifi,Bluetooth,Vidrio,Modulo,Traslucido,Otros,Estado,Lugar,Liberar,PortaSim,Microfono,Botones,Tactil,version) 
                    VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    cursor.execute(sentencia, telefono)
    conexion.commit()
    conexion.close()


def eliminar(imei):
    conexion, cursor = conector()
    cursor.execute("DELETE FROM CELULAR WHERE IMEI = '" + imei + "'")
    conexion.commit()
    conexion.close()


def mostrar_tabla():
    conexion, cursor = conector()
    cursor.execute("SELECT * FROM CELULAR")
    celulares = cursor.fetchall()
    for a in celulares:
        print(a)
    conexion.close()

def vaciar_tabla():
    conexion, cursor = conector()
    cursor.execute("TRUNCATE TABLE CELULAR")
    conexion.close


def obtener_ultimas_versiones():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="administrador",
        database="database"
    )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM CELULAR")
    celulares = mycursor.fetchall()

    ultimas_versiones = []

    # Primero obtenemos la id mas grande
    mayor = "0"
    for a in celulares:
        if int(a[0]) > int(mayor):
            mayor = a[0]

    # Luego recorremos id por id buscando el mayor
    for a in range(int(mayor)+1):

        # Por cada id va a hacer esto (agarrar y devolver en el arreglo todas las versiones
        arreglo = []
        for b in celulares:
            if b[0] == str(a):
                arreglo.append(b)

        # Aca agarro todas las versiones y guardo la ultima
        if len(arreglo) != 0:
            telefono_appendear = arreglo[0]
            for a in arreglo:
                if int(a[-1]) > int(telefono_appendear[-1]):
                    telefono_appendear = a
            ultimas_versiones.append(telefono_appendear)

    mydb.close()
    return ultimas_versiones


def actualizador():
    vaciar_tabla()
    telefonos_ultimos = obtener_ultimas_versiones()
    for a in telefonos_ultimos:
        ultima_version(a)



if __name__ == "__main__":
    print("1- Mostrar tabla\n2- Vaciar tabla\n3- Actualizar tabla")

    opc = input("Seleccione una opcion: ")
    if opc == "1":
        mostrar_tabla()
    if opc == "2":
        vaciar_tabla()
    if opc == "3":
        actualizador()

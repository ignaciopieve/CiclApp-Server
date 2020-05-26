import sqlite3
import csv
import os.path
import mysql.connector
import database2
from datetime import datetime
import match

def flama():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="administrador",
        database="testing"
    )
    mycursor = mydb.cursor()
    conexion, cursor = mydb, mycursor

    cursor.execute("SELECT * FROM Tabla1")
    marca_modelo = cursor.fetchall()
    conexion.commit()
    conexion.close()


    lista = match.matcheo2(marca_modelo[0][0], marca_modelo[0][1])


    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "administrador",
        database = "testing"
    )
    mycursor = mydb.cursor()
    conexion, cursor = mydb, mycursor
    cursor.execute("DELETE FROM Tabla2")
    sentencia = '''INSERT INTO Tabla2 
                    (IMEI, Riesgo, Tiempo, Descripcion) 
                    VALUES
                    (%s,%s,%s,%s)'''
    for a in lista:
        temporal = [a[0], a[1], a[2], a[4]]
        cursor.execute(sentencia, temporal)
    conexion.commit()
    conexion.close()



    print(lista)



flama()





import mysql.connector


def buscar_repuestos(marca, modelo):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="administrador",
        database="inventario"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT marca, modelo, repuesto, cantidad, color FROM repuestos")

    filas = cursor.fetchall()
    resultantes = []


    # 0	CARCASA	                # 8	    BATERIA
    # 1	CAMARA TRASERA	        # 9	    VIDRIO
    # 2	CAMARA DELANTERA	    # 10	MODULO
    # 3	PIN DE CARGA	        # 11	LIBERAR
    # 4	AURICULAR	            # 12	PORTA SIM
    # 5	PARLANTE DELANTERO	    # 13	MICROFONO
    # 6	PARLANTE TRASERO	    # 14	TACTIL
    # 7	SENSOR PROX
    partes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for a in filas:
        if a[0] == marca and a[1] == modelo:
            resultantes.append(a)

            if a[2] == "Carcasa":
                partes[0] = 1
            if a[2] == "Camara trasera":
                partes[1] = 1
            if a[2] == "Camara delantera":
                partes[2] = 1
            if a[2] == "Pin de carga":
                partes[3] = 1
            if a[2] == "Auricular":
                partes[4] = 1
            if a[2] == "Parlante delantero":
                partes[5] = 1
            if a[2] == "Parlante trasero":
                partes[6] = 1
            if a[2] == "Sensor de proximidad":
                partes[7] = 1
            if a[2] == "Bateria":
                partes[8] = 1
            if a[2] == "Vidrio":
                partes[9] = 1
            if a[2] == "Modulo":
                partes[10] = 1
            if a[2] == "Portasim":
                partes[11] = 1
            if a[2] == "Microfono":
                partes[12] = 1
            if a[2] == "Placa madre":
                partes[13] = 1

    if partes[0] == 0:
        resultantes.append([marca, modelo, "Carcasa", "0", ""])
    if partes[1] == 0:
        resultantes.append([marca, modelo, "Camara trasera", "0", ""])
    if partes[2] == 0:
        resultantes.append([marca, modelo, "Camara delantera", "0", ""])
    if partes[3] == 0:
        resultantes.append([marca, modelo, "Pin de carga", "0", ""])
    if partes[4] == 0:
        resultantes.append([marca, modelo, "Auricular", "0", ""])
    if partes[5] == 0:
        resultantes.append([marca, modelo, "Parlante delantero", "0", ""])
    if partes[6] == 0:
        resultantes.append([marca, modelo, "Parlante trasero", "0", ""])
    if partes[7] == 0:
        resultantes.append([marca, modelo, "Sensor de proximidad", "0", ""])
    if partes[8] == 0:
        resultantes.append([marca, modelo, "Bateria", "0", ""])
    if partes[9] == 0:
        resultantes.append([marca, modelo, "Vidrio", "0", ""])
    if partes[10] == 0:
        resultantes.append([marca, modelo, "Modulo", "0", ""])
    if partes[11] == 0:
        resultantes.append([marca, modelo, "Portasim", "0", ""])
    if partes[12] == 0:
        resultantes.append([marca, modelo, "Microfono", "0", ""])
    if partes[13] == 0:
        resultantes.append([marca, modelo, "Placa madre", "0", ""])


    for a in range(len(resultantes)):
        resultantes[a] = ",".join(resultantes[a])
    resultantes = "&".join(resultantes)

    return resultantes


def buscar_repuestos_interno(marca, modelo):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="administrador",
        database="inventario"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT marca, modelo, repuesto, cantidad, color FROM repuestos")
    filas = cursor.fetchall()
    resultantes = []
    lista_repuestos_posibles = ["Carcasa", "Camara trasera", "Camara delantera", "Pin de carga", "Auricular", "Parlante delantero",
             "Parlante trasero", "Sensor de proximidad", "Bateria", "Modulo", "Portasim", "Microfono"]
    repuestos_que_hay = [0,0,0,0,0,0,0,0,0,0,0,0]
    for a in filas:
        if a[0] == marca and a[1] == modelo and (a[2] in lista_repuestos_posibles):
            resultantes.append(a)
            repuestos_que_hay[lista_repuestos_posibles.index(a[2])] = 1


    return repuestos_que_hay


def obtener_ultima_id():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="administrador",
        database="inventario"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM repuestos")

    filas = cursor.fetchall()

    ultima_id = 0
    for a in filas:
        if int(a[0]) > ultima_id:
            ultima_id = int(a[0])

    return ultima_id





def guardar_repuestos(lista_repuestos):
    # */* <<-- Esto va a separar repuestos
    # @/@ <<-- Esto va a separar las partes dentro de los repuestos
    lista_repuestos = lista_repuestos.split("*/*")
    nueva_lista = []
    ultima = obtener_ultima_id()
    for a in range(len(lista_repuestos)):
        cosa = lista_repuestos[a].split("@/@")
        if cosa[3] != "0":
            ultima += 1
            nueva_lista.append([str(ultima)] + cosa)
    cosa_a_anadir = "INSERT INTO `repuestos`(`id`, `marca`, `modelo`, `repuesto`, `cantidad`, `color`) VALUES "
    for a in nueva_lista:
        cosa_a_anadir += '("' + '","'.join(a) + '"),'
    cosa_a_anadir = cosa_a_anadir[:-1] + ';'

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="administrador",
        database="inventario"
    )
    cursor = conexion.cursor()
    print(nueva_lista)
    if len(nueva_lista) > 0:
        cursor.execute("DELETE FROM repuestos WHERE modelo = '" + nueva_lista[0][2] + "' AND marca = '" + nueva_lista[0][1] +"'")
        cursor.execute(cosa_a_anadir)
    conexion.commit()
    conexion.close()


# buscar_repuestos("Samsung", "Galaxy S7 Edgee")
# lista = "Samsung@/@Galaxy S7 Edgee@/@Camara delan@/@0@/@Rojo*/*" \
#         "Samsung@/@Galaxy S7 Edgee@/@Camara trasera@/@0@/@Azul*/*" \
#         "Samsung@/@Galaxy S7 Edgee@/@Carcasa@/@10@/@*/*" \
#         "Samsung@/@Galaxy S7 Edgee@/@Carcasa@/@15@/@*/*" \
#         "Samsung@/@Galaxy S7 Edgee@/@Placa Madre@/@0@/@"
# guardar_repuestos(lista)

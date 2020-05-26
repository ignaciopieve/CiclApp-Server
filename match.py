import mysql.connector
import inventario

def matcheo(marca, modelo):
    telefonos = []

    conexion = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "administrador",
        database = "ultimavers_db"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM CELULAR")
    filas = cursor.fetchall()

    for a in filas:
        if a[2] == marca and a[3] == modelo:
            if es_reparable(a, 0):
                riesgo, tiempo = devolver(a)
                telefonos.append([a[1], round(riesgo), round(tiempo), round(((riesgo + tiempo)/2))])

    telefonos = sorted(telefonos, key=lambda x: x[3])

    conexion.close()

    for a in range(len(telefonos)):
        for b in range(len(telefonos[a])):
            telefonos[a][b] = str(telefonos[a][b])

    return telefonos


def matcheo2(marca, modelo):
    telefonos = []

    conexion = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "administrador",
        database = "ultimavers_db"
    )

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM CELULAR")
    filas = cursor.fetchall()

    for a in filas:
        if a[2] == marca and a[3] == modelo:
            if es_reparable(a, 0):
                riesgo, tiempo = devolver(a)
                telefonos.append([a[1], round(riesgo), round(tiempo), round(((riesgo + tiempo)/2)), es_reparable(a, 1)])

    telefonos = sorted(telefonos, key=lambda x: x[3])
    conexion.close()

    for a in range(len(telefonos)):
        for b in range(len(telefonos[a])):
            telefonos[a][b] = str(telefonos[a][b])

    return telefonos

def devolver(telefono):
    ponderacion_riesgo = 0
    ponderacion_riesgo_promedio = 0
    ponderacion_tiempo = 0
    ponderacion_tiempo_promedio = 0
    cantidad = 0
    lista_ponderaciones = [["Samsung","Galaxy S7 Edge",79,(2,2),(2,3),(2,3),(5,5),(2,3),(3,3),(2,2),(2,2),(2,2),(5,5),(3,4),(5,3),(1,1),(5,5),(5,5)],
                            ["Samsung","Galaxy S8",47,(2,2),(2,3),(2,3),(2,3),(2,3),(3,3),(2,2),(2,2),(2,2),(5,5),(3,4),(5,3),(1,1),(2,3),(5,5)],
                            ["Samsung","Galaxy Grand Prime",46,(1,1),(3,4),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(1,1),(4,5),(3,4),(2,3),(1,1),(3,3),(3,3)],
                            ["Samsung","Galaxy S8+",30,(2,2),(2,3),(2,3),(2,3),(2,3),(3,3),(2,2),(2,2),(2,2),(5,5),(3,4),(5,3),(1,1),(2,3),(5,5)],
                            ["Samsung","Galaxy J1",28,(1,1),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(1,1),(3,4),(3,3),(2,3),(1,1),(3,3),(3,3)],
                            ["Samsung","Galaxy S6 Edge",21,(2,2),(2,3),(2,3),(2,2),(2,2),(3,3),(2,2),(2,2),(2,2),(5,5),(3,4),(2,2),(1,1),(2,2),(5,5)],
                            ["Motorola","Moto G (3rd gen)",20,(1,1),(2,3),(2,3),(3,3),(2,2),(2,2),(3,3),(3,3),(2,2),(3,4),(2,2),(5,5),(2,2),(3,3),(3,3)],
                            ["Samsung","Galaxy J7",13,(1,1),(3,3),(3,3),(3,3),(5,3),(3,3),(3,3),(3,3),(1,1),(4,4),(3,3),(2,2),(3,3),(3,3),(3,3)],
                            ["Samsung","Galaxy J7 (2016)",13,(1,1),(1,2),(1,2),(3,3),(3,4),(1,2),(1,2),(1,2),(1,1),(4,4),(3,3),(2,2),(3,3),(3,3),(3,3)]]

    for a in lista_ponderaciones:
        if telefono[2] == a[0] and telefono[3] == a[1]:
            #	3	CARCASA				9
            if telefono[9] == "X" or telefono[9] == "0":
                ponderacion_riesgo += a[3][0]
                ponderacion_tiempo += a[3][1]
                cantidad += 1

            #	4	CAMARA TRASERA		10
            if telefono[10] == "X" or telefono[10] == "0":
                ponderacion_riesgo += a[4][0]
                ponderacion_tiempo += a[4][1]
                cantidad += 1

            #	5	CAMARA DELANTERA	11
            if telefono[11] == "X" or telefono[11] == "0":
                ponderacion_riesgo += a[5][0]
                ponderacion_tiempo += a[5][1]
                cantidad += 1

            #	6	PIN DE CARGA		12
            if telefono[12] == "X" or telefono[12] == "0":
                ponderacion_riesgo += a[6][0]
                ponderacion_tiempo += a[6][1]
                cantidad += 1

            #	7	AURICULAR			13
            if telefono[13] == "X" or telefono[13] == "0":
                ponderacion_riesgo += a[7][0]
                ponderacion_tiempo += a[7][1]
                cantidad += 1

            #	8	PARLANTE DELANTERO	14
            if telefono[14] == "X" or telefono[14] == "0":
                ponderacion_riesgo += a[8][0]
                ponderacion_tiempo += a[8][1]
                cantidad += 1

            #	9	PARLANTE TRASERO	15
            if telefono[15] == "X" or telefono[15] == "0":
                ponderacion_riesgo += a[9][0]
                ponderacion_tiempo += a[9][1]
                cantidad += 1

            #	10	SENSOR PROX			16
            if telefono[16] == "X" or telefono[16] == "0":
                ponderacion_riesgo += a[10][0]
                ponderacion_tiempo += a[10][1]
                cantidad += 1

            #	11	BATERIA				17
            if telefono[17] == "X" or telefono[17] == "0":
                ponderacion_riesgo += a[11][0]
                ponderacion_tiempo += a[11][1]
                cantidad += 1

            #	14	LIBERAR				27
            if telefono[27] == "X" or telefono[27] == "0":
                ponderacion_riesgo += a[14][0]
                ponderacion_tiempo += a[14][1]
                cantidad += 1

            #	15	PORTA SIM			28
            if telefono[28] == "X" or telefono[28] == "0":
                ponderacion_riesgo += a[15][0]
                ponderacion_tiempo += a[15][1]
                cantidad += 1

            #	16	MICROFONO			29
            if telefono[29] == "X" or telefono[29] == "0":
                ponderacion_riesgo += a[16][0]
                ponderacion_tiempo += a[16][1]
                cantidad += 1

            if cantidad > 0:
                ponderacion_riesgo_promedio = ponderacion_riesgo / cantidad
                ponderacion_tiempo_promedio = ponderacion_tiempo / cantidad

            #	12	VIDRIO 				21
            if telefono[21] == "NO" or telefono[21] == "3":
                ponderacion_riesgo_promedio += a[12][0]
                ponderacion_tiempo_promedio += a[12][1]

            #	13	MODULO				22
            if telefono[22] == "NO" or telefono[22] == "4":
                ponderacion_riesgo_promedio += a[13][0]
                ponderacion_tiempo_promedio += a[13][1]

            #	17	TACTIL				31
            if telefono[31] == "X" or telefono[31] == "0":
                ponderacion_riesgo_promedio += a[17][0]
                ponderacion_tiempo_promedio += a[17][1]

            break

    return ponderacion_riesgo_promedio, ponderacion_tiempo_promedio

def es_reparable(telefono, instruccion):
    # Si la instruccion es 0, solo devuelve un booleano (1 = es reparable / 0 = no es reparable)
    # Si la instruccion es 1, devuelve detalladamente de donde hay que sacar cada parte

    conexion = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "administrador",
        database = "ultimavers_db"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM CELULAR")
    filas = cursor.fetchall()

    # 0	CARCASA	                # 8	    BATERIA
    # 1	CAMARA TRASERA	        # 9	    VIDRIO
    # 2	CAMARA DELANTERA	    # 10	MODULO
    # 3	PIN DE CARGA	        # 11	LIBERAR
    # 4	AURICULAR	            # 12	PORTA SIM
    # 5	PARLANTE DELANTERO	    # 13	MICROFONO
    # 6	PARLANTE TRASERO	    # 14	TACTIL
    # 7	SENSOR PROX
    repuestos_que_hay = inventario.buscar_repuestos_interno(telefono[2], telefono[3])
    partes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sacando_repuestos = []

    mensaje = "ID: " + str(telefono[0]) + "\n"
    mensaje += "IMEI: " + str(telefono[1]) + "\n"
    mensaje += "MARCA: " + str(telefono[2]) + "\n"
    mensaje += "MODELO: " + str(telefono[3]) + "\n\n"


    # Aca vemos que partes necesitan repuesto
    if True:
        if telefono[9] == "X" or telefono[9] == "0":
            partes[0] = 1
        if telefono[10] == "X" or telefono[10] == "0":
            partes[1] = 1
        if telefono[11] == "X" or telefono[11] == "0":
            partes[2] = 1
        if telefono[12] == "X" or telefono[12] == "0":
            partes[3] = 1
        if telefono[13] == "X" or telefono[13] == "0":
            partes[4] = 1
        if telefono[14] == "X" or telefono[14] == "0":
            partes[5] = 1
        if telefono[15] == "X" or telefono[15] == "0":
            partes[6] = 1
        if telefono[16] == "X" or telefono[16] == "0":
            partes[7] = 1
        if telefono[17] == "X" or telefono[17] == "0":
            partes[8] = 1
        if telefono[21] == "NO" or telefono[21] == "3":
            partes[9] = 1
        if telefono[22] == "NO" or telefono[22] == "4":
            partes[10] = 1
        if telefono[27] == "X" or telefono[27] == "0":
            partes[11] = 1
        if telefono[28] == "X" or telefono[28] == "0":
            partes[12] = 1
        if telefono[29] == "X" or telefono[29] == "0":
            partes[13] = 1
        if telefono[31] == "X" or telefono[31] == "0":
            partes[14] = 1

    print("---- INICIO ----")
    print(partes)
    print("---- INICIO ----")
    listo_para_vender = 1
    for a in partes:
        if a == 1:
            listo_para_vender = 0
            break

    if listo_para_vender == 0:
        mensaje += "El telefono es reparable. Las partes a reparar son:\n\n"
        # Armamos la listas de telefonos que coinciden con el modelo, exceptuando el telefono mismo
        telefonos_del_modelo = []
        for a in filas:
            if a[2] == telefono[2] and a[3] == telefono[3] and a[0] != telefono[0]:
                telefono = list(a)
                ponderacion = devolver(a)
                ponderacion_simple = (ponderacion[0] + ponderacion[1]) / 2
                telefono.append(ponderacion_simple)
                telefonos_del_modelo.append(telefono)
        telefonos_del_modelo = sorted(telefonos_del_modelo, key=lambda x: x[-1])

        # ---------------------------------------------------- MATCHEO -------------------------------------------------
        # Ahora vemos telefono por telefono de donde podemos sacar las partes
        if True:
            # Primero revisamos el inventario
            if partes[0] == 1 and repuestos_que_hay[0] == 1:
                partes[0] = 0
                mensaje += "Sacar carcasa del inventario\n"
            if partes[1] == 1 and repuestos_que_hay[1] == 1:
                partes[1] = 0
                mensaje += "Sacar camara trasera del inventario\n"
            if partes[2] == 1 and repuestos_que_hay[2] == 1:
                partes[2] = 0
                mensaje += "Sacar camara delantera del inventario\n"
            if partes[3] == 1 and repuestos_que_hay[3] == 1:
                partes[3] = 0
                mensaje += "Sacar pin de carga del inventario\n"
            if partes[4] == 1 and repuestos_que_hay[4] == 1:
                partes[4] = 0
                mensaje += "Sacar jack de auricular del inventario\n"
            if partes[5] == 1 and repuestos_que_hay[5] == 1:
                partes[5] = 0
                mensaje += "Sacar parlante delantero del inventario\n"
            if partes[6] == 1 and repuestos_que_hay[6] == 1:
                partes[6] = 0
                mensaje += "Sacar parlante trasero del inventario\n"
            if partes[7] == 1 and repuestos_que_hay[7] == 1:
                partes[7] = 0
                mensaje += "Sacar sensor de proximidad del inventario\n"
            if partes[8] == 1 and repuestos_que_hay[8] == 1:
                partes[8] = 0
                mensaje += "Sacar bateria del inventario\n"
            if (partes[10] == 1 or partes[14] == 1) and repuestos_que_hay[9] == 1:
                partes[9] = 0
                partes[10] = 0
                partes[14] = 0
                mensaje += "Sacar modulo del inventario\n"
            if partes[12] == 1 and repuestos_que_hay[10] == 1:
                partes[12] = 0
                mensaje += "Sacar portasim del inventario\n"
            if partes[13] == 1 and repuestos_que_hay[11] == 1:
                partes[13] = 0
                mensaje += "Sacar microfono del inventario\n"

            if partes[11] == 1:
                mensaje += "\nLiberar\n"
                partes[11] = 0

            if partes[9] == 1:
                mensaje += "\nReemplazar vidrio\n"
                partes[9] = 0

            if partes[0] == 1:
                for a in sacando_repuestos:
                    if a[9] == "-" or a[9] == "1":
                        mensaje += "\nCarcasa del telefono con IMEI " + str(a[1])
                        partes[0] = 0
                        break
                if partes[0] == 1:
                    for a in telefonos_del_modelo:
                        if a[9] == "-" or a[9] == "1":
                            mensaje += "\nCarcasa del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[0] = 0
                            break

            if partes[1] == 1:
                for a in sacando_repuestos:
                    if a[10] == "-" or a[10] == "1":
                        mensaje += "\nCamara trasera del telefono con IMEI " + str(a[1])
                        partes[1] = 0
                        break
                if partes[1] == 1:
                    for a in telefonos_del_modelo:
                        if a[10] == "-" or a[10] == "1":
                            mensaje += "\nCamara trasera del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[1] = 0
                            break

            if partes[2] == 1:
                for a in sacando_repuestos:
                    if a[11] == "-" or a[11] == "1":
                        mensaje += "\nCamara delantera del telefono con IMEI " + str(a[1])
                        partes[2] = 0
                        break
                if partes[2] == 1:
                    for a in telefonos_del_modelo:
                        if a[11] == "-" or a[11] == "1":
                            mensaje += "\nCamara delantera del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[2] = 0
                            break

            if partes[3] == 1:
                for a in sacando_repuestos:
                    if a[12] == "-" or a[12] == "1":
                        mensaje += "\nPin de carga del telefono con IMEI " + str(a[1])
                        partes[3] = 0
                        break
                if partes[3] == 1:
                    for a in telefonos_del_modelo:
                        if a[12] == "-" or a[12] == "1":
                            mensaje += "\nPin de carga del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[3] = 0
                            break

            if partes[4] == 1:
                for a in sacando_repuestos:
                    if a[13] == "-" or a[13] == "1":
                        mensaje += "\nJack de auriculares del telefono con IMEI " + str(a[1])
                        partes[4] = 0
                        break
                if partes[4] == 1:
                    for a in telefonos_del_modelo:
                        if a[13] == "-" or a[13] == "1":
                            mensaje += "\nJack de auriculares del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[4] = 0
                            break

            if partes[5] == 1:
                for a in sacando_repuestos:
                    if a[14] == "-" or a[14] == "1":
                        mensaje += "\nParlante delantero del telefono con IMEI " + str(a[1])
                        partes[5] = 0
                        break
                if partes[5] == 1:
                    for a in telefonos_del_modelo:
                        if a[14] == "-" or a[14] == "1":
                            mensaje += "\nParlante delantero del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[5] = 0
                            break

            if partes[6] == 1:
                for a in sacando_repuestos:
                    if a[15] == "-" or a[15] == "1":
                        mensaje += "\nParlante trasero del telefono con IMEI " + str(a[1])
                        partes[6] = 0
                        break
                if partes[6] == 1:
                    for a in telefonos_del_modelo:
                        if a[15] == "-" or a[15] == "1":
                            mensaje += "\nParlante trasero del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[6] = 0
                            break

            if partes[7] == 1:
                for a in sacando_repuestos:
                    if a[16] == "-" or a[16] == "1":
                        mensaje += "\nSensor de proximidad del telefono con IMEI " + str(a[1])
                        partes[7] = 0
                        break
                if partes[7] == 1:
                    for a in telefonos_del_modelo:
                        if a[16] == "-" or a[16] == "1":
                            mensaje += "\nSensor de proximidad del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[7] = 0
                            break

            if partes[8] == 1:
                for a in sacando_repuestos:
                    if a[17] == "-" or a[17] == "1":
                        mensaje += "\nBateria del telefono con IMEI " + str(a[1])
                        partes[8] = 0
                        break
                if partes[8] == 1:
                    for a in telefonos_del_modelo:
                        if a[17] == "-" or a[17] == "1":
                            mensaje += "\nBateria del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[8] = 0
                            break

            if partes[10] == 1:
                for a in sacando_repuestos:
                    if a[22] == "Ok":
                        mensaje += "\nModulo del telefono con IMEI " + str(a[1])
                        partes[10] = 0
                        break
                if partes[10] == 1:
                    for a in telefonos_del_modelo:
                        if a[22] == "Ok":
                            mensaje += "\nModulo del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[10] = 0
                            break

            if partes[12] == 1:
                for a in sacando_repuestos:
                    if a[28] == "-" or a[28] == "1":
                        mensaje += "\nPorta sim del telefono con IMEI " + str(a[1])
                        partes[12] = 0
                        break
                if partes[12] == 1:
                    for a in telefonos_del_modelo:
                        if a[28] == "-" or a[28] == "1":
                            mensaje += "\nPorta sim del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[12] = 0
                            break

            if partes[13] == 1:
                for a in sacando_repuestos:
                    if a[29] == "-" or a[29] == "1":
                        mensaje += "\nMicrofono del telefono con IMEI " + str(a[1])
                        partes[13] = 0
                        break
                if partes[13] == 1:
                    for a in telefonos_del_modelo:
                        if a[29] == "-" or a[29] == "1":
                            mensaje += "\nMicrofono del telefono con IMEI " + str(a[1])
                            sacando_repuestos.append(a)
                            partes[13] = 0
                            break

        # ------------------------------------------------ FIN DEL MATCHEO ---------------------------------------------
    else:
        mensaje += "\nEl telefono esta listo para vender."

        print("---- INICIO ----")
        print(partes)
        print("---- INICIO ----")

    for a in partes:
        if a == 1:
            return False
    if instruccion == 1:
        return mensaje
    else:
        return True
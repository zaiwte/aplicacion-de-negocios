import sqlite3
import sys,random,time
import os
import locale
import datetime
import PySimpleGUI as sg

class NegMotor:
    def __init__(self):
        self.nombre_BDD="BD1"

    def editar_inventario(self,ventana,ip):
        """nombre producto
           actualizar cantidad
           recargar total
           cantidad de producto
           total de producto"""

        l=[('-nombre_inv-',    ip[0]),
           ('-actualizar_inv-',ip[1]),
           ('-recargar_inv-',  ip[2]),
           ('-cantidad_inv-',  ip[3]),
           ('-total_inv-',     ip[4])]

        for i in l:
            ventana[i[0]].update(i[1])

    def pedido(self,ventana,prod):
        """nombre producto
           precio mayor
           precio detal
           etiqueta
           cantidad
           precio total bs
           precio tptal $
           cantidad inv
           total inv"""

        for k in ['-BsM_INI-','-BsD_INI-']:
            ventana[k].update(button_color=sg.theme_button_color())

        p=[('-p_ini-',     prod[0]),
           ('-pm_ini-',    prod[1]),
           ('-pd_ini-',    prod[2]),
           ('-e_ini-',     prod[3]),
           ('-c_ini-',     prod[4]),
           ('-ptbs_ini-',  prod[5]),
           ('-pt$_ini-',   prod[6]),
           ('-ci_ini-',    prod[7]),
           ('-ti_ini-',    prod[8])]
        for i in p:
            ventana[i[0]].update(i[1])

    def valor_dolar(self):
        pd="0,00"

        lista_sql=self.ejecutar_sql("SELECT * FROM precio_Dolar")

        if len(lista_sql):
            pd=[self.coma([p for p in t][0],2) for t in lista_sql][0]

        return pd

    def lista_pedidos(self):
        l=[['','','','','','','']]
        lista_sql=self.ejecutar_sql("SELECT * FROM pedidos")

        total_bs="0,00"
        total_dl="0,0000"


        if len(lista_sql):
            l=[[t[0],self.coma(float(t[1]),2),
                     self.coma(float(t[2]),2),
                     self.coma(float(t[3]),2),
                     self.coma(float(t[4]),2),
                     self.coma(float(t[5]),4),t[6]] for t in lista_sql]

            #suma los totales

            total_bs=self.coma(sum([t[0] for t in self.ejecutar_sql("SELECT pt_bs FROM pedidos")]),2)
            total_dl=self.coma(sum([t[0] for t in self.ejecutar_sql("SELECT pt_d FROM pedidos")]),4)


        return (l, total_bs, total_dl)

    def lista_de_etiquetas(self):
        return [[e for e in t][0] for t in self.ejecutar_sql("SELECT * FROM etiquetas")]

    def lista_nombres_de_productos(self):
        l=[]
        lista_sql=self.ejecutar_sql("SELECT * FROM productos")
        if len(lista_sql):
            l=[n[0] for n in lista_sql]
        return l

    def lista_de_productos(self,ins="SELECT * FROM productos"):
        l=[['','','','']]
        lista_sql=self.ejecutar_sql(ins)
        if len(lista_sql):
            l=[[t[0],self.coma(float(t[1]),2),self.coma(float(t[2]),2),t[3]] for t in lista_sql]
        return l

    def lista_de_inventario(self):
        l=[['','','']]
        lista_sql=self.ejecutar_sql("SELECT * FROM Inventario")
        if len(lista_sql):
            l=[[t[0],self.coma(float(t[1]),2),self.coma(float(t[2]),2)] for t in lista_sql]
        return l

    def coma(self,numero,n):
        locale.setlocale(locale.LC_ALL,"")
        return locale.format_string("%.{}f".format(n),numero,grouping=True)

    def expandir(self,ventana,lista,ex=True,ey=True,er=True):
        for i in lista:
            ventana[i].expand(expand_x = ex,expand_y =ey,expand_row =er)

    def validar_numero(self,ventana,valores,evento,lista):
        for h in lista:
            ventana[h].bind("<Button-1>","B1")
            ventana[h].bind("<Button-2>","B2")
            ventana[h].bind("<B1-Motion>","BM1")
            ventana[h].bind("<B2-Motion>","BM2")
            ventana[h].bind("<ButtonRelease-1>","BR1")
            ventana[h].bind("<ButtonRelease-2>","BR2")

            if evento in (h+'B1',h+'B2',h+'BM1',h+'BM2',h+'BR1',h+'BR2'):
                ventana[h].update(valores[h])

        for i in lista:
            if len(valores[i]) and (valores[i][-1] not in ('0123456789,.') or (valores[i][0]==',') or (valores[i][-1]=='.')):
                ventana[i].update(valores[i][:-1])

            elif "," in valores[i]:
                if valores[i].count(",")>1:
                    ventana[i].update(valores[i][:-1])
                else:
                    try:
                        v=float(self.punto(valores[i]))
                        if len(valores[i][valores[i].index(",")+1:])>2:
                            valores[i]=self.coma(v,'2')
                    except:
                        valores[i]=""
                    ventana[i].update(valores[i])

            elif len(valores[i]):
                valores[i]=valores[i].replace(".","")
                try:
                    valores[i]=self.coma(float(valores[i]),'0')
                except:
                    valores[i]=""
                ventana[i].update(valores[i])

    def validar_cadena(self,valores,lista,limite=10):
        validacion=True
        error="0"
        for i in lista:
            if len(valores[i])>limite:
                validacion=False
                error="1"
                break
            elif len(valores[i])==0:
                validacion=False
                error="2"
                break

        return (validacion,error)

    def punto(self,numero):
        try:
            if "." in numero:
                numero=numero.replace(".","")
                return numero.replace(",",".")
            else:
                return numero.replace(",",".")
        except:
            return numero

    def ejecutar_sql(self,instruccion,parametro=()):
        conexion=sqlite3.connect(self.nombre_BDD)
        cursor1=conexion.cursor()

        cursor1.execute(instruccion,parametro)
        mostrar=cursor1.fetchall()
        conexion.commit()

        conexion.close()
        return mostrar

    def crear_tablas_sql(self):
        tablas=["create table productos (Nombre_producto varchar(50) unique,Precio_mayor real,Precio_detal real,Etiqueta varchar(50))",

				"create table etiquetas (Nombre_etiquetas varchar(50) unique)",

				"create table precio_Dolar (precio_dolar_bs real unique)",

				"create table Inventario (N_producto varchar(50) unique,Cantidad_producto real,Total real)",

                "create table pedidos (n_p varchar(50) unique, p_m real, p_d real, c_p real, pt_bs real, pt_d real, e_p varchar(50),t_inv real)"

				]
        for i in tablas:
            try:
                self.ejecutar_sql(i)
            except:
                print("tabla ya creada")

class Ventana_mensaje:
    def __init__(self,titulo="mensaje"):
        self.titulo=titulo

    def ver(self,mensaje="Texto"):
        dise=[[sg.Text(mensaje,font='18')],
                [sg.Button("OK",key='-OK-',font='20')]]

        ventanaMensaje=sg.Window(self.titulo, dise, element_justification='center',finalize=True,auto_close_duration=3)
        ventanaMensaje.make_modal()
        while True:
            evento,valores=ventanaMensaje.read()

            if evento in (sg.WIN_CLOSED, 'Exit'):
                break

            elif evento=='-OK-':
                ventanaMensaje.close()

        ventanaMensaje.close()

class Ventana_busqueda:
    def __init__(self,titulo="crear"):
        self.titulo=titulo

    def ver(self):
        F_1=[[sg.Table(headings=[i for i in ['PRODUCTO','P. AL MAYOR','P. AL DETAL','CANTIDAD','TOTAL BS','TOTAL $','ETIQUETA']],
                               values=[['','','','','','','']],
                               justification='left',
                               font=['20'],
                               auto_size_columns=False,
                               def_col_width=10,
                               num_rows=12,
                               vertical_scroll_only=False,
                               k='-TABLA-')]]

        F_2=[[sg.Text('NOTA',font='20'),sg.Input(size=(60,0),font='18',k='-nota-')],
             [sg.Text('DOLAR',font='20'),sg.Input(size=(60,0),justification='right',font='24',k='-dolar-')],
             [sg.Text('COMPRA TOTAL BS',font='20'),sg.Input(size=(60,0),justification='right',font='24',k='-ctbs-')],
             [sg.Text('COMPRA TOTAL $',font='20'),sg.Input(size=(60,0,),justification='right',font='24',k='-ct$-')],
             [sg.Button('DOCUMENTAR',size=(66,0),k='-D-')]]

        f1=sg.Frame('',F_1,  element_justification='center',  vertical_alignment='center',k='-f1-')
        f2=sg.Frame('',F_2,  element_justification='center',  vertical_alignment='center',k='-f2-')
        fa=sg.Frame('',[[f1],[f2]],  element_justification='center',  vertical_alignment='center',k='-fa-')
        dise=[[fa]]


        ventanaBuscar=sg.Window(self.titulo, dise, element_justification='center',finalize=True)
        ventanaBuscar.make_modal()
        while True:
            evento,valores=ventanaBuscar.read(timeout=1000)

            if evento in (sg.WIN_CLOSED, 'Exit'):
                break

            #NegMotor().expandir(ventanaBuscar,['-f2-'])

            NegMotor().expandir(ventanaBuscar,['-f2-',
                                               '-nota-',
                                               '-dolar-',
                                               '-ctbs-',
                                               '-ct$-',
                                               '-D-',
                                               ],ey=False)

            if evento=='-D-':
                ventanaBuscar.close()

        ventanaBuscar.close()

class Ventana_dolar:
    def __init__(self,titulo="dolar"):
        self.titulo=titulo

    def ver(self):
        dise=[[sg.Input('1',justification='right',readonly=True,size=(20,0),font='18',k='-dolar-'),sg.Text('$  ',font='20')],
                [sg.Input(NegMotor().valor_dolar(),justification='right',size=(20,0),font='18',k='-dolarBs-',enable_events=True),sg.Text('Bs',font='20')],
                [sg.Button("CAMBIAR",key='-CAMBIAR-',font='20',size=(24,0))]]

        ventanaDolar=sg.Window(self.titulo, dise, element_justification='center',finalize=True)
        ventanaDolar.make_modal()
        while True:
            evento,valores=ventanaDolar.read(timeout=1000)

            if evento in (sg.WIN_CLOSED, 'Exit'):
                break

            NegMotor().validar_numero(ventanaDolar,valores,evento,['-dolarBs-'])


            if evento=='-CAMBIAR-':
                try:
                    try:
                        NegMotor().ejecutar_sql("DELETE FROM precio_Dolar")
                    except:
                        print("nada que borrar")

                    nuevo_precio=float(NegMotor().punto(valores['-dolarBs-']))

                    NegMotor().ejecutar_sql("INSERT INTO precio_Dolar values (?)",(nuevo_precio,))
                    ventanaDolar.close()
                except:
                    print("error")

        ventanaDolar.close()

class Ventana_editar:
    def __init__(self,titulo="editar"):
        self.titulo=titulo

    def ver(self,producto):
        dise=[[sg.Text('NOMBRE',font='20'),sg.Input(producto[0],justification='left',font='18',size=(20,0),key='-nombre-')],
                [sg.Text('P.MAYOR',font='20'),sg.Input(producto[1],justification='left',font='18',size=(20,0),key='-p_mayor-',enable_events=True)],
                [sg.Text('P.DETAL',font='20'),sg.Input(producto[2],justification='left',font='18',size=(20,0),key='-p_detal-',enable_events=True)],
                [sg.Text('ETIQUETA',font='20',pad=(0,(20,0)))],
                [sg.Combo(values=NegMotor().lista_de_etiquetas(),
                               size=(30,0),
                               key='-COMBO-',
                               font='18',
                               default_value=producto[3])],
                [sg.Button('GUARDAR',size=(30,0),pad=(0,(20,0)),key='-GUARDAR-')]]

        ventanaEditar=sg.Window(self.titulo,dise, element_justification='center',finalize=True)
        ventanaEditar.make_modal()
        while True:
            evento,valores=ventanaEditar.read(timeout=1000)

            if evento in (sg.WIN_CLOSED, 'Exit'):
                break

            NegMotor().validar_numero(ventanaEditar,valores,evento,['-p_mayor-','-p_detal-'])

            if evento=='-GUARDAR-':

                validado=NegMotor().validar_cadena(valores,['-nombre-','-p_mayor-','-p_detal-','-COMBO-'],limite=30)

                if not validado[0] and validado[1]=="1":
                    Ventana_mensaje().ver("el limite de caracteres es 10")
                    ventanaEditar.make_modal()

                elif not validado[0] and validado[1]=="2":
                    Ventana_mensaje().ver("rellene todos los campos")
                    ventanaEditar.make_modal()

                elif validado[0]:
                    try:
                        valores['-p_mayor-']=float(NegMotor().punto(valores['-p_mayor-']))
                        valores['-p_detal-']=float(NegMotor().punto(valores['-p_detal-']))

                        NegMotor().ejecutar_sql("""UPDATE productos SET
                                                    Nombre_producto = '{}',
                                                    Precio_mayor = {},
                                                    Precio_detal = {},
                                                    Etiqueta = '{}'
                                                    WHERE Nombre_producto = '{}' """.format(valores['-nombre-'],
                                                                                            valores['-p_mayor-'],
                                                                                            valores['-p_detal-'],
                                                                                            valores['-COMBO-'],
                                                                                            producto[0]))
                        try:
                            NegMotor().ejecutar_sql("""UPDATE Inventario SET
                                                        N_producto = '{}'
                                                        WHERE N_producto = '{}'""".format(valores['-nombre-'],
                                                                                          producto[0]))
                        except:
                            pass
                        ventanaEditar.close()

                    except:
                        Ventana_mensaje().ver("error al editar")
                        ventanaEditar.make_modal()

        ventanaEditar.close()

class Ventana_registro:
    def __init__(self,titulo="registro"):
        self.titulo=titulo

    def ver(self):
        disen=[[sg.Text('NOMBRE',font='20'),sg.Input(justification='left',font='18',key='-nombre-')],
             [sg.Text('P.MAYOR',font='20'),sg.Input(justification='left',font='18',key='-p_mayor-',enable_events=True)],
             [sg.Text('P.DETAL',font='20'),sg.Input(justification='left',font='18',key='-p_detal-',enable_events=True)],
             [sg.Text('ETIQUETA',font='20'),sg.Combo(values=NegMotor().lista_de_etiquetas(),
                                                     size=(40,0),
                                                     key='-COMBO-',
                                                     font='18',
                                                     )],

             [sg.Button('AGREGAR',size=(30,0),key='-AGREGAR-'),sg.Button('ELIMINAR',size=(30,0),key='-ELIMINAR-')],
             [sg.Button('GUARDAR',size=(60,0),key='-GUARDAR-')]]

        ventanaRegistro=sg.Window(self.titulo, disen, element_justification='center',finalize=True)
        ventanaRegistro.make_modal()
        validado=False

        while True:
            evento,valores=ventanaRegistro.read(timeout=1000)

            if evento in (sg.WIN_CLOSED, 'Exit'):
                break

            NegMotor().validar_numero(ventanaRegistro,valores,evento,['-p_mayor-','-p_detal-'])

            if evento=='-AGREGAR-':
                validado=NegMotor().validar_cadena(valores,['-COMBO-'],limite=30)

                if not validado[0] and validado[1]=="1":
                    Ventana_mensaje().ver("el limite de caracteres es 30")
                    ventanaRegistro.make_modal()

                elif not validado[0] and validado[1]=="2":
                    Ventana_mensaje().ver("rellene el campo")
                    ventanaRegistro.make_modal()

                elif validado[0]:
                    try:
                        etiqueta=valores['-COMBO-']

                        NegMotor().ejecutar_sql("INSERT INTO etiquetas values (?)",(etiqueta,))
                        ventanaRegistro['-COMBO-'].update(value="",values=NegMotor().lista_de_etiquetas())
                    except:
                        Ventana_mensaje().ver("error al agregar {}".format(etiqueta))
                        ventanaRegistro.make_modal()




            elif evento=='-ELIMINAR-':
                etiqueta=ventanaRegistro['-COMBO-'].get()

                try:
                    NegMotor().ejecutar_sql("DELETE FROM etiquetas WHERE Nombre_etiquetas='{}'".format(etiqueta))
                    ventanaRegistro['-COMBO-'].update(value="",values=NegMotor().lista_de_etiquetas())
                except:
                    Ventana_mensaje().ver("error al eliminar {}".format(etiqueta))
                    ventanaRegistro.make_modal()



            elif evento=='-GUARDAR-':
                validado=NegMotor().validar_cadena(valores,['-nombre-','-p_mayor-','-p_detal-','-COMBO-'],limite=30)

                if not validado[0] and validado[1]=="1":
                    Ventana_mensaje().ver("el limite de caracteres es 30")
                    ventanaRegistro.make_modal()

                elif not validado[0] and validado[1]=="2":
                    Ventana_mensaje().ver("rellene todos los campos")
                    ventanaRegistro.make_modal()

                elif validado[0]:
                    try:
                        valores['-p_mayor-']=float(NegMotor().punto(valores['-p_mayor-']))
                        valores['-p_detal-']=float(NegMotor().punto(valores['-p_detal-']))

                        producto=(valores['-nombre-'],
                                  valores['-p_mayor-'],
                                  valores['-p_detal-'],
                                  valores['-COMBO-'])

                        NegMotor().ejecutar_sql("INSERT INTO productos values (?,?,?,?)",producto)

                        for indice in ['-nombre-','-p_mayor-','-p_detal-','-COMBO-']:
                            ventanaRegistro[indice].update("")

                        validado=True

                    except:
                        Ventana_mensaje().ver("error al guardar")
                        ventanaRegistro.make_modal()

        ventanaRegistro.close()
        return validado

class Ventas(NegMotor):
    def __init__(self):
        self.nombre_BDD:str
        self.numero:int = 0

    def fecha(self):
        dias_semana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        ahora =datetime.datetime.now()
        dia = ahora.weekday()
        return (dias_semana[dia],ahora.day,ahora.month,ahora.year)

    def contador(self):
        self.numero+=1

        instrucciones = ["DELETE FROM pedidos",
                       "INSERT INTO nop VALUES (?,)",
                       "SELECT * FROM pedidos"]
        for i in instrucciones:
            try:
                self.motor.ejecutar_sql(i,)
            except:
                print()
        try:
            self.motor.ejecutar_sql("DELETE FROM pedidos")
        except:
            print("error delete nop")
        try:
            self.ejecutar_sql("INSERT INTO nop VALUES (?,)",(self.numero,))
        except:
            print("error insert nop")
        try:
            self.motor.ejecutar_sql("SELECT * FROM pedidos")
        except:
            print("error select nop")

        return self.numero

    def carpeta(self,nombreCarpeta:str) -> str:
        try:
            os.mkdir(nombreCarpeta)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("la carpeta ya existe")

        return nombreCarpeta

    def crear_tablas_sql(self):
        tablas = [
            ("compra","create table compra (nop real, n_p varchar(50) unique, p_m real, p_d real, c_p real, pt_bs real, pt_d real, e_p varchar(50))")
            ("factura","create table factura (nop real unique, dlh real, nota varchar(80), ctbs real, ctdl real)")
            ("nop","create table nop(numero int unique)")
                 ]
        for i in tablas:
            try:
                self.ejecutar_sql(i[1])
            except:
                print(f"tabla {i[0]} ya creada")

    def guardar_venta(self,venta:dict):
        #self.nombre_BDD = self.carpeta("ventas") + "/" + [f"{semana}_{dia}_{mes}_{A}" for semana,dia,mes,A in (self.fecha(),)][0]
        #self.crear_tablas_sql()
        self.numero
        nop = self.ejecutar_sql("SELECT * FROM nop)")[0][0]

        try:
            pass
            #self.ejecutar_sql("INSERT INTO nop VALUES (?,)",(,))
        except:
            print("error en nop sql")

        instruccion = { "c":["INSERT INTO compra VALUES (?,?,?,?,?,?,?,?)",venta["c"]],
                        "f":["INSERT INTO factura VALUES (?,?,?,?,?)",venta["f"]],
                        "nop":"INSERT INTO nop VALUES (?,)"}
        try:
            self.ejecutar_sql(comando[llave],parametro)
        except:
            print("error sql")


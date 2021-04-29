import sys,random,time
import os
import negClass
import PySimpleGUI as sg


class NegGui:
    def __init__(self):
        self.h="hola"
        self.motor=negClass.NegMotor()
        self.motor.crear_tablas_sql()
        self.ventanaMensaje=negClass.Ventana_mensaje()
        self.ventanaEditar =negClass.Ventana_editar()
        self.ventanaBuscar =negClass.Ventana_busqueda()
        self.ventanaDolar  =negClass.Ventana_dolar()
        self.ventanaRegistro=negClass.Ventana_registro()

    def tab_inicio(self):
        #sg.Text('Bs',font='14'),sg.Radio('','P',k='-RB1_INI-')
        #sg.Text('Bs',font='14'),sg.Radio('','P',k='-RB2_INI-',default=True)
        #[sg.Button('ACEPTAR',size=(20,0),key='-A_INI-')]

        F_1a=[[sg.Listbox(values=self.motor.lista_nombres_de_productos(),
                             size=(22-6, 20),
                             font=['18'],
                             key='-LISTA_INI-')]]
        F_1b=[[sg.Input(size=(28-6,0),font='20',key='-buscar_ini-')],
                 [sg.Button('BUSCAR',size=(28-6,0),key='-BUSCAR_INI-')],
                 [sg.Button('SELECCIONAR',size=(28-6,0),key='-SELECCIONAR_INI-')] ]


        F_2=[[sg.Input('producto',font='20',size=(28-6,0),justification='center',readonly=True,key='-p_ini-')],
                        [sg.Text('PRECIO MAYOR',font='20')],
                        [sg.Input('0,00',font='18',size=(22-6,0),justification='right',readonly=True,key='-pm_ini-'),sg.Button('Bs M',size=(6,0),key='-BsM_INI-')],
                        [sg.Text('PRECIO DETAL',font='20')],
                        [sg.Input('0,00',font='18',size=(22-6,0),justification='right',readonly=True,key='-pd_ini-'),sg.Button('Bs D',size=(6,0),key='-BsD_INI-')],
                        [sg.Text('ETIQUETA',font='20')],
                        [sg.Input('...',font='20',size=(28-6,0),justification='center',readonly=True,k='-e_ini-')],
                        [sg.Text('CANTIDAD',font='20')],
                        [sg.Input(default_text='1',size=(20-6,0),font='18',justification='center',key='-c_ini-',enable_events=True)],

                        [sg.Text('PRECIO TOTAL',font='20')],
                        [sg.Input('0,00',font='18',justification='right',size=(22-6,0),readonly=True,key='-ptbs_ini-'),sg.Text('Bs',font='14')],
                        [sg.Input('0,0000',font='18',justification='right',size=(22-6,0),readonly=True,key='-pt$_ini-'),sg.Text('$  ',font='14')],
                        [sg.Text('INVENTARIO',font='20')],
                        [sg.Input('0,00',size=(10,0),justification='center',readonly=True,key='-ci_ini-'),sg.Text('/',font='18'),sg.Input('0,00',size=(10,0),justification='center',readonly=True,key='-ti_ini-')],
                        [sg.Button('LLEVAR',size=(28-6,0),key='-LL_INI-')],
                        [sg.Button('CANCELAR',size=(28-6,0),key='-C_INI-')]]


        F_3a=[[sg.Table(values=self.motor.lista_pedidos()[0],
                                headings=['PRODUCTO','P. MAYOR','P. DETAL','CANTIDAD','TOTAL BS','TOTAL $','ETIQUETA'],
                                auto_size_columns=False,
                                justification='left',
                                def_col_width=12,
                                num_rows=12,
                                key='-TABLA_INI-',
                                font=['20'],
                                vertical_scroll_only=False)]]

        F_3b=[[sg.Input(self.motor.valor_dolar(),font='18',justification='right',size=(26+6,0),readonly=True,k='-dolar_ini-'),sg.Button('Bs DOLAR',size=(8,0),k='-CAMBIAR_DOLAR_INI-')],
                [sg.Text('NOTA',font='14'),sg.Input('',font='18',justification='left',size=(14+6,0),k='-nota_ini-')],
                [sg.Input('0,00',font='18',justification='right',size=(20+6,0),readonly=True,k='-ctbs_ini-'),sg.Text('Bs',font='14')],
                [sg.Input('0,0000',font='18',justification='right',size=(20+6,0),readonly=True,k='-ct$_ini-'),sg.Text('$  ',font='14')],
                [sg.Button('CANCELAR',size=(14,0),k='-CANCELAR_INI-'), sg.Button('ELIMINAR',size=(14,0),k='-ELIMINAR_INI-')],
                [sg.Button('GUARDAR',size=(28+6,0),k='-GUARDAR_INI-')]
                          ]
        f1a=sg.Frame('',F_1a,  element_justification='center',  vertical_alignment='center',k='-f1a_ini-')
        f1b=sg.Frame('',F_1b,  element_justification='center',  vertical_alignment='center',k='-f1b_ini-')
        f2=sg.Frame('',F_2,  element_justification='center',  vertical_alignment='center' ,k='-f2_ini-')
        f3a=sg.Frame('',F_3a,  element_justification='center',  vertical_alignment='center' ,k='-f3a_ini-')
        f3b=sg.Frame('',F_3b,  element_justification='center',  vertical_alignment='center' ,k='-f3b_ini-')

        frameA=sg.Frame('',[[f1a],[f1b]], element_justification='center',  vertical_alignment='center',k='-frameA_ini-')
        frameB=sg.Frame('',[[f2]], element_justification='center',  vertical_alignment='center',k='-frameB_ini-')
        frameC=sg.Frame('',[[f3a],[f3b]], element_justification='center',  vertical_alignment='center',k='-frameC_ini-')

        return {"inicio":[frameA,frameB,frameC],
                "frames":['-frameA_ini-',
                          '-frameB_ini-',
                          '-frameC_ini-',
                          '-f1a_ini-',
                          '-f1b_ini-',
                          '-f2_ini-',
                          '-f3a_ini-',
                          '-f3b_ini-'],

                "ex":['-BUSCAR_INI-',
                      '-SELECCIONAR_INI-',
                      '-buscar_ini-',
                      '-p_ini-',
                      '-pm_ini-',
                      '-pd_ini-',
                      '-e_ini-',
                      '-c_ini-',
                      '-ptbs_ini-',
                      '-pt$_ini-',
                      '-ci_ini-',
                      '-ti_ini-',
                      '-LL_INI-',
                      '-C_INI-',
                      '-dolar_ini-',
                      '-nota_ini-',
                      '-ctbs_ini-',
                      '-ct$_ini-',
                      '-BsM_INI-',
                      '-BsD_INI-',
                      '-CANCELAR_INI-',
                      '-ELIMINAR_INI-',
                      '-GUARDAR_INI-'],
                "ey":['-LISTA_INI-',
                      '-TABLA_INI-']}


    def tab_inventario(self):

        F_1=[[sg.Table(headings=[i for i in ['NOMBRE','CANTIDAD','TOTAL']],
                               values=self.motor.lista_de_inventario(),
                               justification='left',
                               font=['20'],
                               vertical_scroll_only=False,
                               auto_size_columns=False,
                               def_col_width=14,
                               num_rows=20,
                               key='-TABLA_INV-')]]

        F_2=[[sg.Input(justification='left',font='20',k='-busqueda_inv-')],
                     [sg.Button('BUSCAR',k='-BUSCAR_INV-')],
                     [sg.Button('SELECCIONAR',k='-SELECCIONAR_INV-')],
                     [sg.Button('ELIMINAR',k='-ELIMINAR_INV-')]]

        F_3=[[sg.Input('PRODUCTO',justification='center',font='20',k='-nombre_inv-',readonly=True)],
                     [sg.Input(justification='center',font='18',size=(10,0),k='-actualizar_inv-',enable_events=True),sg.Button('ACTUALIZAR CANTIDAD',k='-ACTUALIZAR_INV-')],
                     [sg.Input(justification='center',font='18',size=(10,0),k='-recargar_inv-',enable_events=True),sg.Button('RECARGAR TOTAL',k='-RECARGAR_INV-')],
                     [sg.Text('CANTIDAD',font='18',k='-tc-'),sg.Input('0',justification='right',font='18',
                                                                        readonly=True,k='-cantidad_inv-')],
                     [sg.Text('TOTAL',font='18',k='-tt-'),sg.Input('0',justification='right',font='18',
                                                                        readonly=True,k='-total_inv-')],
                     [sg.Button('APLICAR',k='-APLICAR_INV-')]]


        f1=sg.Frame('',F_1,  element_justification='center',  vertical_alignment='center',k='-f1_inv-')
        f2=sg.Frame('',F_2,  element_justification='center',  vertical_alignment='center' ,k='-f2_inv-')
        f3=sg.Frame('',F_3,  element_justification='center',  vertical_alignment='center' ,k='-f3_inv-')

        frameA=sg.Frame('',[[f1]], element_justification='center',  vertical_alignment='center',k='-frameA_inv-')
        frameB=sg.Frame('',[[f2],[f3]], element_justification='center',  vertical_alignment='center',k='-frameB_inv-')

        return {"inventario":[frameA,frameB],
                "frames":['-frameA_inv-','-f1_inv-','-frameB_inv-','-f2_inv-','-f3_inv-'],
                "ex":['-BUSCAR_INV-',
                      '-SELECCIONAR_INV-',
                      '-ELIMINAR_INV-',
                      '-ACTUALIZAR_INV-',
                      '-RECARGAR_INV-',
                      '-APLICAR_INV-',
                      '-nombre_inv-',
                      '-busqueda_inv-',
                      '-cantidad_inv-',
                      '-total_inv-'],
                "ey":['-TABLA_INV-']}

    def tab_config(self):

        #[j for j in i][0] for i in self.negMotor.ejecutar_sql("select * from etiquetas")
        #[sg.Input(justification='center',font='18',size=(20,0), key='-etiqueta_c-')]
        F_1=[[sg.Table(headings=[i for i in ['NOMBRE','PRECIO AL MAYOR','PRECIO AL DETAL','ETIQUETA']],
                               values=self.motor.lista_de_productos(),
                               justification='left',
                               font=['20'],
                               vertical_scroll_only=False,
                               auto_size_columns=False,
                               def_col_width=16,
                               num_rows=18,
                               key='-TABLA_C-')]]



        #[[i for i in ['','','','']] for j in range(0,5)]

        F_2=[[sg.Input(justification='left',k='-busqueda_c-',font='18')],
                     [sg.Button('BUSCAR',size=(60,0),k='-BUSCAR_C-')],
                     [sg.Button('EDITAR',size=(60,0),k='-EDITAR_C-')],
                     [sg.Button('REGISTRO',size=(60,0),k='-REGISTRO_C-')],
                     [sg.Button('ELIMINAR',size=(60,0),k='-ELIMINAR_C-')],
                     [sg.Button('INVENTARIO',size=(60,0),k='-INVENTARIO_C-')]
                     ]

        f1=sg.Frame('',F_1,  element_justification='center',  vertical_alignment='center',k='-f1-')
        #f2=sg.Frame('',F_2,  element_justification='center',  vertical_alignment='center' ,k='-f2-')
        f2=sg.Frame('',F_2,  element_justification='center',  vertical_alignment='center' ,k='-f2-')

        frameA=sg.Frame('',[[f1,f2]], element_justification='center',  vertical_alignment='center',k='-frameA-')

        return {"configuracion":[frameA],
                "frames":['-frameA-','-f1-','-f2-'],
                "ex":['-BUSCAR_C-',
                      '-REGISTRO_C-',
                      '-EDITAR_C-',
                      '-ELIMINAR_C-',
                      '-INVENTARIO_C-',
                      '-busqueda_c-'],
                "ey":['-TABLA_C-']}


    def tab_ventas(self):
        arbol=sg.TreeData()

        def datos():
            arbol.insert(parent='',key='kp',text="19/02/21",values=["lunes"],icon=None)
            arbol.insert(parent='kp',key='kh',text="11:03-am",values=[1],icon=None)
            arbol.insert(parent='',key='kp1',text="20/02/21",values=["lunes"],icon=None)
            arbol.insert(parent='',key='kp2',text="21/02/21",values=["lunes"],icon=None)
            arbol.insert(parent='',key='kp3',text="22/02/21",values=["lunes"],icon=None)
            arbol.insert(parent='',key='kp4',text="23/02/21",values=["lunes"],icon=None)
            arbol.insert(parent='',key='kp5',text="24/02/21",values=["lunes"],icon=None)


        datos()

        F_1=[[sg.Tree(data=arbol,
                      headings=[],
                      auto_size_columns = False,
                      k='-ARBOL-',
                      num_rows=20,
                      col0_width=20)],
             [sg.Button('CREAR',size=(15,0),k='-CREAR_V-')],
             [sg.Button('SELECCIONAR',size=(15,0),k='-SELECCIONAR_V-')],
             [sg.Button('ELIMINAR',size=(15,0),k='-ELIMINAR_V-')]]


        F_2=[[sg.Table(headings=[i for i in ['PRODUCTO','P. AL MAYOR','P. AL DETAL','CANTIDAD','TOTAL BS','TOTAL $','ETIQUETA']],
                               values=[[i for i in ['','','','','','','']] for j in range(0,3)],
                               justification='left',
                               font=['20'],
                               auto_size_columns=False,
                               def_col_width=12,
                               num_rows=14,
                               vertical_scroll_only=False,
                               k='-TABLA_V-')]]


        F_3=[[sg.Input(size=(15,0),font='18',k='-buscar_v-'),sg.Button('BUSCAR',size=(15,0),k='-BUSCAR_V-')],
             [sg.Text('NOMBRE',font='20'),sg.Input(size=(30,0),font='18',k='-n_v-')],
             [sg.Text('COMPRA TOTAL BS',font='20'),sg.Input(size=(30,0),justification='right',font='24',k='-ctbs_v-')],
             [sg.Text('COMPRA TOTAL $   ',font='20'),sg.Input(size=(30,0,),justification='right',font='24',k='-ct$_v-')],
             [sg.Button('DOCUMENTAR',size=(15,0),k='-D_V-'),sg.Button('ELIMINAR',size=(15,0),k='-E_V-')]]



        f1=sg.Frame('',F_1,  element_justification='center',  vertical_alignment='center',k='-f1_v-')
        f2=sg.Frame('',F_2,  element_justification='center',  vertical_alignment='center' ,k='-f2_v-')
        f3=sg.Frame('',F_3,  element_justification='center',  vertical_alignment='center' ,k='-f3_v-')

        frameA=sg.Frame('',[[f1]], element_justification='center',  vertical_alignment='center',k='-frameA_v-')
        frameB=sg.Frame('',[[f2],[f3]], element_justification='center',  vertical_alignment='center',k='-frameB_v-')

        return {"ventas":[frameA,frameB],
                "frames":['-frameA_v-','-frameB_v-','-f1_v-','-f2_v-','-f3_v-'],
                "ex":['-ctbs_v-',
                      '-ct$_v-',
                      '-n_v-',
                      '-buscar_v-',
                      '-BUSCAR_V-',
                      '-D_V-',
                      '-E_V-',
                      '-CREAR_V-',
                      '-SELECCIONAR_V-',
                      '-ELIMINAR_V-'],

                "ey":['-ARBOL-',
                      '-TABLA_V-']}


    def ver(self):

    #sg.Tab('VENTAS',[self.tab_ventas()],
    #                       element_justification='center')

        layout=[ [sg.TabGroup([[sg.Tab('INICIO',[self.tab_inicio()["inicio"]],
                                                element_justification='center'),

                                sg.Tab('INVENTARIO',[self.tab_inventario()["inventario"]],
                                                    element_justification='center'  ),

                                sg.Tab('CONFIGURACION',[self.tab_config()["configuracion"]],
                                                       element_justification='center'  ),

                                sg.Tab('VENTAS',[self.tab_ventas()["ventas"]],
                                                element_justification='center' )

                                ]],k='TAB' ) ] ]


        ventana=sg.Window('NegGui',layout,resizable=True)

        p_elegido=('0,00','0,00')

        while True:
            evento,valores=ventana.read(timeout=1000)

            if evento in (sg.WIN_CLOSED, 'Exit'):
                break

            self.motor.validar_numero(ventana,valores,evento,['-actualizar_inv-','-recargar_inv-','-c_ini-'])

            self.motor.expandir(ventana,['TAB'])

            self.motor.expandir(ventana,self.tab_inicio()["frames"])
            self.motor.expandir(ventana,self.tab_inicio()["ex"],ey=False)
            self.motor.expandir(ventana,self.tab_inicio()["ey"],ex=False)

            self.motor.expandir(ventana,self.tab_config()["frames"])
            self.motor.expandir(ventana,self.tab_config()["ex"],ey=False)
            self.motor.expandir(ventana,self.tab_config()["ey"],ex=False)

            self.motor.expandir(ventana,self.tab_inventario()["frames"])
            self.motor.expandir(ventana,self.tab_inventario()["ex"],ey=False)
            self.motor.expandir(ventana,self.tab_inventario()["ey"],ex=False)

            self.motor.expandir(ventana,self.tab_ventas()["frames"])
            self.motor.expandir(ventana,self.tab_ventas()["ex"],ey=False)
            self.motor.expandir(ventana,self.tab_ventas()["ey"],ex=False)

            ventana['-busqueda_c-'].bind("<Return>","enter")
            ventana['-busqueda_inv-'].bind("<Return>","enter")
            ventana['-buscar_ini-'].bind("<Return>","enter")

            BP={'-BsM_INI-':['-pm_ini-',(valores['-pm_ini-'],'0,00')],
                '-BsD_INI-':['-pd_ini-',('0,00',valores['-pd_ini-'])]}

            ventana['-ctbs_ini-'].update(self.motor.lista_pedidos()[1])
            ventana['-ct$_ini-'].update(self.motor.lista_pedidos()[2])


            #////////////////////////////////////////////////////////////////////////////////////////////////////
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@----INICIO----@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            #////////////////////////////////////////////////////////////////////////////////////////////////////
            if evento in ['-BsM_INI-','-BsD_INI-']:
                for k in ['-BsM_INI-','-BsD_INI-']:
                    ventana[k].update(button_color=sg.theme_button_color())
                ventana[evento].update(button_color=('white','red'))




            if evento in ('-BUSCAR_INI-','-buscar_ini-enter'):
                lista_busqueda=[]
                nombre=ventana['-buscar_ini-'].get()

                for producto in self.motor.lista_nombres_de_productos():
                    if nombre in producto:
                        lista_busqueda.append(producto)

                ventana['-LISTA_INI-'].update(values=lista_busqueda)






            elif evento=='-SELECCIONAR_INI-':
                nombre=valores['-LISTA_INI-']


                try:
                    sql_p=self.motor.ejecutar_sql("SELECT * FROM productos WHERE Nombre_producto='{}'".format(nombre[0]))

                    np=sql_p[0][0]
                    pm=self.motor.coma(sql_p[0][1],2)
                    pd=self.motor.coma(sql_p[0][2],2)
                    e =sql_p[0][3]
                    c ='1'
                    ptbs='0,00'
                    ptd ='0,0000'
                    ci ='0,00'
                    ti ='0,00'

                    try:
                        sql_i=self.motor.ejecutar_sql("SELECT * FROM Inventario WHERE N_producto='{}'".format(nombre[0]))

                        ci=self.motor.coma(sql_i[0][1],2)
                        ti=self.motor.coma(sql_i[0][2],2)

                    except:
                        pass

                    self.motor.pedido(ventana,[np,pm,pd,e,c,ptbs,ptd,ci,ti])

                except:
                    self.ventanaMensaje.ver("seleccione de la lista")







            elif evento in ('-BsM_INI-','-BsD_INI-'):
                nombre = valores['-p_ini-']
                ti="0,00"
                try:
                    sql_i=self.motor.ejecutar_sql("SELECT * FROM Inventario WHERE N_producto='{}'".format(nombre))
                    ti=self.motor.coma(sql_i[0][2],2)

                except:
                    print("pass")
                    pass

                c=ventana['-c_ini-'].get()
                p=ventana[BP[evento][0]].get()
                vd=self.motor.valor_dolar()

                #asignado(BP[evento][1])
                p_elegido=BP[evento][1]

                if not len(c):
                    c=1
                    ventana['-c_ini-'].update("1")

                calculo  =float(self.motor.punto(p))*float(self.motor.punto(c))

                try:
                    calculo_d=calculo/float(self.motor.punto(vd))

                except:
                    calculo_d=0

                calculo_t=0
                if not float(self.motor.punto(ti))==0:
                    calculo_t=float(self.motor.punto(ti))-float(self.motor.punto(c))
                    if calculo_t<0:
                        self.ventanaMensaje.ver("total de inventario excedido")

                ventana['-ti_ini-'].update(self.motor.coma(calculo_t,2))
                ventana['-ptbs_ini-'].update(self.motor.coma(calculo,2))
                ventana['-pt$_ini-'].update(self.motor.coma(calculo_d,4 ))





            elif evento=='-C_INI-':
                print("cancelar")
                self.motor.pedido(ventana,['producto','0,00','0,00','...','1','0,00','0,00','0,00','0,00'])





            elif evento=='-LL_INI-':

                #'-TABLA_INI-'

                lista_pedido=(ventana['-p_ini-'].get(),
                              float(self.motor.punto(p_elegido[0])),
                              float(self.motor.punto(p_elegido[1])),
                              float(self.motor.punto(ventana['-c_ini-'].get())),
                              float(self.motor.punto(ventana['-ptbs_ini-'].get())),
                              float(self.motor.punto(ventana['-pt$_ini-'].get())),
                              ventana['-e_ini-'].get(),
                              float(self.motor.punto(ventana['-ti_ini-'].get())))

                #('-ci_ini-'  ),
                #('-ti_ini-'  )


                if valores['-p_ini-']!='producto':

                    try:

                        self.motor.ejecutar_sql("INSERT INTO pedidos VALUES (?,?,?,?,?,?,?,?)",lista_pedido)


                        #ventana['-ctbs_ini-'].update(self.motor.lista_pedidos()[1])
                        #ventana['-ct$_ini-'].update(self.motor.lista_pedidos()[2])

                    except:
                        self.ventanaMensaje.ver("error al llevar")

                    ventana['-TABLA_INI-'].update(self.motor.lista_pedidos()[0])

                    self.motor.pedido(ventana,['producto','0,00','0,00','...','1','0,00','0,0000','0,00','0,00'])





            elif evento=='-CAMBIAR_DOLAR_INI-':
                pd=ventana['-dolar_ini-'].get()

                self.ventanaDolar.ver()
                ventana['-dolar_ini-'].update(self.motor.valor_dolar())






            elif evento=='-CANCELAR_INI-':
                try:
                    self.motor.ejecutar_sql("DELETE FROM pedidos")

                    ventana['-TABLA_INI-'].update(self.motor.lista_pedidos()[0])

                    self.motor.pedido(ventana,['producto','0,00','0,00','...','1','0,00','0,0000','0,00','0,00'])

                    ventana['-ctbs_ini-'].update("0,00")
                    ventana['-ct$_ini-'].update("0,0000")

                except:
                    self.ventanaMensaje.ver("error al cancelar")






            elif evento=='-ELIMINAR_INI-':
                try:
                    nombre=ventana['-TABLA_INI-'].get()[valores['-TABLA_INI-'][0]][0]

                    self.motor.ejecutar_sql("DELETE FROM pedidos WHERE n_p='{}'".format(nombre))

                    ventana['-TABLA_INI-'].update(self.motor.lista_pedidos()[0])

                except:
                    self.ventanaMensaje.ver("error al borrar")






            elif evento=='-GUARDAR_INI-':
                pass

            #////////////////////////////////////////////////////////////////////////////////////////////////////
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@----INVENTARIO----@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            #////////////////////////////////////////////////////////////////////////////////////////////////////

            elif evento in ('-BUSCAR_INV-','-busqueda_inv-enter'):
                lista_busqueda=[]
                nombre=ventana['-busqueda_inv-'].get()

                for producto in self.motor.lista_de_inventario():
                    if nombre in producto[0]:
                        lista_busqueda.append(producto)

                ventana['-TABLA_INV-'].update(values=lista_busqueda)






            elif evento=='-SELECCIONAR_INV-':
                if len(valores['-TABLA_INV-']):
                    producto=ventana['-TABLA_INV-'].get()[valores['-TABLA_INV-'][0]]

                    self.motor.editar_inventario(ventana,[producto[0],"","",producto[1],producto[2]])

                else:
                    self.ventanaMensaje.ver("seleccione un producto")






            elif evento=='-ELIMINAR_INV-':
                if len(valores['-TABLA_INV-']):
                    try:
                        nombre=ventana['-TABLA_INV-'].get()[valores['-TABLA_INV-'][0]][0]

                        self.motor.ejecutar_sql("DELETE FROM Inventario WHERE N_producto='{}'".format(nombre))
                        ventana['-TABLA_INV-'].update(values=self.motor.lista_de_inventario())

                        self.motor.editar_inventario(ventana,['producto','','','0','0'])

                        self.motor.pedido(ventana,['producto','0,00','0,00','...','1','0,00','0,00','0,00','0,00'])

                        self.motor.ejecutar_sql("DELETE FROM pedidos")

                        ventana['-TABLA_INI-'].update(self.motor.lista_pedidos()[0])

                    except:
                        self.ventanaMensaje.ver("error al eliminar")
                else:
                    self.ventanaMensaje.ver("seleccione un producto")





            elif evento=='-ACTUALIZAR_INV-':
                numero=valores['-actualizar_inv-']
                if len(numero):
                    numero=self.motor.punto(numero)
                    ventana['-cantidad_inv-'].update(value=self.motor.coma(float(numero),2))
                    ventana['-actualizar_inv-'].update("")







            elif evento=='-RECARGAR_INV-':
                numero_r=valores['-recargar_inv-']
                numero_c=valores['-cantidad_inv-']
                if len(numero_r):
                    numero_r=self.motor.punto(numero_r)
                    numero_c=self.motor.punto(numero_c)

                    if float(numero_r)<=float(numero_c):
                        ventana['-total_inv-'].update(value=self.motor.coma(float(numero_r),2))
                        ventana['-recargar_inv-'].update("")
                    else:
                        self.ventanaMensaje.ver("cantidad excedida")






            elif evento=='-APLICAR_INV-':
                nombre=ventana['-nombre_inv-'].get()

                cantidad=float(self.motor.punto(valores['-cantidad_inv-']))
                total=float(self.motor.punto(valores['-total_inv-']))

                if total<=cantidad:
                    try:
                        self.motor.ejecutar_sql("""UPDATE Inventario SET
                                                                Cantidad_producto = {},
                                                                            Total = {}
                                                                WHERE N_producto = '{}'""".format(cantidad,
                                                                                                  total,
                                                                                                  nombre))

                        self.motor.ejecutar_sql("DELETE FROM pedidos")

                        ventana['-TABLA_INI-'].update(self.motor.lista_pedidos()[0])

                        ventana['-TABLA_INV-'].update(values=self.motor.lista_de_inventario())

                    except:
                        self.ventanaMensaje.ver("error al aplicar")

                    self.motor.editar_inventario(ventana,['producto','','','0','0'])

                    self.motor.pedido(ventana,['producto','0,00','0,00','...','1','0,00','0,00','0,00','0,00'])

                else:
                    self.ventanaMensaje.ver("cantidad excedida")



            #////////////////////////////////////////////////////////////////////////////////////////////////////
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@----CONFIGURACION----@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            #////////////////////////////////////////////////////////////////////////////////////////////////////

            elif evento=='-REGISTRO_C-':
                if self.ventanaRegistro.ver():

                    ventana['-TABLA_C-'].update(values=self.motor.lista_de_productos())
                    ventana['-LISTA_INI-'].update(values=self.motor.lista_nombres_de_productos())

                    self.motor.editar_inventario(ventana,['producto','','','0','0'])

                    self.motor.pedido(ventana,['producto','0,00','0,00','...','1','0,00','0,00','0,00','0,00'])

                    self.motor.ejecutar_sql("DELETE FROM pedidos")
                    ventana['-TABLA_INI-'].update(self.motor.lista_pedidos()[0])

            elif evento=='-ELIMINAR_C-':
                if len(valores['-TABLA_C-']):
                    try:
                        nombre=ventana['-TABLA_C-'].get()[valores['-TABLA_C-'][0]][0]

                        self.motor.ejecutar_sql("DELETE FROM productos WHERE Nombre_producto='{}'".format(nombre))
                        ventana['-TABLA_C-'].update(values=self.motor.lista_de_productos())
                        ventana['-LISTA_INI-'].update(values=self.motor.lista_nombres_de_productos())
                        try:
                            self.motor.ejecutar_sql("DELETE FROM Inventario WHERE N_producto='{}'".format(nombre))
                            ventana['-TABLA_INV-'].update(values=self.motor.lista_de_inventario())
                        except:
                            pass

                        self.motor.editar_inventario(ventana,['producto','','','0','0'])

                        self.motor.pedido(ventana,['producto','0,00','0,00','...','1','0,00','0,00','0,00','0,00'])

                        self.motor.ejecutar_sql("DELETE FROM pedidos")

                        ventana['-TABLA_INI-'].update(self.motor.lista_pedidos()[0])

                    except:
                        self.ventanaMensaje.ver("error al eliminar")
                else:
                    self.ventanaMensaje.ver("seleccione un producto")






            elif evento=='-EDITAR_C-':
                if len(valores['-TABLA_C-']):

                    producto=ventana['-TABLA_C-'].get()[valores['-TABLA_C-'][0]]
                    self.ventanaEditar.ver(producto)
                    ventana['-TABLA_C-'].update(values=self.motor.lista_de_productos())
                    ventana['-LISTA_INI-'].update(values=self.motor.lista_nombres_de_productos())
                    ventana['-TABLA_INV-'].update(values=self.motor.lista_de_inventario())

                    self.motor.editar_inventario(ventana,['producto','','','0','0'])

                    self.motor.pedido(ventana,['producto','0,00','0,00','...','1','0,00','0,00','0,00','0,00'])

                    self.motor.ejecutar_sql("DELETE FROM pedidos")

                    ventana['-TABLA_INI-'].update(self.motor.lista_pedidos()[0])

                else:
                    self.ventanaMensaje.ver("seleccione un producto")






            elif evento in ('-BUSCAR_C-', '-busqueda_c-enter'):
                lista_busqueda=[]
                nombre=ventana['-busqueda_c-'].get()
                if nombre[:2]=="e:":
                    lista_busqueda=self.motor.lista_de_productos(ins="SELECT * FROM productos WHERE Etiqueta='{}'".format(nombre[2:]))

                else:
                    for producto in self.motor.lista_de_productos():
                        if nombre in producto[0]:
                            lista_busqueda.append(producto)

                ventana['-TABLA_C-'].update(values=lista_busqueda)






            elif evento=='-INVENTARIO_C-':
                if len(valores['-TABLA_C-']):
                    nombre=ventana['-TABLA_C-'].get()[valores['-TABLA_C-'][0]][0]
                    producto=(nombre,0,0)
                    try:
                        self.motor.ejecutar_sql("INSERT INTO Inventario values (?,?,?)",producto)
                        ventana['-TABLA_INV-'].update(values=self.motor.lista_de_inventario())
                    except:
                        self.ventanaMensaje.ver("error al agregar '{}' al inventario".format(nombre))

                    self.motor.editar_inventario(ventana,['producto','','','0','0'])

                    self.motor.pedido(ventana,['producto','0,00','0,00','...','1','0,00','0,00','0,00','0,00'])

                    self.motor.ejecutar_sql("DELETE FROM pedidos")

                    ventana['-TABLA_INI-'].update(self.motor.lista_pedidos()[0])

                else:
                    self.ventanaMensaje.ver("seleccione un producto")




            #////////////////////////////////////////////////////////////////////////////////////////////////////
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@----Ventas----@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            #////////////////////////////////////////////////////////////////////////////////////////////////////





            elif evento=='-BUSCAR_V-':
                self.ventanaBuscar.ver()


        ventana.close()


NegGui().ver()

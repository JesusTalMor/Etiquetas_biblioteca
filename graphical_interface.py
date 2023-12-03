# Editor: Jesus Talamantes Morales
# Fecha Trabajo: 29 de Noviembre 2023
# Implementacion Orientada a Objetos
#############################################################

#?#********** VARIABLES CONTROL DE VERSIONES **********#
ALPHA = 1
FUNCIONALIDAD = 11
BUGS = 4
VERSION = f'{ALPHA}.{FUNCIONALIDAD}.{BUGS}'

#?#********** IMPORTAR MODULOS **********#
import os
import sys
from datetime import datetime

import PySimpleGUI as sg

import pop_ups as pop
import string_helper as sh
from managers import Libro, ManejoTabla
from support_windows import VentanaModificar
from ticket_maker import DatabaseMaker

# * Tema principal de las ventanas
sg.LOOK_AND_FEEL_TABLE["TEC_Theme"] = {
  "BACKGROUND": "#3016F3",
  "TEXT": "#000000",
  "INPUT": "#DEE6F7",
  "TEXT_INPUT": "#000000",
  "SCROLL": "#DEE6F7",
  "BUTTON": ("#000000", "#FFFFFF"),
  "PROGRESS": ("#DEE6F7", "#DEE6F7"),
  "BORDER": 2,
  "SLIDER_DEPTH": 0,
  "PROGRESS_DEPTH": 0,
}
sg.theme("TEC_Theme")

#?#********** Función apoyo para relative path *********#
def resource_path(relative_path):
  """ Get absolute path to resource, works for dev and for PyInstaller """
  try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)




class VentanaGeneral:
  """ Ventana General para el Generador de Etiquetas """
  titulo_ventana = 'Generador de Etiquetas'
  ruta_archivo = ''
  ruta_folder = ''
  table_manager = ManejoTabla()

  #? LAYOUTS PARA LA VENTANA **********************************
  def clasification_layout(self):
    """ Layout para insertar clasificaciones 
    
    Atributos del libro
    -------------------
      PIPE_A: (str) PIPE A de la clasificacion
      PIPE_B: (str) PIPE B de la clasificacion
      VOL: (int) Volumen del Libro
      COP: (int) Copia del Libro
      CLAS: (str) Clasificacion del Libro
      HEAD: (str) Encabezado del Libro
    """
    #?#********* LAYOUT PARA MANEJO DE PIPE'S #?#*********
    text_format = {
      'font':("Open Sans", 12, "bold"),
      'size' : (6,1), 
      'background_color':"#FFFFFF", 
      'justification':"center",
      'pad' : 0,
    }
    in_format = {
      'size':(15, 1), 
      'font':("Open Sans", 10, "bold"), 
      'justification':"center", 
      'disabled':True,
      'pad' : 5,
    }
    pipe_a_layout = [
      [sg.Text(text="PIPE A", **text_format)],
      [sg.In(key="PIPE_A", **in_format)],
    ]
    pipe_b_layout = [
      [sg.Text(text="PIPE B", **text_format)],
      [sg.In(key="PIPE_B", **in_format)],
    ]
    colum_format = {
      'background_color':"#FFFFFF", 
      'element_justification':"c",
      'pad' : 0
    }
    PIPE_AB_LAYOUT = [[
      sg.Column(layout=pipe_a_layout, **colum_format),
      sg.VSeperator(),
      sg.Column(layout=pipe_b_layout, **colum_format),
    ]]
    
    #?#********* LAYOUT PARA MANEJO DE COPIA Y VOLUMEN #?#*********
    text_format = {
      'font':("Open Sans", 12, 'bold'), 
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    in_format = {
      'size':(2, 1), 
      'enable_events':True,
      'font':("Open Sans", 10, 'bold'), 
      'justification':"center",
      'pad' : 0, 
    }
    VOL_COP_LAYOUT = [
      sg.Text(text="Volumen", **text_format),
      sg.In(key="VOL", **in_format),
      sg.Text(text="Copia", **text_format),
      sg.In(default_text="1", key="COP", **in_format),
    ],
    
    #?#********* LAYOUT PARA MANEJO DE CLASIFICACION Y ENCABEZADO #?#*********
    title_format = {
      'font': ("Open Sans", 14, 'bold'),
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    text_format = {
      'font': ("Open Sans", 12, 'bold'),
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    in_format = {
      'enable_events':True,
      'font':("Open Sans", 12), 
      'justification':"center", 
    }
    frame_format = {
      'background_color':"#FFFFFF", 
      'element_justification':"c",
      'border_width':0
    }
    LAYOUT_GENERAL = [
      #* Titulo de esta seccion
      [sg.Text(text="Agregar Clasificación", **title_format)],
      [sg.In(size=(30, 1), key="CLAS", pad=(10,0), **in_format)], # , pad=(15, 5)
      #* Funcion para agregar un encabezado
      [sg.Text(text="Encabezado", **text_format)],
      [sg.In(size=(20, 1), key="HEAD", pad=0, **in_format)],
      [sg.Frame("",layout=VOL_COP_LAYOUT, **frame_format)],
      [sg.Frame("",layout=PIPE_AB_LAYOUT, **frame_format)],
    ]
    return LAYOUT_GENERAL

  def individual_layout(self):
    """ Layout columna izquierda del programa
    
    Llaves del Layout
    -----------------------------------------------
    PIPE_A:       (str) PIPE A de la clasificacion
    PIPE_B:       (str) PIPE B de la clasificacion
    VOL:          (int) Volumen del Libro
    COP:          (int) Copia del Libro
    CLAS:         (str) Clasificacion del Libro
    HEAD:         (str) Encabezado del Libro
    TITLE:        (str) Título del Libro (Opcional)
    CBARRAS:      (str) Código de Barras Libro (Opcional)
    FILE & ELEM:  (Ventana) Maneja el cambio de ventana en la aplicacion
    Agregar:      (Boton) Agrega una nueva clasificacion

    """
    CLASIF_LAYOUT = self.clasification_layout()
    #?#********* LAYOUT PARA SELECIONAR TIPO DE PROGRAMA #?#*********
    text_format = {
      'font':("Open Sans", 16, "bold"), 
      'background_color':"#FFFFFF",
      'justification':"c",
    }
    radio_format = {
      'background_color':"#FFFFFF",
      'circle_color':"#DEE6F7",
      'font':("Open Sans", 14),
      'enable_events':True,
    }
    SELECCIONAR_LAYOUT = [
      [sg.Text(text="Seleccione una opción:", **text_format)],
      [
        sg.Radio("Cargar Archivo", "O1", default=False, key="FILE", **radio_format),
        sg.Radio("Cargar Elemento", "O1", default=True, key="ELEM", **radio_format),
      ],    
    ]
    #?#********* LAYOUT PARA AGREGAR TITULO Y CBARRAS #?#*********
    text_format = {
      'font': ("Open Sans", 12, 'bold'),
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    in_format = {
      'font':("Open Sans", 10, 'bold'), 
      'justification':"center", 
    }
    INFO_LAYOUT = [
      [
        sg.Text(text="Título", **text_format),
        sg.In(size=(40, 1), key="TITLE", **in_format)
      ],
      [
        sg.Text(text="Código de Barras", pad=((0,20), 0), **text_format),
        sg.In(size=(20, 1), key="CBARRAS", **in_format)
      ],
    ]

    #?#********* LAYOUT GENERAL DE ESTA FUNCION #?#*********
    text_format = {
      'font':("Open Sans", 20, "bold", "italic"), 
      'background_color':"#FFFFFF", 
      'justification':"c", 
    }
    frame_format = {
      'background_color':"#FFFFFF", 
      'element_justification':"c",
    }
    GENERAL_LAYOUT = [
      #* Logo del Tec de Monterrey
      [sg.Image(filename=resource_path("Assets/LogoTecResize.png"), background_color="#FFFFFF")],
      #* Titulo de la aplicacion
      [sg.Text(text=self.titulo_ventana, **text_format)],
      #* Cambiar entre ventanas
      [sg.Frame("",layout=SELECCIONAR_LAYOUT, border_width=0, **frame_format)],
      [sg.HSep(pad=(0, 5))], # Separadores
      #* Layout para agregar etiquetas individuales
      [sg.Frame("",layout=CLASIF_LAYOUT, **frame_format)],
      [sg.HSep(pad=(0, 5))], # Separadores
      [sg.Frame("",layout=INFO_LAYOUT, border_width=0, **frame_format)],
      [sg.HSep(pad=(0, 5))], # Separadores
      [sg.Button("Agregar", font=("Open Sans", 12, 'bold'))],

      #* Layout invisible para guardar en la carpeta
      [
        sg.Input(key="FOLDER", visible=False),
        sg.FolderBrowse("Guardar", target='FOLDER', visible=False),
      ],
    ]
    return GENERAL_LAYOUT
  
  def file_layout(self):
    """ Layout columna izquierda del programa
    
    LLaves que Maneja
    -----------------
    FILE & ELEM: (Ventana) Maneja el cambio de ventana en la aplicacion
    Agregar: (Boton) Agrega una nueva clasificacion
    
    Llaves que Hereda
    -----------------

    """
    #?#********* LAYOUT PARA SELECIONAR TIPO DE PROGRAMA #?#*********
    text_format = {
      'font':("Open Sans", 16, "bold"), 
      'background_color':"#FFFFFF",
      'justification':"c",
    }
    radio_format = {
      'background_color':"#FFFFFF",
      'circle_color':"#DEE6F7",
      'font':("Open Sans", 14),
      'enable_events':True,
    }
    SELECCIONAR_LAYOUT = [
      [sg.Text(text="Seleccione una opción:", **text_format)],
      [
        sg.Radio("Cargar Archivo", "O1", default=True, key="FILE", **radio_format),
        sg.Radio("Cargar Elemento", "O1", default=False, key="ELEM", **radio_format),
      ],    
    ]
    #?#********* LAYOUT PARA SELECCIONAR eL ARCHIVO DE EXCEL #?#*********
    text_format = {
      'font':("Open Sans", 14, "italic"), 
      'background_color':"#FFFFFF",
      'justification':"c",
    }
    ruta_excel = "Sin Archivo" if self.ruta_archivo == "" else self.ruta_archivo.split("/")[-1]    
    SELECCIONAR_ARCHIVO = [
      [
        sg.Button(
          image_source=resource_path('Assets/subir_icon.png'), 
          image_subsample=5, border_width=0, key='UPLOAD'
        )
      ],
      [sg.Text(text=ruta_excel, key="EXCEL_TEXT", **text_format)],
    ]
    #?#********* LAYOUT GENERAL DE ESTA FUNCION #?#*********
    text_format = {
      'font':("Open Sans", 20, "bold", "italic"), 
      'background_color':"#FFFFFF", 
      'justification':"c", 
    }
    frame_format = {
      'background_color':"#FFFFFF", 
      'element_justification':"c",
    }
    GENERAL_LAYOUT = [
      #* Logo del Tec de Monterrey
      [sg.Image(filename=resource_path("Assets/LogoTecResize.png"), background_color="#FFFFFF")],
      #* Titulo de la aplicacion
      [sg.Text(text=self.titulo_ventana, **text_format)],
      #* Seleccion de ventana
      [sg.Frame("",layout=SELECCIONAR_LAYOUT, border_width=0, **frame_format)],
      [sg.HSep(pad=(0, 10))], # Separador 
      #* Seleccion de Archivo
      [sg.Frame("",layout=SELECCIONAR_ARCHIVO, border_width=0, **frame_format)],
      [sg.HSep(pad=(0, (10,30)))], # Separador
      [sg.Button("Cargar", font=("Open Sans", 14, 'bold'))],
      #* Layout Invisible para guardar el archivo
      [
        sg.Input(key="FOLDER", visible=False),
        sg.FolderBrowse("Guardar", target='FOLDER', visible=False),
      ],
      
      #* Layout Invisible para escoger archivo de excel
      [
        sg.In(key="EXCEL_FILE", visible=False),
        sg.FileBrowse("Abrir", target='EXCEL_FILE',visible=False, file_types=(("Excel Files", "*.xlsx"),)),
      ],
    ]
    return GENERAL_LAYOUT  
  
  def table_layout(self):
    """ Layout columna izquierda del programa
    
    LLaves que Maneja
    -----------------
    TABLE : (Tabla) Manejo general de la tabla
    Modificar : (Tabla/ Click Derecho) Modificar una etiqueta de la tabla
    SELECT-ALL : (Boton) Seleccionar todas las etiquetas
    LIMPIAR : (Boton) Reiniciar todo el programa
    DESELECT-ALL : (Boton) Para deseleccionar todas las etiquetas
    EXPORTAR : (Boton) Lanzar la siguiente parte del programa
    
    """
    #?#********** DEFINIR VARIABLES UTILIZADAS #?#**********
    # * Configuración de la tabla
    colum = ["Clasificación", "PIPE_A", "PIPE_B", "STATUS"]
    col_width = [25, 15, 15, 10]
    tabla_principal = self.table_manager.tabla_principal
    row_color_array = self.table_manager.formato_tabla
    boton_font = {'font':("Open Sans", 12),}
    LAYOUT = [
      [sg.Text(text="Lista de Etiquetas", background_color="#FFFFFF",font=("Open", 18, "bold", "italic"),)],
      [
        sg.Table(
          values=tabla_principal,
          headings=colum,
          font=("Open Sans", 9),
          col_widths=col_width,
          row_height=25,
          num_rows=16,
          auto_size_columns=False,
          display_row_numbers=True,
          justification="l",
          expand_y=False,
          enable_events=True,
          right_click_menu=["Etiqueta", ["Modificar", "Eliminar"]],
          alternating_row_color="#FFFFFF",
          background_color="#FFFFFF",
          header_border_width=2,
          row_colors=row_color_array,
          key="TABLE",
        )
      ],
      [
        sg.Button("Seleccionar Todo",  pad=(0, 10), key="SELECT-ALL", **boton_font),
        sg.Button("Limpiar", pad=(30, 10), key='LIMPIAR', **boton_font),
        sg.Button("Deseleccionar", pad=(0, 10), key="DESELECT-ALL", **boton_font),
      ],
      [sg.Button("Exportar", font=("Open Sans", 12, "bold"), key='EXPORTAR')],
    ]
    return LAYOUT

  def create_layout(self, formato = "FILE"):
    """ Crea el layout principal para esta ventana """
    colum_format = {
      'background_color':"#FFFFFF", 
      'element_justification':"c", 
      'pad':0
    }
    COL_IZQ_LAYOUT = self.file_layout() if formato == "FILE" else self.individual_layout()
    COL_DER_LAYOUT = self.table_layout()
    LAYOUT = [
      [
        sg.Column(COL_IZQ_LAYOUT, **colum_format),
        sg.VSep(pad=(5, 0)),
        sg.Column(COL_DER_LAYOUT, **colum_format),
      ],
    ]
    return LAYOUT

  def create_window(self, formato = "FILE"):
    """ Genera un Objeto tipo Ventana de PySimpleGUI """
    LAYOUT = self.create_layout(formato)
    # ? Menu superior de opciones
    MENU_OPCIONES = [
      ['Programa', ['Guardar', 'Salir']],
      ["Ayuda", ["Tutoriales", "Licencia", "Acerca de..."]],
    ]
    MAIN_LAYOUT = [
      #* Menu superior de la APP
      [sg.Menu(MENU_OPCIONES, tearoff=False)],
      [sg.Frame("",layout=LAYOUT, background_color='#FFFFFF', element_justification='c')],
    ]
    
    window = sg.Window(
      title= self.titulo_ventana, 
      layout= MAIN_LAYOUT, 
      element_justification="c", 
      icon=resource_path("Assets/ticket_icon.ico"),
      enable_close_attempted_event=True,
    )  
    return window


  #? FUNCIONAMIENTO PRINCIPAL DE LA VENTANA ***********************
  def run_window(self, window):
    #? MANEJO DE VARIABLES
    bandera_agregar = False
    bandera_modificar = False
    estatus_modificar = 'XXXXXX'
    index_modificar = 0
    
    #? LOOP PRINCIPAL
    while True:
      event, values = window.read()
      self.show_window_events(event, values)
      #? ******** FUNCIONALIDAD BASICA VENTANA  ***************
      #* Cerrar la aplicación
      if event in ('Salir', '-WINDOW CLOSE ATTEMPTED-'):
        #* Ver si quiere guardar el archivo
        if pop.save_file() is True:
          self.guardar_programa(window)
        window.close()
        return "TRUE"
      #* Cambio de Ventana a ARCHIVO
      elif event == "FILE":
        window.close()
        return "FILE"
      #* Cambio de Ventana a INDIVIDUAL
      elif event == "ELEM":
        window.close()
        return "ELEM"
      #* Mostrar licencia del Programa
      elif event == "Licencia":
        pop.info_license()
      #* Mostrar version del Programa
      elif event == "Acerca de...":
        pop.info_about(VERSION)
      #* Guardar progreso del programa
      elif event == 'Guardar':
        self.guardar_programa(window)
      
      #? ********** FUNCIONALIDAD ARCHIVO *******************
      elif event == "UPLOAD":
        window["Abrir"].click() # Activar funcionalidad para abrir archivo
        self.ruta_archivo = window['EXCEL_FILE'].get() # Actualizar ruta del archivo
        # Actualizar nombre del archivo de la ventana
        nombre_archivo = self.ruta_archivo.split('/')[-1] if len(self.ruta_archivo) != 0 else 'Sin Archivo'
        window["EXCEL_TEXT"].update(nombre_archivo)
      elif event == "Cargar":
        self.cargar_excel()
      

      #? ********** FUNCIONALIDAD CLASIFICACION ****************
      elif event in ("CLAS", 'VOL', 'COP', 'HEAD'):
        bandera_agregar = self.checar_clasificacion(window)
      elif event == "Agregar" and bandera_agregar:
        self.agregar_clasificacion(window)
        bandera_agregar = False
      
      #?#********** FUNCIONALIDAD DE TABLA **********#?#
      elif event == "LIMPIAR":
        self.reset_window()
        bandera_agregar = False
        bandera_modificar = False
      elif event == "SELECT-ALL":
        bandera_modificar = False
        self.select_all_table()
      elif event == "DESELECT-ALL":
        bandera_modificar = False
        self.deselect_all_table()
      elif event == "TABLE":
        modify_object = (index_modificar, bandera_modificar, estatus_modificar)
        index_modificar, bandera_modificar, estatus_modificar = self.table_management(values, modify_object)
      elif event == "Modificar" and bandera_modificar is True:
        bandera_modificar = self.modificar_elemento(index_modificar)
      elif event == "Eliminar" and bandera_modificar is True:
        self.eliminar_elemento(index_modificar)
        bandera_modificar = False
      elif event == 'EXPORTAR':
        self.exportar_etiquetas(window)
      
      #? ACTUALIZAR TABLA VISUAL *******************************
      window["TABLE"].update(
        values=self.table_manager.tabla_principal, 
        row_colors=self.table_manager.formato_tabla
      )

  #? FUNCIONALIDAD GENERAL *********************************
  def show_window_events(self, event, values):
    print(f"""
      Imprimiendo Eventos de Suceden
      {'-'*50}
      Eventos que suceden {event}
      Valores guardados {values}
      {'-'*50}
    """)


  #? FUNCIONALIDAD AGREGAR CLASIFICACION *******************
  def checar_clasificacion(self, window):
    clasificacion = window['CLAS'].get()
    # * Revisar si es relevante el cambio
    if len(clasificacion) < 5: return False
    
    #* Se revisa si se puede separa la PIPE B
    if clasificacion.find(' ') < 3:
      window["PIPE_A"].update(value="XXXXXX", text_color='#F04150')
      window["PIPE_B"].update(value="XXXXXX", text_color='#F04150')
      # ? Bandera Falsa no se puede agregar
      return False
    
    if sh.revisar_corte_pipe(clasificacion) and sh.revisar_pipeB(clasificacion):
      posicion_corte, diferencia = sh.buscar_pipe(clasificacion)
      if posicion_corte != 0:
        pipe_a_str = clasificacion[:posicion_corte].replace(' ','.')
        pipe_b_str = '.' + clasificacion[posicion_corte + diferencia :]
        window["PIPE_A"].update(value=pipe_a_str, text_color='#1AB01F')  
        window["PIPE_B"].update(value=pipe_b_str, text_color='#1AB01F')
        # ? Bandera Verdadera se puede agregar
        return True
    else:
      window["PIPE_A"].update(value="XXXXXX", text_color='#F04150')
      window["PIPE_B"].update(value="XXXXXX", text_color='#F04150')
      # ? Bandera Falsa no se puede agregar
      return False
  
  def agregar_clasificacion(self, window):
    #* Tomar datos de la aplicacion
    clasificacion = window['CLAS'].get()
    volumen = window['VOL'].get()
    copia = window['COP'].get()
    encabezado = window['HEAD'].get()
    titulo = window['TITLE'].get()
    cbarras = window['CBARRAS'].get()

    #* Crear Objeto de Tipo Libro
    newLibro = Libro(
      aTitulo= titulo if len(titulo) != 0 else 'Sin Título',
      aCbarras= cbarras,
      aClasif= clasificacion,
      aCopia= copia,
      aEncabezado= encabezado,
      aVolumen= volumen
    )

    #* Se agrega dicho elemento a las listas de datos
    self.table_manager.agregar_elemento(newLibro)
    
    #* Ordenar nuevo libro agregado
    indices_ordenados = self.table_manager.ordenar_libros()
    self.table_manager.ordenar_tabla(indices_ordenados)

    #* Limpiar datos de agregar clasificacion
    window["CLAS"].update('')
    window["VOL"].update('')
    window["COP"].update('1')
    window["HEAD"].update('')
    window['TITLE'].update('')
    window['CBARRAS'].update('')
    window["PIPE_A"].update('')  
    window["PIPE_B"].update('')

  #? FUNCIONALIDAD MANEJO DE TABLA *************************
  def reset_window(self):
    """ Reiniciar todos los valores de la tabla que se trabaja """
    self.table_manager.reset_tabla()

  def select_all_table(self):
    #* Selecciona toda la tabla
    self.table_manager.seleccionar_tabla()
  
  def deselect_all_table(self):
    #* Selecciona toda la tabla
    self.table_manager.deseleccionar_tabla()

  def table_management(self, values, modify_object):
    modify_index, modify_flag, modify_status = modify_object
    # print(modify_index, modify_flag, modify_status)
    #* Manejar excepcion con respecto a datos inexistentes
    if len(values["TABLE"]) == 0: return modify_index, modify_flag, modify_status
    
    index_value = int(values["TABLE"][0])  # * elemento a seleccionar
    print('[INFO] Libro seleccionado:', index_value)
    estatus = self.table_manager.lista_libros[index_value].estatus
    print('[INFO] Estatus libro seleccionado', estatus)

    # * Seleccionar una casilla valida
    if estatus == "Valid":
      # Cambias el estatus de ese elemento a seleccionado
      self.table_manager.actualizar_estatus_elemento(index_value, "Selected")

    # * Seleccionar casilla para modificar
    elif estatus in ("Selected", "Error") and modify_flag is False:
      #* Actualizar datos de modificacion
      modify_status = estatus
      modify_flag = True
      modify_index = index_value
      #* Modificar elemento visualmente
      self.table_manager.actualizar_estatus_elemento(index_value, "Modify")

    # * Quitar casilla de modificar
    elif estatus == "Modify":
      #? Cambiar elemento modificado/seleccionado a Normal
      if modify_status == "Selected":
        self.table_manager.actualizar_estatus_elemento(index_value, "Valid")
      #? Cambiar elemento modificado/error a Error
      elif modify_status == "Error":
        self.table_manager.actualizar_estatus_elemento(index_value, "Error")
      modify_flag = False

    # * Regresar casilla a normalidad
    elif estatus == "Selected" and modify_flag is True:
      self.table_manager.actualizar_estatus_elemento(index_value, "Valid")
    
    return modify_index, modify_flag, modify_status

  def modificar_elemento(self, modify_index):
    #* Sacar los datos de esa etiqueta
    libro_a_modificar = self.table_manager.lista_libros[modify_index]
    clasif_libro_a_modificar = libro_a_modificar.etiqueta.clasif_completa
    #* Mandar llamar ventana modificar
    VM = VentanaModificar(libro_a_modificar)
    estatus, libro_modificado = VM.run_window()
    del VM

    #* Checar si hubieron cambios
    if estatus is False: return True
    
    # * Agregamos elemento a una tabla de modificaciones
    self.table_manager.agregar_elemento_modificado(modify_index, libro_modificado, clasif_libro_a_modificar)

    # * Actualizar valores de tabla de datos
    self.table_manager.actualizar_elemento(modify_index, libro_modificado)

    # * Cambiamos la apariencia del elemento en la tabla
    self.table_manager.actualizar_estatus_elemento(modify_index, 'Valid')
    
    #* Ordenar libro modificado
    indices_ordenados = self.table_manager.ordenar_libros()
    self.table_manager.ordenar_tabla(indices_ordenados)
    
    return False

  def eliminar_elemento(self, modify_index):
    self.table_manager.eliminar_elemento(modify_index)

  #? FUNCIONALIDAD DEL PROGRAMA ***************************
  def exportar_etiquetas(self, window):
    #* Ordenar libro modificado
    indices_ordenados = self.table_manager.ordenar_libros()
    self.table_manager.ordenar_tabla(indices_ordenados)
    
    etiquetas_a_imprimir = self.table_manager.exportar_libros_selecionados()
    # * Revisar que la tabla de seleccionado tenga valores para poder continuar
    if len(etiquetas_a_imprimir) == 0: 
      pop.warning_select()
      return False

    # * Pedir Folder para guardar
    window['Guardar'].click()
    ruta = window['FOLDER'].get()
    if len(ruta) == 0: return False
    today_date = datetime.now().strftime("%d_%m_%Y_%H%M%S") # Chequeo de hora de consulta

    #* Generar base de datos
    DBM = DatabaseMaker()
    DBM.crear_database(etiquetas_a_imprimir, today_date, ruta)  
    DBM.crear_instrucciones_pegado(etiquetas_a_imprimir, today_date, ruta)  

    #* Generar reporte de datos modificados
    self.table_manager.crear_reporte_modificados(ruta, today_date)
    self.table_manager.crear_reporte_QRO(ruta, today_date)
    pop.success_program()
    return True

  def cargar_excel(self):
    # Revisar que tengamos un archivo excel
    if len(self.ruta_archivo) == 0:
      pop.warning_excel_file()
      return False

    # Crear tabla de datos    
    self.table_manager.crear_tabla(self.ruta_archivo)

    #* Ordenar libro modificado
    indices_ordenados = self.table_manager.ordenar_libros()
    self.table_manager.ordenar_tabla(indices_ordenados)

  def guardar_programa(self, window):
    #* Revisar archivo de Excel
    if len(self.ruta_archivo) == 0:
      # * Pedir Folder para guardar
      window['Guardar'].click()
      ruta_archivo = window['FOLDER'].get()
      if len(ruta_archivo) == 0: return False
      today_date = datetime.now().strftime("%d_%m_%Y_%H%M%S") # Chequeo de hora de consulta
      nombre_archivo = f'{today_date}_guardado'
    else:
      nombre_archivo = self.ruta_archivo.split('/')[-1]
      nombre_archivo = nombre_archivo[:nombre_archivo.find('.xlsx')]
      ruta_archivo = self.ruta_archivo[:self.ruta_archivo.find(nombre_archivo)-1]
      nombre_archivo += '_guardado'
    #* Crear y actualizar el dataframe del excel
    guardar_df = self.table_manager.exportar_a_df()
    self.table_manager.escribir_excel(ruta_archivo, nombre_archivo, guardar_df)

def main():
  """ Funcion principal para el manejo de la aplicacion """
  VG = VentanaGeneral()
  formato = "FILE"
  VG_window = VG.create_window(formato)
  while formato in ("FILE", "ELEM"):
    formato = VG.run_window(VG_window)
    VG_window = VG.create_window(formato)

if __name__ == '__main__':
  main()
  pop.check_pdf()

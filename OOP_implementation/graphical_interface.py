#############################################################
# Editor: Jesus Talamantes Morales
# Fecha Trabajo: 21 de Mayo 2023
# Versión: 0.4.3
# Implementacion utilizando OOP
#
#
#
#


#?#********** VARIABLES CONTROL DE VERSIONES **********#
ALPHA = 0
FUNCIONALIDAD = 4
BUGS = 3
VERSION = f'{ALPHA}.{FUNCIONALIDAD}.{BUGS}'

#?#********** IMPORTAR MODULOS **********#
import os
import sys

# import numpy as np
import PySimpleGUI as sg

# import main_ticket_functions as maintf
import pop_ups as pop
import string_helper as sh
from string_helper import creador_clasificacion

# from datetime import datetime


# import support_windows as sw
# import ticket_maker as tm

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

# * Configuración de la tabla
colum = ["Clasificación", "PIPE_A", "PIPE_B", "STATUS"]
col_width = [25, 15, 15, 10]
col_just = ["c", "l", "l", "c"]

# ? Menu superior de opciones
menu_opciones = [
  ["Programa", ["Configuración", "Limpiar", "Salir"]],
  ["Ayuda", ["Tutoriales", "Licencia", "Acerca de..."]],
]

#?#********** Función apoyo para relative path *********#
def resource_path(relative_path):
  """ Get absolute path to resource, works for dev and for PyInstaller """
  try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

# # ? Variables Globales para mejor manejo del programa
# # ! Variables Globales no modificar
# # Variables para guardar rutas de archivos
# ruta_archivo = ""
# ruta_folder = ""

# # Manejo de datos de los libros para modificaciones
# tabla_modify = []

# # Configuracion para impresion
# valores_config = {}
# coordenadas = (None,None)
class VentanaModificar:
  """ Ventana inicial del programa.
  
  Ventana para manejo inicial de programa.
  Archivos, Nombres etc.

  Atributos
  ---------

  Metodos
  -------
  """
  '''
    Modifica el contenido y parametros de una etiqueta

    Parametros:
      clasificacion_completa: Clasificación completa del libro a modificar
      Dicc_info:
        titulo: Titulo del libro a modificar
        cbarras: Codigo de Barras del Libro a modificar
        clasif: Clasificación Basica
        volumen: Volumen expresado en V.(Num)
        copia: Copia expresado en Num.
        encabeza: Encabezado anterior a Clasificación
    
        Retorna:
          2 Listas con datos, en caso de finalizar correctamente.
          Caso contrario regresa 2 listas de la siguiente manera [False],[False]
  '''
  titulo_ventana = 'Modificar Etiqueta'
  def __init__(self, clas_completa:str, dicc_info:dict) -> None:
    self.clasif_completa = clas_completa
    self.clasif = dicc_info['clasif']
    self.volumen = dicc_info['volumen']
    self.copia = dicc_info['copia']
    self.encabezado = dicc_info['encabeza']
    self.titulo = dicc_info['titulo']
    self.volumen = self.volumen[self.volumen.index('V.' + 2):] if 'V.' in self.volumen else '0'
  
  def create_layout(self):
    """ Crea el layout General de Esta Ventana 
    Llaves que Maneja
    -----------------
      INFO: (boton) Muestra el titulo del Libro
      TEXT: (str) Texto de clasificacion completa
      Cancelar: (boton) Cierra la ventana
      Modificar: (boton) Cierra la ventana y mandar los datos modificados


    Llaves que Hereda
    -----------------
      PIPE_A: (str) PIPE A de la clasificacion
      PIPE_B: (str) PIPE B de la clasificacion
      VOL: (int) Volumen del Libro
      COP: (int) Copia del Libro
      CLAS: (str) Clasificacion del Libro
      HEAD: (str) Encabezado del Libro
    """
    INDIV_LAYOUT = self.create_clasification_layout()
    text_format = {'background_color':"#FFFFFF", 'justification':"c",}
    frame_format = {'background_color':"#FFFFFF", 'element_justification':"c",}
    GENERAL_LAYOUT = [
      #* Titulo de la aplicacion y Boton de Mas Info
      [
        sg.Text(
          text=self.titulo_ventana, font=("Open Sans", 18, "bold", "italic"), 
          pad=(0, (0, 10)), ** text_format,
        ),
        sg.Button(
          image_source='Assets/info_icon.png', image_subsample=10, 
          border_width=0, key='INFO', pad=(5,(0,10))
        )
      ],
      [
        sg.Text(
          text=self.clasif_completa, key="TEXT",
          font=("Open Sans", 16, "bold"), **text_format
        )
      ],
      [sg.HorizontalSeparator(pad=(0, (10, 6)))],
      [sg.Frame("", layout=INDIV_LAYOUT, **frame_format)],
      [sg.HorizontalSeparator(pad=(0, (6, 10)))],
      [
        sg.Button("Cancelar", font=("Open Sans", 12, "bold")),
        sg.Button("Modificar", font=("Open Sans", 12, "bold"),),
      ],    
    ]
    return GENERAL_LAYOUT

  def create_clasification_layout(self):
    """ Layout para insertar clasificaciones 
    
    Llaves que Maneja
    -----------------
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
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    in_format = {
      'size':(14, 1), 
      'font':("Open Sans", 10), 
      'justification':"center", 
      'disabled':True,
    }
    pipe_a_layout = [
      [sg.Text(text="PIPE A", pad=5, **text_format)],
      [sg.In(default_text='', key="PIPE_A", ** in_format)],
    ]
    pipe_b_layout = [
      [sg.Text(text="PIPE B", pad=5, **text_format)],
      [sg.In(default_text='', key="PIPE_B", ** in_format)],
    ]
    colum_format = {'background_color':"#FFFFFF", 'element_justification':"c"}
    PIPE_AB_LAYOUT = [[
      sg.Column(layout=pipe_a_layout, **colum_format),
      sg.VSeperator(),
      sg.Column(layout=pipe_b_layout, **colum_format),
    ]]
    
    #?#********* LAYOUT PARA MANEJO DE COPIA Y VOLUMEN #?#*********
    text_format = {
      'font':("Open Sans", 12,), 
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    in_format = {
      'size':(2, 1), 
      'enable_events':True,
      'font':("Open Sans", 10), 
      'justification':"center", 
    }
    VOL_COP_LAYOUT = [
      sg.Text(text="Volumen", **text_format),
      sg.In(default_text=self.volumen, key="VOL", **in_format),
      sg.Text(text="Copia", **text_format),
      sg.In(default_text=self.copia, key="COP", **in_format),
    ],
    
    #?#********* LAYOUT PARA MANEJO DE CLASIFICACION Y ENCABEZADO #?#*********
    text_format = {
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
      [sg.Text(text="Clasificación", font=("Open Sans", 14, "bold"), **text_format)],
      [sg.In(default_text=self.clasif, size=(28, 1), key="CLAS", pad=(15, 5), **in_format)],
      #* Funcion para agregar un encabezado
      [sg.Text(text="Agregar Encabezado", font=("Open Sans", 12), **text_format)],
      [sg.In(default_text=self.encabezado, size=(18, 1), key="HEAD", **in_format)],
      [sg.Frame("",layout=VOL_COP_LAYOUT, **frame_format)],
      [sg.Frame("",layout=PIPE_AB_LAYOUT, **frame_format)],
    ]
    return LAYOUT_GENERAL

  def create_window(self):
    LAYOUT = self.create_layout()
    MAIN_LAYOUT = [[sg.Frame('', LAYOUT, background_color='#FFFFFF', element_justification='c')]]
    window = sg.Window(self.titulo_ventana, MAIN_LAYOUT, element_justification='c', icon=resource_path('Assets/book_icon.ico'))
    return window

  def run_window(self):
    bandera_agregar = False
    clasif_completa = ''
    window = self.create_window()

    while True:
      event, values = window.read()
      self.show_window_events(event, values)
      #* Actualizar boton de modificar
      if bandera_agregar is True: window['Modificar'].update(disabled=False)
      else: window['Modificar'].update(disabled=True)
      
      #* Cerrar programa sin resultados
      if event in (sg.WINDOW_CLOSED, "Exit", "Cancelar"):
        window.close() 
        return False,False
      
      #* Actualizar elemento de Clasificacion Completa
      clasif_completa = self.actualizar_clasif(values)
      window['TEXT'].update(clasif_completa)

      if event in ("CLAS", 'VOL', 'COP', 'HEAD'):
        bandera_agregar = self.checar_clasificacion(window, values)
      elif event == 'Modificar':
        #* Tomar datos para modificar
        tabla_principal = [
          clasif_completa,
          values['PIPE_A'],
          values['PIPE_B'],
          'Modified',
        ]
        tabla_datos = [
          values['CLAS'],
          values['VOL'],
          values['COP'],
          values['HEAD'],
        ]
        window.close()
        return tabla_principal, tabla_datos
      elif event == 'INFO': pop.show_info_libro(self.titulo)

  
  def show_window_events(self, event, values):
    print('-'*50)
    print(f'Eventos que suceden {event}')
    print(f'Valores guardaros {values}')
    print('-'*50 + '\n')

  def actualizar_clasif(self, values):
    """ Construye una clasificacion en tiempo real 
    """
    #* Tomar datos
    try:
      clasif = str(values["CLAS"])
      volumen = str(values['VOL'])
      copia = str(values['COP'])
      encabezado = str(values['HEAD'])
      clasificacion_completa = creador_clasificacion(clasif, encabezado, volumen, copia)
      return clasificacion_completa
    except TypeError:
      return ''

  def checar_clasificacion(self, window, values):
    clasificacion = str(values["CLAS"])
    # * Revisar si es relevante el cambio
    if len(clasificacion) < 5: return False
    
    #* Se revisa si se puede separa la PIPE B
    if sh.revisar_corte_pipe(clasificacion) and sh.revisar_pipeB(clasificacion):
      posicion_corte, diferencia = sh.buscar_pipe(clasificacion)
      if posicion_corte != 0:
        pipe_a_str = clasificacion[:posicion_corte]
        pipe_b_str = clasificacion[posicion_corte + diferencia :]
        window["PIPE_A"].update(pipe_a_str)  
        window["PIPE_B"].update(pipe_b_str)
        # ? Bandera Verdadera se puede agregar
        return True
    else:
      window["PIPE_A"].update("NO")
      window["PIPE_B"].update("APLICA")
      # ? Bandera Falsa no se puede agregar
      return False

class TableManager:
  """ Clase creada para el manejo de los datos de la tabla 
  """
  tabla_principal = []
  tabla_datos = []
  tabla_formato = []
  diccionario_estatus = {}
  diccionario_modificados = {}
  def agregar_elemento(self, principal:list, datos:dict, estatus:str, color="#FFFFFF"):
    """ Agregar un elemento a la tabla general """
    largo_tabla = self.get_len()
    formato = (largo_tabla, color)
    self.tabla_principal.append(principal)
    self.tabla_datos.append(datos)
    self.tabla_formato.append(formato)
    self.diccionario_estatus[largo_tabla] = estatus
  
  def agregar_modificado(self, index:int, new_clasif:str):
    """ Agregar un elemento a un diccionario de modificaciones
    o en su defecto lo actualiza.
    """
    titulo = self.tabla_datos[index]['titulo']
    cbarras = self.tabla_datos[index]['cbarras']
    clasificacion = self.tabla_principal[index][0]
    aux_modify = [titulo, cbarras, clasificacion, new_clasif]
    self.diccionario_modificados[index] = aux_modify

  def actualizar_elemento(self, index:int, estatus:str, color="#FFFFFF"):
    """ Actualizar el color y el status del elemento seleccionado """
    if index > self.get_len(): return False
    self.diccionario_estatus[index] = estatus
    self.tabla_principal[index][3] = estatus
    self.tabla_formato[index] = (int(index), color)
    return True

  def reset_table(self):
    self.tabla_principal = []
    self.tabla_datos = []
    self.tabla_formato = []
    self.diccionario_estatus = {}
  
  def get_len(self):
    return len(self.tabla_principal)
  def get_status_element(self, index):
    return self.diccionario_estatus[index] if index in self.diccionario_estatus else ''
  def get_data_element(self, index):
    return self.tabla_datos[index] if index < self.get_len() else {}
  
  def set_data_element(self, index, data):
    self.tabla_datos[index] = data
  def set_element(self, index, data):
    self.tabla_principal[index] = data

class VentanaInicial:
  """ Ventana inicial del programa.
  
  Ventana para manejo inicial de programa.
  Archivos, Nombres etc.

  Atributos
  ---------

  Metodos
  -------
  """
  def create_layout(self):
    pass

# * Ventana para agregar individualmente eitquetas
class VentanaElementos:
  """ Ventana para cargar elementos (Clasificaciones) individualmente, para su impresion

  ...

  Atributos
  ---------
  En proceso.
  
  Metodos
  -------
  No Hay.
  """
  titulo_ventana = 'Generador de Etiquetas'
  def __init__(self, excel_file='', ruta_folder='', table_manager=TableManager()) -> None:
    self.ruta_archivo = excel_file
    self.ruta_folder = ruta_folder
    self.table_manager = table_manager

  def create_clasification_layout(self):
    """ Layout para insertar clasificaciones 
    
    Llaves que Maneja
    -----------------
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
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    in_format = {
      'size':(14, 1), 
      'font':("Open Sans", 10), 
      'justification':"center", 
      'disabled':True,
    }
    pipe_a_layout = [
      [sg.Text(text="PIPE A", pad=5, **text_format)],
      [sg.In(key="PIPE_A", ** in_format)],
    ]
    pipe_b_layout = [
      [sg.Text(text="PIPE B", pad=5, **text_format)],
      [sg.In(key="PIPE_B", ** in_format)],
    ]
    colum_format = {'background_color':"#FFFFFF", 'element_justification':"c"}
    PIPE_AB_LAYOUT = [[
      sg.Column(layout=pipe_a_layout, **colum_format),
      sg.VSeperator(),
      sg.Column(layout=pipe_b_layout, **colum_format),
    ]]
    
    #?#********* LAYOUT PARA MANEJO DE COPIA Y VOLUMEN #?#*********
    text_format = {
      'font':("Open Sans", 12,), 
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    in_format = {
      'size':(2, 1), 
      'enable_events':True,
      'font':("Open Sans", 10), 
      'justification':"center", 
    }
    VOL_COP_LAYOUT = [
      sg.Text(text="Volumen", **text_format),
      sg.In(key="VOL", **in_format),
      sg.Text(text="Copia", **text_format),
      sg.In(default_text="1", key="COP", **in_format),
    ],
    
    #?#********* LAYOUT PARA MANEJO DE CLASIFICACION Y ENCABEZADO #?#*********
    text_format = {
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
      [sg.Text(text="Agregar Clasificación", font=("Open Sans", 14, "bold"), **text_format)],
      [sg.In(size=(28, 1), key="CLAS", pad=(15, 5), **in_format)],
      #* Funcion para agregar un encabezado
      [sg.Text(text="Agregar Encabezado", font=("Open Sans", 12), **text_format)],
      [sg.In(size=(18, 1), key="HEAD", **in_format)],
      [sg.Frame("",layout=VOL_COP_LAYOUT, **frame_format)],
      [sg.Frame("",layout=PIPE_AB_LAYOUT, **frame_format)],
    ]
    return LAYOUT_GENERAL

  def create_col_izq(self):
    """ Layout columna izquierda del programa
    
    LLaves que Maneja
    -----------------
    FILE: (Ventana) Maneja el cambio de ventana en la aplicacion
    ELEM: (Ventana) Maneja el cambio de ventana en la aplicacion
    Agregar: (Boton) Agrega una nueva clasificacion
    
    Llaves que Hereda
    -----------------
    PIPE_A: (str) PIPE A de la clasificacion
    PIPE_B: (str) PIPE B de la clasificacion
    VOL: (int) Volumen del Libro
    COP: (int) Copia del Libro
    CLAS: (str) Clasificacion del Libro
    HEAD: (str) Encabezado del Libro

    """
    CLASIF_LAYOUT = self.create_clasification_layout()
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
      [sg.Text(text=self.titulo_ventana, **text_format)], #pad=(0, (0, 15)),
      [sg.Frame("",layout=SELECCIONAR_LAYOUT, border_width=0, **frame_format)],
      [sg.HSep(pad=(0, 5))],
      [sg.Frame("",layout=CLASIF_LAYOUT, **frame_format)],
      [sg.HSep(pad=(0, 5))],
      [sg.Button("Agregar", font=("Open Sans", 12, 'bold'))],
      # [
      #   sg.FolderBrowse("Guardar", font=("Open Sans", 12), pad=(5, (0, 10))),
      #   sg.In(
      #     default_text=ruta_folder, size=(50, 1), 
      #     enable_events=True, 
      #     key="FOLDER", 
      #     font=("Open Sans", 9), 
      #     justification="center", 
      #     pad=(5, (0, 5)),
      #   ),
      # ],
    ]
    return GENERAL_LAYOUT
  
  def create_col_der(self):
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
    tabla_principal = self.table_manager.tabla_principal
    row_color_array = self.table_manager.tabla_formato
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
          num_rows=15,
          auto_size_columns=False,
          display_row_numbers=True,
          justification="l",
          expand_y=False,
          enable_events=True,
          right_click_menu=["Etiqueta", ["Modificar"]],
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

  def create_layout(self):
    """ Crea el layout principal para esta ventana 
    
    Llaves que Hereda
    -----------------    
    FILE: (Ventana) Maneja el cambio de ventana en la aplicacion
    ELEM: (Ventana) Maneja el cambio de ventana en la aplicacion
    Agregar: (Boton) Agrega una nueva clasificacion
    PIPE_A: (str) PIPE A de la clasificacion
    PIPE_B: (str) PIPE B de la clasificacion
    VOL: (int) Volumen del Libro
    COP: (int) Copia del Libro
    CLAS: (str) Clasificacion del Libro
    HEAD: (str) Encabezado del Libro
    TABLE : (Tabla) Manejo general de la tabla
    Modificar : (Tabla/ Click Derecho) Modificar una etiqueta de la tabla
    SELECT-ALL : (Boton) Seleccionar todas las etiquetas
    LIMPIAR : (Boton) Reiniciar todo el programa
    DESELECT-ALL : (Boton) Para deseleccionar todas las etiquetas
    EXPORTAR : (Boton) Lanzar la siguiente parte del programa
    """
    colum_format = {
      'background_color':"#FFFFFF", 
      'element_justification':"c", 
      'pad':0
    }
    COL_IZQ_LAYOUT = self.create_col_izq()
    COL_DER_LAYOUT = self.create_col_der()
    LAYOUT = [
      [
        sg.Column(COL_IZQ_LAYOUT, **colum_format),
        sg.VSep(pad=(5, 0)),
        sg.Column(COL_DER_LAYOUT, **colum_format),
      ],
    ]
    return LAYOUT

  def create_window(self):
    """ Genera un Objeto tipo Ventana de PySimpleGUI """
    LAYOUT = self.create_layout()
    MAIN_LAYOUT = [
      #* Menu superior de la APP
      [sg.Menu(menu_opciones, tearoff=False)],
      [sg.Frame("",layout=LAYOUT, background_color='#FFFFFF', element_justification='c')],
    ]
    
    window = sg.Window(self.titulo_ventana, MAIN_LAYOUT, element_justification="c", icon=resource_path("Assets/ticket_icon.ico"))  
    return window

  def run_window(self):
    #?#********** MANEJO DE VARIABLES #?#**********
    bandera_agregar = False
    bandera_modificar = False
    index_modificar = 0
    estatus_modificar = 'K'
    window = self.create_window()
    #?#**********  LOOP PRINCIPAL#?#**********
    while True:
      event, values = window.read()
      self.show_window_events(event, values)
      #* Cerrar la aplicación
      if event in (sg.WINDOW_CLOSED, "Exit"):
        window.close()
        return True
      #* Cambio de Ventana a ARCHIVO
      elif event == "FILE":
        window.close()
        # TODO Mandar llamar la ventana para archivos
      #* Revisar una clasificación
      elif event in ("CLAS", 'VOL', 'COP', 'HEAD'):
        bandera_agregar = self.checar_clasificacion(window, values)
      #* Añadir una clasificación a la tabla 
      elif event == "Agregar" and bandera_agregar:
        self.agregar_clasificacion(window, values)
        bandera_agregar = False
      elif event == "LIMPIAR":
        print("Resetar ventana")
        self.reset_window(window)
        bandera_agregar = False
        bandera_modificar = False
      elif event == "SELECT-ALL":
        bandera_modificar = False
        self.select_all_table(window)
      elif event == "DESELECT-ALL":
        bandera_modificar = False
        self.deselect_all_table(window)
      elif event == "TABLE":
        modify_object = (index_modificar, bandera_modificar, estatus_modificar)
        index_modificar, bandera_modificar, estatus_modificar = self.table_management(window, values, modify_object)
      elif event == "Modificar" and bandera_modificar is True:
        bandera_modificar = self.modificar_elemento(window, index_modificar)
      elif event == 'Exportar':
        pass


  def show_window_events(self, event, values):
    print('-'*50)
    print(f'Eventos que suceden {event}')
    print(f'Valores guardaros {values}')
    print('-'*50 + '\n')

  def checar_clasificacion(self, window, values):
    clasificacion = str(values["CLAS"])
    # * Revisar si es relevante el cambio
    if len(clasificacion) < 5: return False
    
    #* Se revisa si se puede separa la PIPE B
    if sh.revisar_corte_pipe(clasificacion) and sh.revisar_pipeB(clasificacion):
      posicion_corte, diferencia = sh.buscar_pipe(clasificacion)
      if posicion_corte != 0:
        pipe_a_str = clasificacion[:posicion_corte]
        pipe_b_str = clasificacion[posicion_corte + diferencia :]
        window["PIPE_A"].update(pipe_a_str)  
        window["PIPE_B"].update(pipe_b_str)
        # ? Bandera Verdadera se puede agregar
        return True
    else:
      window["PIPE_A"].update("NO")
      window["PIPE_B"].update("APLICA")
      # ? Bandera Falsa no se puede agregar
      return False
  
  def agregar_clasificacion(self, window, values):
    #* Dar formato para la clasificación Completa
    clasificacion = str(values["CLAS"])
    volumen = str(values['VOL'])
    copia = str(values['COP'])
    encabezado = str(values['HEAD'])
    
    volumen = 'V.' + volumen if volumen not in ('', '0') else ''

    clasificacion_completa = creador_clasificacion(clasificacion, encabezado, volumen, copia)
    
    lista_principal = [clasificacion_completa, values["PIPE_A"], values["PIPE_B"], "Added",]
    lista_datos = {
      'titulo':'Sin Titulo', 
      'cbarras':'No Aplica', 
      'clasif':clasificacion, 
      'volumen':volumen,
      'copia':copia, 
      'encabeza':encabezado
    }
    
    #* Se agrega dicho elemento a las listas de datos
    self.table_manager.agregar_elemento(lista_principal, lista_datos, 'True', '#696D7D')

    #* Actualizando la tabla principal
    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.tabla_formato
    )

  def reset_window(self, window):
    """ Reiniciar todos los valores de la tabla que se trabaja """
    self.table_manager.reset_table()
    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.tabla_formato
    )

  def select_all_table(self, window):
    for x in range(self.table_manager.get_len()):
      status = self.table_manager.get_status_element(x)
      if status != "False":
        self.table_manager.actualizar_elemento(x,"Selected","#498C8A")

    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.tabla_formato)
  
  def deselect_all_table(self, window):
    for x in range(self.table_manager.get_len()):
      status = self.table_manager.get_status_element(x)
      if status != "False":
        self.table_manager.actualizar_elemento(x,"True","#FFFFFF")

    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.tabla_formato)

  def table_management(self, window, values, modify_object):
    modify_index, modify_flag, modify_status = modify_object
    print(modify_index, modify_flag, modify_status)
    #* Manejar excepcion con respecto a datos inexistentes
    if len(values["TABLE"]) == 0: return modify_index, modify_flag, modify_status
    
    index_value = int(values["TABLE"][0])  # * elemento a seleccionar
    status = self.table_manager.get_status_element(index_value)  # * Revisar el status del elemento
    # print(status)

    # * Seleccionar una casilla valida
    if status == "True":
      # Cambias el estatus de ese elemento a seleccionado
      self.table_manager.actualizar_elemento(index_value, "Selected", "#498C8A")

    # * Seleccionar casilla para modificar
    elif status in ("Selected", "False") and modify_flag is False:
      #* Actualizar datos de modificacion
      modify_status = status
      modify_flag = True
      modify_index = index_value
      #* Modificar elemento visualmente
      self.table_manager.actualizar_elemento(index_value, "Modify", "#E8871E")

    # * Quitar casilla de modificar
    elif status == "Modify":
      #? Cambiar elemento modificado/seleccionado a Normal
      if modify_status == "Selected":
        self.table_manager.actualizar_elemento(index_value, "True", "#FFFFFF")
      #? Cambiar elemento modificado/error a Error
      elif modify_status == "False":
        self.table_manager.actualizar_elemento(index_value, "False", "#F04150")
      modify_flag = False

    # * Regresar casilla a normalidad
    elif status == "Selected" and modify_flag is True:
      self.table_manager.actualizar_elemento(index_value, "True", "#FFFFFF")
    
    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.tabla_formato)
    return modify_index, modify_flag, modify_status

  def modificar_elemento(self, window, modify_index):
    #* Sacar los datos de esa etiqueta
    clasif_completa = self.table_manager.tabla_principal[modify_index][0]
    datos_etiqueta = self.table_manager.tabla_datos[modify_index]
    #* Mandar llamar ventana modificar
    VM = VentanaModificar(clasif_completa, datos_etiqueta)
    aux_principal, aux_datos = VM.run_window()
    #* Checar si hubieron cambios
    if aux_principal is False: return True
    
    # * Agregamos elemento a una tabla de modificaciones
    self.table_manager.agregar_modificado(modify_index, aux_principal[0])

    # * Cambiamos la apariencia del elemento en la tabla
    self.table_manager.actualizar_elemento(modify_index, 'True', '#D8D8D8')

    # * Actualizar valores de tabla de datos
    aux_tabla_datos = self.table_manager.get_data_element(modify_index)
    aux_tabla_datos['clasif'] = aux_datos[0]
    aux_tabla_datos['volumen'] = aux_datos[1]
    aux_tabla_datos['copia'] = aux_datos[2]
    aux_tabla_datos['encabeza'] = aux_datos[3]
    self.table_manager.set_data_element(modify_index, aux_tabla_datos)

    #* Actualizar valores de tabla principal
    self.table_manager.set_element(modify_index, aux_principal)
    
    #* Actualizar apariencia de la tabla
    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.tabla_formato
    )

    return False

  def exportar_etiquetas(self, values):
    etiquetas_a_imprimir = []
    # * LLenado de lista de elementos seleccionados
    for ind in range(self.table_manager.get_len()):
      status = self.table_manager.get_status_element(ind)
      if status == "Selected":
        # Crear la lista de datos
        aux_datos = self.table_manager.get_data_element(ind)
        encabezado = aux_datos['encabeza']
        clasif = aux_datos['clasif']
        volumen = aux_datos['volumen']
        copia = aux_datos['copia']

        dict_format = {'HEAD':encabezado, 'CLASS':clasif, 'VOL':volumen, 'COP':copia}
        etiquetas_a_imprimir.append(dict_format)
    # * Revisar que la tabla de seleccionado tenga valores para poder continuar
    if len(etiquetas_a_imprimir) == 0: 
      pop.warning_select()
      return False

    #* Pasamos a la ventana de configuración
    #TODO Crear ventana configuracion
    estatus_config, valores_config, coordenadas = sw.ventana_config(valores_config)  
    #? Esta ventana retorna un True o False dependiendo si se modifico la configuración o no
    #? Retorna los valores
    #? Coordenadas si son necesarias
    #* Revisar estatus de configuración
    # True continua con el proceso, False termian el proceso
    if estatus_config is False: return False

    # ? Función para el manejo y creación de eiquetas
    # TODO Posible cambio en este atributo
    today_date = datetime.now().strftime("%d_%m_%Y_%H%M%S") # Chequeo de hora de consulta
    # LLamamos funcion para crear los tickets
    tm.ticket_maker_main(
      config=valores_config, etiquetas_a_imprimir=etiquetas_a_imprimir, 
      titulo=today_date, ruta=ruta_folder, position=coordenadas)
    # Generamos un reporte de modificaciones
    maintf.crear_reporte_modificados(tabla_modify, ruta_folder, today_date)  
    pop.success_program()
    return True
    # TODO Preguntar por la ruta a guardar


def main():
  """ Funcion principal para el manejo de la aplicacion """
  VE = VentanaElementos()
  VE.run_window()

if __name__ == '__main__':
  main()

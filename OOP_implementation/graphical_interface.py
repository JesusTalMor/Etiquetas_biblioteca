#############################################################
# Editor: Jesus Talamantes Morales
# Fecha Trabajo: 17 de Mayo 2023
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

# from datetime import datetime


# import main_ticket_functions as maintf
# import pop_ups as pop
# import string_helper as sh
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

# # Manejo Principal del elemento tabla
tabla_principal = []
# main_dicc = {}
row_color_array = []

# # Manejo de datos de los libros para modificaciones
# tabla_datos = []
# tabla_modify = []

# # Configuracion para impresion
# valores_config = {}
# coordenadas = (None,None)

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
  def __init__(self, excel_file='', ruta_folder='') -> None:
    self.ruta_archivo = excel_file
    self.ruta_folder = ruta_folder

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
    
    Llaves que Maneja
    -----------------    
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
    window = self.create_window()
    while True:
      event, values = window.read()

      # print('-'*50)
      # print(f'Eventos que suceden {event}')
      # print(f'Valores guardaros {values}')
      # print('-'*50 + '\n')

      #* Cerrar la aplicación
      if event in (sg.WINDOW_CLOSED, "Exit"):
        window.close()
        return True

def main():
  """ Funcion principal para el manejo de la aplicacion """
  VE = VentanaElementos()
  VE.run_window()

if __name__ == '__main__':
  main()

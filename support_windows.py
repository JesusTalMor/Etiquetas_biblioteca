import os
import sys

import PySimpleGUI as sg

import pop_ups as pop
from managers import Libro

"""En este modulo se almacenan las ventanas auxiliares de trabajo."""

# * Tema principal de las ventanas
sg.LOOK_AND_FEEL_TABLE["MyCreatedTheme"] = {
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
sg.theme("MyCreatedTheme")

#?#********** Función apoyo para relative path *********#
def resource_path(relative_path):
  """ Get absolute path to resource, works for dev and for PyInstaller """
  try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

class VentanaModificar:
  '''Modifica el contenido y parametros de una etiqueta

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
  def __init__(self, aLibro:Libro):
    self._Libro = aLibro

  def clasification_layout(self):
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
      'font' :  ("Open Sans", 12, "bold"),
      'size' :  (6,1),
      'pad'  :  0,
      'background_color'  : "#FFFFFF", 
      'justification'     : "center",
    }
    in_format = {
      'size':(14, 1), 
      'font':("Open Sans", 10, "bold"), 
      'justification':"center", 
      'disabled':True,
      'text_color' : '#1AB01F' if self._Libro.etiqueta.clasif_valida else '#F04150',
      'pad' : 5,
    }
    pipe_a_layout = [
      [sg.Text(text="PIPE A", **text_format)],
      [sg.In(default_text=self._Libro.etiqueta.PIPE_A, key="PIPE_A", **in_format)],
    ]
    pipe_b_layout = [
      [sg.Text(text="PIPE B", **text_format)],
      [sg.In(default_text=self._Libro.etiqueta.PIPE_B, key="PIPE_B", **in_format)],
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
      'font':("Open Sans", 12,), 
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
      sg.In(default_text=self._Libro.etiqueta.volumen, key="VOL", **in_format),
      sg.Text(text="Copia", **text_format),
      sg.In(default_text=self._Libro.etiqueta.copia, key="COP", **in_format),
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
      [sg.Text(text="Clasificación", **title_format)],
      [sg.In(default_text=self._Libro.etiqueta.clasif, size=(30, 1), key="CLAS", pad=(10, 0), **in_format)],
      #* Funcion para agregar un encabezado
      [sg.Text(text="Encabezado", **text_format)],
      [sg.In(default_text=self._Libro.etiqueta.encabezado, size=(20, 1), key="HEAD", pad=0, **in_format)],
      [sg.Frame("",layout=VOL_COP_LAYOUT, **frame_format)],
      [sg.Frame("",layout=PIPE_AB_LAYOUT, **frame_format)],
    ]
    return LAYOUT_GENERAL

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
    INDIV_LAYOUT = self.clasification_layout()
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
        sg.In(default_text=self._Libro.titulo, size=(40, 1), key="TITLE", **in_format)
      ],
      [
        sg.Text(text="Código de Barras", pad=((0,20), 0), **text_format),
        sg.In(default_text=self._Libro.cbarras, size=(20, 1), key="CBARRAS", **in_format)
      ],
    ]
    #?#********* LAYOUT GENERAL DE ESTA APLICACION #?#*********
    title_format = {
      'font' : ("Open Sans", 20, "bold", "italic"),
      'background_color' : '#FFFFFF',
      'justification' : 'c',
      'pad' : (0, 5),
    }
    text_format = {
      'font' : ("Open Sans", 14, "bold"),
      'background_color':"#FFFFFF", 
      'justification':"c",
    }
    frame_format = {'background_color':"#FFFFFF", 'element_justification':"c",}
    GENERAL_LAYOUT = [
      #* Titulo de la aplicacion y Boton de Mas Info
      [
        sg.Text(text=self.titulo_ventana, **title_format,),
        sg.Button(
          image_source=resource_path('Assets/info_icon.png'), image_subsample=10, 
          border_width=0, key='INFO', pad=(5,5)
        )
      ],
      #* Texto para mostrar clasificacion completa
      [sg.Text(text=self._Libro.etiqueta.clasif_completa, key="TEXT", **text_format)],
      [sg.HSep(pad=(0, 5))], # Separador
      #* Layout para modificar atributos etiquetas
      [sg.Frame("", layout=INDIV_LAYOUT, **frame_format)],
      [sg.HSep(pad=(0, 5))], # Separador
      #* Layout para modificar informacion etiquetas
      [sg.Frame("", layout=INFO_LAYOUT, border_width=0, **frame_format)],
      [sg.HSep(pad=(0, 5))], # Separadores
      [
        sg.Button("Cancelar", font=("Open Sans", 12, "bold")),
        sg.Button("Modificar", font=("Open Sans", 12, "bold"), disabled= not self._Libro.etiqueta.clasif_valida),
      ],    
    ]
    return GENERAL_LAYOUT

  def create_window(self):
    LAYOUT = self.create_layout()
    MAIN_LAYOUT = [[sg.Frame('', LAYOUT, background_color='#FFFFFF', element_justification='c')]]
    window = sg.Window(self.titulo_ventana, MAIN_LAYOUT, element_justification='c', icon=resource_path('Assets/ticket_icon.ico'))
    return window

  #? FUNCIONAMIENTO PRINCIPAL DE LA VENTANA ***********************
  def run_window(self):
    window = self.create_window()

    while True:
      event, values = window.read()
      self.show_window_events(event, values)
      #* Cerrar programa sin resultados
      if event in (sg.WINDOW_CLOSED, "Exit", "Cancelar"):
        window.close() 
        return False, self._Libro
      
      #* Actualizar elemento de Clasificacion Completa
      self.actualizar_clasif(window)
      window['TEXT'].update(self._Libro.etiqueta.clasif_completa)

      if event == 'Modificar':
        window.close()
        return True, self._Libro
      elif event == 'INFO': 
        pop.info_pop('book_info', [self._Libro.titulo, self._Libro.cbarras])

  #? FUNCIONALIDAD GENERAL *********************************
  def show_window_events(self, event, values):
    print(f"""
      Imprimiendo Eventos de Suceden
      {'-'*50}
      Eventos que suceden {event}
      Valores guardados {values}
      {'-'*50}
    """)

  def actualizar_clasif(self, window):
    """ Construye una clasificacion en tiempo real 
    """
    #* Tomar datos
    try:
      self._Libro.etiqueta.clasif = window["CLAS"].get()
      self._Libro.etiqueta.volumen = window['VOL'].get()
      self._Libro.etiqueta.copia = window['COP'].get()
      self._Libro.etiqueta.encabezado = window['HEAD'].get()
      self._Libro.titulo = window['TITLE'].get() if window['TITLE'].get() != '' else self._Libro.titulo
      self._Libro.cbarras = window['CBARRAS'].get() if window['CBARRAS'].get() != '' else self._Libro.cbarras
    except TypeError:
      pass

    if self._Libro.etiqueta.clasif_valida:
      window["PIPE_A"].update(value=self._Libro.etiqueta.PIPE_A, text_color='#1AB01F')  
      window["PIPE_B"].update(value=self._Libro.etiqueta.PIPE_B, text_color='#1AB01F')
      window["Modificar"].update(disabled=False)
    else:
      window["PIPE_A"].update(value="XXXXXX", text_color='#F04150')  
      window["PIPE_B"].update(value="XXXXXX", text_color='#F04150')
      window["Modificar"].update(disabled=True)

if __name__ == "__main__":
  libro_prueba = Libro(
    aID=1,
    aTitulo= 'Titulo_Prueba',
    aCbarras= 'QRO123123123',
    aClasif= 'A00.A00.A00 .A00 1000',
    aVolumen= '0',
    aCopia= '1',
    aEncabezado= '',
  )
  VM = VentanaModificar(libro_prueba)
  estatus, libro_modificado = VM.run_window()
  del VM

  if estatus is True: print(f'[INFO] El Libro fue modificado \n {libro_modificado}')
  else: print(f'[INFO] Libro sin modificaciones \n {libro_prueba}')
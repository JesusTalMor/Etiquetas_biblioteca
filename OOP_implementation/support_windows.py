import PySimpleGUI as sg

import pop_ups as pop
import string_helper as sh

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

class VentanaSeleccionarPosicion:
  """ Ventana encargada para seleccionar la posicion de una pagina """
  def __init__(self, num_row:int, num_column:int):
    self.num_row = num_row
    self.num_column = num_column
  
  def create_layout(self):
    layout = [[sg.Text(text='Seleccione un casilla', font=("Open Sans", 16, "bold", "italic"), background_color='#FFFFFF')]]
    # * Añadimos casillas para de selección
    for row in range(self.num_row):
      new_row = []
      for column in range(self.num_column):
        new_row.append(sg.Button(size=(2,2), key=(row, column)))
      layout.append(new_row)
    layout.append([sg.Button('Guardar', font=("Open Sans", 14, 'bold'))])
    return layout

  def create_window(self):
    LAYOUT = self.create_layout()
    MAIN_LAYOUT = [[sg.Frame('', LAYOUT, background_color='#FFFFFF', element_justification='c')],]
    WINDOW = sg.Window('Seleccionar Posición', MAIN_LAYOUT, icon=resource_path('Assets/ticket_icon.ico'))
    return WINDOW
  
  def run_window(self):
    window = self.create_window()
    select_flag = False
    while True:
      event, values = window.read()
      if event in (sg.WINDOW_CLOSED, 'Cancel'):
        window.close()
        return False
      
      #* Seleccionar una casilla
      if isinstance(event, tuple):
        if select_flag is False:
          position = event
          selected_flag = True
          window[event].update(button_color='green')
        elif event == position:
          selected_flag = False
          window[event].update(button_color='#FFFFFF')

      if event == 'Guardar' and selected_flag:
        window.close()
        return position

class VentanaConfiguracion:
  """ Establecer la configuracion para impresion de etiquetas
  """
  INDI_CONFIG = {
    'PAGE_W':0.0, 'PAGE_H':0.0,
    'INDI_W':4.8, 'INDI_H':3.7,
    'ROW':0, 'COL':0
  }
  PAGE_CONFIG = {
    'PAGE_W':21.59, 'PAGE_H':27.94,
    'INDI_W':2.69, 'INDI_H':4.65,
    'ROW':6, 'COL':8
  }
  titulo_ventana = 'Configuración Etiquetas'
  def __init__(self, config=PAGE_CONFIG) -> None:
    self.main_config = config
  
  def create_layout(self):
    page_layout = self.create_page_layout()
    indi_layout = self.create_indi_layout()
    title_config = {
      'font':("Open Sans", 18, "bold", "italic"),
      'background_color':"#FFFFFF", 
      'justification':"c",
    }
    text_config = {
      'font':("Open Sans", 12, "bold"),
      'background_color':"#FFFFFF", 
      'justification':"c",
    }
    colum_config = {
      'background_color':"#FFFFFF", 
      'element_justification':"c"
    }
    button_config = {
      'size':(8, 1),
      'font':("Open Sans", 13, "bold"),
    }
    radio_config = {
      'background_color':"#FFFFFF",
      'circle_color':"#DEE6F7", 
      'font':("Open Sans", 14, "bold"),
      'enable_events':True,
    }
    MAIN_LAYOUT = [
      [sg.Text(text=self.titulo_ventana, ** title_config),],
      [sg.Text(text="Seleccione una opción:", **text_config)],
      [
        sg.Radio(
          "Tamaño Carta", "O1", key="SHEET",
          default=True, **radio_config
        ),
        sg.Radio(
          "Tamaño Individual", "O1", key="INDIV",
          default=False, **radio_config
        ),
      ],
      [sg.HorizontalSeparator()],
      [
        sg.Column(page_layout, **colum_config),
        sg.Column(indi_layout, **colum_config),
      ],
      [
        sg.Button("Reset", key="RESET", **button_config),
        sg.Button("Aceptar", key="ACCEPT", **button_config),
      ],
    ]
    return MAIN_LAYOUT
  
  def create_page_layout(self):
    main_config = self.main_config
    text_config = {
      'size':(10, 1), 
      'font':("Open Sans", 12, "bold"),
      'background_color':"#FFFFFF", 
      'justification':"c",
    }
    in_config = {
      'size':(10, 1),
      'font':("Open Sans", 12, "bold"),
      'justification':"center", 
      'enable_events':True,
    }
    width_height_layout = [
      [
        sg.Text(text="Ancho (cm)", **text_config),
        sg.Text(text="Alto (cm)", **text_config),
      ],
      [
        sg.In(default_text=main_config['PAGE_W'], key="PAGE_W",**in_config),
        sg.In(default_text=main_config['PAGE_H'], key="PAGE_H", **in_config),
      ],    
    ]
    text_config = {
      'size':(10, 1), 
      'font':("Open Sans", 12, "bold"),
      'background_color':"#FFFFFF", 
      'justification':"c",
    }
    in_config = {
      'size':(10, 1),
      'font':("Open Sans", 12, "bold"),
      'justification':"center", 
      'enable_events':True,
    }
    colum_row_layout = [
      [
        sg.Text(text="Columnas", **text_config),
        sg.Text(text="Filas", **text_config),
      ],
      [
        sg.In(default_text=main_config['COL'], key="COL", **in_config),
        sg.In(default_text=main_config['ROW'], key="ROW", **in_config),
      ],
    ]
    frame_config = {
      'background_color':'#FFFFFF', 
      'element_justification':'c', 
      'border_width':0
    }
    radio_config = {
      'background_color':"#FFFFFF",
      'circle_color':"#DEE6F7",
      'font':("Open Sans", 14, "bold"),
      'enable_events':True,
    }
    PAGE_LAYOUT = [
      [sg.Frame('', width_height_layout, **frame_config)],
      [sg.Frame('', colum_row_layout, **frame_config)],
    ]
    return PAGE_LAYOUT
  def create_indi_layout(self):
    main_config = self.main_config
    text_config = {
      'size':(10, 1), 
      'font':("Open Sans", 12, "bold"),
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    in_config = {
      'size':(10, 1),
      'font':("Open Sans", 12, "bold"),
      'disabled':True, 
      'justification':"c",
    }
    width_height_layout = [
      [
        sg.Text(text="Ancho (cm)", **text_config),
        sg.Text(text="Alto (cm)", **text_config),
      ],
      [
        sg.In(default_text=main_config['INDI_W'], key="INDI_W", **in_config),
        sg.In(default_text=main_config['INDI_H'], key="INDI_H", **in_config),
      ],
    ]
    frame_config = {
      'background_color':"#FFFFFF", 
      'element_justification':'c', 
      'border_width':0
    }
    INDI_LAYOUT = [
      [sg.Frame('', width_height_layout, **frame_config)]
    ]
    return INDI_LAYOUT

  def create_window(self):
    LAYOUT = self.create_layout()
    MAIN_LAYOUT = [[sg.Frame('', LAYOUT, background_color='#FFFFFF', element_justification='c')]]
    window = sg.Window(self.titulo_ventana, MAIN_LAYOUT, icon=resource_path('Assets/ticket_icon.ico'))
    return window
  
  def run_window(self):
    window = self.create_window()
    while True:
      event, values = window.read()
      # * Cerrar la ventana
      if event in (sg.WINDOW_CLOSED, "Exit", "Salir"):
        window.close()
        return False, self.main_config
      #* Calcular Tamaño etiqueta individual
      if event in ("PAGE_W", "PAGE_H", "COL", "ROW"):
        self.calcular_etiquetas(window, values)
      # * Seleccionar pagina
      if event == "SHEET":
        self.cambiar_pagina(window)
      if event == "INDIV":
        self.cambiar_individual(window)
      if event == "RESET":
        self.resetear_valores(window, values["SHEET"])
      if event == 'ACCEPT':
        window.close()
        return True, self.crear_configuracion(values)
  
  def calcular_etiquetas(self, window, values):
    try:
      #* Calcular tamaños de las etiquetas
      cal_height = float(values["PAGE_H"]) / float(values["ROW"])
      cal_width = float(values["PAGE_W"]) / float(values["COL"])
      #* Redondear tamaños de las etiquetas
      cal_height = round(cal_height, 2)
      cal_width = round(cal_width, 2)
      window["INDI_W"].update(cal_width)
      window["INDI_H"].update(cal_height)
    except:
      return
  
  def cambiar_pagina(self, window):
    page_config = self.PAGE_CONFIG
    #* Actualizar valores de Pagina
    window["PAGE_W"].update(page_config["PAGE_W"], disabled=False)
    window["PAGE_H"].update(page_config["PAGE_H"], disabled=False)
    window["COL"].update(page_config["COL"], disabled=False)
    window["ROW"].update(page_config["ROW"], disabled=False)

    #* Desactivar valores individuales
    window["INDI_W"].update(page_config["INDI_W"], disabled=True)
    window["INDI_H"].update(page_config["INDI_H"], disabled=True)

  def cambiar_individual(self, window):
    page_config = self.INDI_CONFIG
    #* Actualizar valores de Pagina
    window["PAGE_W"].update(page_config["PAGE_W"], disabled=True)
    window["PAGE_H"].update(page_config["PAGE_H"], disabled=True)
    window["COL"].update(page_config["COL"], disabled=True)
    window["ROW"].update(page_config["ROW"], disabled=True)

    #* Desactivar valores individuales
    window["INDI_W"].update(page_config["INDI_W"], disabled=False)
    window["INDI_H"].update(page_config["INDI_H"], disabled=False)

  def resetear_valores(self, window, flag):
    if flag is True: config = self.PAGE_CONFIG
    else: config = self.INDI_CONFIG
    window["PAGE_W"].update(config["PAGE_W"])
    window["PAGE_H"].update(config["PAGE_H"])
    window["INDI_W"].update(config["INDI_W"])
    window["INDI_H"].update(config["INDI_H"])
    window["COL"].update(config["COL"])
    window["ROW"].update(config["ROW"])

  def crear_configuracion(self, values):
    main_config = {}
    main_config["PAGE_W"], main_config["PAGE_H"] = values['PAGE_W'], values['PAGE_H']
    main_config["INDI_W"], main_config["INDI_H"] = values['INDI_W'], values['INDI_H']
    main_config["COL"], main_config["ROW"] = values['COL'], values['ROW']
    return main_config

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


if __name__ == "__main__":
  pass
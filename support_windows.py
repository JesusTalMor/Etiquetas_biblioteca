import PySimpleGUI as sg

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



# ? Ventanas de apoyo y configuraciones
def ventana_modificar_clasificacion(clasificacion_completa:str, clasif:str, volumen:str, copia:int, encabezado:str):
  '''Modifica el contenido y parametros de una etiqueta'''
  # TODO Posibilidad de Agregar Nombre del Libro y Codigo de Barras
  bandera_agregar = False
  
  # * actualizar el Volumen a standard
  volumen = volumen[volumen.index('V.') + 2] if 'V.' in volumen else ''

  # * Seccion de Layout de la Ventana
  pipe_a = [
    [
      sg.Text(
        text="PIPE A", 
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF", 
        justification="center", 
        pad=5,
      )
    ],
    [
      sg.In(default_text="ESPERA", size=(14, 1), font=("Open Sans", 10),
      justification="center", key="PIPE_A", disabled=True,)
    ],
  ]
  pipe_b = [
    [
      sg.Text(
        text="PIPE B", 
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF", 
        justification="center", 
        pad=5,
      )
    ],
    [
      sg.In(default_text="MODIFICAR", size=(12, 1),
      font=("Open Sans", 10), justification="center",
      key="PIPE_B", disabled=True,)
    ],
  ]
  indi_layout = [
    [
      sg.Text(
        text="Modif. Clasificación", 
        font=("Open Sans", 14, "bold"), 
        background_color="#FFFFFF", 
        justification="center",
      )
    ],
    [
      sg.In(
        default_text=clasif, 
        size=(28, 1), 
        enable_events=True,
        key="CLAS",
        font=("Open Sans", 12), 
        justification="center", 
        pad=(15, 5),
      )
    ],
    [
      sg.Text(
        text="Agregar Encabezado",
        font=("Open Sans", 12),
        background_color="#FFFFFF",
        justification="center",
      )
    ],
    [
      sg.In(
        default_text=encabezado, 
        size=(18, 1),
        enable_events=True,
        key="HEAD",
        font=("Open Sans", 10),
        justification="center",
      )
    ],
    [
      sg.Text(
        text="Volumen",
        font=("Open Sans", 12),
        background_color="#FFFFFF",
        justification="center",
      ),
      sg.In(
        default_text=volumen, 
        size=(2, 1),
        enable_events=True,
        key="VOL",
        font=("Open Sans", 10),
        justification="center",
      ),
      sg.Text(
        text="Copia",
        font=("Open Sans", 12),
        background_color="#FFFFFF",
        justification="center",
      ),
      sg.In(
        default_text=copia, 
        size=(2, 1),
        enable_events=True,
        key="COP",
        font=("Open Sans", 10),
        justification="center",
      ),
    ],
    [
      sg.Column(
        layout=pipe_a, 
        background_color="#FFFFFF", 
        element_justification="c"
      ),
      sg.VSeperator(),
      sg.Column(
        layout=pipe_b, 
        background_color="#FFFFFF", 
        element_justification="c"
      ),
    ],
  ]
  layout = [
    [
      sg.Text(
        text="Modificar una Etiqueta",
        font=("Open Sans", 18, "bold", "italic"),
        background_color="#FFFFFF",
        justification="center",
        pad=(0, (0, 15)),
      )
    ],
    [
      sg.Text(
        text=clasificacion_completa,
        font=("Open Sans", 16, "bold"),
        background_color="#FFFFFF",
        justification="center",
        key="TEXT",
      )
    ],
    [sg.HorizontalSeparator(color="#000000", pad=(0, (10, 6)))],
    [
      sg.Frame(
        "",
        layout=indi_layout,
        background_color="#FFFFFF",
        element_justification="c",
      )
    ],
    [sg.HorizontalSeparator(color="#000000", pad=(0, (6, 10)))],
    [
      sg.Button("Cancelar", font=("Open Sans", 14, "bold")),
      sg.Button("Modificar", font=("Open Sans", 14, "bold")),
    ],
  ]
  main_layout = [
    [
      sg.Frame("", layout, background_color="#FFFFFF", element_justification="c", pad=0)
    ]
  ]

  # * Creacion de la ventana
  window = sg.Window("Modificar una Etiqueta", main_layout, element_justification="c", icon="Assets/ticket_icon.ico")

  while True:
    event, values = window.read()
    # print('-'*50)
    # print(f'Eventos que suceden {event}')
    # print(f'Valores guardaros {values}')
    # print('-'*50 + '\n')

    # * Actualizar clasificacion
    clasif = str(values["CLAS"])
    volumen = str(values['VOL'])
    copia = str(values['COP'])
    encabezado = str(values['HEAD'])

    encabezado = encabezado + ' ' if encabezado != '' else ''
    volumen = 'V.' + volumen if volumen not in ('', '0') else ''
    clasificacion_completa = encabezado + sh.creador_clasificacion(clasif, volumen, copia)
    window['TEXT'].update(clasificacion_completa)

    if event in (sg.WINDOW_CLOSED, "Exit", "Cancelar"):
      break

    # * Modificar clase
    elif event == "CLAS":
      if len(str(values["CLAS"])) > 5:
        clasif = str(values["CLAS"])
        if sh.revisar_corte_pipe(clasif) and sh.revisar_pipeB(clasif):
          posicion_corte, diferencia = sh.buscar_pipe(clasif)
          if posicion_corte != 0:
            pipe_a_str = clasif[:posicion_corte]
            pipe_b_str = clasif[posicion_corte + diferencia :]
            window["PIPE_A"].update(pipe_a_str)
            window["PIPE_B"].update(pipe_b_str)
            bandera_agregar = True  # ? Bandera Verdadera
        else:
          window["PIPE_A"].update("NO")
          window["PIPE_B"].update("APLICA")
          bandera_agregar = False  # ? Bandera Falsa

    
    # * Modifica la etiqueta y cierra la ventana
    elif event == "Modificar" and bandera_agregar:
      # clasif = str(values["CLAS"])
      # volumen = str(values['VOL'])
      # copia = str(values['COP'])
      # encabezado = str(values['HEAD'])

      # volumen = 'V.' + volumen if volumen not in ('', '0') else ''
      # clasificacion_completa = encabezado + ' ' + sh.creador_clasificacion(clasif, volumen, copia)

      window.close()
      return [clasificacion_completa, values["PIPE_A"], values["PIPE_B"], "True"], [clasif, volumen, copia, encabezado]

  window.close()
  return [False],[False]


def seleccionar_posicion_impresion(num_row:int, num_column:int) -> tuple:
  '''Selecciona la posición inicial de impresion en hoja carta'''
  position = (None,None)
  selected_flag = False

  layout = [
    [sg.Text(text='Seleccione un casilla', font=("Open Sans", 16, "bold", "italic"), background_color='#FFFFFF')]
  ]
  # * Añadimos casillas para de selección
  for row in range(num_row):
    new_row = []
    for column in range(num_column):
      new_row.append(sg.Button(size=(4,2), key=(row, column)))
    layout.append(new_row)
  layout.append([sg.Button('Guardar', font=("Open Sans", 14, 'bold'))])

  main_layout = [[sg.Frame('', layout, background_color='#FFFFFF', element_justification='c')],]
  window = sg.Window('Selccionar Posición', main_layout)

  while True:
    event, values = window.read()
    # print('-'*50)
    # print(f'Eventos que suceden {event}')
    # print(f'Valores guardaros {values}')
    # print('-'*50 + '\n')


    if event in (sg.WINDOW_CLOSED, 'Cancel'):
      window.close()
      return (None,None)
    
    #* Seleccionar una casilla
    if isinstance(event, tuple):
      if not selected_flag:
        position = event
        selected_flag = True
        window[event].update(button_color='green')
      elif event == position:
        position = (None,None)
        selected_flag = False
        window[event].update(button_color='#FFFFFF')

    if event == 'Guardar' and selected_flag:
      # print(f'Salimos del Programa con la posición {position}')
      window.close()
      return position


def ventana_config():
  global main_config
  global position

  # * Variables base para configuración
  ICP = [0, 0, 3.7, 4.8, 0, 0]  # Individual Configuration Parameters
  PCP = [21.59, 27.94, 3.59, 4.65, 6, 6]  # Page Configuration Parameters

  page_conf_layout = [
    [
      sg.Radio(
        "Tamaño Carta",
        "O1",
        default=True,
        background_color="#FFFFFF",
        circle_color="#DEE6F7",
        font=("Open Sans", 14, "bold"),
        key="SHEET",
        enable_events=True,
        pad=((30, 20), (5, 8)),
      ),
    ],
    [sg.HorizontalSeparator(color="#000000")],
    [
      sg.Text(
        text="Ancho (cm)",
        size=(10, 1),
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF",
        justification="c",
        pad=((5, 5), (4, 4)),
      ),
      sg.Text(
        text="Alto (cm)",
        size=(10, 1),
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF",
        justification="c",
        pad=((5, 0), (4, 4)),
      ),
    ],
    [
      sg.In(
        size=(6, 1),
        default_text=main_config[0],
        font=("Open Sans", 12, "bold"),
        justification="center",
        enable_events=True,
        key="WP",
        pad=((25, 0), (0, 4)),
      ),
      sg.In(
        size=(6, 1),
        default_text=main_config[1],
        font=("Open Sans", 12, "bold"),
        justification="center",
        enable_events=True,
        key="HP",
        pad=((55, 0), (0, 4)),
      ),
    ],
    [
      sg.Text(
        text="Columnas",
        size=(8, 1),
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF",
        justification="c",
        pad=((10, 0), (4, 4)),
      ),
      sg.Text(
        text="Filas",
        size=(8, 1),
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF",
        justification="c",
        pad=((30, 0), (4, 4)),
      ),
    ],
    [
      sg.In(
        size=(4, 1),
        default_text=main_config[4],
        font=("Open Sans", 12, "bold"),
        justification="center",
        enable_events=True,
        key="COL",
        pad=((35, 0), (0, 4)),
      ),
      sg.In(
        size=(4, 1),
        default_text=main_config[5],
        font=("Open Sans", 12, "bold"),
        justification="center",
        enable_events=True,
        key="ROW",
        pad=((70, 0), (0, 4)),
      ),
    ],
  ]

  indi_conf_layout = [
    [
      sg.Radio(
        "Tamaño Individual",
        "O1",
        default=False,
        background_color="#FFFFFF",
        circle_color="#DEE6F7",
        font=("Open Sans", 14, "bold"),
        key="INDIV",
        enable_events=True,
        pad=((20, 30), (5, 8)),
      ),
    ],
    [sg.HorizontalSeparator(color="#000000")],
    [
      sg.Text(
        text="Ancho (cm)",
        size=(10, 1),
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF",
        justification="center",
        pad=((5, 5), (4, 4)),
      ),
      sg.Text(
        text="Alto (cm)",
        size=(10, 1),
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF",
        justification="center",
        pad=((0, 18), (4, 4)),
      ),
    ],
    [
      sg.In(
        size=(6, 1),
        default_text=main_config[2],
        font=("Open Sans", 12, "bold"),
        disabled=True,
        justification="center",
        key="WI",
        pad=((0, 45), (0, 4)),
      ),
      sg.In(
        size=(6, 1),
        default_text=main_config[3],
        font=("Open Sans", 12, "bold"),
        disabled=True,
        justification="center",
        key="HI",
        pad=((0, 45), (0, 4)),
      ),
    ],
    [
      sg.Radio(
        "Vertical",
        "O2",
        default=True,
        background_color="#FFFFFF",
        circle_color="#DEE6F7",
        font=("Open Sans", 12, "bold"),
        key="VERTICAL",
        disabled=True,
        enable_events=True,
        pad=((0, 25), (25, 0)),
      ),
      sg.Radio(
        "Horizontal",
        "O2",
        default=False,
        background_color="#FFFFFF",
        circle_color="#DEE6F7",
        font=("Open Sans", 12, "bold"),
        key="HORIZONTAL",
        disabled=True,
        enable_events=True,
        pad=((0, 25), (25, 0)),
      ),
    ],
  ]

  main_layout = [
    [
      sg.Text(
        text="Configuración Etiquetas",
        font=("Open Sans", 18, "bold", "italic"),
        background_color="#FFFFFF",
        justification="left",
        pad=(0, (15, 15)),
      ),
    ],
    [
      sg.Text(
        text="Seleccione una opción:",
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF",
        justification="left",
      )
    ],
    [
      sg.Column(
        page_conf_layout, background_color="#FFFFFF", element_justification="l"
      ),
      sg.Column(
        indi_conf_layout, background_color="#FFFFFF", element_justification="r"
      ),
    ],
    [
      sg.Button(
        "Reset",
        size=(6, 1),
        font=("Open Sans", 13, "bold"),
        key="RESET",
        pad=((10, 10), (22, 5)),
      ),
      sg.Button(
        "Aceptar",
        size=(8, 1),
        font=("Open Sans", 13, "bold"),
        key="ACCEPT",
        pad=((10, 10), (22, 5)),
      ),
    ],
  ]

  layout = [
    [
      sg.Frame(
        "", main_layout, background_color="#FFFFFF", element_justification="c"
      )
    ],
  ]

  window = sg.Window("Generador de Etiquetas", layout, element_justification="c", icon="Assets/ticket_icon.ico")

  while True:
    event, values = window.read()

    # print('-'*50)
    # print(f'Eventos que suceden {event}')
    # print(f'Valores guardaros {values}')
    # print('-'*50 + '\n')

    # * Cerrar la ventana
    if event in (sg.WINDOW_CLOSED, "Exit", "Salir"):
      window.close()
      return False

    # * Calculo de Etiqueta Individual
    if event in ("WP", "HP", "COL", "ROW"):
      try:
        cal_height = float(float(values["HP"]) / int(values["ROW"]))
        cal_width = float(float(values["WP"]) / int(values["COL"]))
        window["WI"].update(cal_width)
        window["HI"].update(cal_height)
      except:
        pass

    # * Seleccionar pagina
    if event == "SHEET":
      # Update Values
      window["WP"].update(PCP[0], disabled=False)
      window["HP"].update(PCP[1], disabled=False)
      window["COL"].update(PCP[4], disabled=False)
      window["ROW"].update(PCP[5], disabled=False)

      # Disable Individual Values
      window["WI"].update(PCP[2], disabled=True)
      window["HI"].update(PCP[3], disabled=True)
      window["HORIZONTAL"].update(disabled=True)
      window["VERTICAL"].update(disabled=True)

    # * Seleccionar Individual
    if event == "INDIV":
      # Update Values
      window["WI"].update(ICP[2], disabled=False)
      window["HI"].update(ICP[3], disabled=False)
      window["HORIZONTAL"].update(disabled=False)
      window["VERTICAL"].update(disabled=False)

      # Disable Page Values
      window["WP"].update(ICP[0], disabled=True)
      window["HP"].update(ICP[1], disabled=True)
      window["COL"].update(ICP[4], disabled=True)
      window["ROW"].update(ICP[5], disabled=True)

    # * Valores Default
    if event == "RESET":
      if values["SHEET"] == True:
        window["WP"].update(PCP[0])
        window["HP"].update(PCP[1])
        window["WI"].update(PCP[2])
        window["HI"].update(PCP[3])
        window["COL"].update(PCP[4])
        window["ROW"].update(PCP[5])
      else:
        window["WP"].update(ICP[0])
        window["HP"].update(ICP[1])
        window["WI"].update(ICP[2])
        window["HI"].update(ICP[3])
        window["COL"].update(ICP[4])
        window["ROW"].update(ICP[5])

    # * Mandar Valores de configuración
    if event == "ACCEPT":
      main_config[0] = values["WP"]
      main_config[1] = values["HP"]
      main_config[2] = values["WI"]
      main_config[3] = values["HI"]
      main_config[4] = values["COL"]
      main_config[5] = values["ROW"]
      main_config[6] = values["SHEET"]
      if values["SHEET"]:
        position = select_initialposition(
          int(values["ROW"]), int(values["COL"])
        )
        if position != (None, None):
          window.close()
          return True
        else:
          window.close()
          return False

      else:
        if values["HORIZONTAL"]:
          main_config[3] = values["WI"]
          main_config[2] = values["HI"]
          window.close()
          return True
        else:
          window.close()
          return True

def prueba_ventana_modificacion():
  prueba = ['BF109.78.J89C791 V.2 C.1', 'BF109.J89C791', 'V.2', '1', '']
  cosa1, cosa2 = ventana_modificar_clasificacion(prueba[0], prueba[1], prueba[2], prueba[3], prueba[4])
  print(cosa1)
  print(cosa2)



if __name__ == "__main__":
  # prueba_ventana_modificacion()
  print(seleccionar_posicion_impresion(8,6))
  pass
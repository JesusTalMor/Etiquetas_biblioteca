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


def seleccionar_posicion_impresion(num_row:int, num_column:int) -> tuple:
  '''Selecciona la posición inicial de impresion en hoja carta'''
  position = (None,None)
  selected_flag = False

  layout = [[sg.Text(text='Seleccione un casilla', font=("Open Sans", 16, "bold", "italic"), background_color='#FFFFFF')]]
  # * Añadimos casillas para de selección
  for row in range(num_row):
    new_row = []
    for column in range(num_column):
      new_row.append(sg.Button(size=(2,2), key=(row, column)))
    layout.append(new_row)
  layout.append([sg.Button('Guardar', font=("Open Sans", 14, 'bold'))])

  main_layout = [[sg.Frame('', layout, background_color='#FFFFFF', element_justification='c')],]
  window = sg.Window('Selccionar Posición', main_layout, icon='Assets/ticket_icon.ico')

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


def ventana_config(main_config = {}) -> (tuple):
  '''
  Establece la configuracion para impresion de etiquetas
  Retorna una tupla con un status, configuración y Posición
  '''

  # * Variables base de ventana configuración
  ICP = {'PW':0, 'PH':0, 'TW':4.8, 'TH':3.7, 'PR':0, 'PC':0}  # Individual Configuration Parameters
  PCP = {'PW':21.59, 'PH':27.94, 'TW':2.69, 'TH':4.65, 'PR':6, 'PC':8} # Page Configuration Parameters

  # * Revisa si el diccionario esta vacio para asignarle valores por defecto
  main_config = PCP if not any(main_config) else main_config

  page_conf_layout = [
    [
      sg.Radio(
        "Tamaño Carta", "O1",
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
        size=(10, 1), font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF", justification="c",
        pad=((5, 5), (4, 4)),
      ),
      sg.Text(
        text="Alto (cm)",
        size=(10, 1), font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF", justification="c",
        pad=((5, 0), (4, 4)),
      ),
    ],
    [
      sg.In(
        size=(6, 1),
        default_text=main_config['PW'],
        font=("Open Sans", 12, "bold"),
        justification="center", enable_events=True,
        key="WP", pad=((25, 0), (0, 4)),
      ),
      sg.In(
        size=(6, 1),
        default_text=main_config['PH'],
        font=("Open Sans", 12, "bold"),
        justification="center", enable_events=True,
        key="HP", pad=((55, 0), (0, 4)),
      ),
    ],
    [
      sg.Text(
        text="Columnas", size=(8, 1),
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF", justification="c",
        pad=((10, 0), (4, 4)),
      ),
      sg.Text(
        text="Filas", size=(8, 1),
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF", justification="c",
        pad=((30, 0), (4, 4)),
      ),
    ],
    [
      sg.In(
        size=(4, 1),
        default_text=main_config['PC'],
        font=("Open Sans", 12, "bold"),
        justification="center",
        enable_events=True,
        key="COL",
        pad=((35, 0), (0, 4)),
      ),
      sg.In(
        size=(4, 1),
        default_text=main_config['PR'],
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
        "Tamaño Individual", "O1",
        default=False, background_color="#FFFFFF",
        circle_color="#DEE6F7", font=("Open Sans", 14, "bold"),
        key="INDIV", enable_events=True,
        pad=((20, 30), (5, 8)),
      ),
    ],
    [sg.HorizontalSeparator(color="#000000")],
    [
      sg.Text(
        text="Ancho (cm)",
        size=(10, 1), font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF", justification="center",
        pad=((5, 5), (4, 4)),
      ),
      sg.Text(
        text="Alto (cm)", size=(10, 1),
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF", justification="center",
        pad=((0, 18), (4, 4)),
      ),
    ],
    [
      sg.In(
        size=(6, 1),
        default_text=main_config['TW'],
        font=("Open Sans", 12, "bold"),
        disabled=True, justification="center",
        key="WI", pad=((0, 45), (0, 4)),
      ),
      sg.In(
        size=(6, 1),
        default_text=main_config['TH'],
        font=("Open Sans", 12, "bold"),
        disabled=True, justification="center",
        key="HI", pad=((0, 45), (0, 4)),
      ),
    ],
    [
      sg.Radio(
        "Vertical", "O2",
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
        "Horizontal", "O2",
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
        background_color="#FFFFFF", justification="left",
        pad=(0, (15, 15)),
      ),
    ],
    [
      sg.Text(
        text="Seleccione una opción:",
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF", justification="left",
      )
    ],
    [
      sg.Column(page_conf_layout, background_color="#FFFFFF", element_justification="l"),
      sg.Column(indi_conf_layout, background_color="#FFFFFF", element_justification="r"),
    ],
    [
      sg.Button(
        "Reset", size=(6, 1),
        font=("Open Sans", 13, "bold"),
        key="RESET", pad=((10, 10), (22, 5)),
      ),
      sg.Button(
        "Aceptar", size=(8, 1),
        font=("Open Sans", 13, "bold"),
        key="ACCEPT", pad=((10, 10), (22, 5)),
      ),
    ],
  ]

  layout = [[sg.Frame("", main_layout, background_color="#FFFFFF", element_justification="c")],]
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
      return False, main_config, (None,None)

    #* Calcular Tamaño etiqueta individual
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
      window["WP"].update(PCP["PW"], disabled=False)
      window["HP"].update(PCP["PH"], disabled=False)
      window["COL"].update(PCP["PC"], disabled=False)
      window["ROW"].update(PCP["PR"], disabled=False)

      # Disable Individual Values
      window["WI"].update(PCP["TW"], disabled=True)
      window["HI"].update(PCP["TH"], disabled=True)
      window["HORIZONTAL"].update(disabled=True)
      window["VERTICAL"].update(disabled=True)

    # * Seleccionar Individual
    if event == "INDIV":
      # Update Values
      window["WI"].update(ICP["TW"], disabled=False)
      window["HI"].update(ICP["TH"], disabled=False)
      window["HORIZONTAL"].update(disabled=False)
      window["VERTICAL"].update(disabled=False)

      # Disable Page Values
      window["WP"].update(ICP["PW"], disabled=True)
      window["HP"].update(ICP["PH"], disabled=True)
      window["COL"].update(ICP["PC"], disabled=True)
      window["ROW"].update(ICP["PR"], disabled=True)

    # * Valores Default
    if event == "RESET":
      if values["SHEET"]: temp = PCP
      else: temp = ICP
      window["WP"].update(temp["PW"])
      window["HP"].update(temp["PH"])
      window["WI"].update(temp["TW"])
      window["HI"].update(temp["TH"])
      window["COL"].update(temp["PC"])
      window["ROW"].update(temp["PR"])

    # * Mandar Valores de configuración
    if event == "ACCEPT":
      main_config["PW"], main_config["PH"] = values['WP'], values['HP']
      main_config["TW"], main_config["TH"] = values['WI'], values['HI']
      main_config["PC"], main_config["PR"] = values['COL'], values['ROW']

      #* Valores para etiqueta individual
      window.close()
      if values['INDIV']: return True, main_config, (None, None)
      #* Valores para configuración de Página
      coordenadas = seleccionar_posicion_impresion(num_row=int(main_config['PR']), num_column=int(main_config["PC"])) 
      if coordenadas[0] == None: return False, main_config, coordenadas
      else: return True, main_config, coordenadas


  # prueba_ventana_seleccion()
  prueba_configuracion()

if __name__ == "__main__":
  pass
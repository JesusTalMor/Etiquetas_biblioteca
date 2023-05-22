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
  while True:
    event, values = window.read()
    

    # * Valores Default
    if event == "RESET":

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
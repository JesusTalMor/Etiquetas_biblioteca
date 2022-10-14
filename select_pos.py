import PySimpleGUI as sg

#* Tema principal de las ventanas
sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {
  'BACKGROUND': '#3016F3',
  'TEXT': '#000000',
  'INPUT': '#DEE6F7',
  'TEXT_INPUT': '#000000',
  'SCROLL': '#DEE6F7',
  'BUTTON': ('#000000', '#FFFFFF'),
  'PROGRESS': ('#DEE6F7', '#DEE6F7'),
  'BORDER': 2, 'SLIDER_DEPTH': 0,
  'PROGRESS_DEPTH': 0,
}
sg.theme('MyCreatedTheme')

def select_initialposition(num_row, num_column):
  position = (None,None)
  selected_flag = False

  layout = [[sg.Text(text='Seleccione un casilla', font=("Open Sans", 16, "bold", "italic"), background_color='#FFFFFF')]]
  for row in range(num_row):
    new_row = []
    for column in range(num_column):
      new_row.append(sg.Button(size=(3,2), key=(row, column)))
    layout.append(new_row)

  layout.append([sg.Button('Guardar', font=("Open Sans", 14, 'bold'))])

  main_layout = [[sg.Frame('', layout, background_color='#FFFFFF', element_justification='c')],]

  window = sg.Window('Seleccionar Pos', main_layout)

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

  
if __name__ == '__main__':
  select_initialposition(6, 6)



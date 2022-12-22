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
# TODO Agregar que acepte otros parametros para mejor funcionamiento
def ventana_modificar_clasificacion(clasificacion_completa:str, clasif:str, volumen:str, copia:int, encabezado:str):
  bandera_agregar = False
  # TODO actualizar el Volumen a standard
  if 'V.' in volumen: 
    posicion_auxiliar = volumen.index('V.')
    volumen = volumen[posicion_auxiliar + 2]
  else: volumen = ''

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
            volumen = str(values['VOL'])
            copia = str(values['COP'])
            encabezado = str(values['HEAD'])

            volumen = 'V.' + volumen if volumen not in ('', '0') else ''
            clasificacion_completa = sh.creador_clasificacion(clasif, volumen, copia)
            window['TEXT'].update(encabezado + ' ' + clasificacion_completa)
            bandera_agregar = True  # ? Bandera Verdadera
        else:
          window["PIPE_A"].update("NO")
          window["PIPE_B"].update("APLICA")
          bandera_agregar = False  # ? Bandera Falsa
    
    # * Modificar Volumen
    elif event == 'VOL':
      clasif = str(values["CLAS"])
      volumen = str(values['VOL'])
      copia = str(values['COP'])
      encabezado = str(values['HEAD'])

      volumen = 'V.' + volumen if volumen not in ('', '0') else ''
      clasificacion_completa = sh.creador_clasificacion(clasif, volumen, copia)
      window['TEXT'].update(encabezado + ' ' + clasificacion_completa)
    
    # * Modificar Copia
    elif event == 'COP':
      clasif = str(values["CLAS"])
      volumen = str(values['VOL'])
      copia = str(values['COP'])
      encabezado = str(values['HEAD'])

      volumen = 'V.' + volumen if volumen not in ('', '0') else ''
      clasificacion_completa = sh.creador_clasificacion(clasif, volumen, copia)
      window['TEXT'].update(encabezado + ' ' + clasificacion_completa)
    
    # * Modificar Encabezado
    elif event == 'HEAD':
      clasif = str(values["CLAS"])
      volumen = str(values['VOL'])
      copia = str(values['COP'])
      encabezado = str(values['HEAD'])

      volumen = 'V.' + volumen if volumen not in ('', '0') else ''
      clasificacion_completa = sh.creador_clasificacion(clasif, volumen, copia)
      window['TEXT'].update(encabezado+ ' ' + clasificacion_completa)

    # * Modifica la etiqueta y cierra la ventana
    elif event == "Modificar" and bandera_agregar:
      clasif = str(values["CLAS"])
      volumen = str(values['VOL'])
      copia = str(values['COP'])
      encabezado = str(values['HEAD'])

      volumen = 'V.' + volumen if volumen not in ('', '0') else ''
      clasificacion_completa = encabezado + ' ' + sh.creador_clasificacion(clasif, volumen, copia)

      window.close()
      return [clasificacion_completa, values["PIPE_A"], values["PIPE_B"], "True"], [clasif, volumen, copia, encabezado]
  window.close()
  return [False],[False]


if __name__ == "__main__":
  prueba = ['BF109.78.J89 .C791 2015 V.2 C.1', 'BF109.78.J89 .C791 2015', 'V.2', '1', '']
  cosa1, cosa2 = ventana_modificar_clasificacion(prueba[0], prueba[1], prueba[2], prueba[3], prueba[4])
  print(cosa1)
  print(cosa2)
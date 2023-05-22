def ventana_elemento():
  """
    Esta ventana se puede agregar individualmente Claificaciones para su impresión
  """
  # ? Declaración de variables para uso global
  global ruta_archivo
  global ruta_folder

  global tabla_principal
  global row_color_array
  global main_dicc

  global tabla_modify
  global tabla_datos

  global valores_config
  global coordenadas

  # ? Bandera para agregar una nueva clasificación
  bandera_agregar = False

  # ? Variables para manejo de modificacion
  modify_flag = False
  modify_index = 0
  modify_status = ""




  while True:
    event, values = window.read()


    # * Dar ruta para guardar el archivo DONE
    if event == "FOLDER": ruta_folder = values["FOLDER"]

    # * Mostrar licencia
    if event == "Licencia":pop.info_license()

    # * Mostrar Acerca de
    if event == "Acerca de...":pop.info_about(VERSION)

    # * Abrir ventana de configuración
    if event == "Configuración": 
      flag, temp_valores_config, temp_coordenadas = sw.ventana_config(valores_config)
      valores_config = temp_valores_config if flag else valores_config
      coordenadas = temp_coordenadas if flag else coordenadas


    #* Modificar un elemento de la tabla
    if event == "Modificar" and modify_flag == True:

    # * Exporta los elementos seleccionados a impresión
    if event == "Exportar":
      # * Revisamos que exista una ruta de folder
      if ruta_folder == "":
        pop.warning_folder()
        continue
      
      etiquetas_a_imprimir = []  # Lista con elementos seleccionados

      # * LLenado de lista de elementos seleccionados
      for ind in range(len(tabla_principal)):
        status = main_dicc[ind]
        if status == "Selected":
          # Crear la lista de datos
          encabezado = tabla_datos[ind]['encabeza']
          clasif = tabla_datos[ind]['clasif']
          volumen = tabla_datos[ind]['volumen']
          copia = tabla_datos[ind]['copia']

          dict_format = {'HEAD':encabezado, 'CLASS':clasif, 'VOL':volumen, 'COP':copia}
          etiquetas_a_imprimir.append(dict_format)

      # * Revisar que la tabla de seleccionado tenga valores para poder continuar
      if len(etiquetas_a_imprimir) == 0: 
        pop.warning_select()
        continue
      
      #* Pasamos a la ventana de configuración
      estatus_config, valores_config, coordenadas = sw.ventana_config(valores_config)  
      #? Esta ventana retorna un True o False dependiendo si se modifico la configuración o no
      #? Retorna los valores
      #? Coordenadas si son necesarias
      
      #* Revisar estatus de configuración
      # True continua con el proceso, False termian el proceso
      if not estatus_config: continue
      
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

  window.close()


# * Ventana para cargar archivo
def ventana_archivo():
  # ? Declaración de variables para uso
  global ruta_archivo
  global ruta_folder

  global tabla_principal
  global row_color_array
  global main_dicc

  global tabla_modify
  global tabla_datos

  global valores_config
  global coordenadas

  # ? Variables para manejo de modificacion
  modify_flag = False
  modify_index = 0
  modify_status = ""

  # * Layout para cargar archivo de Excel
  excel_layout = [
    [
      sg.FileBrowse("Abrir", font=("Open Sans", 12)),
      sg.In(
        default_text=ruta_archivo, size=(50, 1), 
        key="EXCEL_FILE", font=("Open Sans", 9), 
        justification="center",
      ),
    ],
  ]

  layout_izq = [
    [sg.Image(filename="Assets/LogoTecResize.png", background_color="#FFFFFF")],
    [sg.Text(text="Generador de Etiquetas", font=("Open Sans", 20, "bold", "italic"), background_color="#FFFFFF", justification="left", pad=(0, (0, 20)),)],
    [sg.Text(text="Seleccione una opción:", font=("Open Sans", 16, "bold"), background_color="#FFFFFF", justification="left",)],
    [
      sg.Radio(
        "Cargar Archivo", "O1", default=True,
        background_color="#FFFFFF",
        circle_color="#DEE6F7",
        font=("Open Sans", 14),
        key="FILE", enable_events=True,
      ),
      sg.Radio(
        "Cargar Elemento", "O1",
        default=False, background_color="#FFFFFF",
        circle_color="#DEE6F7",
        font=("Open Sans", 14),
        key="ELEM", enable_events=True,
      ),
    ],
    [sg.HorizontalSeparator(color="#000000", pad=(0, (40, 30)))],
    [sg.Frame("", layout=excel_layout, background_color="#FFFFFF", element_justification="r", )],
    [sg.HorizontalSeparator(color="#000000", pad=(0, (30, 40)))],
    [
      sg.FolderBrowse("Guardar", font=("Open Sans", 12), pad=(5, (0, 15))),
      sg.In(default_text=ruta_folder, size=(50, 1), enable_events=True, key="FOLDER",font=("Open Sans", 9), justification="center", pad=(5, (0, 10)),),
    ],
    [sg.Button("Cargar", font=("Open Sans", 12, "bold"))],
  ]
  # * Layout tabla general de etiquetas,
  layout_der = [
    [sg.Text(text="Lista de Clasificaciones a Imprimir", background_color="#FFFFFF", font=("Open", 16, "bold", "italic"),)],
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
      sg.Button("Seleccionar Todo", font=("Open Sans", 12), pad=((0), 10), key="SELECT-ALL",),
      sg.Button("Limpiar", font=("Open Sans", 12), pad=(30, 10)),
      sg.Button("Deseleccionar", font=("Open Sans", 12), pad=((0, 0), 10), key="DESELECT-ALL",),
    ],
    [sg.Button("Exportar", font=("Open Sans", 12, "bold"))],
  ]

  # * Despliegue General del layout
  layout = [
    [sg.Menu(menu_opciones, tearoff=False)],
    [
      sg.Column(layout_izq, background_color="#FFFFFF", element_justification="c", pad=0 ),
      sg.VerticalSeparator(color="#000000", pad=(5, 0)),
      sg.Column( layout_der, background_color="#FFFFFF", element_justification="c", pad=0 ),
    ],
  ]

  # * Creacion de la ventana
  window = sg.Window("Generador de Etiquetas", layout, element_justification="c", icon="Assets/ticket_icon.ico")

  while True:
    event, values = window.read()

    # print('-'*50)
    # print(f'Eventos que suceden {event}')
    # print(f'Valores guardaros {values}')
    # print('-'*50 + '\n')

    # * Cerrar ventana
    if event in (sg.WINDOW_CLOSED, "Exit", "Salir"): break

    #  * Cambio de ventana a elemento
    if event == "ELEM":
      window.close()
      ventana_elemento()

    # * Cargar Etiquetas de un Excel
    if event == "Cargar":
      #* Ruta del Archivo
      ruta_archivo = values["EXCEL_FILE"]  

      # Revisar si se tiene un archivo
      if len(ruta_archivo) == 0:
        pop.warning_excel_file()
        continue
      
      #* Vamos a cargar toda la información del excel de una
      # Sacar el dataframe del excel
      dataframe = maintf.cargar_excel(ruta_archivo)
      # Sacar las hojas del excel
      hojas_excel = list(dataframe)
      # Bluce para sacar la información de todo el documento
      for hoja in hojas_excel:
        #* Sacar todos los datos de los libros del excel
        temp_etiquetas = maintf.generar_etiquetas_libros(dataframe[hoja])  
        temp_infomacion = maintf.generar_informacion_libros(dataframe[hoja])  

        # ? Se cargaron etiquetas ?
        if not temp_etiquetas[0]: 
          print(f'Etiquetas no cargadas para hoja {hoja}')
          continue

        # * Generamos la tabla de datos para el Excel
        for ind in range(len(temp_etiquetas)):
          status = temp_etiquetas[ind][3]
          main_dicc[len(tabla_principal) + ind] = status
          row = ((len(tabla_principal) + ind), "#F04150") if status == 'False' else ((len(tabla_principal) + ind), "#FFFFFF")
          row_color_array.append(row)
      
        # * Concatenamos los nuevos datos a los antiguos
        if len(tabla_principal) != 0:
          tabla_principal = np.concatenate((np.array(tabla_principal), np.array(temp_etiquetas)), axis=0)
          tabla_principal = tabla_principal.tolist()

          tabla_datos = np.concatenate((np.array(tabla_datos), np.array(temp_infomacion)), axis=0)
          tabla_datos = tabla_datos.tolist()
        # * No tenemos aun datos en la tabla 
        else: 
          tabla_principal = temp_etiquetas
          tabla_datos = temp_infomacion

        window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)

    # * Limpiar Tabla por completo
    if event == "Limpiar":
      # Pasamos a datos por defecto
      tabla_principal = []
      row_color_array = []
      tabla_datos = []
      main_dicc = {}
      modify_flag = False

      window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)

    # * Seleccionar toda la tabla
    if event == "SELECT-ALL":
      modify_flag = False
      for x in range(len(tabla_principal)):
        status = main_dicc[x]
        if status != "False":
          main_dicc[x] = "Selected"
          tabla_principal[x][3] = "Selected"
          row_color_array[x] = (int(x), "#498C8A")
      window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)

    # * Des Seleccionar toda la tabla
    if event == "DESELECT-ALL":
      modify_flag = False
      for x in range(len(tabla_principal)):
        status = main_dicc[x]
        if status != "False":
          main_dicc[x] = "True"
          tabla_principal[x][3] = "True"
          row_color_array[x] = (int(x), "#FFFFFF")
      window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)

    # * Dar ruta para guardar el archivo
    if event == "FOLDER": ruta_folder = values["FOLDER"]

    # * Mostrar licencia
    if event == "Licencia": pop.info_license()

    # * Mostrar Acerca de
    if event == "Acerca de...": pop.info_about(version)

    # * Abrir ventana de configuración
    if event == "Configuración": 
      flag, temp_valores_config, temp_coordenadas = sw.ventana_config(valores_config)
      valores_config = temp_valores_config if flag else valores_config
      coordenadas = temp_coordenadas if flag else coordenadas

    # * Eventos dentro de la tabla
    if event == "TABLE":
      if values["TABLE"] != []:
        index_value = int(values["TABLE"][0])  # * elemento a seleccionar
        status = main_dicc[index_value]  # * Revisar el status del elemento

        # * Seleccionar una casilla valida
        if status == "True":
          # Cambias el estatus de ese elemento a seleccionado
          main_dicc[index_value] = "Selected"
          tabla_principal[index_value][3] = "Selected"
          row_color_array[index_value] = (int(index_value), "#498C8A")

        # * Seleccionar casilla para modfiicar
        elif status in ("Selected", "False") and not modify_flag:
          # Tomar datos de la casilla
          modify_status = status
          modify_flag = True
          modify_index = index_value
          # Modificar casilla visualmente
          main_dicc[index_value] = "Modify"
          tabla_principal[index_value][3] = "Modify"
          row_color_array[index_value] = (int(index_value), "#E8871E")

        # * Quitar casilla de modificar
        elif status == "Modify":
          if modify_status == "Selected":
            main_dicc[index_value] = "True"
            tabla_principal[index_value][3] = "True"
            row_color_array[index_value] = (int(index_value), "#FFFFFF")
          elif modify_status == "False":
            main_dicc[index_value] = "False"
            tabla_principal[index_value][3] = "False"
            row_color_array[index_value] = (int(index_value), "#F04150")
          modify_flag = False

        # * Regresar casilla a normalidad
        elif status == "Selected" and modify_flag:
          main_dicc[index_value] = "True"
          tabla_principal[index_value][3] = "True"
          row_color_array[index_value] = (int(index_value), "#FFFFFF")

      window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)

    # * Modificar un elemento de la tabla
    if event == "Modificar" and modify_flag == True:
      # * Vamos a abrir una nueva pantalla para modificar el texto
      modif_principal, modif_datos = sw.ventana_modificar_clasificacion(
        clasificacion_completa= tabla_principal[modify_index][0], dicc_info=tabla_datos[modify_index])

      #* Checar si hubieron cambios
      if not modif_principal[0]: continue # Se checa si se realizaron cambios
      
      # * Agregamos elemento a una tabla de modificaciones
      title = tabla_datos[modify_index]['titulo']
      cbarras = tabla_datos[modify_index]['cbarras']
      aux_modify = [title, cbarras, tabla_principal[modify_index][0], modif_principal[0]]
      tabla_modify.append(aux_modify)

      # * Cambiamos la apariencia del elemento en la tabla
      main_dicc[modify_index] = "True"
      tabla_principal[modify_index] = modif_principal
      row_color_array[modify_index] = (int(modify_index), "#D8D8D8")
      modify_flag = False

      # * Actualizar valores de tabla de datos
      tabla_datos[modify_index]['clasif'] = modif_datos[0]
      tabla_datos[modify_index]['volumen'] = modif_datos[1]
      tabla_datos[modify_index]['copia'] = modif_datos[2]
      tabla_datos[modify_index]['encabeza'] = modif_datos[3]

      window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)
    
    # * Exporta los elementos seleccionados a impresión
    if event == "Exportar":
      # * Revisamos que exista una ruta de folder
      if ruta_folder == "":
        pop.warning_folder()
        continue
      
      etiquetas_a_imprimir = []  # Lista con elementos seleccionados

      # * LLenado de lista de elementos seleccionados
      for ind in range(len(tabla_principal)):
        status = main_dicc[ind]
        if status != "Selected": continue
        
        #* Crear la lista de datos
        encabezado = tabla_datos[ind]['encabeza']
        clasif = tabla_datos[ind]['clasif']
        volumen = tabla_datos[ind]['volumen']
        copia = tabla_datos[ind]['copia']

        dict_format = {'HEAD':encabezado, 'CLASS':clasif, 'VOL':volumen, 'COP':copia}
        etiquetas_a_imprimir.append(dict_format)

      # * Revisar que la tabla de seleccionado tenga valores para poder continuar
      if len(etiquetas_a_imprimir) == 0: 
        pop.warning_select()
        continue
      
      #* Pasamos a la ventana de configuración
      estatus_config, valores_config, coordenadas = sw.ventana_config(valores_config)  
      #? Esta ventana retorna un True o False dependiendo si se modifico la configuración o no
      #? Retorna los valores
      #? Coordenadas si son necesarias
      
      #* Revisar estatus de configuración
      # True continua con el proceso, False termian el proceso
      if not estatus_config: continue
      
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

  window.close()



def ventana_inicial():
  ''' Ventana principal, de inicio del programa'''
  layout_incial = [
    [sg.Image(filename="Assets/LogoTecResize.png", background_color="#FFFFFF")],
    [
      sg.Text(
        text="Generador de Etiquetas",
        font=("Open Sans", 20, "bold", "italic"),
        background_color="#FFFFFF", justification="left", pad=(0, (0, 15)),
      )
    ],
    [
      sg.Text(
        text="Seleccione una opción:",
        font=("Open Sans", 18, "bold"), 
        background_color="#FFFFFF", justification="center",
      )
    ],
    [
      sg.Radio(
        "Cargar Archivo",
        "O1",
        default=False, background_color="#FFFFFF",
        circle_color="#DEE6F7", font=("Open Sans", 16),
        key="FILE", enable_events=True,
      ),
      sg.Radio(
        "Cargar Elemento",
        "O1",
        default=False, background_color="#FFFFFF",
        circle_color="#DEE6F7", font=("Open Sans", 16),
        key="ELEM", enable_events=True,
      ),
    ],
  ]

  layout = [[sg.Frame("",layout_incial, background_color="#FFFFFF", element_justification="c",)],]
  window = sg.Window("Generador de Etiquetas", layout, element_justification="c", icon="Assets/ticket_icon.ico")

  while True:
    event, values = window.read()

    # print('-'*50)
    # print(f'Eventos que suceden {event}')
    # print(f'Valores guardaros {values}')
    # print('-'*50 + '\n')

    if event in (sg.WINDOW_CLOSED, "Exit", "Salir"):
      break
    if event == "FILE":
      window.close()
      ventana_archivo()
    if event == "ELEM":
      window.close()
      ventana_elemento()

  # * Finalizamos el programa
  window.close()


if __name__ == "__main__":
  ventana_inicial()
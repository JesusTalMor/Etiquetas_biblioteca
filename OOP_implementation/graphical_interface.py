#############################################################
# Editor: Jesus Talamantes Morales
# Fecha Trabajo: 30 de Mayo 2023
# Versión: 0.4.3
# Implementacion utilizando OOP
#
#
#
#


#?#********** VARIABLES CONTROL DE VERSIONES **********#
ALPHA = 0
FUNCIONALIDAD = 6
BUGS = 7
VERSION = f'{ALPHA}.{FUNCIONALIDAD}.{BUGS}'

#?#********** IMPORTAR MODULOS **********#
import os
import sys
from datetime import datetime

import PySimpleGUI as sg

import pop_ups as pop
import string_helper as sh
from string_helper import creador_clasificacion
from support_windows import (VentanaConfiguracion, VentanaModificar,
                             VentanaSeleccionarPosicion)
from table_manager import ExcelManager, TableManager
from ticket_maker import TicketMaker

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




class VentanaGeneral:
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
  def __init__(self) -> None:
    self.ruta_archivo = ''
    self.ruta_folder = ''
    self.table_manager = TableManager()
    self.excel_manager = ExcelManager()

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

  def create_col_izq_indi(self):
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
      [
        sg.Input(key="FOLDER", visible=False),
        sg.FolderBrowse("Guardar", target='FOLDER', visible=False),
      ],
    ]
    return GENERAL_LAYOUT
  
  def create_col_izq_file(self):
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
        sg.Radio("Cargar Archivo", "O1", default=True, key="FILE", **radio_format),
        sg.Radio("Cargar Elemento", "O1", default=False, key="ELEM", **radio_format),
      ],    
    ]
    #?#********* LAYOUT PARA SELECCIONAR eL ARCHIVO DE EXCEL #?#*********
    text_format = {
      'font':("Open Sans", 14, "italic"), 
      'background_color':"#FFFFFF",
      'justification':"c",
    }
    ruta_excel = "Sin Archivo" if self.ruta_archivo == "" else self.ruta_archivo.split("/")[-1]    
    SELECCIONAR_ARCHIVO = [
      [
        sg.Button(
          image_source=resource_path('Assets/subir_icon.png'), image_subsample=5, 
          border_width=0, key='UPLOAD'
        )
      ],
      [sg.Text(text=ruta_excel, key="EXCEL_TEXT", **text_format)],
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
      [sg.Frame("",layout=SELECCIONAR_ARCHIVO, border_width=0, **frame_format)],
      [sg.HSep(pad=(0, (5,30)))],
      [sg.Button("Cargar", font=("Open Sans", 14, 'bold'))],
      [
        sg.Input(key="FOLDER", visible=False),
        sg.FolderBrowse("Guardar", target='FOLDER', visible=False),
      ],
      [
        sg.In(key="EXCEL_FILE", visible=False),
        sg.FileBrowse("Abrir", target='EXCEL_FILE',visible=False, file_types=(("Excel Files", "*.xlsx"),)),
      ],
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

  def create_layout(self, formato = "FILE"):
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
    COL_IZQ_LAYOUT = self.create_col_izq_file() if formato == "FILE" else self.create_col_izq_indi()
    COL_DER_LAYOUT = self.create_col_der()
    LAYOUT = [
      [
        sg.Column(COL_IZQ_LAYOUT, **colum_format),
        sg.VSep(pad=(5, 0)),
        sg.Column(COL_DER_LAYOUT, **colum_format),
      ],
    ]
    return LAYOUT

  def create_window(self, formato = "FILE"):
    """ Genera un Objeto tipo Ventana de PySimpleGUI """
    LAYOUT = self.create_layout(formato)
    MAIN_LAYOUT = [
      #* Menu superior de la APP
      [sg.Menu(menu_opciones, tearoff=False)],
      [sg.Frame("",layout=LAYOUT, background_color='#FFFFFF', element_justification='c')],
    ]
    
    window = sg.Window(self.titulo_ventana, MAIN_LAYOUT, element_justification="c", icon=resource_path("Assets/ticket_icon.ico"))  
    return window

  def run_window(self, window):
    #?#********** MANEJO DE VARIABLES #?#**********
    bandera_agregar = False
    bandera_modificar = False
    index_modificar = 0
    estatus_modificar = 'K'
    #?#**********  LOOP PRINCIPAL#?#**********
    while True:
      event, values = window.read()
      self.show_window_events(event, values)
      #* Cerrar la aplicación
      if event in (sg.WINDOW_CLOSED, "Exit", "__TIMEOUT__"):
        window.close()
        return "TRUE"
      #* Cambio de Ventana a ARCHIVO
      elif event == "FILE":
        window.close()
        return "FILE"
      #* Cambio de Ventana a INDIVIDUAL
      elif event == "ELEM":
        window.close()
        return "ELEM"
      #?#********** FUNCIONALIDAD ARCHIVO **********#?#
      elif event == "UPLOAD":
        window["Abrir"].click()
        self.ruta_archivo = window['EXCEL_FILE'].get()
        nombre_archivo = self.ruta_archivo.split('/')[-1]
        window["EXCEL_TEXT"].update(nombre_archivo)
      elif event == "Cargar":
        self.cargar_excel(window)
      
      #?#********** FUNCIONALIDAD INDIVIDUAL **********#?#      
      #* Revisar una clasificación
      elif event in ("CLAS", 'VOL', 'COP', 'HEAD'):
        bandera_agregar = self.checar_clasificacion(window, values)
      #* Añadir una clasificación a la tabla 
      elif event == "Agregar" and bandera_agregar:
        self.agregar_clasificacion(window, values)
        bandera_agregar = False
      
      #?#********** FUNCIONALIDAD DE TABLA **********#?#
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
      elif event == 'EXPORTAR':
        self.exportar_etiquetas(window)


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
    
    volumen = 'V.' + volumen if volumen not in (' ', '0') else ' '

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
    del VM
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
    print(aux_tabla_datos)
    self.table_manager.set_data_element(modify_index, aux_tabla_datos)

    #* Actualizar valores de tabla principal
    self.table_manager.set_element(modify_index, aux_principal)
    
    #* Actualizar apariencia de la tabla
    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.tabla_formato
    )

    return False

  def exportar_etiquetas(self, window):
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
    VC = VentanaConfiguracion()
    estatus, configuracion = VC.run_window()
    del VC
    # * Revisar que tengamos configuraciones
    if estatus is False: return False

    # * Checar si se uso el formato de pagina
    position = False
    if int(configuracion['COL']) != 0: 
      # * Formato de pagina
      VSP = VentanaSeleccionarPosicion(int(configuracion['ROW']),int(configuracion['COL']))
      position = VSP.run_window()
      del VSP
      if position is False: return False

    # * Pedir Folder para guardar
    window['Guardar'].click()
    ruta = window['FOLDER'].get()
    if len(ruta) == 0: return False
    today_date = datetime.now().strftime("%d_%m_%Y_%H%M%S") # Chequeo de hora de consulta

    # ? Función para el manejo y creación de eiquetas
    try:
      TM = TicketMaker(etiquetas_a_imprimir, today_date, ruta, configuracion, position)
      if position is False: TM.crear_base_datos_etiquetas()
      else: TM.imprimir_paginas()
    except:
      return False
    # Generamos un reporte de modificaciones
    self.table_manager.crear_reporte_modificados(ruta, today_date)
    self.table_manager.crear_reporte_QRO(ruta, today_date)
    pop.success_program()
    return True

  def cargar_excel(self, window):
    # Revisar que tengamos un archivo excel
    if len(self.ruta_archivo) == 0:
      pop.warning_excel_file()
      return False
    
    # * Cargar datos del Excel
    estatus = self.excel_manager.cargar_datos_excel(self.ruta_archivo, self.table_manager)
    if estatus is False: return False
    #* Actualizar apariencia de la tabla
    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.tabla_formato
    )


def main():
  """ Funcion principal para el manejo de la aplicacion """
  VG = VentanaGeneral()
  formato = "FILE"
  VG_window = VG.create_window(formato)
  while formato in ("FILE", "ELEM"):
    formato = VG.run_window(VG_window)
    VG_window = VG.create_window(formato)

def prueba():
  #* Pasamos a la ventana de configuración
  VC = VentanaConfiguracion()
  estatus, configuracion = VC.run_window()
  del VC
  # * Revisar que tengamos configuraciones
  if estatus is False: return False

  # * Checar si se uso el formato de pagina
  if int(configuracion['COL']) != 0: 
    # * Formato de pagina
    VSP = VentanaSeleccionarPosicion(int(configuracion['ROW']),int(configuracion['COL']))
    position = VSP.run_window()
    del VSP
    if position is False: return False

  return True
  


if __name__ == '__main__':
  main()
  # print(prueba())


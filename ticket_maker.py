import os

import PySimpleGUI as sg
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

import pop_ups as pop

# TODO Ajustar el encabezado 1 cm de margen, listo pero no me convence
# TODO Queda pendiente PNG o PDF - Dejar en PNG etiquetas individuales

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
# * Tipografia de la etiquetas
FONT_SIZE = 40
MAIN_FONT = ImageFont.truetype("Assets/Khmer OS Muol.otf", size=FONT_SIZE)
ESCALA = 100  #? Escala de la etiqueta recomendado 100
COLOR = "rgb(0, 0, 0)"

#? Tema principal tipo Tec para las ventanas
sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {
  'BACKGROUND': '#000000',
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



def max_len_list(lista: list) -> int:
  max_len = 0
  for texto in lista:
    max_len = len(texto) if len(texto) > max_len else max_len
  return max_len


def separar_STR(STR:str):
  """ Separa un Clasificación y retorna una lista"""
  lista_salida = []
  # * Separar por espacios separa PIPE A de PIPE B y la anterior en autor y año
  space_list = STR.split(' ')  
  # Ejemplo 'PQ7298.424.A76 .O744 2007' -> [PQ7298.424.A76] [.O744] [2007]
  #* Separa el PIPE A en sus atributos: Categorias XD
  pipe_a = space_list.pop(0) 
  # Ejemplo [PQ7298.424.A76] [.O744] [2007] -> [PQ7298.424.A76] | [.O744] [2007]
  pipe_a = pipe_a.split('.') 
  # Ejemplo [PQ7298.424.A76] -> [PQ7298] [424] [A76]
  letras_tema = pipe_a.pop(0)
  # Ejemplo [PQ7298] [424] [A76] -> [PQ7298] | [424] [A76]
  # print(space_list, pipe_a, letras_tema, sep='\n')
  #* Trabajar en separar letras y numeros
  letras_tema = [letras_tema[:2], letras_tema[2:]] if letras_tema[1] in alphabet else [letras_tema[:1], letras_tema[1:]]
  # Ejemplo PQ7298 -> [PQ, 7298] si 2 letras otro caso P7298 -> [P, 7298]
  # print(space_list, pipe_a, letras_tema, sep='\n')
  #* Juntar todas las listas en la salida
  lista_salida.extend(letras_tema)
  lista_salida.extend(pipe_a)
  lista_salida.extend(space_list)
  # Ejemplo [PQ, 7298] + [424, A76] + [.O744, 2007] -> ['PQ', '7298', '424', 'A76', '.O744', '2007']
  # print('Entrada', STR, sep='\n')
  # print('Salida Final', lista_salida, sep='\n')
  return lista_salida


def separate_list(str_dict: dict):
  """ Recibe un diccionario y crea una lista para imprimir """
  lista_salida = []
  #* Usando un diccionario obtener todos los elementos
  encabezado = [str_dict['HEAD']]
  clasif = separar_STR(str_dict["CLASS"])
  volumen = [str_dict['VOL']] if 'V.' in str_dict['VOL'] else ['']
  copia = ['C.' + str_dict['COP']] if str_dict['COP'] not in ('1', '0', '', ' ') else ['']
  #* Juntar todos los elementos
  lista_salida.extend(encabezado)
  lista_salida.extend(clasif)
  lista_salida.extend(volumen)
  lista_salida.extend(copia)
  #* Limpiar elementos vacios
  # lista_salida = [x for x in lista_salida if x != '']
  # print('Entrada', str_dict, sep='\n')
  # print('Salida', lista_salida, sep='\n')
  return lista_salida


def imprimir_etiqueta(lista_a_imprimir: list, config: dict, ruta: str, titulo:str, num=0000):
  ''' 
    Genera una imagen PNG de la Etiqueta de un Libro
    ! Sujeto a posibles cambios a futuro

    NOTAS:
    Sin modificar el FONT_SIZE de 40, en la etiqueta, común entran 8 filas, para una altura de 370 pxl.

  '''
  global FONT_SIZE
  #* Configuración de la Etiqueta
  IW, IH = config['TW'], config['TH']

  #* Medidas en pixeles de la etiqueta
  img_width = int(ESCALA * float(IW))
  img_height = int(ESCALA * float(IH))
  
  #* Variables para posicionarse
  max_len = max_len_list(lista_a_imprimir)
  limpiar_lista = [x for ind, x in enumerate(lista_a_imprimir) if x != '' or ind == 0]
  FONT_SIZE = 35 if len(limpiar_lista) > 8 else 40 
  real_font_size = (FONT_SIZE * 0.6) 
  # row_diff = 8 - len(lista_a_imprimir)
  jump_size = FONT_SIZE * 1.125
  superior_border =  -(FONT_SIZE * 0.3)
  
  #* Posicion del cursor para escribir
  Y_pos = superior_border
  X_pos = (img_width/2) - ((max_len/2) * real_font_size)

  #* Llenado de la etiqueta
  main_img = Image.new("RGB", (img_width, img_height), color=(255, 255, 255))
  image_draw = ImageDraw.Draw(main_img) # objeto para dibujar
  #* Imprime todo el texto en una imagen
  y_print = Y_pos # Posicion del encabeza
  for texto in limpiar_lista:
    image_draw.text((X_pos, y_print), texto, fill=COLOR, font=MAIN_FONT)
    y_print += jump_size
  #* Guardar la imagen
  ruta_img = f'{ruta}/{num}.png'
  main_img.save(ruta_img)
  return ruta_img


def imprimir_pagina(lista_a_imprimir:list, config: dict, ruta: str, titulo:str, position:tuple):
  global FONT_SIZE
  fpdf = FPDF() # Objeto para crear pdfs
  lista_imagenes_auxiliares = []
  #* Configuración de la Etiqueta
  PW, PH = config['PW'], config['PH'] 
  IW, IH = config['TW'], config['TH']
  COL, ROW = config['PC'], config['PR']
  
  #* Medidas para etiqueta individual (Posible cambio)
  img_width = int(ESCALA * float(IW))
  img_height = int(ESCALA * float(IH))
  #* Medidas para la hoja completa (Posible Cambio)
  page_width = int(ESCALA * float(PW))
  page_height = int(ESCALA * float(PH))


  #? Llenado de la pagina
  #* Generamos una nueva pagina en blanco
  main_img = Image.new("RGB", (page_width, page_height), color=(255, 255, 255))
  image_draw = ImageDraw.Draw(main_img) # Objeto para dibujar en la imagen
  
  #* Posición inicial para el cursor
  y, x = position
  page_counter = 0
  #* Tomar datos de etiqueta
  for etiqueta in lista_a_imprimir: 
    #* Variables para posicionarse    
    max_len = max_len_list(etiqueta)
    limpiar_lista = [dato for dato in etiqueta if x != '']
    FONT_SIZE = 35 if len(limpiar_lista) > 8 else 40 
    real_font_size = (FONT_SIZE * 0.6) 
    # row_diff = 8 - len(lista_a_imprimir)
    jump_size = FONT_SIZE * 1.125
    superior_border =  -(FONT_SIZE * 0.3)
    
    #* Posicion del cursor para escribir
    Y_pos = superior_border # Se queda estatico
    X_pos = (img_width/2) - ((max_len/2) * real_font_size) # Centrado dinamico


    #* Cambio de Linea - Se terminan las columnas
    if x == int(COL):  
      x = 0
      y += 1

    #* Cambio de página - Se terminan las filas
    if y == int(ROW):
      ruta_img = f'{ruta}/{page_counter}_aux_image.png'
      main_img.save(ruta_img) # Guardar imagen actual
      lista_imagenes_auxiliares.append(ruta_img) # Agregar imagen a cola de imagenes
      
      #* Generamos una nueva pagina en blanco
      main_img = Image.new("RGB", (page_width, page_height), color=(255, 255, 255))
      image_draw = ImageDraw.Draw(main_img)

      #* Nueva posición inicial para el cursor
      y, x = 0, 0
      page_counter += 1

    #* Imprimir contenido de etiqueta
    # Cursor para etiqueta individual
    x_print = X_pos + (img_width * x)
    y_print = Y_pos + (img_height * y)
    # print('Contadores', x, y, sep=' ')
    # print('Posicion cursor', x_print, y_print, sep=' ')
    
    for text in etiqueta:
      image_draw.text((x_print, y_print), text, fill=COLOR, font=MAIN_FONT)
      y_print += jump_size
    #* Cambio de Columna
    
    x += 1  

  # * Muestreo de la Imagen (Guardar Imagen)
  ruta_img = f'{ruta}/{page_counter}_aux_image.png'
  main_img.save(ruta_img) # Guardar imagen actual
  lista_imagenes_auxiliares.append(ruta_img) # Agregar imagen a cola de imagenes
  
  #* Generar PDF
  answer = image_viewer(lista_imagenes_auxiliares, True)
  if answer:
    for aux_image in lista_imagenes_auxiliares:
      fpdf.add_page()
      fpdf.image(aux_image, 0,0, w=210)
      os.remove(aux_image)
    fpdf.output(f'{ruta}/{titulo}.pdf')
  else:
    for aux_ruta in lista_imagenes_auxiliares:
      os.remove(aux_ruta)


def ticket_maker_main(etiquetas_a_imprimir: list, titulo: str, ruta:str, config:dict, position:tuple):
  """
  
  Toma una lista de strings y genera imagenes ya sean formato PNG o PDF.
  
  :param str_list: 
    Es una lista que contiene las cadenas a imprimir
    Ejemplo Entrada: ['ARVIZU', 'HG4551 .R8 2010', 'V.2', '2']
  :param titulo: 
    Nombre para ponerle al archivo de salida
  :param root: La ruta de guardado de los archivos generados
  :param config: La configuración de las imagenes que se generarán
  :param position: !Solo caso de Tamaño carta! Posición de inicio para imprimir
  """
  
  #* Transforma la lista de diccionarios a una lista para imprimir
  lista_a_imprimir = [separate_list(elem) for elem in etiquetas_a_imprimir]
  if position[0] != None:
    imprimir_pagina(
      config=config, lista_a_imprimir=lista_a_imprimir, position=position,
      ruta=ruta, titulo=titulo)
  #? Imprimir etiquetas individuales
  else:
    #* Crear carpeta nueva
    nueva_ruta = f'{ruta}/{titulo}'
    os.mkdir(nueva_ruta)
    lista_imagenes_auxiliares = []
    for ind, etiqueta in enumerate(lista_a_imprimir):
      ruta_aux = imprimir_etiqueta(
        lista_a_imprimir=etiqueta, config=config, ruta=nueva_ruta, 
        titulo=titulo, num=ind
      )
      lista_imagenes_auxiliares.append(ruta_aux)
    # Visualizar o Generar PDF
    image_viewer(lista_imagenes_auxiliares, False)


def image_viewer(lista_de_rutas: list, flag: bool):
  #* Estandarizar tamaño de la imagen
  lista_de_rutas = lista_de_rutas[:5] if not flag else lista_de_rutas
  divisor = 5 if flag else 2
  cursor = 0
  if not os.path.exists(lista_de_rutas[cursor]):
    return False
  image = Image.open(lista_de_rutas[cursor])
  iw, ih = image.size
  image.thumbnail((iw/divisor,ih/divisor))
  image.save('temp.png')
  
  # * Formato de la Interfaz de Usuario
  layout = [
    #? Generar una imagen
    [sg.Text('Muevase con las flechas del Teclado', font=('Open Sans', 16, 'bold', 'italic'), background_color='#FFFFFF', pad=0)],
    [sg.Frame(title='', layout=[[sg.Image(filename='temp.png', key='IMAGEN', pad=0)]], background_color='#000000')],
    [sg.Button('OK', font=('Open Sans', 12, 'bold'), pad=0)]
  ]
  main_layout = [[sg.Frame(title='',layout=layout, background_color="#FFFFFF", element_justification="c", pad=0)]]
  
  #* Inicializar Ventana
  window = sg.Window(
    'Visualizador Etiquetas', main_layout, element_justification='c', 
    icon='Assets/book_icon.ico', finalize=True, return_keyboard_events=True)

  #* Loop principal
  while True:
    event, values = window.read()
    # print(event,values, sep=',')
    #? Salir de la pestaña
    if event in ('OK', 'Exit', sg.WINDOW_CLOSED):
      window.close()
      os.remove('temp.png')
      if flag:
        answer = pop.check_images()
        return answer
      else: return False
    
    #? Esperar evento de teclado
    else:
      # * Avanzar imagen a la derecha
      if 'Right' in event or 'Up' in event:
        cursor = 0 if cursor+1 >= len(lista_de_rutas) else cursor + 1
      elif 'Left' in event or 'Down' in event:
        cursor = len(lista_de_rutas)-1 if cursor-1 < 0 else cursor - 1
      
      #* Revisa si existe el archivo
      if not os.path.exists(lista_de_rutas[cursor]):
        window.close()
        os.remove('temp.png')
        return False
      
      #* Abre la imagen y la cambia de tamaño
      image = Image.open(lista_de_rutas[cursor])
      iw, ih = image.size
      image.thumbnail((iw/divisor,ih/divisor))
      image.save('temp.png')
      window['IMAGEN'].update(filename='temp.png')


if __name__ == "__main__":
  # main_list = {'HEAD': '', 'CLASS':'BF109.78.J89 .C791 2010', 'VOL':'', 'COP':'1'}
  # main_list2 = {'HEAD': 'ARVIZU', 'CLASS':'BF109.78.J89 .C791 2010', 'VOL':'V.2', 'COP':'2'}
  # PCP = {'PW':21.59, 'PH':27.94, 'TW':2.69, 'TH':4.65, 'PR':6, 'PC':8} 
  # ruta = 'C:/Users/EQUIPO/Desktop/Proyecto_Intercalador/Pruebas/prueba_mario'
  # # print(separate_list(main_list))
  # ticket_maker_main(config=PCP, etiquetas_a_imprimir=[main_list, main_list2], position=(0,0), ruta=ruta, titulo='Prueba')
  print(separar_STR('Q126.4 .E88 2019'))
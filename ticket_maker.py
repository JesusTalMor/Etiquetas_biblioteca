import os
from typing import List

from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

from ApoyoSTRLIST import *

# TODO Ajustar el encabezado 1 cm de margen, listo pero no me convence
# TODO Queda pendiente PNG o PDF - Dejar en PNG etiquetas individuales

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def separate_STR(STR:str):
  """ Separa un STR en retorna una lista separada """
  return_list = []
  
  # separar por espacios
  aux_list = STR.split(' ')
  # print(aux_list)
  
  split_list = 0
  # Caso con encabezado
  if aux_list[0][2] in alphabet: 
    split_list = 1
    # Agregamos el encabezado a la lista final
    return_list.append(aux_list[0])
  
  # Separando Pipe A en una lista
  pipe_a_list = aux_list[split_list].split('.')
  # print(pipe_a_list)

  clas_split = 1
  # Caso con Clase 2 letras
  if pipe_a_list[0][1] in alphabet: clas_split = 2

  # Separando clase y subclase del string
  class_str = pipe_a_list[0][:clas_split]
  subclass_str = pipe_a_list[0][clas_split:]

  # print(class_str, subclass_str)
  return_list.append(class_str)
  return_list.append(subclass_str)

  # Actualizar listas de elementos
  pipe_a_list = pipe_a_list[1:]
  aux_list = aux_list[split_list+1:]
  # print(pipe_a_list)
  # print(aux_list)
  
  for elem in pipe_a_list: return_list.append('.' + elem)
  for elem in aux_list: return_list.append(elem)

  # print(return_list)
  return return_list

def separate_list(str_list: list):
  """ Recibe una lista de strings y retorna una lista de listas """
  return_list = []
  for indiv_str in str_list:
    return_list.append(separate_STR(indiv_str))
  
  return return_list

def ticket_maker_main(str_list: list, date: str, root:str, config:list, position:tuple):
  """
  * Toma una lista de strings y genera imagenes ya sean formato PNG o PDF
  
  @param str_list: Es una lista que contiene las cadenas a imprimir
  @param date: Fecha para poder nombrar los archivos
  @param root: La ruta de guardado de los archivos generados
  @param config: La configuración de las imagenes que se generarán
  @param position: !Solo caso de Tamaño carta! Posición de inicio para imprimir
  """
  #* Recibe la configuración para las etiquetas
  PW, PH, IW, IH, COL, ROW, OPTION = config
  #* Transforma una lista de strings a una lista de listas
  ticket = separate_STR(str_list)

  scale = 100  # * Escala de la etiqueta recomendado 100
  # * (Individual) Medidas de Etiqueta
  Iwidth = int(scale * float(IW))
  Iheight = int(scale * float(IH))
  # * Hoja Completa Medidas Hoja
  Pwidth = int(scale * float(PW))
  Pheight = int(scale * float(PH))

  # * Margen en eje Y
  Y_pos = int(0.5*scale) # Ajuste de margen ya definido
  # * Calcular la posición del cursor en X
  X_pos = int(Iwidth / 2) - 40


  # * Escalado de la tipografia
  font = ImageFont.truetype("Assets/Khmer OS Muol.otf", size=40)

  if OPTION:
    # * Definicion y Escritura del mensaje en la imagen generada
    fpdf = FPDF()
    main_image = Image.new("RGB", (Pwidth, Pheight), color=(255, 255, 255))
    image_draw = ImageDraw.Draw(main_image)
    color = "rgb(0, 0, 0)"
    # ? Print on a full Sheet of paper
    y, x = position
    page_counter = 0
    for main_ticket in ticket:  # recibe una lista de una lista de listas
      # print(main_ticket)
      # Decidir donde se va a imprimir
      if x == int(COL):  # Si no podemos imprimir en la fila actual
        x = 0
        y += 1

      if y == int(ROW):  # Si no podemos imprimir en la hoja
        main_image.save(f"{root}/{page_counter}_aux_image.png")
        os.system(f"powershell -c {root}/{page_counter}_aux_image.png")
        # Generamos una imagen nueva en blanco
        main_image = Image.new("RGB", (Pwidth, Pheight), color=(255, 255, 255))
        image_draw = ImageDraw.Draw(main_image)
        color = "rgb(0, 0, 0)"
        # Actualizamos los contadores
        y = 0
        x = 0
        page_counter += 1

      # Imprimimos con las posiciones
      x_print = X_pos + (Iwidth * x)
      y_print = Y_pos + (Iheight * y)
      for text in main_ticket:
        image_draw.text((x_print, y_print), text, fill=color, font=font)
        y_print += 40
      x += 1  # Actualizamos valor de X despues de imprimir

    # * Muestreo de la Imagen (Guardar Imagen)
    # print(str(ID) + '_' + str(date) + '.png')
    main_image.save(f"{root}/{page_counter}_aux_image.png")
    os.system(f"powershell -c {root}/{page_counter}_aux_image.png")
    # Borrar imagenes no utiles
    for index in range(page_counter+1):
      fpdf.add_page()
      aux_image = f"{root}/{index}_aux_image.png"
      fpdf.image(aux_image, 0,0, w=210)
      os.remove(aux_image)
    fpdf.output(root + "/" + str(date) + ".pdf")


  else:
    # ? Print individual ticket
    # print(ticket)
    for num, main_ticket in enumerate(ticket):  # recibe una lista de una lista de listas

      main_image = Image.new("RGB", (Iwidth, Iheight), color=(255, 255, 255))
      image_draw = ImageDraw.Draw(main_image)
      color = "rgb(0, 0, 0)"
      y_print = Y_pos
      for text in main_ticket:
        image_draw.text((X_pos, y_print), text, fill=color, font=font)
        y_print += 40

      # * Muestreo de la Imagen (Guardar Imagen)
      # print(str(ID) + '_' + str(date) + '.png')
      # if num == 0: main_image.show()
      main_image.save(root + "/" + str(num) + "_" + str(date) + ".png")


if __name__ == "__main__":
  # hoy = date.today()
  one = "JAPAN SB822.2 .L418 1974 V.1 C.1"
  two = "SB822.2 .L418 1974 V.1 C.1"
  thing = "HG4572 .L4418 2009"
  train_list = [one, two]
  # for clasify in train_list:
  #   # print(clasify)
  #   print(upd_separate_STR(clasify))
  print(separate_list(train_list))
  
  # heigth = 5
  # width = 3
  # ICP = [0, 0, width, heigth, 0, 0, False]  # Individual Configuration Parameters
  # ticket_maker_main(train_list, 'Nan', 'Nan', ICP, (None,None))

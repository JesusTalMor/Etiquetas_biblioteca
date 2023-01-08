import os

from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

import pop_ups as pop

# TODO Ajustar el encabezado 1 cm de margen, listo pero no me convence
# TODO Queda pendiente PNG o PDF - Dejar en PNG etiquetas individuales

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def separar_STR(STR:str):
  """ Separa un STR y retorna una lista"""
  lista_salida = []
  # * Separar por espacios
  aux_list = STR.split(' ')
  aux_list_2 = aux_list[0].split('.')
  if aux_list_2[0][1] in alphabet:
    aux_list_3 = [aux_list_2[0][:2], aux_list_2[0][2:]]
  elif aux_list_2[0][0] in alphabet:
    aux_list_3 = [aux_list_2[0][:1], aux_list_2[0][1:]]
  
  for elem in aux_list_3:
    lista_salida.append(elem)
  for index, elem in enumerate(aux_list_2):
    if index != 0: lista_salida.append(elem)
  for index, elem in enumerate(aux_list):
    if index != 0: lista_salida.append(elem)
  return lista_salida

def separate_list(str_list: list):
  """ Recibe una lista de strings y retorna una lista de listas """
  return_list = []
  for index, indiv_str in enumerate(str_list):
    if index != 1 and indiv_str != '':
      return_list.append(indiv_str)
    if index == 1:
      lista_temp = separar_STR(indiv_str)
      for elem in lista_temp:
        if elem != '': return_list.append(elem)
  
  return return_list

def ticket_maker_main(str_list: list, date: str, root:str, config:dict, position:tuple):
  """
  
  Toma una lista de strings y genera imagenes ya sean formato PNG o PDF.
  
  :param str_list: Es una lista que contiene las cadenas a imprimir
  :param date: Fecha para poder nombrar los archivos
  :param root: La ruta de guardado de los archivos generados
  :param config: La configuración de las imagenes que se generarán
  :param position: !Solo caso de Tamaño carta! Posición de inicio para imprimir
  """
  # * Recibe la configuración para las etiquetas
  PW, PH = config['PW'], config['PH'] 
  IW, IH = config['TW'], config['TH']
  COL, ROW = config['PC'], config['PR']
  
  # * Transforma una lista de strings a una lista de listas
  ticket = [separate_list(elem) for elem in str_list]
  scale = 100  # * Escala de la etiqueta recomendado 100
  
  # * (Individual) Medidas de Etiqueta
  Iwidth = int(scale * float(IW))
  Iheight = int(scale * float(IH))
  # * Hoja Completa Medidas Hoja
  Pwidth = int(scale * float(PW))
  Pheight = int(scale * float(PH))

  # * Margen en eje Y
  Y_pos = int(0.6*scale) # Ajuste de margen ya definido
  # * Calcular la posición del cursor en X
  X_pos = int(Iwidth / 2) - 40

  # * Escalado de la tipografia
  font = ImageFont.truetype("Assets/Khmer OS Muol.otf", size=40)

  if int(COL) != 0:
    # * Definicion y Escritura del mensaje en la imagen generada
    fpdf = FPDF()
    main_image = Image.new("RGB", (Pwidth, Pheight), color=(255, 255, 255))
    image_draw = ImageDraw.Draw(main_image)
    color = "rgb(0, 0, 0)"
    # ? Print on a full Sheet of paper
    y, x = position
    page_counter = 0
    for main_ticket in ticket:  # recibe una lista de una lista de listas
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
        y_print += 45
      x += 1  # Actualizamos valor de X despues de imprimir

    # * Muestreo de la Imagen (Guardar Imagen)
    # print(str(ID) + '_' + str(date) + '.png')
    main_image.save(f"{root}/{page_counter}_aux_image.png")
    os.system(f"powershell -c {root}/{page_counter}_aux_image.png")

    
    # Mostrar pop up de confirmación
    answer = pop.check_images()
    if answer:
      for index in range(page_counter+1):
        fpdf.add_page()
        aux_image = f"{root}/{index}_aux_image.png"
        fpdf.image(aux_image, 0,0, w=210)
        os.remove(aux_image)
      fpdf.output(root + "/" + str(date) + ".pdf")
    else:
      for index in range(page_counter+1):
        aux_image = f"{root}/{index}_aux_image.png"
        os.remove(aux_image)


  else:
    # ? Print individual ticket
    for num, main_ticket in enumerate(ticket): 
      main_image = Image.new("RGB", (Iwidth, Iheight), color=(255, 255, 255))
      image_draw = ImageDraw.Draw(main_image)
      color = "rgb(0, 0, 0)"
      y_print = Y_pos
      for text in main_ticket:
        image_draw.text((X_pos, y_print), text, fill=color, font=font)
        y_print += 45

      # * Muestreo de la Imagen (Guardar Imagen)
      main_image.save(root + "/" + str(num) + "_" + str(date) + ".png")


if __name__ == "__main__":
  main_list = ['SLAP', 'BF109.78.J89 .C791 2010', 'V.1', 'C.1']
  print(separate_list(main_list))
  
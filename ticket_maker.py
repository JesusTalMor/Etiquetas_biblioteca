import os

from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

from ApoyoSTRLIST import *

# TODO Ajustar el encabezado 1 cm de margen, listo pero no me convence
# TODO Queda pendiente PNG o PDF - Dejar en PNG etiquetas individuales

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def upd_separate_STR(STR):
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


def primitive_cutter(STR):
  exit_list = []
  while True:
    pos_list = pos_Separadores(STR[1:])
    # print(STR)
    # print(pos_list)
    if pos_list[0] + pos_list[1] + pos_list[2] == 0:
      exit_list.append(STR.replace(" ", ""))
      break
    pos_cut = pos_corte(pos_list)
    exit_list.append(STR[: pos_cut + 1].replace(" ", ""))
    STR = STR[pos_cut + 1 :]
  return exit_list


def separate_STR(STR_List):
  """Recibe una lista de string, retorna una lista de listas de los string separados"""
  global max_lenght
  global max_row
  
  
  # * Esta función separa los parametros de las etiquetas de manera primitiva
  exit_list = []
  for STR in STR_List:
    # print(STR)
    aux_list = []
    vol = ""
    cop = ""
    
    if "C." in STR:
      cop_pos = STR.index("C.")
      cop = "C." + STR[cop_pos + 2]
      STR = STR[: cop_pos - 1]
      # print(cop)

    # * Revisar si tenemos copia o volumen
    if "V." in STR:
      vol_pos = STR.index("V.")
      vol = "V." + STR[vol_pos + 2]
      STR = STR[: vol_pos - 1]
      # print(vol)

    # * Checar si existe un encabezado
    if " " in STR and STR[2] in letras_array:
      pos_enca = STR.index(" ")
      aux_list.append(STR[:pos_enca])
      # print(f"Encabezado es {STR[:pos_enca]}")
      STR = STR[pos_enca + 1 :]
      # print(f"el string ahora es {STR}")

    # * Primero separar encabezado (DS, D, HB.)
    for index in range(len(STR)):
      if STR[index] not in alphabet:
        aux_list.append(STR[:index])
        STR = STR[index:]
        break

    if " ." in STR or ". " in STR:
      try:
        dotesp_pos = STR.index(" .")
      except:
        dotesp_pos = 1000

      try:
        espdot_pos = STR.index(". ")
      except:
        espdot_pos = 1000

      if espdot_pos == 1000:
        main_cut = dotesp_pos
      else:
        main_cut = espdot_pos

      STR_aux = STR[main_cut + 1 :]
      STR = STR[:main_cut]

      # print(STR)
      # print(STR_aux)

      STRA_list = primitive_cutter(STR)
      STRB_list = primitive_cutter(STR_aux)

      for arr in STRA_list:
        aux_list.append(arr)
      for arr in STRB_list:
        aux_list.append(arr)

      # print(aux_list)

    else:
      STR_list = primitive_cutter(STR)
      for arr in STR_list:
        aux_list.append(arr)

    if vol != "":
      aux_list.append(vol)
    if cop != "":
      aux_list.append(cop)

    # print(aux_list)
    exit_list.append(aux_list)

  return exit_list


def ticket_maker_main(STR, date, root, config, position):
  PW, PH, IW, IH, COL, ROW, OPTION = config
  ticket = separate_STR(STR)

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
  print(upd_separate_STR(thing))
  # # main_STR = ["SB822 .L418 1974"]
  # root = ""
  # # print(separate_STR(main_STR))
  # heigth = 5
  # width = 3
  # ICP = [0, 0, width, heigth, 0, 0, False]  # Individual Configuration Parameters
  # ticket_maker_main(main_STR, 'Nan', root, ICP, (None, None))

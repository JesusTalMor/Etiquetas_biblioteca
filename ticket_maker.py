from datetime import date

from PIL import Image, ImageDraw, ImageFont

from ApoyoSTRLIST import *

# TODO EN el siguiente programa esta el creador de etiquetas individuales
max_lenght = 0
max_row = 0


def utility_max(STR_list):
	max_length = 0
	for y in STR_list:
		if len(y) > max_length:
			max_length = len(y)
	return max_length


def max_check(num, main_max):
	if num > main_max:
		return num
	else:
		return main_max


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
	alphabet = [
		"A",
		"B",
		"C",
		"D",
		"E",
		"F",
		"G",
		"H",
		"I",
		"J",
		"K",
		"L",
		"M",
		"N",
		"O",
		"P",
		"Q",
		"R",
		"S",
		"T",
		"U",
		"V",
		"W",
		"X",
		"Y",
		"Z",
	]
	# * Esta función separa los parametros de las etiquetas de manera primitiva
	exit_list = []
	for STR in STR_List:
		# print(STR)
		aux_list = []
		vol = ""
		cop = ""
		# * Revisar si tenemos copia o volumen
		if "V." in STR:
			vol_pos = STR.index("V.")
			vol = "V." + STR[vol_pos + 2]
			STR = STR[: vol_pos - 1]
			# print(vol)
		if "C." in STR:
			cop_pos = STR.index("C.")
			cop = "C." + STR[cop_pos + 2]
			STR = STR[: cop_pos - 1]
			# print(cop)

		# * Checar si existe un encabezado
		if " " in STR and STR[2] in letras_array:
			pos_enca = STR.index(" ")
			aux_list.append(STR[:pos_enca])
			print(f"Encabezado es {STR[:pos_enca]}")
			STR = STR[pos_enca + 1 :]
			print(f"el string ahora es {STR}")

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

		max_lenght = max_check(utility_max(aux_list), max_lenght)
		max_row = max_check(len(aux_list), max_row)
		exit_list.append(aux_list)

	return exit_list, max_lenght, max_row


def ticket_maker_main(STR, date, root, config, position):
	PW, PH, IW, IH, COL, ROW, OPTION = config
	ticket, max_ticket_len, ticket_len = separate_STR(STR)
	# print(ticket)
	# ticket = ['DS', '822', '.2', '.L418', '1974']
	# ticket = ['DS', '827', '.S3', '.G3718', '2007']
	# ticket = ['DS', '835', '.P47', '.2009']

	scale = 100  # * Escala de la etiqueta recomendado 100
	# * (Individual) Medidas de Etiqueta
	Iwidth = int(scale * float(IW))
	Iheight = int(scale * float(IH))
	# * Hoja Completa Medidas Hoja
	Pwidth = int(scale * float(PW))
	Pheight = int(scale * float(PH))

	# * Escalado de la tipografia
	# TODO Mejorar el proceso
	# FX_scale = int(Iwidth/(max_ticket_len))
	FY_scale = int(Iheight / (ticket_len + 4))
	# print('Tamaño de letra segun X: ', FX_scale)
	# print('Tamaño de letra segun Y: ', FY_scale)
	# FF_scale = int((FX_scale + FY_scale)/2)
	# print('Tamaño promediado: ', FF_scale)
	# XY_pos = (int(FX_scale*2), int(FY_scale/2))
	# X_pos = int(FX_scale*2)
	Y_pos = int(FY_scale)
	# Scale the font
	font = ImageFont.truetype("Assets/Khmer OS Muol.otf", size=40)

	if OPTION:
		# * Definicion y Escritura del mensaje en la imagen generada
		main_image = Image.new("RGB", (Pwidth, Pheight), color=(255, 255, 255))
		image_draw = ImageDraw.Draw(main_image)
		color = "rgb(0, 0, 0)"
		# ? Print on a full Sheet of paper
		page_count = 0
		y, x = position
		for main_ticket in ticket:  # recibe una lista de una lista de listas
			# print(main_ticket)
			# Decidir donde se va a imprimir
			if x == int(COL):  # Si no podemos imprimir en la fila actual
				x = 0
				y += 1

			if y == int(ROW):  # Si no podemos imprimir en la hoja
				main_image.show()
				main_image.save(
					root + "/" + str(page_count) + "_" + str(date) + ".pdf"
				)  # Salvamos la imagen
				# Generamos una imagen nueva en blanco
				main_image = Image.new("RGB", (Pwidth, Pheight), color=(255, 255, 255))
				image_draw = ImageDraw.Draw(main_image)
				color = "rgb(0, 0, 0)"
				# Actualizamos los contadores
				y = 0
				x = 0
				page_count += 1

			# * Calcular la posición del cursor
			X_pos = int(Iwidth / 2) - 40
			if len(main_ticket[0]) >= 3:  # Tenemos un Encabezado
				if len(main_ticket[1]) == 2:  # Tenemos 2 Caracteres tenemos que ajustar
					X_pos -= 40
			elif len(main_ticket[0]) == 2:  # Tenemos 2 Caracteres tenemos que ajustar
				X_pos -= 40

			# Imprimimos con las posiciones
			x_print = X_pos + (Iwidth * x)
			y_print = Y_pos + (Iheight * y)
			for text in main_ticket:
				image_draw.text((x_print, y_print), text, fill=color, font=font)
				y_print += 40
			x += 1  # Actualizamos valor de X despues de imprimir
			# print(f"Posición en X {x_print} limite de la hoja {Pwidth}")
			# print(f"Contador de x = {x} \n")

		# * Muestreo de la Imagen (Guardar Imagen)
		# print(str(ID) + '_' + str(date) + '.png')
		main_image.show()
		main_image.save(root + "/" + str(page_count) + "_" + str(date) + ".pdf")

	else:
		# ? Print individual ticket
		for num, main_ticket in enumerate(
			ticket
		):  # recibe una lista de una lista de listas

			# * Calcular la posición del cursor
			X_pos = int(Iwidth / 2) - 40
			if len(main_ticket[0]) >= 3:  # Tenemos un Encabezado
				if len(main_ticket[1]) == 2:  # Tenemos 2 Caracteres tenemos que ajustar
					X_pos -= 40
			elif len(main_ticket[0]) == 2:  # Tenemos 2 Caracteres tenemos que ajustar
				X_pos -= 40

			main_image = Image.new("RGB", (Iwidth, Iheight), color=(255, 255, 255))
			image_draw = ImageDraw.Draw(main_image)
			color = "rgb(0, 0, 0)"
			y_print = Y_pos
			for text in main_ticket:
				image_draw.text((X_pos, y_print), text, fill=color, font=font)
				y_print += 35

			# * Muestreo de la Imagen (Guardar Imagen)
			# print(str(ID) + '_' + str(date) + '.png')
			if num == 0:
				main_image.show()
			main_image.save(root + "/" + str(num) + "_" + str(date) + ".png")


if __name__ == "__main__":
	hoy = date.today()
	# main_STR = ['JAPAN DS822.2 .L418 1974 V.1', 'D510.4 .W310 1974', 'SC510.4 .W310 1974 C.1']
	main_STR = ["JAPAN S822.2 .L418 1974 V.1"]
	root = "C:/Users/EQUIPO/Desktop"
	# print(separate_STR(main_STR))
	ICP = [0, 0, 4.8, 3.7, 0, 0, False]  # Individual Configuration Parameters
	ticket_maker_main(main_STR, hoy, root, ICP, (None, None))

import pandas as pd

import string_helper as sh


def crear_reporte_modificados(lista, ruta, fecha):
  '''Genera un reporte en un txt de libros modificados'''
  if len(lista) == 0: return # Revisar si tenemos datos
  
  txt_path = f'{ruta}/{str(fecha)}_modificados.txt'
  modif_file = open(txt_path, 'w', encoding="utf-8")
  modif_file.write(f'Lista de Clasificaciones Modificadas\n')
  for target in lista:
    for elem in target:
      if len(elem) > 40: modif_file.write(f'{elem[:40]}... | ')
      else: modif_file.write(f'{elem} | ')
    modif_file.write('\n')
  modif_file.close()
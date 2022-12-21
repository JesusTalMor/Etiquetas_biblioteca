import pandas as pd

import string_helper as sh


def cargar_excel(path:str):
  '''Obtiene todo el dataframe de datos de un excel'''
  Datos = pd.read_excel(path, sheet_name=None)
  return Datos

def cargar_clasif_libros(dataframe):
  ''' Carga los datos para generar clasificaciones'''
  clasif = [False]
  volumen = [False]
  copia = [False]

  llaves = list(dataframe)

  # Revisar si podemos extraer los datos necesarios
  if 'Clasificación' in llaves and 'Volumen' in llaves and 'Copia' in llaves:
    clasif = dataframe['Clasificación']
    volumen = dataframe['Volumen']
    copia = dataframe['Copia']
  
  return clasif, volumen, copia

def cargar_informacion_libros(dataframe):
  ''' Carga los datos de información de los libros'''
  titulo = [False]
  codigo_barras = [False]

  llaves = list(dataframe)

  if 'C. Barras' in llaves: titulo = dataframe['Título']
  if 'Título' in llaves: codigo_barras = dataframe['C. Barras']
  
  return titulo, codigo_barras

def generar_etiquetas_libros(ruta_archivo:str):
  """ Genera las etiquetas de un archivo Excel """
  salida = []
  error_flag = False
  dataframe = cargar_excel(ruta_archivo)
  paginas_excel = list(dataframe)
  for hoja in paginas_excel:
    CLAS, VOL, COP = cargar_clasif_libros(dataframe[hoja])
    len_data = len(CLAS)
    
    # * Checa si se cargaron todos los datos
    if not CLAS[0]:
      error_flag = True
      continue
    
    # * Inicia proceso de sacar todas las clasificaciones
    for i in range(len_data):
      STR = CLAS[i]
      STR_C = str(COP[i])
      STR_V = VOL[i]
      # print(STR_V)

      # * Checar si el atributo CLAS esta vacio
      if pd.isna(STR):
        salida.append(['None', 'No', 'Aplica', 'False'])
        continue

      # * Eliminar caracteres LX y MAT
      if 'LX' in STR: STR = sh.cortar_string(STR, 'LX')
      if 'MAT' in STR: STR = sh.cortar_string(STR, 'MAT')

      # * Checar si el atributo VOL esta vacio
      if pd.isna(STR_V): STR_V = ''

      # * Checar si el atributo VOL esta vacio
      if pd.isna(STR_C): STR_C = ''

      STR_Clas = sh.creador_clasificacion(STR, STR_V, STR_C)
      
      # * Revisar si tenemos Volumen o Copia donde no corresponden
      if 'V.' in STR or 'C.' in STR:
        salida.append([STR_Clas, 'No', 'Aplica', 'False'])
        continue

      # * Revisamos si se puede dividir Pipe A y Pipe B
      if sh.revisar_corte_pipe(STR) and sh.revisar_pipeB(STR):
        pos_div, sum = sh.buscar_pipe(STR)
        pipe_a_str = STR[:pos_div]
        pipe_b_str = STR[pos_div+sum:]
        salida.append([STR_Clas, pipe_a_str, pipe_b_str, 'True'])
      else:
        salida.append([STR_Clas, 'No', 'Aplica', 'False'])
  
  if len(salida) != 0: return salida, error_flag
  else: return [False]

def generar_informacion_libros(ruta_archivo:str):
  '''
  Genera una lista completa con la información de 
  Titulo y codigo de Barras de los libros
  '''
  titulo = []
  codigo_barras = []
  dataframe = cargar_excel(ruta_archivo)
  paginas_excel = list(dataframe)
  
  for hoja in paginas_excel:
    temporal_titulo, temporal_codigo_barras = cargar_informacion_libros(dataframe[hoja])
    titulo.extend(temporal_titulo)
    codigo_barras.extend(temporal_codigo_barras)  
  return titulo, codigo_barras

def crear_reporte(modificados, ruta, fecha):
  '''Genera un reporte en un txt de libros modificados'''
  
  txt_path = f'{ruta}/{str(fecha)}_modificados.txt'
  # print(txt_path)
  modif_file = open(txt_path, 'w', encoding="utf-8")
  if len(modificados) > 0:
    modif_file.write(f'Lista de Clasificaciones Modificadas\n')
    for target in modificados:
      for elem in target:
        if len(elem) > 40:
          modif_file.write(f' {elem[:40]}... | ')
        else:
          modif_file.write(f' {elem} | ')
      modif_file.write('\n')
  else:
    modif_file.write(f'No existen modificaciones\n')
  # print('Archivo Creado')
  modif_file.close()
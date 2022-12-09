import pandas as pd

from ApoyoSTRLIST import *


def cargarExcel(path):
  Datos = pd.read_excel(path,sheet_name=None)
  return Datos

def cargarDatos(dataframe):
  lClas = [False]
  lVol = [False]
  lCop = [False]

  llaves = list(dataframe)

  if 'Clasificación' in llaves and 'Volumen' in llaves and 'Copia' in llaves:
    lClas = dataframe['Clasificación']
    lVol = dataframe['Volumen']
    lCop = dataframe['Copia']
  
  return lClas, lVol, lCop

def cargarStat(dataframe):
  lTitulo = [False]
  lQRO = [False]

  llaves = list(dataframe)

  if 'C. Barras' in llaves and 'Título' in llaves:
    lTitulo = dataframe['Título']
    lQRO = dataframe['C. Barras']
  
  return lTitulo, lQRO

def detectar_etiquetas(ruta_archivo):
  """ Sacas las etiquetas de un archivo Excel """
  Salida = []
  Error_flag = False
  dataFrame = cargarExcel(ruta_archivo)
  paginas_excel = list(dataFrame)
  for key in paginas_excel:
    CLAS, VOL, COP = cargarDatos(dataFrame[key])
    # * Checa si se cargaron todos los datos
    if not CLAS[0]:
      Error_flag = True
      continue
    len_data = len(CLAS)
    # * Inicia proceso de sacar todas las clasificaciones
    for i in range(len_data):
      STR = CLAS[i]

      # Control de Excepciones
      # GN25 .C3818 2013
      # Buscar espacio despues de letra

      STR_C = str(COP[i])
      STR_V = VOL[i]
      # print(STR_V)

      # * Checar si el atributo VOL esta vacio
      if pd.isna(STR_V): STR_V = ''

      # * Checar si el atributo VOL esta vacio
      if pd.isna(STR_C): STR_C = ''

      STR_Clas = clas_maker(STR, STR_V, STR_C, False)

      if pd.isna(STR):
        Salida.append(['None', 'No', 'Aplica', 'False'])
      else:
        if 'LX' in STR: 
          char = 'LX'  # Para casos con XL
          STR = STR_cutter(STR, char)
        elif 'MAT' in STR: 
          char = 'MAT' # Para casos con MAT COM
          STR = STR_cutter(STR, char)

        if 'V.' in STR or 'C.' in STR:
          Salida.append([STR_Clas, 'No', 'Aplica', 'False'])
        elif revisarSep(STR) and revisarPipeB(STR):
          pos_div, sum = buscarPIPE(STR)
          pipe_a_str = STR[:pos_div]
          pipe_b_str = STR[pos_div+sum:]
          Salida.append([STR_Clas, pipe_a_str, pipe_b_str, 'True'])
        else:
          Salida.append([STR_Clas, 'No', 'Aplica', 'False'])
  if Salida != []: return Salida, Error_flag
  else: return []

def detectar_stat(ruta_archivo):
  Ftitulo = []
  FQRO = []
  dataFrame = cargarExcel(ruta_archivo)
  paginas_excel = list(dataFrame)
  for key in paginas_excel:
    titulo, QRO = cargarStat(dataFrame[key])
    # print(titulo)
    # print(QRO)
    Ftitulo.extend(titulo)
    FQRO.extend(QRO)  
  # print(Ftitulo)
  # print(FQRO)
  return Ftitulo, FQRO

def crear_reporte(modificados, ruta, fecha):
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

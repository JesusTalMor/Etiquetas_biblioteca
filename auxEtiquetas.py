import pandas as pd

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
import pandas as pd


class TableManager:
  """ Clase creada para el manejo de los datos de la tabla 
  """
  tabla_principal = []
  tabla_datos = []
  tabla_formato = []
  diccionario_estatus = {}
  diccionario_modificados = {}
  def agregar_elemento(self, principal:list, datos:dict, estatus:str, color="#FFFFFF"):
    """ Agregar un elemento a la tabla general """
    largo_tabla = self.get_len()
    formato = (largo_tabla, color)
    self.tabla_principal.append(principal)
    self.tabla_datos.append(datos)
    self.tabla_formato.append(formato)
    self.diccionario_estatus[largo_tabla] = estatus
  
  def agregar_modificado(self, index:int, new_clasif:str):
    """ Agregar un elemento a un diccionario de modificaciones
    o en su defecto lo actualiza.
    """
    titulo = self.tabla_datos[index]['titulo']
    cbarras = self.tabla_datos[index]['cbarras']
    clasificacion = self.tabla_principal[index][0]
    aux_modify = [titulo, cbarras, clasificacion, new_clasif]
    self.diccionario_modificados[index] = aux_modify

  def actualizar_elemento(self, index:int, estatus:str, color="#FFFFFF"):
    """ Actualizar el color y el status del elemento seleccionado """
    if index > self.get_len(): return False
    self.diccionario_estatus[index] = estatus
    self.tabla_principal[index][3] = estatus
    self.tabla_formato[index] = (int(index), color)
    return True

  def reset_table(self):
    self.tabla_principal = []
    self.tabla_datos = []
    self.tabla_formato = []
    self.diccionario_estatus = {}
  
  def get_len(self):
    return len(self.tabla_principal)
  def get_status_element(self, index):
    return self.diccionario_estatus[index] if index in self.diccionario_estatus else ''
  def get_data_element(self, index):
    return self.tabla_datos[index] if index < self.get_len() else {}
  
  def set_data_element(self, index, data):
    self.tabla_datos[index] = data
  def set_element(self, index, data):
    self.tabla_principal[index] = data

class ExcelManager:
  """ Clase Diseñada para el manejo de archivo de excel
  """
  dataframe = {}
  def cargar_datos_excel(self, ruta_archivo):
    #* Vamos a cargar toda la información del excel de una
    # Sacar el dataframe del excel
    self.dataframe = self.cargar_datos_excel(ruta_archivo)
    # Sacar las hojas del excel
    hojas_excel = list(self.dataframe)
    # Bluce para sacar la información de todo el documento
    for hoja in hojas_excel:
      #* Sacar todos los datos de los libros del excel
      temp_etiquetas = self.generar_etiquetas_libros(self.dataframe[hoja])  
      temp_infomacion = self.generar_informacion_libros(self.dataframe[hoja])  
  def cargar_excel(self, path:str):
    '''Obtiene todo el dataframe de datos de un excel'''
    Datos = pd.read_excel(path, sheet_name=None)
    return Datos
  
def cargar_clasif_libros(dataframe):
  '''
    Carga los datos para generar clasificaciones
    NOTA: Unicamente carga los datos de las columnas de Excel, no realiza modificaciones
  '''
  encabeza = []
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
  ''' 
    Carga los datos de información de los libros
    NOTA: Unicamente carga los datos de las columnas de Excel, no realiza modificaciones
  '''
  titulo = [False]
  codigo_barras = [False]
  clasif = [False]
  volumen = [False]
  copia = [False]
  encabezado = [False]

  llaves = list(dataframe)

  if 'Título' in llaves: titulo = dataframe['Título']
  if 'C. Barras' in llaves: codigo_barras = dataframe['C. Barras']
  if 'Clasificación' in llaves: clasif = dataframe['Clasificación']
  if 'Volumen' in llaves: volumen = dataframe['Volumen']
  if 'Copia' in llaves: copia = dataframe['Copia']
  if 'Encabezado' in llaves: encabezado = dataframe['Encabezado']
  
  return titulo, codigo_barras, clasif, volumen, copia, encabezado


def generar_etiquetas_libros(dataframe):
  """ Genera las etiquetas de un archivo Excel """
  salida = []
  
  # * Solo vamos a usar una pagina en este programa
  CLAS, VOL, COP = cargar_clasif_libros(dataframe)
  len_data = len(CLAS)
  
  # * Checa si se cargaron todos los datos
  if not CLAS[0]: return [False]
  
  # * Inicia proceso de sacar todas las clasificaciones
  for i in range(len_data):
    STR = CLAS[i] # ya vienen como String por defecto
    STR_C = str(COP[i])
    STR_V = VOL[i] # ya vienen como String por defecto

    # * Checar si el atributo CLAS esta vacio
    if pd.isna(STR):
      salida.append(['None', 'No', 'Aplica', 'False'])
      continue

    STR = sh.limpiar_clasif(STR)

    # * Checar si el atributo VOL esta vacio
    if pd.isna(STR_V): STR_V = ''

    # * Checar si el atributo COP esta vacio
    if pd.isna(STR_C): STR_C = ''

    STR_Clas = sh.creador_clasificacion(STR, STR_V, STR_C)
    
    # * Revisamos si se puede dividir Pipe A y Pipe B
    if sh.revisar_corte_pipe(STR) and sh.revisar_pipeB(STR):
      pos_div, sum = sh.buscar_pipe(STR)
      pipe_a_str = STR[:pos_div]
      pipe_b_str = STR[pos_div+sum:]
      salida.append([STR_Clas, pipe_a_str, pipe_b_str, 'True'])
    else:
      salida.append([STR_Clas, 'No', 'Aplica', 'False'])
  
  if len(salida) != 0: return salida
  else: return [False]


def cargar_informacion_libros(dataframe):
  '''
  Genera una lista completa con la información de 
  Titulo y codigo de Barras de los libros
  '''
  llaves = list(dataframe)
  
  titu, cb, clas, vol, cop, enc = cargar_informacion_libros(dataframe)
  # * Checar si clase tiene error
  if not clas[0]: return [False]

  for index in range(len(clas)):
    # * Creamos el diccionario
    temp_dicc = {}
    # * Rellenamos el diccionario
    temp_dicc['titulo'] = str(titu[index]) if titu[0] else ''
    temp_dicc['cbarras'] = str(cb[index]) if cb[0] else ''
    temp_dicc['clasif'] = str(sh.limpiar_clasif(clas[index])) if clas[0] and not pd.isna(clas[index]) else ''
    temp_dicc['volumen'] = str(vol[index]) if vol[0] and not pd.isna(vol[index]) else ''
    temp_dicc['copia'] = str(cop[index]) if cop[0] and not pd.isna(cop[index]) else ''
    temp_dicc['encabeza'] = str(enc[index]) if enc[0] else ''
    # * Añadimos el diccionario
    Salida.append(temp_dicc)
  return Salida

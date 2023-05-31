import pandas as pd

import string_helper as sh


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
  
  def crear_reporte_modificados(self, path:str, nombre:str,):
    '''Genera un reporte en un txt de libros modificados'''
    if not self.diccionario_modificados: return False # Revisar si tenemos datos
    
    txt_path = f'{path}/{str(nombre)}_modificados.txt'
    modif_file = open(txt_path, 'w', encoding="utf-8")
    modif_file.write(f'Lista de Clasificaciones Modificadas\n')
    for target in self.diccionario_modificados.values():
      for elem in target:
        if len(elem) > 40: modif_file.write(f'{elem[:40]}... | ')
        else: modif_file.write(f'{elem} | ')
      modif_file.write('\n')
    modif_file.close()
    return True

  def crear_reporte_QRO(self, path:str, nombre:str,):
    '''Genera un reporte en un txt de libros modificados'''
    if not self.diccionario_modificados: return False # Revisar si tenemos datos
    
    txt_path = f'{path}/{str(nombre)}_QRO.txt'
    modif_file = open(txt_path, 'w', encoding="utf-8")
    for target in self.diccionario_modificados.values():
        modif_file.write(f'{target[1]}')
        modif_file.write('\n')
    modif_file.close()
    return True
  
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
  def cargar_datos_excel(self, ruta_archivo, table_manager=TableManager()):
    #* Vamos a cargar toda la información del excel de una
    estatus = False
    # Sacar el dataframe del excel
    dataframe = self.cargar_excel(ruta_archivo)
    # Sacar las hojas del excel
    hojas_excel = list(dataframe)
    # Bluce para sacar la información de todo el documento
    for hoja in hojas_excel:
      #* Sacar todos los datos de los libros del excel
      temp_etiquetas = self.generar_etiquetas_libros(dataframe[hoja])  
      temp_infomacion = self.generar_informacion_libros(dataframe[hoja])

      # ? Se cargaron etiquetas para esta hoja ?
      if temp_etiquetas is False or temp_infomacion is False:
        print(f"Etiquetas no cargadas para hoja {hoja}")
        continue
        
      # * Generamos la tabla de datos para el Excel
      for ind in range(len(temp_etiquetas)):
        etiqueta_principal = temp_etiquetas[ind]
        etiqueta_datos = temp_infomacion[ind]
        estatus_etiqueta = etiqueta_principal[3]
        color = "#F04150" if estatus_etiqueta == "False" else "#FFFFFF"
        table_manager.agregar_elemento(
          principal= etiqueta_principal,
          datos= etiqueta_datos,
          estatus= estatus_etiqueta, 
          color= color
        )
      
      # * si cargamos algunos datos 
      estatus = True
    
    return estatus
  
  def cargar_excel(self, path:str):
    '''Obtiene todo el dataframe de datos de un excel'''
    Datos = pd.read_excel(path, sheet_name=None)
    return Datos
  
  def generar_etiquetas_libros(self, dataframe):
    """ Genera las etiquetas de un archivo Excel """
    salida = []
    
    # * Solo vamos a usar una pagina en este programa
    llaves = list(dataframe)
    CLAS = dataframe['Clasificación'] if 'Clasificación' in llaves else False
    VOL = dataframe['Volumen'] if 'Volumen' in llaves else False
    COP = dataframe['Copia'] if 'Copia' in llaves else False
    HEAD = dataframe['Encabezado'] if 'Encabezado' in llaves else False
    
    #! Manejo de Excepciones
    if CLAS is False: 
      #? No se encontro la columna de Clasificacion
      # TODO Mostrar Popup error
      return False
    if len(CLAS) == 0:
      #? No se tienen datos en la columna de clasificacion
      # TODO Mostrar Popup error
      return False    
    
    # * Inicia proceso de sacar todas las clasificaciones
    for i in range(len(CLAS)):
      STR = CLAS[i] # ya vienen como String por defecto
      STR_C = str(COP[i]) if COP is not False else ''
      STR_V = VOL[i] if VOL is not False else '' # ya vienen como String por defecto
      STR_H = HEAD[i] if HEAD is not False else ''

      # * Checar si el atributo CLAS esta vacio
      if pd.isna(STR):
        salida.append(['None', 'No', 'Aplica', 'False'])
        continue

      STR = sh.limpiar_clasif(STR)

      # * Checar si el atributo VOL esta vacio
      if pd.isna(STR_V): STR_V = ''

      # * Checar si el atributo COP esta vacio
      if pd.isna(STR_C): STR_C = ''

      # * Checar si el encabezado esta vacio
      if pd.isna(STR_H): STR_H = ''

      STR_Clas = sh.creador_clasificacion(STR, STR_H, STR_V, STR_C)
      
      # * Revisamos si se puede dividir Pipe A y Pipe B
      if sh.revisar_corte_pipe(STR) and sh.revisar_pipeB(STR):
        pos_div, sum = sh.buscar_pipe(STR)
        pipe_a_str = STR[:pos_div]
        pipe_b_str = STR[pos_div+sum:]
        salida.append([STR_Clas, pipe_a_str, pipe_b_str, 'True'])
      else:
        salida.append([STR_Clas, 'No', 'Aplica', 'False'])
    
    if len(salida) != 0: return salida
    else: return False
  
  def generar_informacion_libros(self, dataframe):
    ''' 
      Carga los datos de información de los libros
      NOTA: Unicamente carga los datos de las columnas de Excel, no realiza modificaciones
    '''
    # Saca las columnas del excel
    llaves = list(dataframe)

    clasif = dataframe['Clasificación'] if 'Clasificación' in llaves else False
    #! Manejo de Excepciones
    if clasif is False: 
      #? No se encontro la columna de Clasificacion
      # TODO Mostrar Popup error
      return False
    if len(clasif) == 0:
      #? No se tienen datos en la columna de clasificacion
      # TODO Mostrar Popup error
      return False
    
    lista_columnas_deseadas = [
      ('Título', 'titulo', 'Título' in llaves),
      ('C. Barras', 'cbarras', 'C. Barras' in llaves),
      ('Clasificación', 'clasif', 'Clasificación' in llaves),
      ('Volumen', 'volumen', 'Volumen' in llaves),
      ('Copia', 'copia', 'Copia' in llaves),
      ('Encabezado', 'encabeza', 'Encabezado' in llaves),
    ]
    lista_salida = []
    #* Generar diccionarios
    for index in range(len(clasif)):
      temp_dict = {} # Diccionario temporal
      # * Rellenamos el diccionario
      for columna, llave, bandera in lista_columnas_deseadas:
        temp_dict[llave] = str(dataframe[columna][index]) if bandera and not pd.isna(dataframe[columna][index]) else ''
      # * Añadimos el diccionario
      lista_salida.append(temp_dict)
    
    return lista_salida

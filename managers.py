from pandas import read_excel

import string_helper as sh


class Clasificacion:
  """ Objeto para separar todos los elementos de una clasificacion """
  def __init__(self) -> None:
    self._clase = 'A0'
    self._subdecimal = 'A0'
    self._temaesp = 'A0'
    self._autor = 'A0'
    self._anio = '1000'

  #? GETTERS Y SETTERS ********************************
  @property
  def clase(self): return self._clase
  @property
  def subdecimal(self): return self._subdecimal
  @property
  def temaesp(self): return self._temaesp
  @property
  def autor(self): return self._autor
  @property
  def anio(self): return self._anio

  #? FUNCIONALIDAD DE LA CLASE *****************************
  def sacar_atributos(self, PIPE_A, PIPE_B):
    atributos_pipe_a = PIPE_A.split('.')
    atributos_pipe_b = PIPE_B[1:].split(' ')
    # Rellenar en diccionario
    for index, elem in enumerate(atributos_pipe_a):
      if index == 0: self._clase = elem
      elif index == 1: self._subdecimal = elem
      elif index == 2: self._temaesp = elem
    
    for index, elem in enumerate(atributos_pipe_b):
      if index == 0: self._autor = elem
      elif index == 1: self._anio = elem

    # Revisar los casos especiales
    # ? Autor no tiene letra 
    if self._autor[0].isalpha() is False: 
      self._anio = self._autor
      self._autor = 'A0'

    self.estandarizar_atributos()

  def estandarizar(self, STR):
    largo_max = 10
    ceros = (largo_max - len(STR)) * '0'
    for ind, char in enumerate(STR):
      if char.isalpha() is False:
        str_salida = STR[:ind] + ceros + STR[ind:]
        break
    
    return str_salida

  def estandarizar_atributos(self):
    self._clase = self.estandarizar(self.clase)
    self._subdecimal = self.estandarizar(self.subdecimal)
    self._temaesp = self.estandarizar(self.temaesp)
    self._autor = self.estandarizar(self.autor)

  def __str__(self) -> str:
    return f"""  
      Imprimiendo Atributos de Clasificacion:
      ---------------------------------------
      Clase: {self.clase} Subdecimal: {self.subdecimal} temaesp: {self.temaesp}
      Autor: {self.autor} Año: {self.anio}
      """

class Etiqueta:
  """ Objeto de tipo Etiqueta que contenga toda la informacion de una etiqueta comun """
  def __init__(self, aClasif='', aEncabezado='', aVolumen='', aCopia='') -> None:
    # Asignar valores al objeto
    self.atributos = Clasificacion()
    self._clasif = self.limpiar_clasif(aClasif)
    self._encabezado = aEncabezado if aEncabezado not in ['', ' ', 'nan'] else ''
    self._volumen = aVolumen if aVolumen not in ['', ' ', 'nan'] else '0'
    self._copia = aCopia if aCopia not in ['', ' ', 'nan'] else '1'
    self._PIPE_A = 'XXXXXX'
    self._PIPE_B = 'XXXXXX'
    self._clasif_valida = False
    self._clasif_completa = ''

    # llenar pipe_a_b y marcar como correcta la etiqueta
    self.revisar_clasificacion()
    # Llenar los atributos de clasificacion
    if self.clasif_valida is True:
      self.atributos.sacar_atributos(self._PIPE_A, self.PIPE_B)
    # Crear clasificacion completa
    self.crear_clasif_completa()
  
  #? GETTERS Y SETTERS *********************************
  @property
  def clasif(self): return self._clasif
  @clasif.setter
  def clasif(self, aClasif):
    self._clasif = self.limpiar_clasif(aClasif)
    self.revisar_clasificacion()
    # Llenar los atributos de clasificacion
    if self.clasif_valida is True:
      self.atributos.sacar_atributos(self._PIPE_A, self.PIPE_B)
    self.crear_clasif_completa()
  
  @property
  def volumen(self): return self._volumen
  @volumen.setter
  def volumen(self, aVolumen):
    #* Unicamente acepta numeros
    self._volumen = aVolumen if aVolumen not in ['', ' ', 'nan'] else '0'
    self.crear_clasif_completa()
  
  @property
  def copia(self):return self._copia
  @copia.setter
  def copia(self, aCopia):
    #* Unicamente acepta numeros
    #* No acepta {'', ' ', '1', 'nan'}
    self._copia = aCopia if aCopia not in ['', ' ', 'nan'] else '1'
    self.crear_clasif_completa()
  
  @property
  def encabezado(self): return self._encabezado
  @encabezado.setter
  def encabezado(self, aEncabezado):
    #* Unicamente palabras.
    #* No acepta {'', ' ', 'nan'}
    self._encabezado = aEncabezado if aEncabezado not in ['', ' ', 'nan'] else ''
    self.crear_clasif_completa()

  @property
  def clasif_valida(self): return self._clasif_valida
  @property
  def clasif_completa(self):return self._clasif_completa
  @property
  def PIPE_A(self): return self._PIPE_A
  @property
  def PIPE_B(self): return self._PIPE_B

  #? FUNCIONALIDAD DE LA CLASE *******************************************
  def limpiar_clasif(self, STR:str) -> str:
    ''' Limpiar la clasificación del libro de Caracteres no Necesarios'''
    # * Eliminar caracteres no deseados
    if 'LX' in STR: STR = sh.cortar_string(STR, 'LX')
    if 'MAT' in STR: STR = sh.cortar_string(STR, 'MAT')
    if 'V.' in STR: STR = sh.cortar_string(STR, 'V.')
    if 'C.' in STR: STR = sh.cortar_string(STR, 'C.')
    return STR
  def revisar_clasificacion(self):
    """ Revisar si la clasificacion cumple el estandar """
    # Buscar un espacio en los primeros indices
    if self.clasif.find(' ') < 3:
      self._clasif_valida = False
    elif sh.revisar_corte_pipe(self.clasif) and sh.revisar_pipeB(self.clasif):
      pos_div, sum = sh.buscar_pipe(self.clasif)
      self._PIPE_A = self.clasif[:pos_div].replace(' ','.')
      self._PIPE_B = '.' + self.clasif[pos_div+sum:]
      self._clasif_valida = True
      self._clasif = self._PIPE_A + ' ' + self._PIPE_B
    else:
      self._clasif_valida = False
  def crear_clasif_completa(self):
    ''' Genera un atributo completo de clasificacion '''
    clasif_completa = self.clasif
    #* Manejo de el parametro de Encabezado
    clasif_completa = self.encabezado + ' ' + clasif_completa if self.encabezado != '' else clasif_completa
    #* Manejo de el parametro de volumen
    clasif_completa += ' V.' + self.volumen if self.volumen != '0' else ''
    #* Manejo de el parametro de copia
    clasif_completa += ' C.' + self.copia if self.copia != '1' else ''
    self._clasif_completa = clasif_completa

  def __str__(self) -> str:
    return f"""  
      Imprimiendo Etiqueta:
      ---------------------
      Clasificacion completa: {self._clasif_completa}
      Clasificacion correcta? {self._clasif_valida}
      
      Atributos:
      ----------
      Volumen: {self._volumen} Copia: {self._copia} Encabezado: {self._encabezado}
      Clasificacion: {self._clasif} PIPES: {self._PIPE_A}|{self._PIPE_B}

      {self.atributos}
      """

class Libro:
  """ Clase para generar objectos de tipo libro con todos sus datos """
  def __init__(self, aID=1, aTitulo='', aCbarras='', aClasif='', aVolumen='0', aCopia='1', aEncabezado=''):
    # Asignar Valores al objeto
    self._titulo = aTitulo
    self._cbarras = aCbarras
    self._ID = aID
    # Crear objeto de tipo etiqueta
    self.etiqueta = Etiqueta(
      aClasif= aClasif,
      aEncabezado= aEncabezado,
      aVolumen= aVolumen,
      aCopia= aCopia,
    )
    self._estatus = 'Valid' if self.etiqueta.clasif_valida else 'Error'
    # Agregar libro a una lista de objetos
    # Libro.all.append(self)
  
  #? GETTERS Y SETTERS *****************************
  @property
  def titulo(self): return self._titulo
  
  @property
  def cbarras(self): return self._cbarras

  @property
  def ID(self): return self._ID
  @ID.setter
  def ID(self, aID): self._ID = aID

  @property
  def estatus(self): return self._estatus
  @estatus.setter
  def estatus(self, aEstatus): self._estatus = aEstatus
  
  @classmethod
  def llenar_desde_excel(cls, ruta):
    df = read_excel(ruta, header=0)
    header = df.head(0)

    lista_libros = []
    for ind in df.index:
      # Manejo del volumen en los datos      
      lista_libros.append(Libro(
        aID = ind,
        aTitulo= str(df['Título'][ind]) if 'Título' in header else '',
        aCbarras= str(df['C. Barras'][ind]) if 'C. Barras' in header else '',
        aClasif= str(df['Clasificación'][ind]) if 'Clasificación' in header else '',
        aCopia= str(df['Copia'][ind]) if 'Copia' in header else '',
        aEncabezado= str(df['Encabezado'][ind]) if 'Encabezado' in header else '',
        aVolumen= str(df['Volumen'][ind]) if 'Volumen' in header else ''
      ))
    
    return lista_libros
  
  #? IMPRIMIR OBJETO **********************
  def __str__(self) -> str:
    return f"""  
      Imprimiendo Libro:
      ---------------------
      Libro num. : {self._ID}
      Titulo: {self._titulo}
      Codigo de Barras: {self._cbarras}

      {self.etiqueta}
      """

class ManejoTabla:
  """ Clase para manejo de Tabla """
  tabla_principal = []
  formato_tabla = []
  lista_libros = []
  lista_modificados = {}
  _tabla_len = 0
  estatus_color = {'Error':'#F04150', 'Valid':'#FFFFFF', 'Selected':'#498C8A', 'Modify':'#E8871E'}

  def agregar_elemento(self, aLibro:Libro):
    """ Agregar un elemento a la tabla general """
    color = self.estatus_color[aLibro.estatus]
    formato = (self.tabla_len, color)
    principal = [
      aLibro.etiqueta.clasif_completa, 
      aLibro.etiqueta.PIPE_A, 
      aLibro.etiqueta.PIPE_B, 
      aLibro.estatus
    ]
    self.tabla_principal.append(principal)
    self.lista_libros.append(aLibro)
    self.formato_tabla.append(formato)
    self._tabla_len += 1
    print(
      f"""
      [INFO] Elemento Agregado
      {aLibro}
      """
    )
    # self.diccionario_estatus[largo_tabla] = estatus    

  def crear_tabla(self, aRuta:str):
    lista_libros = Libro.llenar_desde_excel(aRuta)
    for libro in lista_libros: 
      # print(libro)
      self.agregar_elemento(libro)

  def seleccionar_tabla(self):
    # recorrer tabla por completo
    for num_libro in range(self.tabla_len):
      estatus = self.lista_libros[num_libro].estatus
      if estatus != "Error":
        self.actualizar_estatus_elemento(num_libro,"Selected")

  def deseleccionar_tabla(self):
    # recorrer tabla por completo
    for num_libro in range(self.tabla_len):
      estatus = self.lista_libros[num_libro].estatus
      if estatus != "Error":
        self.actualizar_estatus_elemento(num_libro,"Valid")

  def reset_tabla(self):
    """ Reiniciar datos de la tabla por completo """
    self.tabla_principal = []
    self.formato_tabla = []
    self.lista_libros = []
    self._tabla_len = 0
    # self.diccionario_estatus = {}

  def actualizar_estatus_elemento(self, num_elem, aEstatus):
    self.lista_libros[num_elem].estatus = aEstatus
    self.tabla_principal[num_elem][3] = aEstatus
    color = self.estatus_color[aEstatus]
    formato = (num_elem, color)
    self.formato_tabla[num_elem] = formato

  def agregar_elemento_modificado(self, num_elem, aLibro, aClasifAnterior):
    self.lista_modificados[num_elem] = (aLibro, aClasifAnterior)
    print('Elemento agregado')
  
  def actualizar_elemento(self, num_elem, aLibro):
    principal = [
      aLibro.etiqueta.clasif_completa, 
      aLibro.etiqueta.PIPE_A, 
      aLibro.etiqueta.PIPE_B, 
      aLibro.estatus
    ]
    self.tabla_principal[num_elem] = principal
    self.lista_libros[num_elem] = aLibro

  def exportar_libros_selecionados(self):
    libros_a_imprimir = []
    #* Recorrer todos los libros de la tabla
    for ind in range(self.tabla_len):
      estatus = self.lista_libros[ind].estatus
      if estatus == "Selected":
        libros_a_imprimir.append(self.lista_libros[ind])
    
    # TODO crear una funcion de ordenamiento
    return libros_a_imprimir

  def crear_reporte_modificados(self, path:str, nombre:str,):
    '''Genera un reporte en un txt de libros modificados'''
    if not self.lista_modificados: return False # Revisar si tenemos datos
    
    txt_path = f'{path}/{str(nombre)}_modificados.txt'
    modif_file = open(txt_path, 'w', encoding="utf-8")
    modif_file.write(f'Lista de Clasificaciones Modificadas\n')
    for libro, clasif_anterior in self.lista_modificados.values():
      titulo_comprimido = libro.titulo[:40] if len(libro.titulo) > 40 else libro.titulo + (' '*(40 - len(libro.titulo)))
      texto_libro = f"{titulo_comprimido} | {libro.etiqueta.clasif_completa} | {clasif_anterior} | {libro.cbarras}"
      modif_file.write(texto_libro)
      modif_file.write('\n')
    modif_file.close()

  def crear_reporte_QRO(self, path:str, nombre:str,):
    '''Genera un reporte en un txt de libros modificados'''
    if not self.lista_modificados: return False # Revisar si tenemos datos
    
    txt_path = f'{path}/{str(nombre)}_QRO.txt'
    modif_file = open(txt_path, 'w', encoding="utf-8")
    for libro, clasif_anterior in self.lista_modificados.values():
        modif_file.write(libro.cbarras)
        modif_file.write('\n')
    modif_file.close()
    return True

  @property
  def tabla_len(self): return self._tabla_len


if __name__ == '__main__':
  # ruta1 = 'C:/Users/EQUIPO/Desktop/Proyectos_biblioteca/Etiquetas/Pruebas/Mario_excel.xlsx'
  # libros = Libro.llenar_desde_excel(ruta1)
  # print(libros[0])
  etiqueta1 = Etiqueta('B2430.D484 .P6818 1997', '', '1', '1')
  print(etiqueta1)
  # etiqueta1 = Etiqueta('B2430.D484 P6818 1997', '', '', '1')
  # print(etiqueta1)
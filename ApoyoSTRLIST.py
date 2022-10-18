import re

'''
Paquete de Funciones de apoyo para el trabajo de Strings y Manejo de Grupos para programa Descarte
'''

letras_array = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def checarLetras(STR):
  '''Cuenta las letras de un string'''
  C_letras = len(re.findall('[ABCDEFGHIJKLMNOPQRSTUVWXYZ]',STR))
  return C_letras != 0

def buscarEspacioPunto(STR):
  '''
    Busca " ." dentro de un String
    Retorna la posicion del " ."
  '''
  pos = 0
  if ' .' in STR: pos = STR.index(' .')
  return pos

def buscarEspacio(STR):
  '''Buscar ' ' dentro de un string. Retorna la posición de ' ' '''
  pos = 0
  if ' ' in STR: pos = STR.index(' ')
  return pos

def buscarPuntoEspacio(STR):
  ''' Busca ". " y regresa la posición de este '''
  pos = 0
  if '. ' in STR: pos = STR.index('. ')
  return pos

def buscarPIPE(STR):
  ''' Retorna la posición para partir PIPE '''
  pos = 0
  pos = buscarEspacioPunto(STR)
  if pos != 0: return pos, 2
  pos = buscarPuntoEspacio(STR)
  if pos != 0: return pos, 2
  pos = buscarEspacio(STR)
  if pos != 0: return pos, 1
  return pos, 0

def contarSeparadores(STR):
  '''
    Detecta y cuenta los separadores basicos ('.',',',' ') \n
    Tambien se toman en cuenta (' .', '. ') \n
    Retorna la cantidad de separadores encontrados
  '''
  sep_cont = len(re.findall('[. ,]', STR))
  length = len(STR)
  if sep_cont != 0:
    for pos in range(length):
      # Caso para detectar ". " punto + espacio
      if STR[pos] == '.' and pos + 1 <= (length-1):
        if STR[pos + 1] == ' ': sep_cont = sep_cont - 1
      # Caso para detectar "  " doble espacios
      if STR[pos] == ' ' and pos + 1 <= (length-1):
        if STR[pos + 1] == ' ': sep_cont = sep_cont - 1
    if 'MAT' in STR: sep_cont = sep_cont - 2
    elif 'V.' in STR: sep_cont = sep_cont - 2
  return sep_cont

def pos_Separadores(STR):
  ''' Retorna una lista con la posicion de los separadores (',', '.', ' ')'''
  pos = [0,0,0]
  if '.' in STR: pos[0]=STR.index('.') #Checa si existe algun punto en el string
  if ' ' in STR: pos[1]=STR.index(' ') #Checa si existe algun espacio en el string, sin marcar error
  if ',' in STR: pos[2]=STR.index(',') #Checa si existe alguna coma en el string sin marcar error
  return pos

def pos_corte(sep_pos):
  ''' Retorna la posición del separador más cercana (',', '.', ' ') '''
  punto_p = sep_pos[0] #Posicion de Punto
  espa_p = sep_pos[1]  #Posicion de Espacio
  coma_p = sep_pos[2]  #Posicion de Coma  //Caso especial

  if espa_p == 0 or punto_p == 0: main_pos = max(punto_p,espa_p)
  elif abs(punto_p - espa_p) == 1: main_pos = max(punto_p,espa_p)
  elif punto_p - espa_p < 0: main_pos = punto_p
  elif punto_p - espa_p > 0: main_pos = espa_p
  return main_pos

def revisarSep(STR):
  ''' Revisa casos sin Estandar o Extraños '''
  pos_div, sum = buscarPIPE(STR)
  if pos_div == 0: return False
  PIPE_A = STR[:pos_div]
  PIPE_B = STR[pos_div+sum:]
  A = contarSeparadores(PIPE_A)
  B = contarSeparadores(PIPE_B)
  if A > 3: return False
  if B > 1: return False
  return True

def revisarPipeB(STR, tipo=0):
  if tipo != 0:
    if tipo == 1: char = 'LX' # Para casos con XL
    elif tipo == 2: char = 'MAT' # Para casos con MAT COM
    elif tipo == 3  or tipo == 5: char = 'V.'
    elif tipo == 4: char = 'C.'
    text_pos = STR.index(char) 
    STR = STR[:text_pos]
  posPIPE, flag = buscarPIPE(STR)
  newSTR = STR[::-1]
  length = len(newSTR)
  for pos in range(length):
    if newSTR[pos] in letras_array: 
      newpos = pos
      break
  #if newpos > 4: print("Tiene año")
  #print("Cadena: ", STR, "posPIPE ", posPIPE)
  #print("Cadena invertida: ", newSTR, "posPIPE ", newpos+1)
  newposPIPE = length-1-(newpos+flag)
  if posPIPE == newposPIPE: return True
  return False

def Porcent(X,MAX):
  ''' Retorna el valor en porcentaje de una variable '''
  return round(((X/MAX)*100),2)

def MaxCheck(MAX,X):
  ''' Checa si el numero (x) es mayor al maximo '''
  if X >= MAX: MAX = X
  return MAX

def Limpieza(STR):
  ''' Remueve los caracteres no deseados de una cadena '''
  STRPrueba = STR
  CharNoDeseado = ". ,-"
  for x in CharNoDeseado:
    STRPrueba = STRPrueba.replace(x,'')
  return STRPrueba

def Estandarizar(STR, maxLen):
  '''
    Estandariza las cadenas a un tamaño fijo
    @STR: Cadena a estandarizar
    @maxLen: Tamanio maximo que ha obtenido una cadena
  '''
  #Toma el elemento de la lista de diccionarios, funciona de elemento en elemento
  length = len(STR)
  dif = maxLen - length
  #creamos una cadena llena de ceros para estandarizar
  cadena_ceros = '0' * dif
  final_STR = STR + cadena_ceros 
  #Reemplaza el valor estadarizado en la lista
  return final_STR

def clas_maker(clas, vol, cop, flag):
  ''' 
  Retorna una clasificacion completa
  @clas: Clasificación incompleta
  @vol, cop, flag: Parametros a agregar
  '''
  STR_clas = clas
  # caso principal tenemos datos
  if vol != '':
    # Checar si es de tipo texto completo o solo numero
    if 'V.' in vol: STR_clas += ' ' + vol
    else: STR_clas += ' V.' + vol
  
  if cop not in ('1',''): STR_clas += ' C.' + cop
  return STR_clas

def STR_limit(STR, size):
  ''' Limitar el tamañó de un string'''
  if len(STR) > size: return STR[:size] + '...'
  else: return STR

def STR_cutter(STR, char):
  '''Funcion para cotar una seccion de una cadena con base a un caracter'''
  text_pos = STR.index(char)
  return STR[:text_pos]

if __name__ == '__main__':
  pass

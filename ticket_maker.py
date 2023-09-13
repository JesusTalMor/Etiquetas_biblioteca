from managers import Etiqueta

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

class DatabaseMaker:
  """ Clase implementada para crear bases de datos con txt tipo csv """
  def crear_database(self, aListaLibros:list, aNombre:str, aRuta:str):
    if len(aListaLibros) == 0: return # Revisar que tenemos datos
    txt_path = f'{aRuta}/{aNombre}_etiquetas.txt'
    database_writer = open(txt_path, 'w', encoding="utf-8")
    #* Crear encabezado de base de datos
    for num in range(9):
      database_writer.write(f'C{num},')
    database_writer.write('\n')
    #* Recorrer todos los libros
    for libro in aListaLibros:
      #* Crear lista para base de datos
      lista_etiqueta = self.separar_lista(libro.etiqueta)
      limpiar_lista = [x for ind, x in enumerate(lista_etiqueta) if x != '' or ind == 0]
      #* Recorrer todos los elementos de la etiqueta.
      for elem in limpiar_lista: database_writer.write(f'{elem},')
      if len(limpiar_lista) < 9: database_writer.write(','*(9-len(limpiar_lista)))
      database_writer.write('\n')
    database_writer.close()

    
  def separar_lista(self, aEtiqueta:Etiqueta):
    """ Recibe un diccionario y crea una lista para imprimir """
    lista_salida = []
    #* Usando un diccionario obtener todos los elementos
    encabezado = [aEtiqueta.encabezado]
    clasif = self.separar_clasificacion(aEtiqueta.clasif)
    volumen = ['V.' + aEtiqueta.volumen] if aEtiqueta.volumen != '0' else ['']
    copia = ['C.' + aEtiqueta.copia] if aEtiqueta.copia != '1' else ['']
    #* Juntar todos los elementos
    lista_salida.extend(encabezado)
    lista_salida.extend(clasif)
    lista_salida.extend(volumen)
    lista_salida.extend(copia)
    #* Limpiar elementos vacios
    # lista_salida = [x for x in lista_salida if x != '']
    # print('Entrada', str_dict, sep='\n')
    # print('Salida', lista_salida, sep='\n')
    return lista_salida
  def separar_clasificacion(self, STR:str):
    """ Separa un Clasificación y retorna una lista"""
    lista_salida = []
    # * Separar por espacios separa PIPE A de PIPE B y la anterior en autor y año
    space_list = STR.split(' ')  
    # Ejemplo 'PQ7298.424.A76 .O744 2007' -> [PQ7298.424.A76] [.O744] [2007]
    # Ejemplo 'PQ7298 424 A76 .O744 2007' -> [PQ7298] [424] [A76] [.O744] [2077]
    # Ejemplo 'PQ 7298.424.A76 .O744 2007' -> [PQ] [7298.424.A76] [.O744] [2007]
    # Ejemplo 'PQE 7298.424.A76 .O744 2007' -> [PQE] [7298.424.A76] [.O744] [2007]
    #* Separa el PIPE A en sus atributos: Categorias XD
    pipe_a = space_list.pop(0) 
    # Ejemplo [PQ7298.424.A76] [.O744] [2007] -> [PQ7298.424.A76] | [.O744] [2007]
    # Ejemplo [PQ7298] [424] [A76] [.O744] [2077] -> [PQ7298] | [424] [A76] [.O744] [2077]
    # Ejemplo [PQ] [7298.424.A76] [.O744] [2007] -> [PQ] | [7298.424.A76] [.O744] [2007]
    # Ejemplo [PQE] [7298.424.A76] [.O744] [2007] -> [PQE] | [7298.424.A76] [.O744] [2007]
    pipe_a = pipe_a.split('.') 
    # Ejemplo [PQ7298.424.A76] -> [PQ7298] [424] [A76]
    # Ejemplo [PQ7298] -> [PQ7298]
    # Ejemplo [PQ] -> [PQ] 
    # Ejemplo [PQE] -> [PQE]
    letras_tema = pipe_a.pop(0)
    # Ejemplo [PQ7298] [424] [A76] -> [PQ7298] | [424] [A76]
    # Ejemplo [PQ7298] -> [PQ7298]
    # Ejemplo [PQ] -> [PQ] 
    # Ejemplo [PQE] -> [PQE]
    #* Trabajar en separar letras y numeros
    #! Poco rebuscado pero funcional
    # Intenta obtener un tercer elemento sino sigue con el basico  
    if letras_tema[2] in alphabet: letras_tema = [letras_tema[:3], letras_tema[3:]]
    elif letras_tema[1] in alphabet: letras_tema = [letras_tema[:2], letras_tema[2:]]
    else: letras_tema = [letras_tema[:1], letras_tema[1:]]
  
    # Ejemplo PQ7298 -> [PQ, 7298] si 2 letras otro caso P7298 -> [P, 7298]
    # Ejemplo [PQ7298] -> [PQ, 7298]
    # Ejemplo [PQ] -> [PQ] No existe 3 elemento, truena el programa 
    # Ejemplo [PQE] -> [PQE] Si existe 3 elemento, No truena el programa
    # print(space_list, pipe_a, letras_tema, sep='\n')
    #* Juntar todas las listas en la salida
    lista_salida.extend(letras_tema)
    lista_salida.extend(pipe_a)
    lista_salida.extend(space_list)
    # Ejemplo [PQ, 7298] + [424, A76] + [.O744, 2007] -> ['PQ', '7298', '424', 'A76', '.O744', '2007']
    # Ejemplo [PQ, 7298] + [424] [A76] [.O744] [2077] -> [PQ, 7298, 424, A76, .O744, 2077]
    # Ejemplo [PQ] -> [PQ] No existe 3 elemento, truena el programa 
    # Ejemplo [PQE] -> [PQE] Si existe 3 elemento, No truena el programa
    # print('Entrada', STR, sep='\n')
    # print('Salida Final', lista_salida, sep='\n')
    return lista_salida

if __name__ == "__main__":
  pass
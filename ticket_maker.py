from managers import Etiqueta, Libro


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

  def crear_instrucciones_pegado(self, aListaLibros:list, aNombre:str, aRuta:str):
    if len(aListaLibros) == 0: return # Revisar que tenemos datos
    txt_path = f'{aRuta}/{aNombre}_instrucciones.txt'
    instruc_writer = open(txt_path, 'w', encoding="utf-8")
    #* Recorrer todos los libros
    for ind, libro in enumerate(aListaLibros):
      #* Escribir en el archivo      
      indice = str(ind)
      ceros = '0'*(len(str(len(aListaLibros))) - len(indice))
      indice = ceros + indice
      cbarras = libro.cbarras
      titulo = libro.titulo[:40] if len(libro.titulo) > 40 else libro.titulo + ('_'*(40 - len(libro.titulo)))
      clasif = libro.etiqueta.clasif_completa
      texto = f'{indice}|{cbarras}|{titulo.upper()}|{clasif}\n'
      print(texto)
      instruc_writer.write(texto)
    instruc_writer.close()

  def separar_lista(self, aEtiqueta:Etiqueta):
    """ Recibe un diccionario y crea una lista para imprimir """
    lista_salida = []
    #* Usar atributos del objeto para llenar una lista
    atributos_lista = aEtiqueta.atributos_lista()
    tema_separado = self.separar_tema(atributos_lista.pop(0))
    volumen = ['V.' + aEtiqueta.volumen] if aEtiqueta.volumen != '0' else ['']
    copia = ['C.' + aEtiqueta.copia] if aEtiqueta.copia != '1' else ['']
    #* Juntar todos los elementos
    lista_salida.append(aEtiqueta.encabezado) # Agregar encabezado
    lista_salida.extend(tema_separado)
    lista_salida.extend(atributos_lista)
    lista_salida.extend(volumen)
    lista_salida.extend(copia)

    return lista_salida

  def separar_tema(self, STR:str):
    if len(STR) >= 3 and STR[2].isalpha(): salida = [STR[:3], STR[3:]]
    elif STR[1].isalpha(): salida = [STR[:2], STR[2:]]
    else: salida = [STR[:1], STR[1:]]

    return salida

if __name__ == "__main__":
  db = DatabaseMaker()
  print(db.separar_tema('B111'))
  print(db.separar_tema('BV11'))
  print(db.separar_tema('BVD1'))
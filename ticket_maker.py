import pandas as pd

from managers import Etiqueta, Libro


class DatabaseMaker:
  """ Clase implementada para crear bases de datos con txt tipo csv """
  def crear_database(self, aListaLibros:list, aRuta:str, aNombre=''):
    if len(aListaLibros) == 0: return # Revisar que tenemos datos
    # txt_path = f'{aRuta}/{aNombre}_etiquetas.txt' # Version sin carpeta
    txt_path = f'{aRuta}/Etiquetas.txt' # Version generada usando carpeta auxiliar
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
    print('[INFO] Base de Datos Creada Correctamente')

  def crear_instrucciones_pegado(self, libros_lista:list, ruta:str, nombre=''):
    if len(libros_lista) == 0: return # Revisar que tenemos datos
    nombre = f'{nombre}_Instrucciones' if len(nombre) != 0 else 'Instrucciones'
    #* Crear dataframe de los datos
    instruc_df = {
      'Indice' : [index for index in range(len(libros_lista))],
      'Clasificación' : [libro.etiqueta.clasif_completa for libro in libros_lista],
      'Título'        : [libro.titulo for libro in libros_lista],
      'C. Barras'     : [libro.cbarras for libro in libros_lista],
    }
    instruc_df = pd.DataFrame(instruc_df)
    self.escribir_excel(ruta, nombre, instruc_df)
    print('[INFO] Archivo de Instrucciones Creado Correctamente')
  
  def escribir_excel(self, ruta, nombre, dataframe):
    """ Escribe un archivo excel usando un dataframe """
    excel_path = f'{ruta}/{nombre}.xlsx'
    try:
      excel_writer = pd.ExcelWriter(excel_path, mode='w')
      dataframe.to_excel(excel_writer, index=False)
      excel_writer.close()
      print(f'[INFO] Archivo Escrito Correctamente')
    except:
      print(f'[WARNING] Archivo Abierto Creando Copia')
      excel_path = f'{ruta}/{nombre}_copia.xlsx'
      excel_writer = pd.ExcelWriter(excel_path, mode='w')
      dataframe.to_excel(excel_writer, index=False)
      excel_writer.close()
      print(f'[INFO] Archivo Escrito Correctamente')

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
  pass
  # db = DatabaseMaker()
  # print(db.separar_tema('B111'))
  # print(db.separar_tema('BV11'))
  # print(db.separar_tema('BVD1'))
  # dinero_inicial = 19000 * 0.1 * 12
  # dinero = dinero_inicial
  # interes = 11.29
  # periodo = 100
  # # total = 4300000000
  # for n in range(1, periodo+1):
  #   dinero += dinero_inicial # Anadir dinero cada ano
  #   dinero = dinero * (1 + (interes/100.0))
  #   porcentaje = ((dinero / dinero_inicial) * 100) - 100
  #   if n%5 == 0:
  #     print(f'Dinero acumulado al ano {n} = {dinero:.2f} $')
  #     print(f'Aumento en porcentaje de {porcentaje:.2f} %')
  #     print('-'*100)
  # # print(f'Total de Dinero acumulado en {periodo} anos es: {dinero}')
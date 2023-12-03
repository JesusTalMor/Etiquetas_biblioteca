import os
import sys
from tkinter import Tk, messagebox


#?#********** Función apoyo para relative path *********#
def resource_path(relative_path):
  """ Get absolute path to resource, works for dev and for PyInstaller """
  try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

window = Tk()
window.iconbitmap(resource_path('Assets/ticket_icon.ico'))
window.withdraw()

# ? POP_up de advertencia (Warning)
def warning_pop(option:str):
  """ Generar un pop up de Advertencia
    Opciones
    ----------
    selection : No se seleccionaron elementos de etiquetas
    no_file   : No se tiene un archivo de excel para usar
  """
  posible_options = {
    'selection' : (
      'No selection',
      f'!Advertencia!\n Seleccione elementos a imprimir'
    ),
    'no_file' : (
      'No Excel File',
      f'!Fallo!\n Selecione un archivo de Excel'
    ),
  }
  title, msg = posible_options[option]
  messagebox.showwarning(title=title, message=msg, parent=window)

def error_pop(option:str):
  """ Genera un pop up de error 
    Opciones
    ---------
    excel_file : El archivo de excel cuenta con errores graves
  """
  posible_options = {
    'excel_file' : (
      'Excel File Error',
      f'!Fallo!\n Ninguna Etiqueta se cargo'
    ),
  }
  title, msg = posible_options[option]
  messagebox.showerror(title=title, message=msg, parent=window)


def info_pop(option:str, aditional=''):
  """ Genera un pop up de informacion 
    Opciones
    ---------
    success   : El programa finalizo con exito
    license   : Informacion en licencia de la aplicacion. Aditional(Firma)
    about     : Informacion del programa en general.      Aditional(Version)
    book_info : Informacion adicional del libro.          Aditional(Titulo, Cbarras)
  """
  posible_options = {
    'success' : (
      'Program Success',
      f'!Felicidades!\n El programa finalizó con éxito'
    ),
    'license' : (
      'Program License',
      f'Programa bajo uso de Licencia.\nTecnológico de Monterrey {aditional}\n!No reproducir sin permiso!'
    ),
    'about' : (
      'About Program',
      f'Manejador de Etiquetas.\nVersión: {aditional}\n Por: Jesus Talamantes Morales\n CEL: 442 343 6407 ©2022-2023'
    ),
    'book_info': (
      'Book Aditional Info',
      f'Título del Libro: {aditional[0]}\n Código de Barras: {aditional[1]}'
    )

  }
  title, msg = posible_options[option]
  messagebox.showinfo(title=title, message=msg, parent=window)

def ask_pop(option:str):
  """ Genera un pop up de pregunta  
    Opciones
    ----------
    save : Guardar el progreso del programa
  """
  posible_options = {
    'save' : (
      'Save Program Progress',
      f'Desea guardar su progreso ?'
    ),
  }
  title, msg = posible_options[option]
  return messagebox.askokcancel(title=title, message=msg, parent=window)


if __name__ == "__main__":
  pass
  




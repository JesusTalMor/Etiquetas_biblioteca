from tkinter import messagebox


# # ? POP_up de advertencia (Warning)
##########################################################
def warning_element():
  msg = f'!Advertencia!\nEl reporte de registros modificados no se generará.'
  messagebox.showwarning("Inicio Elemento", msg)

def warning_excel_file():
  msg = f'!Fallo!\nSeleccione un archivo de Excel'
  messagebox.showwarning("No Excel File", msg)

def warning_excel_file_data_error():
  msg = f'!Advertencia!\n Algunas Etiquetas no logran cargarse'
  messagebox.showwarning("File Data Warning", msg)

def warning_folder():
  msg = f'!Fallo!\nSeleccione una carpeta de Salida'
  messagebox.showwarning("No Folder", msg)
##########################################################

# # ? up de Error (Error)
##########################################################
def error_excel_file():
  msg = f'!Fallo!\n Ninguna Etiqueta se cargo'
  messagebox.showerror("Excel File Error", msg)
##########################################################

# # ? up de Informacion (Info)
##########################################################
def success_program():
  msg = f'Felicidades\n El programa finalizó con exito'
  messagebox.showinfo("Finalize", msg)

def info_license():
  msg = f'Programa Bajo Licencia del Tecnológico de Monterrey\n !No reproducir sin permiso!'
  messagebox.showinfo("Licencia", msg)

def info_about():
  msg = f'Programa Generador de Etiquetas\n Por: Jesus Talamantes Morales 2022'
  messagebox.showinfo("Licencia", msg)

# # ? up de OkCancel Ask (askokcancel)
##########################################################
def check_images():
  msg = f'Imágenes Generadas\n Presione Aceptar para continuar con su PDF'
  answer = messagebox.askokcancel("Confirmar", msg)
  return answer

if __name__ == "__main__":
  print(check_images())




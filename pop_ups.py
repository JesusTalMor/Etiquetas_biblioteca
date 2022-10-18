from tkinter import messagebox


# # ? POP_up de advertencia (Warning)
##########################################################
def pop_warning_element():
  msg = f'!Advertencia!\nEl reporte de registros modificados no se generará.'
  messagebox.showwarning("Inicio Elemento", msg)

def pop_warning_excel_file():
  msg = f'!Fallo!\nSeleccione un archivo de Excel'
  messagebox.showwarning("No Excel File", msg)

def pop_warning_excel_file_data_error():
  msg = f'!Advertencia!\n Algunas Etiquetas no logran cargarse'
  messagebox.showwarning("File Data Warning", msg)

def pop_warning_folder():
  msg = f'!Fallo!\nSeleccione una carpeta de Salida'
  messagebox.showwarning("No Folder", msg)
##########################################################

# # ? POP_up de Error (Error)
##########################################################
def pop_error_excel_file():
  msg = f'!Fallo!\n Ninguna Etiqueta se cargo'
  messagebox.showerror("Excel File Error", msg)
##########################################################

# # ? POP_up de Informacion (Info)
##########################################################
def pop_success_program():
  msg = f'Felicidades\n El programa finalizó con exito'
  messagebox.showinfo("Finalize", msg)

def pop_info_license():
  msg = f'Programa Bajo Licencia del Tecnológico de Monterrey\n !No reproducir sin permiso!'
  messagebox.showinfo("Licencia", msg)

def pop_info_about():
  msg = f'Programa Generador de Etiquetas\n Por: Jesus Talamantes Morales 2022'
  messagebox.showinfo("Licencia", msg)

# # ? POP_up de OkCancel Ask (askokcancel)
##########################################################
def pop_check_images():
  msg = f'Imagenes Generadas\n Presione Aceptar para continuar con su PDF'
  answer = messagebox.askokcancel("Confirmar", msg)
  return answer

if __name__ == "__main__":
  print(pop_check_images())




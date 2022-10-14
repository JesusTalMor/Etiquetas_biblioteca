from fpdf import FPDF

def create_pdf():
  fpdf = FPDF()

  #* Add a blank page to the pdf
  fpdf.add_page()
  
  #* Change the color of the text
  fpdf.set_text_color(34,78,90)

  #* Set the font to use
  fpdf.set_font("Arial", size=70)
  
  #* Add some text to the pdf
  fpdf.text(x=50, y=50, txt='Hello World')

  #* Add an image to the pdf
  fpdf.image('GUI_look.png',100,100,w=120)

  #* Save the pdf document custom made
  fpdf.output('output.pdf')


if __name__ == '__main__':
  create_pdf()
from PyPDF2 import PdfFileWriter, PdfFileReader
import fitz


import fitz

doc = fitz.open('docs/39-2021 evidenziata.pdf')
page = doc[0]  # get first page
rect = fitz.Rect(0, 70.0, page.rect.width - 20.0, page.rect.height - 60.0)  # define your rectangle here
text = page.get_textbox(rect)  # get text from rectangle
clean_text = ' '.join(text.split())

print(clean_text)

# with open("docs/sent. 103 - 2021 v.pdf", "rb") as in_f:
#     input1 = PdfFileReader(in_f)
#     output = PdfFileWriter()

#     numPages = input1.getNumPages()

#     sizes = input1.pages[0].mediabox

#     print(sizes[3])

#     x, y, w, h = (0, 70.0, float(sizes[2])-20.0, float(sizes[3])-120.0)

#     page_x, page_y = input1.getPage(0).cropBox.getUpperLeft()
#     upperLeft = [page_x.as_numeric(), page_y.as_numeric()] # convert PyPDF2.FloatObjects into floats
#     new_upperLeft  = (upperLeft[0] + x, upperLeft[1] - y)
#     new_lowerRight = (new_upperLeft[0] + w, new_upperLeft[1] - h)

#     for i in range(numPages):
#         page = input1.getPage(i)
#         page.cropBox.upperLeft  = new_upperLeft
#         page.cropBox.lowerRight = new_lowerRight

#         output.addPage(page)

#     with open("docs/out.pdf", "wb") as out_f:
#         output.write(out_f)




# with open("docs/out.pdf", "rb") as in_f:
#     reader = PdfFileReader(in_f)
#     number_of_pages = len(reader.pages)

#     # Estraggo l'intero contenuto dei PDF
#     text = ""
#     for i in range(number_of_pages):
#         page = reader.getPage(i)
#         text += page.extract_text()

#     print(text)
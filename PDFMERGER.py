# is program ko bana na main mujha 3 sa 4 din lagya han 22-3-2025
import PyPDF2 as p
import os
merger = p.PdfWriter()
files = os.listdir()
for file in files:
 if file.endswith(".pdf"):
  try:
     merger.append(file)
  except:
    print("This file cannot be merge.Due to some Error")

merger.write("merge-pdf.pdf")
merger.close()
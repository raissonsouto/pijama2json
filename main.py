import PyPDF2
import json

with open('2022.2.pdf', 'rb') as pdf_file:

    pdf_reader = PyPDF2.PdfReader(pdf_file)
    data = []

    for page_num in range(len(pdf_reader.pages)):

        page = pdf_reader.pages[page_num]
        lines = page.extract_text().split('\n')
        data.append(lines)

for dt in data:
    print(dt)

print(data)

for i in range(0, len(data), 4):
    id_ = data[i].split(" - ")[i]
    turma = " ".join(data[0].split(" - ")[1].split()[:-2])
    professor = data[-1].replace(",", "").replace("- ", "")
    aulas = []
    sala = ""
    print(f"id: {id_}")
    print(f"turma: {turma}")
    print(f"professor: {professor}")
    print(f"sala: {sala}")

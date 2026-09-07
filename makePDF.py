# Author: Rajiv Williams
# Date: November 20, 2025
# Description: This script converts text files to PDF format using the FPDF library.

import os
import io
import textwrap

from pathlib import Path
from fpdf import FPDF, XPos, YPos

#docx2pdf import convert for Windows only where Word Installed
from docx2pdf import convert

#convert("input.docx", "output.pdf")

#Libre Office command for all systems
import subprocess
subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', 'input.docx', '--outdir', 'tmp'], check=True)

## Program Begin

input_path = input("Enter the file / directory path you would like to convert to PDF: ")
output_path = "./output/"
temp_path = "./temp/temp.txt"
file_names = []

# Function to convert text file to PDF
def text_to_pdf(input_txt, output_pdf):
    pdf = FPDF()
    
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    # pdf.add_font("Arial", '', 'arial.ttf', uni=True)
    # pdf.set_font("helvetica", size=12)
    pdf.add_font(fname="DejaVuSansCondensed.ttf")
    pdf.set_font("DejaVuSansCondensed", size=12)
    # pdf.add_font(fname="./symbola/Symbola.ttf")
    # pdf.set_font("Symbola", size=12)

    a4_width = 210
    margin = 10
    effective_width = a4_width - 2 * margin
    char_width = pdf.get_string_width('a') # Width of a single character
    max_chars_per_line = int(effective_width / char_width)

    print(f"Processing file: {input_txt}")
    
    with open(input_txt, 'r') as file:
            
        for line in file:
            #pdf.multi_cell(0, 10, line)
            wrapped_lines = textwrap.wrap(line.strip(),width=max_chars_per_line)

            if not wrapped_lines:
                pdf.ln()  # Handle empty lines

            for wrap in wrapped_lines:
                pdf.cell(0, 5, text=wrap, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')

        if(not os.path.exists(output_path)):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        pdf.output(output_pdf)
        print(f"PDF created successfully: {output_pdf}")

    


if os.path.isdir(input_path):

    if (os.path.exists(temp_path)):
        os.remove(temp_path)
    else:
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith('.txt'):
                file_names.append(file)

                # Changes a werid file name to Dream_<file name> to avoid issues
                # weirdlyNamedFile = Path(os.path.join(root, file))
                # if(weirdlyNamedFile.exists()):
                #     weirdlyNamedFile.rename("Dream_"+weirdlyNamedFile.name)
                
                
                try:
                    with io.open(os.path.join(root, file), 'r',errors="ignore") as f:
                        content = f.read()

                    with open(temp_path, 'a') as temp_file:
                        temp_file.write(file+ "\n\n"+ content + "\n\n")

                except FileNotFoundError:
                    print(f"File {file} not found.")
                except Exception as e:
                    print(f"An error occurred while reading {file}: {e}")
            if file.lower().endswith('.docx'):
                #do something   
                print(f"Found a docx file: {file}. Converting to PDF...")     
    
    if(os.path.exists(temp_path)):
        output_pdf = output_path + input("Enter the output PDF file name: ") + ".pdf"
        text_to_pdf(temp_path, output_pdf) 

    # print("Text files found:")

    # for name in file_names:
    #     print(name)
else:
    if (os.path.exists(temp_path)):
        os.remove(temp_path)
    else:
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    if(os.path.isfile(input_path)):
        output_pdf = output_path + input("Enter the output PDF file name: ") + ".pdf"
        text_to_pdf(input_path, output_pdf)
    else:
        print(f"File {input_path} not found.")

# if __name__ == "__main__":
#     input_txt = "input.txt"   # Change to your text file path
#     output_pdf = input("Enter the output PDF file name: ") + ".pdf"
#     text_to_pdf(input_path, output_pdf)
    
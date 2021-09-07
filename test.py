print("hi %s how are you doing %d" % ("john",7)) 

"""import pdfplumber
with pdfplumber.open('G:\My Drive\CLIENTS\Earth Stripes\Earth Stripes Codebase\data\EPA Climate Impacts\climate-change-ak.pdf') as pdf:
    first_page = pdf.pages[1]
    print(first_page.extract_text())"""

# importing required modules 
import PyPDF2
    
# creating a pdf file object 
pdfFileObj = open('G:\My Drive\CLIENTS\Earth Stripes\Earth Stripes Codebase\data\EPA Climate Impacts\climate-change-ak.pdf', 'rb') 
    
# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    
# printing number of pages in pdf file 
print(pdfReader.numPages) 
    
# creating a page object 
pageObj = pdfReader.getPage(1) 
    
# extracting text from page 
print(pageObj.extractText()) 
    
# closing the pdf file object 
pdfFileObj.close()

#testing the git stuff
from docx import Document

document = Document()
r = 2 # Number of rows you want
c = 2 # Number of collumns you want
table = document.add_table(rows=r, cols=c)
table.style = 'LightShading-Accent1' # set your style, look at the help documentation for more help
'''
for y in range(r):
    for x in range(c):
        cell.text = 'text goes here'
        '''
document.save('demo.docx') # Save document
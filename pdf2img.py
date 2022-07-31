
from pdf2image import convert_from_path
from sys import argv

def pdf2img(filepath):
    try:
        images = convert_from_path(filepath)
        i = 0
        for img in images:
            img.save(f'output{i}.jpg', 'JPEG')
            i += 1
 
    except  :
        Result = "NO pdf found"
        print(Result) 
    else:
        Result = "success"
        print(Result)

pdf2img(argv[1])

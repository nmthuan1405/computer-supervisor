from flask import Flask,send_file
from os import listdir
from os.path import isfile
from io import BytesIO
from PIL import Image

HOST = '0.0.0.0'
PORT = 5155

app = Flask(__name__)
'''
# Webpage to display all the photos taken on the socket server.
#   -  Coobster
'''
# check_if_png will check the file signature for PNG image files and return False if the file is not a PNG
def check_if_png(filename):
  data = open(filename,'r+b').read(32)
  # allowing onlt PNG files to be uploaded
  mimes_allowed = ['0A0D0D0A', '89504E470D0A1A0A']
  for test in mimes_allowed:
    if data.hex().upper()[:len(test)] == test:
        return True
  return False

def load_image_dir(location='images/'):  
    print(location)
    return [i for i in listdir(location) if isfile(location+i) and check_if_png(location + i)]

@app.route('/')
def index():
    width = 7
    directory = load_image_dir()
    links = ""
    for e,i in enumerate(directory):
        links += '<a href="{}"><img src="thumb/{}"></a>'.format(i,i)
        if not (e +1 )% width:
            links += '<br>'
    return links
@app.route('/thumb/<loc>')
def thumb(loc):
    filename = 'images/'+loc
    tmp = BytesIO()
    if isfile(filename):
        im = Image.open(filename).resize((100,80))
        im.save(tmp,format='PNG')
        return send_file(BytesIO(tmp.getvalue()),mimetype='image/PNG')
    else:
        return "ERROR"
@app.route('/<loc>')
def link(loc):
    filename = 'images/'+loc
    print(filename)

    if isfile(filename):
        with open(filename,'r+b') as fp:
            #data = fp.read()
            return send_file(filename,mimetype='image/png')
            #return 'image found'
    else:
        return 'File not found'
if __name__ == '__main__':
    app.run(host=HOST,port=PORT)

import base64
import io
from PIL import Image
from flask import Flask, request, render_template, send_file
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/ocr', methods=['POST','OPTIONS'])
def ocr():
    b64 = request.form['file'] + '=' * (-len(request.form['file']) % 4)
    print(len(b64))
    # print(b64)
    img = Image.open(io.BytesIO(base64.urlsafe_b64decode(b64)))
    img.save('captcha.png')
    files = {
        'file': open('captcha.png', 'rb'),
    }
    data = {
        'lang': 'eng',
    }
    # print(requests.post('https://api8.ocr.space/parse/image', data=data).json())
    r = (requests.post('http://195.148.30.97/cgi-bin/ocr.py',data=data, files=files).text)
    import re
    # <p><p>060953</p><p>
    a=  re.findall(r'<p><p>(.*?)</p><p>',r)
    return a[0] if a else 'Error'

if __name__ == '__main__':
    app.run(debug=True)

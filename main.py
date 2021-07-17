# coding=utf-8
from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet
import base64
import io

############## encryption key, this is NOT SECURE at all. Use for demo only #######
KEY = b'mANM2S7Vx49lRmmlIfSSX9NCy8QvB1G7EX8iGpRw3T8='
##########################################################################

app = Flask(__name__)

######### make the qrcode ###########
import qrcode
# for putting the logo in the QR code center
from PIL import Image
Logo_link = "static/logo.jpg" # absolute path /home/Danjoe4/PAT_QR_generator/static/logo.jpg
logo = Image.open(Logo_link)
# various image parameters that will not change
basewidth = 100
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
##########################

# a few more useful globals
BASE_URL = "http://djbroderick.xyz/send?" 




@app.route("/",methods=['GET'])
def index():
    return render_template("home.html")


@app.route("/code", methods=["POST"])
def code():
    if request.method == 'POST':
        print('Incoming..')
        qr_img = make_qr(request.form['brand'], 
        request.form['product'], 
        request.form['model'], 
        request.form['serial'])
        
        return render_template("QR_output.html", img_data=qr_img.decode('utf-8'))
        #return 'OK', 200

    return "Please go back and submit the form"




def make_qr(brand, product, model, serial):
    # taking url or text
    ciphertext = encrypt_params(b"[{brand},{product},{model},{serial}]")
    url = BASE_URL + "id=" + str(ciphertext)
    
    # add URL to QRcode and generate
    QRcode.add_data(url)
    QRcode.make()

    # adding color to QR code
    QRimg = QRcode.make_image(
    fill_color='black', back_color="white").convert('RGB')

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
    (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    
    # save the image in an io buffer, encode and return it
    data = io.BytesIO()
    QRimg.save(data, 'PNG')
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data


def encrypt_params(params):
    f = Fernet(KEY)
    token = f.encrypt(params)
    return token


@app.route("/qrcode", methods=["GET"])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get("data", "")
    return send_file(qrcode(data, mode="raw"), mimetype="image/png")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
    #make_qr("Bose", "HEADPHONES", "6DBL", "SOMESERIAL2423567")
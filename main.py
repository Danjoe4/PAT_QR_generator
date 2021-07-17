# coding=utf-8
from flask import Flask, render_template, request, send_file
#from cryptography.fernet import Fernet
import zlib # for compression
import base64 
import io



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
    """ the root page with the fillable form
    """
    return render_template("home.html")


@app.route("/code", methods=["POST"])
def code():
    """ makes the QR code if it received a POST request from the root page
    """
    if request.method == 'POST':
        qr_img = make_qr(request.form['brand'], 
        request.form['product'], 
        request.form['model'], 
        request.form['serial'])
        
        return render_template("QR_output.html", img_data=qr_img.decode('utf-8'))
    
    return "Please go back and submit the form"




def make_qr(brand, product, model, serial):
    """ Takes the params and returns a base64 encoded image object
    """

    # HASH (add encryption) the params and create the url
    ciphertext = obscure_params(b"[{brand},{product},{model},{serial}]")
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
    print("QR code version: "+ str(QRcode.version))
    return encoded_img_data


def encrypt_params(params):
    """ Encrypts the list of params: [brand,product,model,serial] and returns the 
    encrypted string.
    This algorithm produces a string that is too long, use a different one
    """
    f = Fernet(KEY)
    token = f.encrypt(params)
    print(token)
    return token


def obscure_params(data: bytes) -> bytes:
    """ A temporary solution to getting a smaller output. Converts to base64
    then uses compression
    """
    out = base64.urlsafe_b64encode(zlib.compress(data, 9))
    print(out)
    return out




if __name__ == "__main__":
    #app.run(port=5000, debug=True)
    make_qr("Bose", "HEADPHONES", "6DBL", "SOMESERIAL2423567")
    #test1 = obscure_params(b'["Bose", "HEADPHONES", "6DBL", "SOMESERIAL2423567"]')
    #unobscure(test1)
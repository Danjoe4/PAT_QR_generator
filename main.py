# coding=utf-8
from flask import Flask, render_template, request, send_file, redirect
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64 
import io
import yaml


app = Flask(__name__)

######### make the qrcode ##############
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
########################################

# a few more useful global CONSTANTS
def load_globals():
    with open("config.yaml") as f_stream:
        config_file = yaml.load(f_stream, yaml.FullLoader)

    global ENCRYPTION_KEY_1 # set the encryption key
    salt = bytes(config_file["encryption_salt_1"], encoding='utf8')
    password = bytes(config_file["encryption_password_1"], encoding='utf8')
    ENCRYPTION_KEY_1 = derive_encryption_key(salt, password)
    print("here is the encryption key:")
    print(ENCRYPTION_KEY_1)

BASE_URL = "http://www.vaultqr.com/send?" 
###############################
@app.route("/",methods=['GET'])
def root():
    return redirect("/make-product-code")


@app.route("/make-product-code",methods=['GET'])
def index():
    """ the page with the fillable form
    """
    return render_template("make_product_code.html")


@app.route("/code", methods=["POST"])
def code():
    """ makes the QR code if it received a POST request from the form page
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
    url = make_url(brand, product, model, serial)
    print("the full url:")
    print(url)
    
    # initialize, add URL to QRcode and generate
    QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H)
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


def make_url(brand, product, model, serial):
    # HASH (add encryption) the params and create the url
    ciphertext = encrypt_params(f"{brand},{product},{model},{serial}".encode('utf-8'))
    url = BASE_URL + "v=" + str(ciphertext)[2:-1] # str cast adds b'...' to the cipher
    print("the url: " + url)
    return url


def encrypt_params(data: bytes) -> bytes:
    """ aes128 the string
    """
    print("the paramaters to be encoded: ")
    print(data)
    f = Fernet(ENCRYPTION_KEY_1)
    token = f.encrypt(data)
    print("encrypted paramter: ")
    print(token)
    return token


def derive_encryption_key(salt, password):
    """ Uses our salt and password to derive the key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key




if __name__ == "__main__":
    app.before_first_request(load_globals) 
    app.run(port=5000, debug=True)
    
    #load_globals()
    #enc_str = encrypt_params("brand,product,model,serial".encode('utf-8'))
    #make_qr("Bose", "HEADPHONES", "123456", "SOMESERIAL123")
    #decrypt_params(enc_str)
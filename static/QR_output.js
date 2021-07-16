function generate_qr_parameters (){
  var values = "[random,stuff,goes,here]";
  document.getElementById("randotest").innerHTML = values;
  var statement2 = "../my_static/icon.jpg";
  var statement3 = "{{ qrcode('${values}', error_correction='H', icon_img='icon.jpg') }}>;";
  document.getElementById("QR_image").src = statement2;
};

generate_qr_parameters();
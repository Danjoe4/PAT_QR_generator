V0_2 QR code is much smaller thanks to encoding/compression. We're putting off solving this problem because I'm not sure how to balance security vs QRcode size. Will probably result in having multiple QRcode versions depending on the client needs. Only the serial no. will reduce size as well. Easiest option is to suck it up and have phat QR codes, but at least for the demo I'd rather not have it look disgusting.

V0_2_5 On the second page, add width & height options and a print button.

V3 After you play with the dimensions on your printer, I will make the default dimensions the appropriate size. We can also hook up the domain at this time.

V0_4 (Post-Demo) Discard the entire frontend and turn this into a REST API, likely with some sort of authentication for clients (username/password or API key). Should conform to the needs of the Bose packaging designers/software/process.

########################################################
Hosted at http://danjoe4.pythonanywhere.com/
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from mail_load_constants import MAIL_CONSTANTS

def SendMail(To = MAIL_CONSTANTS["RECV"],my_msg: str = "", msgImage = None,):
    # img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Toto_je_test'
    msg['From'] = MAIL_CONSTANTS["LOGIN"]
    msg['To'] = MAIL_CONSTANTS["RECV"]

    if msgImage:
        try:
            fp = open('{some_file}.png', 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<image1>')
            msg.attach(msgImage)
        except FileNotFoundError as e:
            print(f"FILE SOUCH A FILE ! \t{e}")
    text = MIMEText("<b>Blaba<i>OtherBla</i> </b>BAL<br><img src='cid:image1'><br>Nifty!"+my_msg, 'html')
    msg.attach(text)
    s = smtplib.SMTP(MAIL_CONSTANTS["SMTP"], MAIL_CONSTANTS["SMTP_PORT"])
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(MAIL_CONSTANTS["LOGIN"], MAIL_CONSTANTS["PWD"])
    s.sendmail(MAIL_CONSTANTS["LOGIN"], To, msg.as_string())
    s.quit()

# SendMail(MAIL_CONSTANTS["RECV"])
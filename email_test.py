import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

bhejne_wala = "APKI_EMAIL@gmail.com" #Jis email se apne email bhejni hai (sender)
recieve_karnewala = "gibrantareen@gmail.com" #Jis email ko apne email bhejni hai (Reciever)

msg = MIMEMultipart()
msg['To'] = recieve_karnewala # store receivers email address
msg['Subject'] = "INRTDUER ALERT" # stores subject

body = "Inruder activity detected at house, Code Red intitiated"
msg.attach(MIMEText(body, 'plain')) #store the body of the mail as plain text

# loads the file to be sent
filename = "pakka_intruder0.jpg"
file_ka_path = open("E:\\00 Python Work\\advanced-ai-security-ca-project\\pakka_intruder0.jpg", "rb")

# instance bnaenge MIMEBase ka and name it as x
x = MIMEBase('application', 'octet-stream')
x.set_payload((file_ka_path).read())

# encode into base64
encoders.encode_base64(x)

x.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(x)

# SMTP ka session starts now
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(bhejne_wala, "APKA_PASSWORD")
text = msg.as_string()

s.sendmail(bhejne_wala, recieve_karnewala, text) # sending the mail

# terminate the session
s.quit()

import time
import datetime
import RPi.GPIO as GPIO
import storeFridgeFB
from signal import pause
from picamera import PiCamera
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import sendsms
from dotenv import dotenv_values

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

config = dotenv_values(".env")

door_open = 0

camera = PiCamera()
camera.start_preview()
frame = 1

# Send an email with an attachment using SMTP
def send_mail(eFrom, to, subject, text, attachment):
    # SMTP Server details: update to your credentials or use class server
    smtpServer=config['Server']
    smtpUser=config['User']
    smtpPassword=config['Password']
    port=587

    # open attachment and read in as MIME image
    fp = open(attachment, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    #construct MIME Multipart email message
    msg = MIMEMultipart()
    msg.attach(MIMEText(text))
    msgImage['Content-Disposition'] = 'attachment; filename="image.jpg"'
    msg.attach(msgImage)
    msg['Subject'] = subject

    # Authenticate with SMTP server and send
    s = smtplib.SMTP(smtpServer, port)
    s.login(smtpUser, smtpPassword)
    s.sendmail(eFrom, to, msg.as_string())
    s.quit()



while True:
	if GPIO.input(17):
		print("Door is Closed")
		door_open = 0
		time.sleep(5)
	else:  
		door_open += 1
		print("Door is Open: %d seconds" % door_open)
		time.sleep(1)

		if door_open == 5:
			fileLoc = f'/home/pi/Assignment2/images/frame{frame}.jpg' # set the location of image file and current time
			currentTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
			camera.capture(fileLoc) # capture image and store in fileLoc
			storeFridgeFB.store_file(fileLoc)
			storeFridgeFB.push_db(fileLoc,currentTime)
			frame += 1

		if door_open == 20:
			text= f'Hi,\n the attached image was taken today at {currentTime}'
			send_mail('damiendriver81@gmail.com', 'driverdamien@hotmail.com', 'Fridge Door Open',text, fileLoc)

		if door_open == 30:
			sendsms.send_twilio_alert()

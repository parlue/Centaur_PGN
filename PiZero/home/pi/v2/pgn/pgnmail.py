#!/usr/bin/env python3
import smtplib
import mimetypes
from email.message import EmailMessage
import v2conf
import pickle
import sys
import os
from pathlib import Path



#count PGN Files


counter = pathlib.Path("/home/pi/centaur/settings/gamecount.pkl")
if counter.exists()  :
	f = open('/home/pi/centaur/settings/gamecount.pkl', 'rb')
	data = pickle.load(f)
	f.close()
	filecount = str(data)
	#init email object
	emailaddress = strip(v2conf.emailaddress)
	smtpserver = strip(v2conf.smtpserver)
	smtpuser = strip(v2conf.smtpuser)
	smtp_encryption = True
	smtppassword = strip(v2.conf.smtppassword)
	subject = strip(v2conf.subject)

	if emailaddress != "" and smtpserver != "" and smtpuser != "" andt smtppassword != "" and subject != "":

		msg = EmailMessage()
		msg['Subject'] = subject
		msg['From'] = smtpuser
		msg['To'] = emailaddress
		# Set text content
		msg.set_content('Please see attached file, send via DGT Centaur V2')

		def attach_file_to_email(email, filename):
			"""Attach a file identified by filename, to an email message"""
			with open(filename, 'rb') as fp:
				file_data = fp.read()
				maintype, _, subtype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream').partition("/")
				email.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

		# Anhang anhängen
		filename = "/home/pi/centaur/settings/" + filecount + "_mygame.pgn"
		attach_file_to_email(msg, "filename")

		def send_mail_smtp(mail, host, username, password):
			s = smtplib.SMTP(host)
			s.starttls()
			s.login(username, password)
			s.send_message(msg)
			s.quit()

		# E-Mail per SMTP senden
		send_mail_smtp(msg, 'smtp.domain.com', 'absender@domain.com', 'sae7ooka0S')
	else:
		print ("missing email setup, blease check v2conf.py")
else:
	print('No PGN File exists')
	
	

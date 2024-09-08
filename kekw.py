from imap_tools import MailBox, AND
import json
import datetime
import telebot


def read_email(config_data):
	ORG_EMAIL   = config_data['mail_adress']
	FROM_PWD    = config_data['mail_pass']
	SMTP_SERVER = config_data['imap_server']
	mail = MailBox(SMTP_SERVER).login(ORG_EMAIL, FROM_PWD)
	messages = mail.fetch(criteria=AND(seen=False),mark_seen=False,bulk=True)
	
	files=[]
	result = []
	for msg in messages:
		msg.date_lt=datetime.date.today().isoformat()
		print('Message from:', msg.from_,'\nMessage subject: ', msg.subject,'\nMessage text:', msg.text)
		result.append(msg.from_ + msg.subject + msg.text)
		files +=[att.payload for att in msg.attachments if att.filename.endswith(('.pdf','.docx','.jpeg','.xlsx','.png','.jpg'))]  #TODO decode
	print(files)

	return result

with open('config.json', 'r') as file:
	opened_config = file.read()
config_data = json.loads(opened_config)

bot=telebot.TeleBot(config_data['bot_key'])

@bot.message_handler(commands=['start'])
def start_message(message):
	if message.text == '/start':
		messages = read_email(config_data)
		for msg in messages:
			bot.send_message(config_data['chat_id'], msg)

bot.infinity_polling(skip_pending=True)


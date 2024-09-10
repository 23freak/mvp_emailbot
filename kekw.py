import datetime
import json

from imap_tools import MailBox, AND
import telebot


def read_email(config_data):
	org_email = config_data['mail_adress']
	from_pwd = config_data['mail_pass']
	smtp_server = config_data['imap_server']
	mail = MailBox(smtp_server).login(org_email, from_pwd)
	messages = mail.fetch(criteria=AND(seen=False),mark_seen=False,bulk=True)
	
	files = []
	result = []
	for msg in messages:
		msg.date_lt = datetime.date.today().isoformat()
		result.append('Message from: ' + msg.from_ + '\nmessage subject: ' + msg.subject + '\nmessage text:' + msg.text)
		files += [att.payload for att in msg.attachments if att.filename.endswith(('.pdf','.docx','.jpeg','.xlsx','.png','.jpg'))]  #TODO decode
	return result

with open('config.json', 'r') as file:
	opened_config = file.read()
config_data = json.loads(opened_config)

bot=telebot.TeleBot(config_data['bot_key'])
	
@bot.message_handler(commands = ['start'])
def start_message(message):
	if message.text == '/start':
		messages = read_email(config_data)
		for msg in messages:
			bot.send_message(config_data['chat_id'], msg)




bot.infinity_polling(skip_pending=True)


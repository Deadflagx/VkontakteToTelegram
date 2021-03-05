import traceback
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import vk_api

import telebot
from telebot.types import InputMediaPhoto

from settings import TELETOKEN, CHAT_ID, VKTOKEN, GROUP_ID


#Telegram AUTH
bot = telebot.TeleBot(TELETOKEN)

#VK AUTH
vk = vk_api.VkApi(token=VKTOKEN) 
vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, GROUP_ID)

#Get better image resolution from Vk response
def get_biggest_photo(photo_attachment):
	return sorted(list(int(photo_attachment[6:]) for photo_attachment in photo_attachment if 'photo' in photo_attachment))[-1]

#Photos uploader to Telegram			
def upload_photos(photos_array):
	#if array is empty
	#return without errors
	if photos_array == []:
		return 0
	bot.send_media_group(chat_id=CHAT_ID, media=photos_array)

def create_poll(question, answers):
	bot.send_poll(chat_id=CHAT_ID, is_anonymous=True, question=question, options=answers)

def send_msg(text):
	bot.send_message(chat_id=CHAT_ID, text=text)


#@bot.channel_post_handler(content_types=['text', 'audio', 'document', 'photo', 'video'])
#def test(message):
	#print(message)
#bot.polling()

try:
	for event in longpoll.listen():
		if event.type == VkBotEventType.WALL_POST_NEW:
			photos_array = []
			text = event.object['text'] #text from Vk post
			if 'attachments' not in str(event):
				send_msg(text)
			if 'attachments' in str(event):
				for attachment in event.object['attachments']:
					if attachment['type'] == 'photo':
						photos_array.append(InputMediaPhoto(attachment['photo']['photo_{}'.format(get_biggest_photo(attachment['photo']))],caption=text))
						text = ''
					elif attachment['type'] == 'poll':
						send_msg(event.object['text'])
						question = attachment['poll']['question']
						answers = attachment['poll']['answers']
						answ_list = list(answers['text'] for answers in answers)
						create_poll(question, answ_list)
					else:
						pass
				upload_photos(photos_array)
				photos_array.clear()
except:
	print(traceback.format_exc())





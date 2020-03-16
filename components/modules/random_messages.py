import random
from vk_api.utils import get_random_id

class RandMessages(object):
	def __init__(self, api):
		self.api = api

		self.words = {}
		return

	def start(self, message_data):
		text = message_data[0]
		peer_id = message_data[1]
		from_id = message_data[2]
		# обработка бреда от бота
		if peer_id in self.words:
			for word in text.split():
				self.words[peer_id]["words"].append(word)
			self.words[peer_id]["messages_helded"] += 1
			if self.words[peer_id]["messages_helded"]\
				>= self.words[peer_id]["max_messages_helded"]:
				# генерируем бред
				message_text = ""
				random.shuffle(self.words[peer_id]["words"])
				i = 0
				for word in self.words[peer_id]["words"]:
					message_text += word + " "
					i += 1
					# ограничение по длине бреда
					if i > (len(self.words[peer_id]["words"])/2)-\
						(len(self.words[peer_id]["words"])/2/2):
						break
				self.words[peer_id] = {
					"words": [],
					"max_messages_helded": self.api.messages.getConversationMembers\
						(peer_id=peer_id)["count"],
					"messages_helded": 0
				}
				self.api.messages.send(
					chat_id=peer_id,
					message=message_text,
					random_id=get_random_id()
				)
			return
		else:
			self.words[peer_id] = {
				"words": [],
				"max_messages_helded": self.api.messages.getConversationMembers\
					(peer_id=peer_id)["count"],
				"messages_helded": 0
			}
		return
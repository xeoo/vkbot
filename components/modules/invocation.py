from ..functions import ShrinkedFuncs

class Invocation(object):
	def __init__(self, api):
		self.api = api

		self.shrinks = ShrinkedFuncs(self.api)
		return

	def start(self, message_data):
		text = message_data[0]
		peer_id = message_data[1]
		from_id = message_data[2]

		response = self.api.messages.getConversationMembers(peer_id=peer_id+2000000000)
		message = f"Призвал/написал [id{from_id}|он]\n\nТекст сообщения: "
		for word in text.split()[1::]:
			message += word + " "
		message += "\n["
		for user in response["items"]:
			if int(user["member_id"]) > 0:
				message += f"[id{user['member_id']}|.]"
		message += "]"
		self.shrinks.answer(chat_id=peer_id, text=message)

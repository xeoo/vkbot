from .functions import ShrinkedFuncs
from . import texts

class Exceptions(object):
	def __init__(self, api):
		self.api = api
		self.shrinks = ShrinkedFuncs(self.api)
		return

	def CommandNotFoundError(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text=texts.COMMAND_NOT_FOUND)
		return

	def KickIsAdminError(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text=texts.COMMAND_NOT_FOUND)
		return

	def AdminNotFoundInAdminListError(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text=texts.ADMIN_NOT_IN_LIST)
		return




	def BlockForPrivateMessagesWarn(self, user_id):
		self.shrinks.answer(user_id=user_id, text=texts.BLOCK_PRIVATE_MESSAGES)
		return

	def CommandNotExistsWithTemplateWarn(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text=texts.COMMAND_NOT_EXISTS_FOR_TEMPLATE)
		return

	def UnknownWarn(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text=texts.UNKNOWN_WARN)
		return

	def UserNotIsAdminWarn(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text=texts.NOT_HAVE_PERMISSION)
		return

	def MentionNotFoundWarn(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text=texts.MENTION_NOT_FOUND)
		return





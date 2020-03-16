from .functions import ShrinkedFuncs

class Exceptions(object):
	def __init__(self, api):
		self.api = api
		self.shrinks = ShrinkedFuncs(self.api)
		return

	def CommandNotFoundError(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text="Данной команды нет и пошел нахуй, долбаеб сука")
		return

	def KickIsAdminError(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text="Ты ахуел админа кикать?")
		return

	def AdminNotFoundError(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text="Он не админ, додик ебаный")
		return




	def BlockForPrivateMessagesWarn(self, user_id):
		self.shrinks.answer(user_id=user_id, text="Пiшов нахой")
		return

	def CommandNotExistsWithTemplateWarn(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text="Команда не соотвествует шаблону")
		return

	def UnknownWarn(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text="Хуй знает что ты хотел сделать, но ты долбаеб")
		return

	def UserNotIsAdminWarn(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text="Вы не имеете права на это")
		return

	def MentionNotFoundWarn(self, peer_id):
		self.shrinks.answer(chat_id=peer_id, text="Нет упоминания")
		return





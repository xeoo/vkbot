# [VK API]
from vk_api.bot_longpoll import VkBotEventType
from vk_api import exceptions

# [Необходимые модули]
from .errors import Exceptions
from .functions import is_admin, load_json, save_json, ShrinkedFuncs
import re

# [Подключение модулей бота из папки 'modules']
from .modules import nmap
from .modules import random_messages


class Bot(object):
	def __init__(self, api, longpoll, config):
		self.api = api
		self.longpoll = longpoll
		self.prefix = config["prefix"]
		self.admins = config["admins"]
		self.config = config

		self.shrinks = ShrinkedFuncs(self.api)
		self.exceptions = Exceptions(self.api)
		return

	def start_bot(self):
		# Инициализируем вне обработчика, т.к. он будет пересоздавать экземпляр класса
		self.rand_messages = random_messages.RandMessages(self.api)		
		for event in self.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW and event.message.text:
				self.message_handler(event)
				# [Повторная подгрузка конфига]
				self.admins = load_json()["admins"]
				self.prefix = load_json()["prefix"]
				self.config = load_json()

	def message_handler(self, event):
		# [Обработка сообщений]
		self.text = event.message.text.lower()
		self.peer_id = event.message.peer_id-2000000000
		self.from_id = event.message.from_id
		if event.from_chat:
			if self.text[0] == self.prefix:
				# [Исполнение команд (какая команда, такой и метод: !nmap -> self.nmap)]
				try:
					eval(f"self.{self.text[1::].split()[0]}()")
				except AttributeError:
					self.exceptions.CommandNotFoundError(self.peer_id)
				return
			else:
				try:
					# Нужен доступ админа
					self.rand_messages.start([self.text, self.peer_id, self.from_id])
				except exceptions.ApiError:
					pass
				return
		if event.from_user:
			self.exceptions.BlockForPrivateMessagesWarn(self.from_id)
		return

	# [Встроенный метод бота]
	def help(self):
		HELP = "!help - этот текст\n"\
		"Модули:\n"\
		"!nmap <ip/domain> - утилита nmap\n"\
		"Администрирование:\n"\
		"!kick <mention> - кикнуть участника беседы\n"\
		"!add_admin <mention> - добавить администратора\n"
		self.shrinks.answer(chat_id=self.peer_id, text=HELP)
		return

	# [Встроенные обработчики модуля]
	def nmap(self):
		if len(self.text.split()) != 2:
			self.exceptions.CommandNotExistsWithTemplateWarn(self.peer_id)
			return
		nmap_object = nmap.Nmap(self.text[1::].split()[1])
		response = nmap_object.start()
		if response is None:
			self.exceptions.UnknownWarn(self.peer_id)
			return
		self.shrinks.answer(chat_id=self.peer_id, text=response)
		return

	# [Методы администрирования]
	def kick(self):
		print(self.admins)
		print(self.from_id)
		if not is_admin(self.from_id, self.admins):
			self.exceptions.UserNotIsAdminWarn(self.peer_id)
			return
		if len(self.text.split()) != 2:
			self.exceptions.CommandNotExistsWithTemplateWarn(self.peer_id)
			return
		response = re.match(r"\[id\d{1,}\|\w{1,}\]", self.text[1::].split()[1].replace("*", "").replace("@", ""))
		if response is None:
			self.exceptions.MentionNotFoundWarn(self.peer_id)
			return
		user_id = re.findall(r"(\d+)", self.text[1::].split()[1])
		try:
			if not user_id in self.admins:
				self.api.messages.removeChatUser(
					chat_id=self.peer_id,
					user_id=user_id[0]
				)
				self.shrinks.answer(chat_id=self.peer_id, text="ГАТОВА ЕПТА!")
			else:
				KickIsAdminError(self.peer_id)
		except exceptions.ApiError:
			# Нужен доступ админа
			self.exceptions.KickIsAdminError(self.peer_id)
		return

	def add_admin(self):
		if not is_admin(self.from_id, self.admins):
			self.exceptions.UserNotIsAdminWarn(self.peer_id)
			return
		if len(self.text.split()) != 2:
			self.exceptions.CommandNotExistsWithTemplateWarn(self.peer_id)
			return
		response = re.match(r"\[id\d{1,}\|\w{1,}\]", self.text[1::].split()[1].replace("*", "").replace("@", ""))
		if response is None:
			self.exceptions.MentionNotFoundWarn(self.peer_id)
			return
		user_id = re.findall(r"(\d+)", self.text[1::].split()[1])
		self.config["admins"].append(user_id[0])
		self.shrinks.answer(chat_id=self.peer_id, text="Администратор добавлен")
		save_json(self.config)
		return

	def remove_admin(self):
		if not is_admin(self.from_id, self.admins):
			self.exceptions.UserNotIsAdminWarn(self.peer_id)
			return
		if len(self.text.split()) != 2:
			self.exceptions.CommandNotExistsWithTemplateWarn(self.peer_id)
			return
		response = re.match(r"\[id\d{1,}\|\w{1,}\]", self.text[1::].split()[1].replace("*", "").replace("@", ""))
		if response is None:
			self.exceptions.MentionNotFoundWarn(self.peer_id)
			return
		user_id = re.findall(r"(\d+)", self.text[1::].split()[1])
		try:
			self.config["admins"].remove(user_id[0])
			self.shrinks.answer(chat_id=self.peer_id, text="Администратор удален")
		except ValueError:
			self.exceptions.AdminNotFoundError(self.peer_id)
			return
		save_json(self.config)
		return

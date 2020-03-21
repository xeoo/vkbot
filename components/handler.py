# [VK API]
from vk_api.bot_longpoll import VkBotEventType
from vk_api import exceptions

# [Необходимые модули]
from .errors import Exceptions
from .functions import is_admin, load_json, is_valid_command, save_json, ShrinkedFuncs
import re
from . import texts

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
		self.rand_messages = random_messages.RandMessages(self.api)
		return

	def start_bot(self):
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
			if self.text[0] == self.prefix and is_valid_command(self.text[1::].split()[0]):
				# [Исполнение команд (какая команда, такой и метод: !nmap -> self.nmap)]
				try:
					eval(f"self.{self.text[1::].split()[0]}()")
				except AttributeError as e:
					print(e)
					self.exceptions.CommandNotFoundError(self.peer_id)
				return
			else:
				try:
					# Нужен доступ админа
					self.rand_messages.start([self.text, self.peer_id, self.from_id])
				except exceptions.ApiError as e:
					print(e)
					pass
				return
		if event.from_user:
			self.exceptions.BlockForPrivateMessagesWarn(self.from_id)
		return

	# [Встроенный метод бота]
	def help(self):
		self.shrinks.answer(chat_id=self.peer_id, text=texts.HELP.replace("<prefix>", self.prefix))
		return

	# [Встроенные обработчики модуля]
	def nmap(self):
		# если текст имеет больше или меньше элементов: ошибка шаблона
		if len(self.text.split()) != 2:
			self.exceptions.CommandNotExistsWithTemplateWarn(self.peer_id)
			return
		# запускаем модуль сканирования (там же он проверяет валидность хоста)
		nmap_object = nmap.Nmap(self.text[1::].split()[1])
		response = nmap_object.start()
		if response is None or not bool(len(response.strip())):
			self.exceptions.UnknownWarn(self.peer_id)
			return
		self.shrinks.answer(chat_id=self.peer_id, text=response)
		return

	# [Методы администрирования]
	def kick(self):
		# это админ? (кто отправил команду): нет - ошибка
		if not is_admin(self.from_id, self.admins):
			self.exceptions.UserNotIsAdminWarn(self.peer_id)
			return
		# если текст имеет больше или меньше элементов: ошибка шаблона
		if len(self.text.split()) != 2:
			self.exceptions.CommandNotExistsWithTemplateWarn(self.peer_id)
			return
		# проверка упоминания по шаблону: не сходится (отдает None): ошибка упоминания
		response = re.match(r"\[(id|club)\d+\|.+\]",\
			self.text[1::].split()[1].replace("*", "").replace("@", ""))
		if response is None:
			self.exceptions.MentionNotFoundWarn(self.peer_id)
			return
		# берем id участника беседы
		member_id = re.findall(r"\d+", self.text[1::].split()[1])
		try:
			if "club" in self.text[1::].split()[1].split("|")[0]:
				# бот группы
				self.api.messages.removeChatUser(
					chat_id=self.peer_id,
					member_id=f"-{member_id[0]}"
				)
			else:
				# обычный пользователь
				self.api.messages.removeChatUser(
					chat_id=self.peer_id,
					member_id=member_id[0]
				)
		except exceptions.ApiError as e:
			print(e)
			self.shrinks.answer(chat_id=self.peer_id, text=texts.ACCESS_ERROR_OR_USER_NOT_FOUND)
			return
		return

	def add_admin(self):
		# это админ? (кто отправил команду): нет - ошибка
		if not is_admin(self.from_id, self.admins):
			self.exceptions.UserNotIsAdminWarn(self.peer_id)
			return
		# если текст имеет больше или меньше элементов: ошибка шаблона
		if len(self.text.split()) != 2:
			self.exceptions.CommandNotExistsWithTemplateWarn(self.peer_id)
			return
		# проверка упоминания по шаблону: не сходится (отдает None): ошибка упоминания
		response = re.match(r"\[id\d+\|.+\]", self.text[1::].split()[1].replace("*", "").replace("@", ""))
		if response is None:
			self.exceptions.MentionNotFoundWarn(self.peer_id)
			return
		# берем id участника беседы и добавляем
		member_id = re.findall(r"\d+", self.text[1::].split()[1])
		self.config["admins"].append(str(member_id[0]))
		self.shrinks.answer(chat_id=self.peer_id, text=texts.ADMIN_ADDED)
		save_json(self.config)
		return

	def remove_admin(self):
		# это админ? (кто отправил команду): нет - ошибка
		if not is_admin(self.from_id, self.admins):
			self.exceptions.UserNotIsAdminWarn(self.peer_id)
			return
		# если текст имеет больше или меньше элементов: ошибка шаблона
		if len(self.text.split()) != 2:
			self.exceptions.CommandNotExistsWithTemplateWarn(self.peer_id)
			return
		# проверка упоминания по шаблону: не сходится (отдает None): ошибка упоминания
		response = re.match(r"\[id\d+\|.+\]", self.text[1::].split()[1].replace("*", "").replace("@", ""))
		if response is None:
			self.exceptions.MentionNotFoundWarn(self.peer_id)
			return
		# берем id участника беседы и удаляем
		member_id = re.findall(r"\d+", self.text[1::].split()[1])
		try:
			self.config["admins"].remove(str(member_id[0]))
			self.shrinks.answer(chat_id=self.peer_id, text=texts.ADMIN_REMOVED)
		except ValueError as e:
			print(e)
			self.exceptions.AdminNotFoundInAdminListError(self.peer_id)
			return
		save_json(self.config)
		return

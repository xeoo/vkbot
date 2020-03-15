from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id
from .modules import nmap
from .functions import is_admin, load_json, save_json
from vk_api import exceptions
import re


class Bot(object):
	def __init__(self, api, longpoll, config):
		self.api = api
		self.longpoll = longpoll
		self.prefix = config["prefix"]
		self.admins = config["admins"]
		self.config = config
		return

	def start_bot(self):
		for event in self.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW and event.message.text:
				self.message_handler(event)
				# reload configs
				self.admins = load_json()["admins"]
				self.prefix = load_json()["prefix"]
				self.config = load_json()

	def message_handler(self, event):
		self.text = event.message.text.lower()
		self.peer_id = event.message.peer_id-2000000000
		self.from_id = event.message.from_id
		if event.from_chat:
			if self.text[0] == self.prefix:
				# try:
				eval(f"self.{self.text[1::].split()[0]}()")
				# except AttributeError:
					# self.api.messages.send(
						# chat_id=self.peer_id,
						# message="Данной команды нет и пошел нахуй, долбаеб сука",
						# random_id=get_random_id()
					# )
		if event.from_user:
			self.api.messages.send(
				user_id=self.from_id,
				message="Пiшов нахой",
				random_id=get_random_id()
			)
		return

	# bot
	def help(self):
		HELP = "!help - этот текст"\
		"Модули:"\
		"!nmap <ip/domain> - утилита nmap"\
		"Администрирование:"\
		"!kick <mention> - кикнуть участника беседы"\
		"!add_admin <mention> - добавить администратора"
		self.api.messages.send(
			chat_id=self.peer_id,
			message=HELP,
			random_id=get_random_id()
		)
		return

	# modules
	def nmap(self):
		if len(self.text.split()) != 2:
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Команда не соотвествует шаблону",
				random_id=get_random_id()
			)
			return
		nmap_object = nmap.Nmap(self.text[1::].split()[1])
		response = nmap_object.start()
		if response is None:
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Хуй знает что ты хотел сделать, но ты долбаеб",
				random_id=get_random_id()
			)
			return
		self.api.messages.send(
			chat_id=self.peer_id,
			message=response,
			random_id=get_random_id()
		)
		return

	# administration
	def kick(self):
		if not is_admin(self.from_id, self.admins):
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Вы не имеете права на это",
				random_id=get_random_id()
			)
			return
		if len(self.text.split()) != 2:
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Команда не соотвествует шаблону",
				random_id=get_random_id()
			)
			return
		response = re.match(r"\[id\d{1,}\|\w{1,}\]", self.text[1::].split()[1].replace("*", "").replace("@", ""))
		if response is None:
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Нет упоминания",
				random_id=get_random_id()
			)
			return
		user_id = re.findall(r"(\d+)", self.text[1::].split()[1])
		try:
			if not user_id in self.admins:
				self.api.messages.removeChatUser(
					chat_id=self.peer_id,
					user_id=user_id[0]
				)
				self.api.messages.send(
					chat_id=self.peer_id,
					message="ГАТОВА ЕПТА!",
					random_id=get_random_id()
				)
			else:
				self.api.messages.send(
					chat_id=self.peer_id,
					message="Ты ахуел админа кикать?",
					random_id=get_random_id()
				)
		except exceptions.ApiError:
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Ты ахуел админа кикать?",
				random_id=get_random_id()
			)
		return

	def add_admin(self):
		if not is_admin(self.from_id, self.admins):
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Вы не имеете права на это",
				random_id=get_random_id()
			)
			return
		if len(self.text.split()) != 2:
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Команда не соотвествует шаблону",
				random_id=get_random_id()
			)
			return
		response = re.match(r"\[id\d{1,}\|\w{1,}\]", self.text[1::].split()[1].replace("*", "").replace("@", ""))
		if response is None:
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Нет упоминания",
				random_id=get_random_id()
			)
			return
		user_id = re.findall(r"(\d+)", self.text[1::].split()[1])
		self.config["admins"].append(user_id[0])
		self.api.messages.send(
			chat_id=self.peer_id,
			message="Администратор добавлен",
			random_id=get_random_id()
		)
		save_json(self.config)
		return

	def remove_admin(self):
		if not is_admin(self.from_id, self.admins):
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Вы не имеете права на это",
				random_id=get_random_id()
			)
			return
		if len(self.text.split()) != 2:
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Команда не соотвествует шаблону",
				random_id=get_random_id()
			)
			return
		response = re.match(r"\[id\d{1,}\|\w{1,}\]", self.text[1::].split()[1].replace("*", "").replace("@", ""))
		if response is None:
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Нет упоминания",
				random_id=get_random_id()
			)
			return
		user_id = re.findall(r"(\d+)", self.text[1::].split()[1])
		try:
			self.config["admins"].remove(user_id[0])
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Администратор удален",
				random_id=get_random_id()
			)
		except ValueError:
			self.api.messages.send(
				chat_id=self.peer_id,
				message="Он не админ, додик ебаный",
				random_id=get_random_id()
			)
			return
		save_json(self.config)
		return
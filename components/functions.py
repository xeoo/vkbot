import json
from vk_api.utils import get_random_id
import re

default_json = {
	"prefix": "",
	"admins": [],
	"token": "",
	"group_id": None,
}

def load_json(filename="config.json"):
	try:
		with open(f"./{filename}", "r") as file:
			return json.loads(file.read())
	except Exception as e:
		print(e)
		with open(f"./{filename}", "w") as file:
			json.dump(default_json, file)
		exit()
	return

def save_json(json_data, filename="config.json"):
	with open(f"./{filename}", "w") as file:
		json.dump(json_data, file)
	return

def is_admin(user_id, admin_list):
	if str(user_id) in admin_list:
		return True
	return False

def is_valid_command(command):
	return not re.match(r"^\w+$", command) is None


class ShrinkedFuncs(object):
	def __init__(self, api):
		self.api = api
		return

	def answer(self, text, chat_id=None, user_id=None):
		if not chat_id is None:
			self.api.messages.send(
				chat_id=chat_id,
				message=text,
				random_id=get_random_id()
			)
			return
		if not user_id is None:
			self.api.messages.send(
				user_id=user_id,
				message=text,
				random_id=get_random_id()
			)
			return
		return

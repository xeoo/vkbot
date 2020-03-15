import json

default_json = {
	"prefix": "",
	"admins": [],
	"token": "",
	"group_id": None
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
	if user_id in admin_list:
		return True
	return False

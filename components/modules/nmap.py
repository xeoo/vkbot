import re
import os

class Nmap(object):
	def __init__(self, host):
		self.host = host
		return

	def start(self):
		temp = self._host_valid()
		if not temp:
			return
		return os.popen(f"nmap {self.host}").read()

	def _host_valid(self):
		temp = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", self.host)
		if not temp is None:
			return True
		temp = re.match(r"^(\w+\.\w+){1,}$", self.host)
		if not temp is None:
			return True
		return False

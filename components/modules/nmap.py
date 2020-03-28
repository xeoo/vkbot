import re
import sys
import os

class Nmap(object):
	def __init__(self, host):
		sys.path.append(os.path.join(os.getcwd(), "nmap"))
		self.host = host
		return

	def start(self):
		temp = self._host_valid()
		if not temp:
			return
		return os.popen(f"nmap -Pn {self.host}").read()

	def _host_valid(self):
		temp = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", self.host)
		if not temp is None:
			return True
		temp = re.match(r"^(\w+\.\w+){1,}$", self.host)
		if not temp is None:
			return True
		return False

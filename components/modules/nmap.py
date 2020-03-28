import re
import nmap
import sys
import os

class Nmap(object):
	def __init__(self, host):
		sys.path.append(os.path.join(os.getcwd(), "nmap"))
		self.host = host
		return

	def start(self):
		hostnames = ""
		temp = self._host_valid()
		if not temp:
			return
		nmScan = nmap.PortScanner()
		result = nmScan.scan(self.host)
		if not bool(len(result["scan"])):
			return "Хост не найден (ответ не получен)"
			
		for hostname in result["scan"][self.host]["hostnames"]:
			hostnames += f"\nName: {hostname['name']} | Type: {hostname['type']}"
		for ip in result["scan"][self.host]["tcp"]:
			ips = f"\n{ip} {result['scan'][self.host]['tcp'][ip]['state']}"
		out =   f"INPUT: {self.host}\n"\
				f"\nUSED COMMAND: {result['nmap']['command_line']}\n"\
				f"\nHOSTNAMES: {hostnames}\n"\
				f"\nSTATUS: {result['scan'][self.host]['status']['state']}\n"\
				f"\nTCP: {ips}\n"
		return out

	def _host_valid(self):
		temp = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", self.host)
		if not temp is None:
			return True
		temp = re.match(r"^(\w+\.\w+){1,}$", self.host)
		if not temp is None:
			return True
		return False

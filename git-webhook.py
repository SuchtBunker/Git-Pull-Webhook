import subprocess, tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

GameServerPort = 27015
GameServerPath = os.path.dirname(os.path.realpath(__file__)) + "/garrysmod/addons/"
WebserverPort = GameServerPort + 10000 #->37015

Commands = [
	["git", "reset", "--hard"], 
	["git", "clean", "-fd"],
	["git", "pull", "--force"],
	
	["git", "submodule", "foreach", "--recursive", "git", "reset", "--hard"],
	["git", "submodule", "foreach", "--recursive", "git", "clean", "-fd"],
	["git", "submodule", "foreach", "--recursive", "git", "pull", "--force"],
]

class Webhook(BaseHTTPRequestHandler):
	def do_GET(self):
		self.handle_request()

	def do_POST(self):
		self.handle_request()

	def handle_request(self):
		for cmd in Commands:
			print(subprocess.run(
				cmd,
				cwd=GameServerPath,
				check=False,
				capture_output=True,
			))

		self.send_response(200)
		self.send_header("Content-Type", "text/plain")
		self.end_headers()
		self.wfile.write(b"Ok")

httpd = HTTPServer(("0.0.0.0", WebserverPort), Webhook)
print("Serving..")
httpd.serve_forever()
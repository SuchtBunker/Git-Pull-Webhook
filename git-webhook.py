import subprocess, tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

GameServerPort = 27015
GameServerPath = os.path.dirname(os.path.realpath(__file__)) + "/garrysmod/addons/"
DeployKey = """-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----"""
WebserverPort = GameServerPort + 10000 #->37015

Commands = [
	["git", "reset", "--hard"], 
	["git", "clean", "-fd"],
	["git", "pull", "--force"]
]

class Webhook(BaseHTTPRequestHandler):
	def do_GET(self):
		self.handle_request()

	def do_POST(self):
		self.handle_request()

	def handle_request(self):
		with tempfile.NamedTemporaryFile(delete=True) as keyFile:
			keyFile.write(DeployKey.encode())
			for cmd in Commands:
				print(subprocess.run(
					cmd,
					cwd=GameServerPath,
					check=False,
					capture_output=True,
					env={"GIT_SSH_COMMAND": f"ssh -i {keyFile.name} -o IdentitiesOnly=yes"}
				))
			keyFile.close()

			self.send_response(200)
			self.send_header("Content-Type", "text/plain")
			self.end_headers()
			self.wfile.write(b"Ok")

httpd = HTTPServer(("0.0.0.0", WebserverPort), Webhook)
print("Serving..")
httpd.serve_forever()
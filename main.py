from flask import Flask, render_template, send_from_directory, request
from modules import api, utils, exceptions, datatypes
import pathlib
import logging

app = Flask(__name__)
app.json_encoder = datatypes.CustomJSONEncoder

#===== load config =====
base_path = pathlib.Path(__file__).parent.resolve()
config_path = base_path / "config"
utils.load_config(config_path)
if utils.config["debug"]:
  print("Debug mode enabled. Stacktraces will be included in error responses.")

#===== error pages =====

@app.errorhandler(404)
def hanle_404(e):
  return render_template("404.html"), 404
  
#===== api routes =====

@app.route("/api/default_endpoint", methods=["GET"])
def get_default_endpoint():
  try:
    response = {"endpoint": utils.config["default_endpoint"]}
    return utils.generate_response(response)
  except Exception as e:
    return utils.handle_exception(e)

@app.route("/api/login", methods=["POST"])
def login():
  try:
    auth, headers = utils.extract_data(request)
    if "cookie" in headers: del headers["cookie"]
    data = request.json
    
    if not "username" in data or not "password" in data:
      raise exceptions.BadRequestError("Username or password missing.")
    if data["username"] == "":
      raise exceptions.BadRequestError("Username cannot be empty.")
    if data["password"] == "":
      raise exceptions.BadRequestError("Password cannot be empty.")
    
    session = api.login(auth["endpoint"], data["username"], data["password"], headers=headers)
    response = {"success": True}
    return utils.generate_response(response, session)
  
  except Exception as e:
    return utils.handle_exception(e)
    
@app.route("/api/students")
def get_students():
  try:
    auth, headers = utils.extract_data(request)
    endpoint = auth["endpoint"]
    
    response = {
      "students": api.get_students(endpoint, auth["session"], headers=headers)
    }
    return utils.generate_response(response)
    
  except Exception as e:
    return utils.handle_exception(e)

#===== user-visible pages =====

@app.route("/")
def homepage():
  return render_template("index.html")

@app.route("/assignments")
def assignments():
  return render_template("assignments.html")
  
#===== assets and static files =====

@app.route("/js/<path:path>")
def js(path):
  return send_from_directory("js", path)
  
@app.route("/assets/<path:path>")
def assets(path):
  return send_from_directory("assets", path)

@app.route("/css/<path:path>")
def css(path):
  return send_from_directory("css", path)

#===== start server =====

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=utils.config["debug"])
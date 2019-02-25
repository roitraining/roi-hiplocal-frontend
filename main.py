from flask import Flask, render_template, request, redirect, abort, jsonify
import requests
from datetime import datetime
import re
import os
from google.cloud import storage
import uuid
import auth
import json
from collections import namedtuple
try:
  import googleclouddebugger
  googleclouddebugger.enable()
except ImportError:
  pass

app = Flask(__name__)

try:
  app.config.from_object(os.environ['APP_SETTINGS'])
  URL = app.config['API']
  BUCKET = app.config['BUCKET']
  PROJECT_NAME = app.config['PROJECT']
except:
  # This occurs when testing locally from the command line
  #  - if no env variable is set, these defaults are set 
  # Port is 5000 because only reason for running from command line locally
  # is because backend is being debugged in vscode, in which case it is on port 5000
  URL = 'http://localhost:5000'
  PROJECT_NAME = 'roi-hiplocal'
  BUCKET = 'roi-hiplocal'

@app.route("/")
def home():
  try:
    data =  requests.get(URL + '/happenings').content
    # Parse JSON into a python object with attributes corresponding to dict keys.
    model = { 'happenings': json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))} 
  except Exception: 
    # backend is down, so provide alternative data
    model = {}
  model['greeting'] = os.getenv('GREETING', 'Welcome to Hip Local')
  return render_template("home.html", model=model, bucket=BUCKET)

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/happening")
def happening():
  try:
    auth.authorize(request)
  except Exception: 
      pass
      return redirect('/login')
  return render_template("happening.html")

@app.route("/happenings/add", methods=['POST'])
def create_happening():
  try:
    print('checking user has logged in')
    auth.authorize(request)
  except Exception: 
    print('user attempted to post new happening when not logged in')
    abort(403)
  # create guid to use for image name when approved, and as id of firestore object
  image_name = str(uuid.uuid4())
  url = URL + '/happenings/add/' + image_name
  data = request.form.to_dict(flat=True)
  # Default to empty image - shows No Image placeholder on site 
  data['image'] = '' 
  if 'image' in request.files.keys():
    print('user uploaded an image, initalizing storage client')
    storage_client = storage.Client(project = PROJECT_NAME)
    bucket = storage_client.get_bucket(BUCKET)
    try:
      print('Saving image ' + image_name + '.jpg to bucket ' + BUCKET)
      blob = bucket.blob('{}.jpg'.format(image_name))
      blob.upload_from_string(request.files["image"].read(), content_type=request.files["image"].content_type)
      data['image'] = 'pending' 
    except Exception as err:
      # want to save the happening, even if image was not successfully saved
      # but do want a record of what went wrong
      print(str(err))
  print(requests.post(url, data=data))
  return redirect('/')

@app.route("/happening/like/<id>")
def like(id):
  # uncomment following code to enforce authentication for liking
  # try:
  #   print('checking user has logged in')
  #   auth.authorize(request)
  # except Exception: 
  #   print('user attempted to like a happening when not logged in')
  #   return redirect('/login')
  url = URL + '/happening/like/' + id
  likes = requests.get(url)
  return jsonify(likes.text)

@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/terms")
def terms():
  return render_template("terms.html")

@app.route('/health', methods=['GET'])
def healthCheck():
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

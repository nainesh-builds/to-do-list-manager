from flask import Flask, render_template, request
from flask import jsonify
from flasgger import Swagger
from to_do import To_do
from datetime import datetime, timezone
import os

app = Flask(__name__)

FRONTEND_ORIGIN = "https://frontendtodoapp-production-7b4a.up.railway.app"

def cors_options_response():
    response = app.make_default_options_response()
    response.headers['Access-Control-Allow-Origin'] = FRONTEND_ORIGIN
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

def cors_data_response(data,status=200):
    response = jsonify(data)
    response.status_code = status
    response.headers['Access-Control-Allow-Origin'] = FRONTEND_ORIGIN
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

app.config['SWAGGER'] = {
    'openapi': '3.0.3',
    'uiversion': 3
}
swagger = Swagger(
    app,
    template_file=os.path.join(app.root_path, "openapi.yaml")
)

timestamp = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

def save():
    with open("to_do_list.txt", "w+") as f:
        for item in to_do_list:
            f.write(f"{item.get_id()}|{item.get_title()}|{item.get_desc()}\n")

to_do_list = []

if os.path.exists("to_do_list.txt"):
    with open("to_do_list.txt", "r") as f:
        for line in f:
            task_id, title, desc = line.strip().split("|")
            task = To_do(title, desc, task_id)
            print(f"{task_id}|{task.title}|{task.desc}")
            to_do_list.append(task)

@app.route("/api/v1/list",methods=["GET","OPTIONS"])
def listall_tasks():
    if request.method == "OPTIONS":
        return cors_options_response()
    items = []
    for task in to_do_list:
        item = {
            "id": task.get_id(),
            "title": task.get_title(),
            "description": task.get_desc()
        }       
        items.append(item)

    return cors_data_response({"items": items})


@app.route("/api/v1/create", methods=["POST","OPTIONS"])
def create_task():
    if request.method == "OPTIONS":
        return cors_options_response()
    data = request.get_json()

    title = data["title"]
    description = data["description"]

    task = To_do(title, description, None)
    to_do_list.append(task)
    save()
    return cors_data_response({"status": True, "timestamp": timestamp})

@app.route("/api/v1/list/<id>", methods=["GET","OPTIONS"])
def list_task(id):
    if request.method == "OPTIONS":
        return cors_options_response()    
    for task in to_do_list:
        if task.get_id() == id:
            item = {
                "id": task.get_id(),
                "title": task.get_title(),
                "description": task.get_desc(),
            }

            return cors_data_response(item)
    return cors_data_response({"Error": "Task not found"},404)

@app.route("/api/v1/edit/<id>", methods=["PUT","OPTIONS"])
def edit_task(id):
    if request.method == "OPTIONS":
        return cors_options_response()
    data = request.get_json()
    
    title = data["title"]
    description = data["description"]

    for task in to_do_list:
        if task.get_id() == id:
            task.set_title(title)
            task.set_desc(description)

            save() 

            item = {
                "id": task.get_id(),
                "title": task.get_title(),
                "description": task.get_desc(),
                "timestamp": timestamp
            }

            return cors_data_response(item)
        
    return cors_data_response({"Error": "Task not found"},404)


@app.route("/api/v1/delete/<id>", methods=["DELETE","OPTIONS"])
def delete_task(id):
    if request.method == "OPTIONS":
        return cors_options_response()
    for task in to_do_list:
        if task.get_id() == id:
            to_do_list.remove(task)

            save()

            return cors_data_response({"status": True, "timestamp": timestamp})
        
    return cors_data_response({"Error": "Task not found. So unable to remove the task"},404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
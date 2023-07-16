from flask import Flask, render_template, request
from logs_handler import LogsAPI, DB


app = Flask(__name__)
db = DB()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        db.insert_logs(request.form.get("message"))
    last_ten_logs = db.get_last_ten_logs()
    return render_template("index.html", logs_list=last_ten_logs)


@app.route("/api/logs", methods=["GET", "POST", "DELETE"])
def logs_api():
    api = LogsAPI()
    if request.method == "GET":
        return api.get_logs()
    elif request.method == "POST":
        return api.post_logs(request.data)
    elif request.method == "DELETE":
        return api.delete_logs()


@app.route("/api")
def api():
    return render_template("api.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8999, debug=True)

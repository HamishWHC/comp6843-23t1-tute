import secrets
from flask import Flask, abort, render_template, request, render_template_string

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(64)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bad", endpoint="bad")
@app.route("/fine", endpoint="fine")
@app.route("/better", endpoint="better")
def ssti():
    user = request.args.get("user")

    if request.endpoint == "bad":
        if user is not None:
            content = f"Oh hey it's {user}."
        else:
            content = "Who tf are you? Please provide user parameter."

        with open("templates/bad.html") as f:
            return render_template_string(f.read().format(content=content), title="Hello There!")

    if request.endpoint == "fine":
        with open("templates/good.html") as f:
            return render_template_string(f.read(), user=user)

    if request.endpoint == "better":
        return render_template("good.html", user=user)

    abort(500, "unreachable")


if __name__ == "__main__":
    app.run(debug=True)

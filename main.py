from flask import jsonify, Flask, render_template, url_for, request, redirect, session
from util import json_response

import data_handler

app = Flask(__name__)
app.secret_key = "thisisthemostsecretkey12345678910"


@app.route("/")
def index():
    """
    This is a one-pager which shows all the boards and cards
    """
    logout = request.args.get("logout")
    if logout:
        session.clear()
    return render_template('/index.html')


@app.route("/get-boards")
@json_response
def get_boards():
    """
    All the boards
    """
    user = get_user()
    return data_handler.get_boards(user)


@app.route("/get-cards/<int:board_id>")
@json_response
def get_cards_for_board(board_id: int):
    """
    All cards that belongs to a board
    :param board_id: id of the parent board
    """
    return data_handler.get_cards_for_board(board_id)


@app.route('/login', methods=["GET", "POST"])
def route_login():
    if request.method == "POST":
        user_name = request.form["userName"]
        password = request.form["password"]
        if data_handler.check_user_login(user_name, password):
            session["user"] = user_name

            return redirect(url_for("index"))
        else:
            error_message = "Wrong login details. Please try again."
            return render_template('login.html', page_type="Login", error_message=error_message)

    return render_template('login.html', page_type="Login")


@app.route('/registration', methods=['GET', 'POST'])
def route_registration():
    if request.method == "POST":
        user_name = request.form["userName"]
        password = request.form["password"]
        data_handler.save_user_details(user_name, password)
        return redirect(url_for("index"))
    return render_template('login.html', page_type="Register")


def get_user():
    if session.get("user"):
        user = session["user"]
    else:
        user = ""
    return user


@app.route('/get_current_user')
def get_current_user():
    username = get_user()
    return jsonify(username=username)


def main():
    app.run(debug=True)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()

from flask import Flask, render_template, url_for, request
from flask import jsonify, Flask, render_template, url_for, request, redirect, session
from util import json_response
import json
import psycopg2

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
    user = get_user()[0]
    return data_handler.get_boards(user)


@app.route("/get-board", methods=['GET', 'POST'])
@json_response
def get_board():
    if request.method == 'POST':
        new_board_id = json.loads(request.data)['max']
        return data_handler.get_board(int(new_board_id))
    return render_template('/index.html')


@app.route("/change-board-title", methods=['GET', 'POST'])
@json_response
def route_change_board_title():
    if request.method == 'POST':
        chosen_title = json.loads(request.data)[0]
        board_id = json.loads(request.data)[1]
        table = json.loads(request.data)[2]
        data_handler.update_chosen_title(chosen_title, int(board_id), table)
    return render_template('/index.html')


@app.route("/get-cards/<int:board_id>")
@json_response
def get_cards_for_board(board_id: int):
    """
    All cards that belongs to a board
    :param board_id: id of the parent board
    """
    return data_handler.get_cards_for_board(board_id)


@app.route("/create-new-board", methods=['GET', 'POST'])
@json_response
def create_new_board():
    if request.method == 'POST':
        new_board_data = request.json
        return data_handler.insert_new_board(new_board_data)
    return render_template('/index.html')


@app.route("/delete-card", methods=["GET", "POST"])
def route_delete_card():
    if request.method == 'POST':
        card_id = json.loads(request.data)[0]
        data_handler.delete_card(card_id)
        return card_id


@app.route('/login', methods=["GET", "POST"])
def route_login():
    if request.method == "POST":
        user_name = request.form["userName"]
        password = request.form["password"]
        if data_handler.check_user_login(user_name, password):
            user_id = data_handler.get_user_id_by_user_name(user_name)
            session["user"] = user_name
            session["user_id"] = user_id
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
        try:
            data_handler.save_user_details(user_name, password)
        except:
            error_message = "Username already exist. Please choose an other one!"
            return render_template('login.html', page_type="Register", error_message=error_message)
        return redirect(url_for("index"))
    return render_template('login.html', page_type="Register")


def get_user():
    if session.get("user"):
        user = session["user"]
        user_id = session["user_id"]
    else:
        user = ""
        user_id = ""
    return [user, user_id]


@app.route('/get_current_user')
def get_current_user():
    user = get_user()
    return jsonify(user=user)


@app.route("/card/", methods=['POST'])
@json_response
def create_card():
    req = request.get_json()
    board_id = req['boardId']
    return data_handler.add_new_card(board_id)


def main():
    app.run(debug=True)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()

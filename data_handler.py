import persistence
import database_common
from psycopg2 import sql
from werkzeug.security import check_password_hash, generate_password_hash


def get_card_status(status_id):
    """
    Find the first status matching the given id
    :param status_id:
    :return: str
    """
    statuses = persistence.get_statuses()
    return next((status['title'] for status in statuses if status['id'] == str(status_id)), 'Unknown')


@database_common.connection_handler
def get_boards(cursor):
    cursor.execute("""SELECT * FROM boards
                      """)
    data = cursor.fetchall()
    return data


@database_common.connection_handler
def get_cards_for_board(cursor, board_id):
    cursor.execute(
        sql.SQL("""SELECT * FROM cards
                   WHERE board_id = {board_id}
                       """).format(board_id=sql.Literal(board_id)))
    cards_data = cursor.fetchall()

    return cards_data


def check_user_login(user_name, user_input_password):
    stored_password = get_user_stored_password(user_name)
    if check_password_hash(stored_password, user_input_password):
        return True
    else:
        return False


@database_common.connection_handler
def get_user_stored_password(cursor, user_name):
    cursor.execute(
        sql.SQL("""SELECT password FROM users
                   WHERE username = {username}
                   """).format(username=sql.Literal(user_name))
    )
    data = cursor.fetchone()
    return data['password']


@database_common.connection_handler
def save_user_details(cursor, user_name, password):
    hashed_password = generate_password_hash(password, salt_length=8)
    cursor.execute(
        sql.SQL("""INSERT INTO users (username, password)
                   VALUES ({username}, {password});
                   """).format(username=sql.Literal(user_name),
                               password=sql.Literal(hashed_password))
    )
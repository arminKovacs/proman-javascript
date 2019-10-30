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
def get_boards(cursor, user):
    if user:
        cursor.execute(
            sql.SQL("""SELECT id FROM users
                      WHERE username = {username};
                      """).format(username=sql.Literal(user)))
        actual_user_id = cursor.fetchone()["id"]
    else:
        actual_user_id = "999999999"

    cursor.execute(
        sql.SQL("""SELECT * FROM boards
                   WHERE user_id ISNULL OR user_id = {userID}
                   ORDER BY id;
                   """).format(userID=sql.Literal(actual_user_id))
    )
    data = cursor.fetchall()
    return data


@database_common.connection_handler
def get_board(cursor, board_id):
    cursor.execute(
        sql.SQL("""SELECT * FROM boards
                   WHERE id = {board_id}
                """).format(board_id=sql.Literal(board_id)))

    board = cursor.fetchall()

    return board


@database_common.connection_handler
def get_cards_for_board(cursor, board_id):
    cursor.execute(
        sql.SQL("""SELECT * FROM cards
                   WHERE board_id = {board_id};
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
def get_user_id_by_user_name(cursor, user_name):
    cursor.execute(
        sql.SQL("""SELECT users.id FROM users
                    WHERE users.username = {user_name};""").format(user_name=sql.Literal(user_name))
    )
    data = cursor.fetchone()
    return data['id']



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


@database_common.connection_handler
def insert_new_board(cursor, board_title):
    cursor.execute(
        sql.SQL("""INSERT INTO boards(title)
                   VALUES ({board_title});
    """).format(board_title=sql.Literal(board_title)))

    cursor.execute(
        sql.SQL("""SELECT MAX(id) FROM boards
                """)
    )

    latest_id = cursor.fetchone()

    return latest_id


@database_common.connection_handler
def update_chosen_title(cursor, board_title, board_id, table):
    cursor.execute(
        sql.SQL("""UPDATE {table}
                   SET title = {board_title}
                   WHERE id = {board_id};
    """).format(board_title=sql.Literal(board_title),
                board_id=sql.Literal(board_id),
                table=sql.Identifier(table)))


@database_common.connection_handler
def delete_card(cursor, card_id):
    cursor.execute(
        sql.SQL("""DELETE FROM cards
                   WHERE id = {card_id}
                   """).format(card_id=sql.SQL(card_id))
    )
    return card_id


@database_common.connection_handler
def add_new_card(cursor, board_id):
    cursor.execute(
                    """INSERT INTO cards (board_id, title, status_id)
                    VALUES (%s, 'new card', '0') RETURNING id""", (board_id,))
    card_id = cursor.fetchone()['id']

    cursor.execute("""SELECT * FROM cards
                      WHERE id = %s""", (card_id,))
    return cursor.fetchall()

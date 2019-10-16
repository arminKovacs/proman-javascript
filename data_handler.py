import persistence
import database_common
from psycopg2 import sql


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
    cursor.execute("""SELECT boards.id as board_id, boards.title as board_title, cards.id AS card_id, 
                        cards.board_id AS card_board_id, cards.title AS card_title, cards.status_id, cards.order_id
                      FROM boards
                      JOIN cards ON (boards.id=cards.board_id)""")
    data = cursor.fetchall()
    return data


@database_common.connection_handler
def get_cards_for_board(cursor, board_id):
    cursor.execute(
        sql.SQL("""SELECT * FROM cards
                   WHERE board_id = {boardID}
                   """).format(boardID=sql.Literal(board_id))
    )
    data = cursor.fetchall()
    return data

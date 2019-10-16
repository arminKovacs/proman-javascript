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
    cursor.execute("""SELECT * FROM boards
                      """)
    data = cursor.fetchall()

    return data
    # return persistence.get_boards(force=True)


@database_common.connection_handler
def get_cards_for_board(cursor, board_id):
    cursor.execute(
        sql.SQL("""SELECT * FROM cards
                   WHERE board_id = {board_id}
                       """).format(board_id=sql.Literal(board_id)))
    cards_data = cursor.fetchall()

    return cards_data

    #persistence.clear_cache()
    #all_cards = persistence.get_cards()
    #matching_cards = []
    #for card in all_cards:
    #    if card['board_id'] == str(board_id):
    #        card['status_id'] = get_card_status(card['status_id'])  # Set textual status for the card
    #        matching_cards.append(card)
    #return matching_cards


@database_common.connection_handler
def insert_new_board(cursor, board_title):
    print(board_title)
    cursor.execute(
        sql.SQL("""INSERT INTO boards(title)
                   VALUES ({board_title});
    """).format(board_title=sql.Literal(board_title)))

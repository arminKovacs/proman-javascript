ALTER TABLE IF EXISTS ONLY public.boards DROP CONSTRAINT IF EXISTS pk_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.boards DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.cards DROP CONSTRAINT IF EXISTS pk_card_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.cards DROP CONSTRAINT IF EXISTS fk_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.statuses DROP CONSTRAINT IF EXISTS pk_status_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS pk_user_id CASCADE ;

DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.users_id_seq;
CREATE TABLE users (
    id serial NOT NULL,
    username text unique,
    password text
);

DROP TABLE IF EXISTS public.boards;
DROP SEQUENCE IF EXISTS  public.boards_id_seq;
CREATE TABLE boards (
    id serial NOT NULL,
    title text,
    user_id integer
);

DROP TABLE IF EXISTS public.cards;
DROP SEQUENCE IF EXISTS public.cards_id_seq;
CREATE TABLE cards (
    id serial NOT NULL,
    board_id integer,
    title text,
    status_id integer,
    order_id integer
);

DROP TABLE IF EXISTS public.statuses;
DROP SEQUENCE IF EXISTS public.statuses_id_seq;
CREATE TABLE statuses (
    id serial NOT NULL,
    title text
);

ALTER TABLE ONLY users ADD CONSTRAINT pk_user_id PRIMARY KEY (id);
ALTER TABLE ONLY boards ADD CONSTRAINT pk_board_id PRIMARY KEY (id);
ALTER TABLE ONLY boards ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE ONLY cards ADD CONSTRAINT pk_card_id PRIMARY KEY (id);
ALTER TABLE ONLY cards ADD CONSTRAINT fk_board_id FOREIGN KEY (board_id) REFERENCES boards(id);
ALTER TABLE ONLY statuses ADD CONSTRAINT pk_status_id PRIMARY KEY (id);

INSERT INTO statuses VALUES (0, 'new');
INSERT INTO statuses VALUES (1, 'in progress');
INSERT INTO statuses VALUES (2, 'testing');
INSERT INTO statuses VALUES (3, 'done');

INSERT INTO users VALUES (0, 'admin1', 'pbkdf2:sha256:150000$g984J6tx$d4d127de34cacddeb8c3cace3ee90251cf7ca09cdbbe8d08940adf6d0ee7e991')

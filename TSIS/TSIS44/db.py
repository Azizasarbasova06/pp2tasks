import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS game_sessions (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    level_reached INTEGER NOT NULL,
    played_at TIMESTAMP DEFAULT NOW()
);
"""


def get_connection(dict_cursor=False):
    cursor_factory = RealDictCursor if dict_cursor else None
    return psycopg2.connect(**DB_CONFIG, cursor_factory=cursor_factory)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)
        conn.commit()


def get_or_create_player(username):
    username = (username or "Player").strip()[:50] or "Player"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO players(username)
                VALUES (%s)
                ON CONFLICT (username) DO NOTHING
                RETURNING id
                """,
                (username,),
            )
            row = cur.fetchone()

            if row:
                player_id = row[0]
            else:
                cur.execute("SELECT id FROM players WHERE username = %s", (username,))
                player_id = cur.fetchone()[0]

        conn.commit()

    return player_id


def save_game_result(username, score, level_reached):
    player_id = get_or_create_player(username)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO game_sessions(player_id, score, level_reached)
                VALUES (%s, %s, %s)
                """,
                (player_id, int(score), int(level_reached)),
            )
        conn.commit()


def get_personal_best(username):
    username = (username or "Player").strip()[:50] or "Player"

    with get_connection(dict_cursor=True) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COALESCE(MAX(gs.score), 0) AS best_score
                FROM players p
                LEFT JOIN game_sessions gs ON gs.player_id = p.id
                WHERE p.username = %s
                """,
                (username,),
            )
            row = cur.fetchone()

    return int(row["best_score"] or 0)


def get_top_10():
    with get_connection(dict_cursor=True) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    p.username,
                    gs.score,
                    gs.level_reached,
                    TO_CHAR(gs.played_at, 'YYYY-MM-DD HH24:MI') AS played_at
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC, gs.level_reached DESC, gs.played_at ASC
                LIMIT 10
                """
            )
            rows = cur.fetchall()

    return rows

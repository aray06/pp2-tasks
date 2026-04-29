import psycopg2
from config import DB_PARAMS

def get_connection():
    return psycopg2.connect(DB_PARAMS)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY, player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL, level_reached INTEGER NOT NULL, played_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    p_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return p_id

def save_game(p_id, score, level):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", (p_id, score, level))
    conn.commit()
    cur.close()
    conn.close()

def get_personal_best(p_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (p_id,))
    res = cur.fetchone()[0]
    cur.close()
    conn.close()
    return res if res is not None else 0

def get_top_10():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, s.score, s.level_reached 
        FROM game_sessions s 
        JOIN players p ON s.player_id = p.id 
        ORDER BY s.score DESC LIMIT 10
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data
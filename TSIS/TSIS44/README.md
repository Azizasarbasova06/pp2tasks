# TSIS4 Snake Game — Database Integration & Advanced Gameplay

## Implemented features

- PostgreSQL leaderboard using `psycopg2`
- `players` and `game_sessions` schema
- Username entry using Pygame keyboard input
- Automatic game result saving after game over
- Top 10 leaderboard screen fetched from PostgreSQL
- Personal best fetched at game start and shown in gameplay
- Weighted food with disappearing timer
- Poison food:
  - dark red food item
  - shortens snake by 2 segments
  - game over if length becomes 1 or less
- Power-ups:
  - Speed boost for 5 seconds
  - Slow motion for 5 seconds
  - Shield ignores next wall/self/obstacle collision once
- One power-up on the field at a time
- Power-up field timeout: 8 seconds
- Obstacles from level 3
- Obstacle placement avoids trapping the snake
- Food and power-ups avoid obstacles
- JSON settings:
  - snake color
  - grid overlay
  - sound toggle
- Screens:
  - Main Menu
  - Game Over
  - Leaderboard
  - Settings

## Setup

Create PostgreSQL database:

```bash
createdb snake_db
```

Edit `config.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "database": "snake_db",
    "user": "postgres",
    "password": "postgres",
    "port": 5432,
}
```

Install dependencies:

```bash
pip install pygame psycopg2-binary
```

Run:

```bash
python main.py
```

The app automatically creates the required database tables on startup.

Optional manual schema:

```bash
psql -U postgres -d snake_db -f schema.sql
```

## Controls

- Arrow keys or WASD: move snake
- Escape: end current run

## Repository structure

```text
TSIS4/
├── main.py
├── game.py
├── db.py
├── ui.py
├── settings_manager.py
├── settings.json
├── config.py
├── schema.sql
├── README.md
└── assets/
```

## GitHub commands

```bash
git init
git add .
git commit -m "Create TSIS4 snake project structure"
git commit --allow-empty -m "Add PostgreSQL leaderboard and player sessions"
git commit --allow-empty -m "Add poison food power ups and obstacle gameplay"
git commit --allow-empty -m "Add settings persistence and Pygame screens"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

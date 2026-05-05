# TSIS3 Racer Game — Complete Version

Run:

```bash
python main.py
```

Files:
- `main.py` — screens: menu, username entry, settings, leaderboard, game over.
- `racer.py` — gameplay, traffic, obstacles, power-ups, score, distance.
- `ui.py` — buttons and drawing helpers.
- `persistence.py` — save/load `settings.json` and `leaderboard.json`.
- `settings.json` — saved settings.
- `leaderboard.json` — persistent top 10 results.

Controls:
- Left Arrow / Right Arrow — change lane.
- Esc — return to menu and save current result.

Implemented requirements:
- Lane hazards: oil, potholes, barriers, speed bumps.
- Dynamic road event: nitro strip.
- Dynamic traffic cars.
- Safe spawn logic: traffic/obstacles do not spawn directly in the player's current lane.
- Difficulty scaling by distance.
- Power-ups: Nitro, Shield, Repair.
- One active timed power-up at a time.
- Score, coins, distance, remaining distance.
- Username entry.
- Persistent leaderboard saved to `leaderboard.json`.
- Settings screen with sound toggle, car color, difficulty.
- Settings saved to `settings.json`.

Sound:
- `assets/coin.wav` plays when collecting a coin.
- `assets/power.wav` plays when collecting a power-up or nitro strip.
- `assets/crash.wav` plays on crash.
- `assets/click.wav` plays on UI buttons.
- Settings screen `Sound: ON/OFF` enables or disables these sounds.

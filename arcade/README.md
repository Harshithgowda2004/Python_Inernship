# 🕹 PixelArcade — Python Flask Game Hub

A modern, neon-themed arcade game hub with 5 games, user authentication, score tracking, and a live leaderboard.

---

## 🎮 Games

| Game | Description | Points |
|------|-------------|--------|
| 🎯 Number Guess | Guess the secret number (1–100) in 7 tries | Up to 50 pts |
| 🧠 Trivia Quiz | 10 general knowledge questions | Up to 100 pts |
| ⭕ Tic Tac Toe | Play against an unbeatable minimax AI | 75 pts per win |
| 🐍 Snake | Classic snake — eat food, don't crash | 1 pt per 10 score |
| 🃏 Memory Match | Flip 16 cards and match all 8 pairs | Up to 80 pts |

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install flask
```

### 2. Initialize the database
```bash
python database.py
```

### 3. Start the server
```bash
python app.py
```

### 4. Open your browser
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
arcade/
├── app.py            ← Flask server & routes
├── database.py       ← DB initializer
├── arcade.db         ← SQLite database (auto-created)
└── templates/
    ├── base.html     ← Shared layout (neon UI, nav, toast)
    ├── login.html    ← Login page
    ├── register.html ← Registration page
    ├── dashboard.html← Game hub + leaderboard
    ├── guess.html    ← Number Guess game
    ├── quiz.html     ← Trivia Quiz game
    ├── tictactoe.html← Tic Tac Toe vs AI
    ├── snake.html    ← Snake game (canvas)
    └── memory.html   ← Memory Match card game
```

---

## 🔐 Security Notes

- Passwords are hashed with SHA-256 before storage
- Sessions are server-side via Flask's secret key
- All DB queries use parameterized statements (no SQL injection)

---

## 🎨 Tech Stack

- **Backend:** Python 3 + Flask
- **Database:** SQLite3
- **Frontend:** Vanilla HTML/CSS/JS (no frameworks)
- **Fonts:** Orbitron + Rajdhani (Google Fonts)
- **Theme:** Neon retro-arcade dark UI

# Music App Backend

This is the Flask backend for a music streaming application. It provides secure user authentication, playlist management, and audio streaming functionality. Users can log in, browse songs, create playlists, and play tracks from the static audio library.

## Getting Started

### Prerequisites
- Python 3.9+
- Flask
- PostgreSQL (or SQLite for testing)

### Installation

```bash
git clone https://github.com/yourusername/music-backend.git
cd music-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory and configure:

```env
SECRET_KEY=your-secret
DATABASE_URL=sqlite:///dev.db
JWT_SECRET_KEY=your-jwt-secret
```

### Running the Server

```bash
flask db upgrade
flask run
```

Server runs at [http://localhost:5000](http://localhost:5000)

---

## Project Structure

```
backend/
├── app/
│ ├── __init__.py
│ ├── models.py
│ ├── routes/
│ │ ├── auth.py
│ │ ├── songs.py
│ │ └── playlists.py
├── static/
│ └── audio/
├── seed_from_static.py
├── README.md
```

---

## Authentication

- `POST /api/auth/login` – Logs in a user and returns a JWT token
- `POST /api/auth/register` – Registers a new user
- All protected routes require `Authorization: Bearer <token>` header

---

## Audio Streaming

Serve MP3 files via:

```
GET /audio/<filename>
```

Returns streamed audio from the `static/audio/` folder.

---

## Sample Frontend Usage

Frontend requests must attach the JWT token:

```js
fetch("/api/songs", {
  headers: {
    Authorization: `Bearer ${token}`
  }
})
```

---

## Running Tests

```bash
pytest
```

Use `test/` folder for unit and route tests.

---

## Credits

Made using Flask and SQLAlchemy.
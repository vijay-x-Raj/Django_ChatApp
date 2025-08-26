git clone https://github.com/yourusername/django-chatapp.git
<div align="center">

# 💬 Django ChatApp

Lightweight multi-room chat built with **Django**. It currently uses **simple AJAX polling** (every 2s) to fetch new messages – deliberately beginner‑friendly (no extra libraries, no WebSocket server required). Messages are stored in the database and rendered into a clean, responsive UI.

🎯 Goal: show how to go from a plain Django project to a functional live-ish chat with minimal moving parts.

</div>

---

## ✅ Current Feature Set

| Area | What’s Implemented |
|------|--------------------|
Auth | Login / Logout (Django built‑in), room list accessible after auth |
Rooms | Static set of `Room` objects (name + slug) listed at `/rooms/` |
Messaging | Persisted `Message` model (user, room, content, timestamp) |
Live Updates | AJAX polling JSON endpoint (`?after=<last_id>`) every 2 seconds |
UI | Tailwind via CDN, responsive layout, own vs others’ message styling |
Security | CSRF protection on POST, auth required for all room + message endpoints |

> NOTE: Earlier experimental WebSocket code (Channels) is present in history but not required for current functionality.

---

## 🧱 Architecture (High Level)

```
Browser
	├─ Loads room page (HTML rendered by Django)
	├─ JavaScript polls /rooms/<slug>/messages/?after=<last_id>
	├─ Sends new message via POST /rooms/<slug>/messages/create/
	└─ Appends any new JSON messages to the DOM

Django Views
	├─ rooms() -> list rooms
	├─ room() -> initial HTML + last N messages
	├─ room_messages() -> JSON incremental fetch
	└─ create_message() -> JSON create

Database
	├─ Room(id, name, slug)
	└─ Message(id, room_id, user_id, content, date_added)
```

The polling approach keeps logic simple: the client only asks for messages with an `id` greater than the latest it has.

---

## 📦 Data Models

Room:
```text
name (CharField)
slug (SlugField, unique)
```

Message:
```text
room (FK -> Room)
user (FK -> User)
content (Text)
date_added (auto timestamp)
ordering = date_added asc
```

---

## � Endpoints (Current)

| Method | Path | Purpose | Returns |
|--------|------|---------|---------|
GET | `/rooms/` | Room listing | HTML |
GET | `/rooms/<slug>/` | Room chat UI + initial messages | HTML |
GET | `/rooms/<slug>/messages/?after=<id>` | New messages after given id | `{messages: [...]}` |
POST | `/rooms/<slug>/messages/create/` | Create a message | New message JSON or 400 |

JSON message shape:
```json
{
	"id": 42,
	"content": "Hello world",
	"username": "alice",
	"date": "13:57:02"
}
```

---

## 🖥️ UI Behavior

1. Page renders last 25 messages (oldest at top).
2. JS determines the highest message `id` (`lastId`).
3. A `setInterval` runs every 2000 ms calling the JSON endpoint with `?after=lastId`.
4. New messages (if any) are appended; `lastId` updates.
5. Sending a message (Enter / Send) POSTs, then triggers an immediate fetch.

Advantages (for beginners):
- No extra dependency beyond Django.
- Easy to debug with browser network tab.

Limitations:
- Slight delay (up to polling interval).
- Inefficient if many rooms/users; WebSockets or Server-Sent Events scale better.

---

## � Quick Start (Windows PowerShell / Git Bash)

```bash
# Clone your fork / this repo
git clone https://github.com/vijay-x-Raj/Django_ChatApp.git
cd Django_ChatApp

# (Optional) create virtual environment
python -m venv venv
source venv/Scripts/activate  # or: . venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# (Optional) create initial user
python manage.py createsuperuser

# Run dev server
python manage.py runserver
```

Visit: http://127.0.0.1:8000/ then sign in and go to `/rooms/`.

---

## 🔄 How Polling Works (Incremental Fetch)

Pseudo-flow in the room script:
```js
lastId = highestExistingId();
setInterval(async () => {
	const res = await fetch(`/rooms/<slug>/messages/?after=${lastId}`);
	const { messages } = await res.json();
	for (const m of messages) { append(m); lastId = m.id; }
}, 2000);
```

To reduce latency you can lower the interval (e.g. 1000 ms) or swap in WebSockets later.

---

## 🧪 Manual Testing Checklist

| Action | Expected |
|--------|----------|
Open `/rooms/<slug>/` in two browsers | Messages appear the same after ≤2s |
Send message in one tab | Appears immediately there & in other after next poll |
Send blank message | Not created (400 response) |
Refresh page | Last 25 messages load |

---

## 🔁 Upgrade Paths (When Ready)

| Goal | Suggestion |
|------|------------|
Lower latency | Switch to Django Channels WebSockets (consumer already scaffolded) |
Reduce DB load | Increase `after` batching; consider caching layer |
Mobile app / SPA | Convert endpoints to proper REST (rename create path; add pagination) |
Real presence | Add Redis + track user connect/disconnect events |
Typing indicators | Add lightweight endpoint or WebSocket event |

---

## 🛠️ Converting Endpoints to REST Style (Example)

Current create URL: `/rooms/<slug>/messages/create/`

RESTful alternative:
```
POST /api/rooms/<slug>/messages/
GET  /api/rooms/<slug>/messages/?after=<id>
```
Both share the same collection path; method distinguishes action.

---

## ❓ FAQ

**Why not WebSockets now?**  Keeping onboarding simple; polling teaches data flow first. You can swap in Channels later by running an ASGI server (daphne / uvicorn) and wiring the template back to the consumer.

**Will polling scale?**  For a handful of users, yes. For hundreds of concurrent rooms, move to push (WebSockets or SSE) + Redis.

**How do I change the polling interval?**  Edit the `setInterval(poll, 2000);` line in `room.html`.

**How many past messages load?**  Currently the last 25. Adjust the slice in `room/views.py`.

---

## 🧹 Housekeeping Ideas

- Remove unused `channels` dependency if you commit to polling only.
- Add tests for `room_messages` and `create_message` endpoints.
- Add pagination (e.g. `?before=<id>` for older history).
- Add Dockerfile for easier onboarding.

---

## 🐛 Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
Messages not showing | Polling endpoint blocked by auth | Ensure you are logged in |
CSRF 403 on send | Missing CSRF cookie | Visit any GET page first or add `{% csrf_token %}` if using a form submission |
Time always same | Browser cached page | Hard refresh (Ctrl+F5) |

---

## 📄 License

MIT (adjust if needed). Feel free to use and extend.

---

Happy building! ✨

If you’d like a WebSocket or SSE branch set up next, just ask.

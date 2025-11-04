```markdown
# 🌟 Qwik – Ephemeral Social Media Platform

Qwik is a cross-platform social media app that empowers users to share spontaneous moments—photos, videos, or status updates—that disappear after 24 hours. Inspired by platforms like Instagram and Snapchat, Qwik prioritizes **authenticity**, **privacy**, and **real-time interaction** in a world of curated content.

For detailed project requirements, see [PRD.md](docs/PRD.md). For MVP specifics, check [MVP.md](docs/MVP.md).

---

## 🚀 Features

- 📸 **Ephemeral Posts**: Share “Blinks” (photos/videos/status) that auto-delete after 24 hours.
- 🎭 **Mood & Moment Tags**: Tag your posts with moods like happy, chill, or excited.
- 💬 **Real-Time Chat**: One-to-one messaging with seen status and typing indicators.
- 😍 **Reactions & Comments**: Express yourself with emoji reactions and comments.
- 🔔 **Smart Notifications**: Get notified only when it matters.
- 🔐 **Privacy Controls**: Choose who sees your content—public, friends, or close circle.
- 🛡️ **Admin Panel**: Manage users, moderate content, and view analytics.

---

## 🧱 Tech Stack

| Layer         | Technology                        |
| ------------- | --------------------------------- |
| Frontend      | Flutter (Android, iOS, Web)       |
| Backend       | Django + Django REST Framework    |
| Database      | PostgreSQL                        |
| Real-Time     | Django Channels + Redis           |
| Media Storage | Cloudinary / AWS S3               |
| Auth          | JWT (SimpleJWT)                   |
| Notifications | Firebase Cloud Messaging (optional) |

---

## 📁 Project Structure

```
qwik/
├── backend/       # Django backend with REST APIs and real-time features
├── frontend/      # Flutter frontend for cross-platform app
├── docs/          # Documentation: PRD, MVP, and architecture details
└── README.md      # This file
```

---

## 🛠️ Getting Started

### Prerequisites

- **Python 3.8+** for backend
- **Flutter SDK** for frontend
- **PostgreSQL** database
- **Redis** for real-time messaging (optional for MVP)
- **Git** for version control

### 🔧 Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend/
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   env\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

### 📱 Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend/
   ```

2. Install dependencies:
   ```bash
   flutter pub get
   ```

3. Run the app:
   ```bash
   flutter run
   ```

For web deployment, ensure Flutter web is enabled: `flutter config --enable-web`.

---

## 🧪 MVP Scope

- ✅ User authentication (JWT-based)
- ✅ Post ephemeral content with mood tags
- ✅ Feed from friends and public posts
- ✅ 1-to-1 real-time chat
- ✅ In-app notifications
- ✅ Basic admin panel for moderation

---

## 📌 Roadmap

- [ ] AI-powered feed recommendations
- [ ] Group chat functionality
- [ ] Voice/video calls
- [ ] AR filters and stickers
- [ ] Push notifications
- [ ] Advanced analytics dashboard

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

For major changes, please open an issue first to discuss.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ✨ Credits

Built with ❤️ by [Adithyan](https://github.com/YOUR_USERNAME).  
Inspired by real-time, privacy-first social sharing platforms.
```
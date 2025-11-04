```markdown
# 🌟 Qwik – Ephemeral Social Media Platform

**Qwik** is a cross-platform social media app that empowers users to share spontaneous moments — photos, videos, or status updates — that automatically disappear after 24 hours. Inspired by platforms like Instagram and Snapchat, Qwik prioritizes **authenticity**, **privacy**, and **real-time interaction** in a world dominated by curated content.

📄 For detailed requirements, see [docs/PRD.md](docs/PRD.md)  
📦 For MVP scope, check [docs/MVP.md](docs/MVP.md)

---

## 🚀 Key Features

- 📸 **Ephemeral Posts**: Share “Blinks” that vanish after 24 hours.
- 🎭 **Mood & Moment Tags**: Add emotional context to your posts.
- 💬 **Real-Time Chat**: One-to-one messaging with seen status and typing indicators.
- 😍 **Reactions & Comments**: Express yourself with emojis and comments.
- 🔔 **Smart Notifications**: Get notified only when it matters.
- 🔐 **Privacy Controls**: Choose your audience — public, friends, or close circle.
- 🛡️ **Admin Panel**: Moderate content, manage users, and view reports.

---

## 🧱 Tech Stack

| Layer         | Technology                        |
|---------------|-----------------------------------|
| Frontend      | Flutter (Android, iOS, Web)       |
| Backend       | Django + Django REST Framework    |
| Database      | PostgreSQL                        |
| Real-Time     | Django Channels + Redis           |
| Media Storage | Cloudinary / AWS S3               |
| Authentication| JWT (SimpleJWT)                   |
| Notifications | Firebase Cloud Messaging (optional)|

---

## 📁 Project Structure

```text
qwik/
├── backend/       # Django backend with REST APIs and real-time features
├── frontend/      # Flutter frontend for cross-platform app
├── docs/          # Documentation: PRD, MVP, and architecture details
└── README.md      # This file
```

---

## 🛠️ Getting Started

### 🔧 Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend/
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   env\Scripts\activate  # On Windows
   source env/bin/activate  # On macOS/Linux
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

---

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

💡 For web deployment:
```bash
flutter config --enable-web
```

---

## 🧪 MVP Scope

- ✅ JWT-based user authentication
- ✅ Ephemeral post creation with mood tags
- ✅ Feed from friends and public posts
- ✅ Real-time 1-to-1 chat
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

We welcome contributions! To get started:

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request

For major changes, please open an issue first to discuss your ideas.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## ✨ Credits

Built with ❤️ by [Adithyan](https://github.com/Adithyan-k-p)  
Inspired by real-time, privacy-first social sharing platforms.
```

---

Let me know if you’d like me to generate the `PRD.md` and `MVP.md` files next, or scaffold your backend with models and APIs. You’re building something awesome — let’s keep Qwik moving!
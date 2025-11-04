📄 Product Requirement Document (PRD) – Qwik
1. 🧭 Project Overview
Project Name: Qwik Type: Cross-Platform Social Media App Platform: Flutter (Mobile/Web) + Django REST Framework (Backend) Goal: A privacy-focused, ephemeral content-sharing platform where users post short-lived “Blinks” that disappear after 24 hours. Qwik emphasizes authenticity, mood tagging, and real-time interaction.

2. ❓ Problem Statement
Traditional social media platforms prioritize permanence and curated content. Qwik solves this by:

Encouraging spontaneous, short-lived sharing

Prioritizing privacy and control

Reducing notification fatigue

Supporting real-time chat and reactions

3. 🎯 Objectives
Build a full-stack social media app with ephemeral posts

Enable mood tagging and interactive reactions

Support real-time chat and smart notifications

Ensure cross-platform access via Flutter

Showcase scalable architecture and clean codebase

4. 👥 User Roles
Role	Permissions
User	Register, post Blinks, chat, react, manage privacy
Admin	Moderate content, manage users, view reports
5. 🔑 Core Features
✅ User Features
JWT-based authentication

Profile creation and editing

Post Blinks (photo/video/status) with auto-expiry

Feed from friends and public posts

Emoji reactions and comments

Real-time 1-to-1 chat

Notification system

Privacy controls (Public/Friends/Close Circle)

✅ Admin Features
Admin login

User and content moderation

Report handling

Basic analytics dashboard

6. ⚙️ System Requirements
Functional
Ephemeral post logic (auto-delete after 24h)

Real-time messaging (Django Channels)

Notifications (in-app + optional push)

Secure APIs with JWT

Non-Functional
Fast feed loading (<3s)

Secure password hashing

Scalable backend

99% uptime target

7. 🧱 Tech Stack
Layer	Technology
Frontend	Flutter (Dart)
Backend	Django + DRF
Database	PostgreSQL
Real-Time	Django Channels + Redis
Media Storage	Cloudinary / AWS S3
Auth	JWT (SimpleJWT)
Notifications	Firebase Cloud Messaging (optional)
8. 🗃️ Database Schema (Simplified)
Table	Fields
users	id, username, email, password, bio, profile_pic
posts	id, user_id, media_url, caption, timestamp, expires_at
chat_messages	id, sender_id, receiver_id, message, timestamp, seen
notifications	id, user_id, type, content, is_read, timestamp
reports	id, reporter_id, post_id, reason, status

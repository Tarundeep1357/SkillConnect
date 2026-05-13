# Live Messaging README

## Overview

This project now includes a live messaging feature for communication between students and recruiters.

The chat is:

- real-time: messages appear instantly without refreshing
- persistent: messages are saved in MySQL
- secure: access is controlled by JWT login and application ownership
- workflow-based: chat is tied to a job application, not random user-to-user messaging

That design keeps the feature simple and matches the current project structure.

## What Was Used

### Backend

- `FastAPI` for REST APIs
- `FastAPI WebSocket` support for real-time delivery
- `MySQL` for storing conversations and messages
- `JWT` token authentication using the existing login system
- an in-memory connection manager on the server to track currently connected users

### Frontend

- `React` for the messaging UI
- `Axios` for REST API calls
- native browser `WebSocket` for live updates
- existing `localStorage` token and role handling

## Main Idea

Instead of building an open chat system where any user can message any other user, messaging is attached to an existing `job_application`.

That means:

- a student can message only for applications they submitted
- a recruiter can message only for applications belonging to jobs they posted
- every conversation is linked to one application

This avoids complicated permission rules and fits well with the current database design.

## Data Model

### New Table

The live chat uses a new table:

`job_application_messages`

### Columns

- `id`: primary key
- `application_id`: links message to a job application
- `sender_id`: user who sent the message
- `recipient_id`: user who should receive the message
- `message_text`: actual message content
- `created_at`: when the message was sent
- `read_at`: when the recipient read the message

### Why This Structure

- `application_id` keeps the conversation tied to the hiring workflow
- `sender_id` and `recipient_id` make delivery and unread counting easy
- `read_at` supports unread badges and read tracking

## Backend Architecture

### 1. Database Initialization

On backend startup, the app creates the `job_application_messages` table if it does not already exist.

It also creates:

- indexes for fast lookups
- foreign keys to `job_applications` and `users`

This is handled inside the existing startup migration flow in `main.py`.

### 2. Connection Manager

The backend uses a `MessageConnectionManager`.

Its job is to:

- accept WebSocket connections
- store active sockets by `user_id`
- send events to one or more connected users
- remove broken sockets automatically

Important note:

- this manager is in memory
- it works well for a single backend instance
- if you scale to multiple servers later, you would need Redis or another shared pub/sub layer

### 3. Authorization Rules

Before loading or sending messages, the backend checks:

- is the user a `student` or `recruiter`
- does the application exist
- is the student the owner of the application
- or is the recruiter the owner of the job connected to that application

If not, access is denied.

## REST API Endpoints

### `GET /messages/threads`

Returns the current user's conversation list.

Each thread includes:

- `application_id`
- `job_id`
- job title and company
- application status
- counterpart user info
- latest message preview
- latest activity time
- unread count

### `GET /messages/threads/{application_id}`

Returns:

- thread summary
- all messages in that application conversation

This endpoint also marks unread messages as read for the current user.

### `POST /messages/threads/{application_id}`

Creates a new message in a thread.

Input:

```json
{
  "message": "Hello, I am interested in the next interview step."
}
```

Response:

- the created message
- updated thread summary

After saving the message, the backend pushes a live event through WebSocket.

### `POST /messages/threads/{application_id}/read`

Marks unread messages in that thread as read for the current user.

Used to keep unread counts accurate.

## WebSocket Endpoint

### `GET /ws/messages?token=YOUR_JWT_TOKEN`

The frontend opens a WebSocket connection using the login token.

### Why Token In Query

The browser WebSocket API does not let us easily send the normal Axios `Authorization` header in the same way as REST calls, so the token is passed as a query parameter.

The backend validates the token before accepting the socket.

### Events Used

#### Server -> Client

`connection.ready`

Sent after the socket is accepted.

Example:

```json
{
  "type": "connection.ready",
  "user_id": 7
}
```

`message.created`

Sent when a message is created for the sender and recipient.

Example:

```json
{
  "type": "message.created",
  "application_id": 12,
  "message": {
    "id": 18,
    "application_id": 12,
    "sender_id": 7,
    "recipient_id": 2,
    "sender_name": "Priya Singh",
    "message": "Thank you for the update.",
    "created_at": "2026-04-10T14:00:00Z",
    "read_at": null
  }
}
```

#### Client -> Server

`ping`

Used to keep the connection active.

Example:

```json
{
  "type": "ping"
}
```

#### Server -> Client

`pong`

Response to keepalive ping.

## Frontend Architecture

### Messaging Page

A new shared page was added:

`skillconnect-frontend/src/pages/MessagesPage.jsx`

This page is used by both:

- `/student/messages`
- `/recruiter/messages`

### What The Page Does

- loads the logged-in profile
- loads conversation threads
- loads messages for the selected thread
- opens the WebSocket connection
- listens for new messages
- updates the UI without refresh
- sends new messages through REST

### Why REST + WebSocket Together

The system uses both, because each one solves a different problem:

- REST is used for loading existing threads and storing messages reliably
- WebSocket is used for instant delivery after a message is saved

This is a common and stable pattern.

## UI Flow

### Student Side

Entry points:

- student dashboard -> `Messaging`
- job board top bar -> `Messages`
- my applications section -> `Message Recruiter`

### Recruiter Side

Entry points:

- recruiter dashboard top bar -> `Messages`
- applications inside a posted job -> `Message Candidate`

### How A Conversation Opens

The messages page can accept:

`?applicationId=123`

If present, that thread opens automatically.

This is how buttons like `Message Recruiter` and `Message Candidate` jump directly into the correct conversation.

## Full Message Flow

### Send Message

1. User types message in the UI
2. Frontend sends `POST /messages/threads/{application_id}`
3. Backend validates access
4. Backend stores message in MySQL
5. Backend pushes `message.created` through WebSocket
6. Sender and recipient UIs update instantly

### Open Thread

1. Frontend calls `GET /messages/threads/{application_id}`
2. Backend checks access
3. Backend returns full message history
4. Backend marks recipient-side unread messages as read
5. Frontend renders the chat

## How To Know If It Is Live

On the Messages page, a status pill is shown at the top.

Possible values:

- `Connecting...`
- `Live`
- `Offline`

### Meaning

- `Live`: WebSocket is connected and real-time updates should work
- `Connecting...`: connection is still opening
- `Offline`: live socket is not connected

### Real Test

If one user sends a message and the other user sees it instantly without refreshing, then live messaging is working.

## How To Test Properly

Because the app uses `localStorage`, one browser profile can only stay logged in as one user at a time.

### Best Test Methods

- normal browser window for student + incognito window for recruiter
- Chrome for student + Edge for recruiter
- two different browser profiles

### Suggested Test Steps

1. Start backend
2. Start frontend
3. Login as recruiter in one browser session
4. Login as student in another browser session
5. Student applies for a recruiter's job
6. Student opens `My Applications` and clicks `Message Recruiter`
7. Recruiter opens the job application list and clicks `Message Candidate`
8. Send messages from both sides
9. Confirm they appear immediately without page refresh

## Files Added Or Updated

### Backend

- `main.py`
- `schemas.py`

### Frontend

- `skillconnect-frontend/src/App.jsx`
- `skillconnect-frontend/src/pages/MessagesPage.jsx`
- `skillconnect-frontend/src/pages/messages-page.css`
- `skillconnect-frontend/src/pages/StudentDashboard.jsx`
- `skillconnect-frontend/src/pages/StudentJobsPage.jsx`
- `skillconnect-frontend/src/pages/student-jobs-page.css`
- `skillconnect-frontend/src/pages/RecruiterDashboard.jsx`
- `skillconnect-frontend/src/pages/recruiter-dashboard.css`

## Why This Approach Was Chosen

This design was chosen because it fits the current project well:

- your backend already uses FastAPI and JWT auth
- your frontend already uses React and Axios
- your app already has a strong relationship between students, recruiters, jobs, and applications

So instead of adding a heavy external chat service, the live messaging feature was built directly into your existing stack.

## Current Limitations

### 1. Single Server Memory Connections

The active WebSocket connection map is stored in memory.

That means:

- good for local development and single-server deployment
- not enough for multi-server scale-out

For larger deployment, use:

- Redis pub/sub
- shared session state
- possibly a message broker

### 2. No Attachments

The current version supports text messages only.

### 3. No Typing Indicators

The current version does not show:

- typing...
- online/offline presence
- delivered status

### 4. Query Token Authentication

The WebSocket uses the JWT token in the query string.

This is acceptable for local or controlled setups, but for production you should review:

- secure HTTPS/WSS usage
- token expiry handling
- stricter socket auth strategies if needed

## Possible Future Improvements

- typing indicators
- online presence
- last seen status
- message search
- file attachments
- pagination for long conversations
- push notifications
- Redis-backed multi-instance WebSocket broadcasting
- admin conversation monitoring tools

## Verification Done

The implementation was checked with:

- Python syntax validation
- backend startup validation
- frontend production build

## Summary

The live messaging feature in this project uses:

- FastAPI REST APIs for persistence and thread loading
- FastAPI WebSockets for instant message delivery
- MySQL for message storage
- React + Axios + native WebSocket on the frontend
- job-application-based authorization for security and simplicity

This gives you a practical real-time chat feature without needing an external chat platform.

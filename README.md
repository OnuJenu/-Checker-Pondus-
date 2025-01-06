# Mobile Voting Platform Backend

This is a Python-based backend REST API for a mobile voting platform, where users can submit questions in various formats (video, graphics, audio, or text) and vote between two options.

## Features

- OAuth-based login for user authentication.
- Create polls with two voting options, supporting text, video, audio, or image formats.
- Vote and view results in real-time.
- Dynamic question board similar to TikTok, allowing users to explore polls through an engaging feed.
- Media file handling and optimization, including validation and storage.
- Designed for future personalization of user experiences via segmentation and bubbles.

## Project Structure

```
pondus_one/
│
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── poll.py
│   │   ├── vote.py
│   │   └── media.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── poll.py
│   │   └── media.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── poll_service.py
│   │   └── media_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── validation.py
│   └── databases/
│       ├── __init__.py
│       └── database.py
└── tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_poll.py
    └── test_media.py
```

## Installation

1. Clone the repository.
2. Install the dependencies using `pip install -r requirements.txt`.
3. Run the application using `python app/main.py`.

## Future Enhancements

- User segmentation and AI-driven recommendations.
- Enhanced security features and scalability improvements.

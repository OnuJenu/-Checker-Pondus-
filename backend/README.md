# Mobile Voting Platform Backend

This is a Python-based backend REST API for a mobile voting platform, where users can submit questions in various formats (video, graphics, audio, or text) and vote between two options.

## Features

- OAuth-based login for user authentication
- Create polls with two voting options, supporting text, video, audio, or image formats
- Vote and view results in real-time
- Dynamic question board similar to TikTok, allowing users to explore polls through an engaging feed
- Media file handling and optimization, including validation and storage
- Designed for future personalization of user experiences via segmentation and bubbles

## Project Structure

```
pondus_one/
│
├── README.md
├── requirements.txt
├── api-docs.yaml
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── poll.py
│   │   ├── vote.py
│   │   ├── media.py
│   │   └── voting_option.py
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

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pondus_one.git
   cd pondus_one
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```
5. Create database:
   ```bash
   alembic upgrade head
   ```

5. Run the application:
   ```bash
   python3 -m app.main
   ```

## Tests

For run test use command:
```bash
   python3 -m pytest tests/test_poll.py -v 
```

## API Documentation

The API documentation is available in OpenAPI format in `api-docs.yaml`. You can view it using Swagger UI or Redoc.

## Contribution Guidelines

1. Fork the repository and create your feature branch
2. Ensure your code follows PEP 8 style guidelines
3. Write tests for new features
4. Submit a pull request with a detailed description of your changes

## Future Enhancements

- User segmentation and AI-driven recommendations
- Enhanced security features and scalability improvements
- Real-time notifications and push updates
- Advanced media processing and optimization
- Integration with social media platforms

## License

[MIT License](LICENSE)

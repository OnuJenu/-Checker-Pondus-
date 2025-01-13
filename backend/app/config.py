# Configuration settings for different environments

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    CORS_HEADERS = 'Content-Type'
    UPLOAD_FOLDER = '/media/mswiderski/Data/workspace/OnuJenu/pondus/pondus_one/backend/uploads'
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp', 
        'mp4', 'mov', 'avi', 'webm', 'wav', 'mp3', 'ogg', 'aac'
    }
    GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"  # Replace with your Google Client ID
    GOOGLE_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"  # Replace with your Google Client Secret
    GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google_callback"
    TWITTER_CLIENT_ID = "YOUR_TWITTER_CLIENT_ID"  # Replace with your Twitter Client ID
    TWITTER_CLIENT_SECRET = "YOUR_TWITTER_CLIENT_SECRET"  # Replace with your Twitter Client Secret
    TWITTER_REDIRECT_URI = "http://localhost:8000/auth/twitter_callback"
    FACEBOOK_CLIENT_ID = "YOUR_FACEBOOK_CLIENT_ID"  # Replace with your Facebook Client ID
    FACEBOOK_CLIENT_SECRET = "YOUR_FACEBOOK_CLIENT_SECRET"  # Replace with your Facebook Client Secret
    FACEBOOK_REDIRECT_URI = "http://localhost:8000/auth/facebook_callback"

# Create settings instance
settings = Config()

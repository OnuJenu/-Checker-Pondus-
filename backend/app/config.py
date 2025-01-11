# Configuration settings for different environments

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    CORS_HEADERS = 'Content-Type'
    UPLOAD_FOLDER = '/media/mswiderski/Data/workspace/OnuJenu/pondus/pondus_one/backend/uploads'
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp', 
        'mp4', 'mov', 'avi', 'webm', 'wav', 'mp3', 'ogg', 'aac'
    }

# Create settings instance
settings = Config()

import os

class Config:
    """Base configuration class. Contains default settings."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # other default configurations can be added here

class DevelopmentConfig(Config):
    """Configuration settings for development environment."""
    DEBUG = True
    # Override any other settings specific to development here

class TestingConfig(Config):
    """Configuration settings for testing environment."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite database for testing
    # Override any other settings specific to testing here

class ProductionConfig(Config):
    """Configuration settings for production environment."""
    # Override any settings specific to production here

# Dictionary to map environment names to configuration classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


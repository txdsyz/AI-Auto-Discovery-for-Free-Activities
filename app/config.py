"""
Configuration loader - loads environment variables
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings loaded from environment variables"""
    
    # API Keys
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # API Configuration
    TAVILY_BASE_URL: str = "https://api.tavily.com"
    
    # Pipeline Configuration
    DEFAULT_MAX_ORGANIZATIONS: int = 3
    DEFAULT_SEARCH_DEPTH: str = "advanced"
    DEFAULT_EXTRACT_DEPTH: str = "basic"
    MAX_CONTENT_LENGTH: int = 10000  # characters
    
    # Category to Query Mapping (Swedish search terms)
    CATEGORY_QUERIES = {
        "sports": "idrottsföreningar Stockholm ungdom",
        "youth_centers": "fritidsgård Stockholm verksamhet",
        "scouts": "scoutkårer Stockholm",
        "cultural": "kulturföreningar Stockholm barn",
        "educational": "studieförbund Stockholm ungdom"
    }
    
    def validate(self):
        """Validate that required settings are present"""
        missing = []
        
        if not self.TAVILY_API_KEY:
            missing.append("TAVILY_API_KEY")
        if not self.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if not self.FIREBASE_CREDENTIALS_PATH:
            missing.append("FIREBASE_CREDENTIALS_PATH")
            
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        # Check if Firebase credentials file exists
        creds_path = Path(self.FIREBASE_CREDENTIALS_PATH)
        if not creds_path.is_absolute():
            creds_path = Path(__file__).parent.parent / self.FIREBASE_CREDENTIALS_PATH
        
        if not creds_path.exists():
            raise FileNotFoundError(
                f"Firebase credentials file not found at: {creds_path}\n"
                "Please download it from Firebase Console and place it in the backend directory."
            )


# Create global settings instance
settings = Settings()

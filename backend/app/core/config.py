import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables with root .env priority.
core_dir = Path(__file__).resolve().parent
backend_dir = core_dir.parent.parent
project_root = backend_dir.parent
root_env_file = project_root / ".env"
backend_env_file = backend_dir / ".env"

if root_env_file.exists():
    load_dotenv(dotenv_path=root_env_file)
elif backend_env_file.exists():
    load_dotenv(dotenv_path=backend_env_file)


class Settings:
    # App settings
    APP_NAME: str = os.getenv("APP_NAME", "Clinic AI Receptionist")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # API settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-prod")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./clinic.db"
    )
    
    # Groq LLM settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # Email settings
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")
    EMAIL_FROM_NAME: str = os.getenv("EMAIL_FROM_NAME", "Clinic Reception")
    
    # SMS (Twilio) settings
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_NUMBER: str = os.getenv("TWILIO_WHATSAPP_NUMBER", "")
    
    # Google Calendar settings
    GOOGLE_CALENDAR_CREDENTIALS_FILE: str = os.getenv(
        "GOOGLE_CALENDAR_CREDENTIALS_FILE", 
        ""
    )
    GOOGLE_CALENDAR_ID: str = os.getenv("GOOGLE_CALENDAR_ID", "")
    
    # Clinic information
    CLINIC_NAME: str = os.getenv("CLINIC_NAME", "Aesthetic Clinic")
    CLINIC_EMAIL: str = os.getenv("CLINIC_EMAIL", "")
    CLINIC_PHONE: str = os.getenv("CLINIC_PHONE", "")
    CLINIC_ADDRESS: str = os.getenv("CLINIC_ADDRESS", "")
    CLINIC_WORKING_HOURS: str = os.getenv(
        "CLINIC_WORKING_HOURS", 
        "Monday-Friday: 9AM-6PM, Saturday: 10AM-4PM"
    )
    
    # Default appointment settings
    DEFAULT_APPOINTMENT_DURATION_MINUTES: int = int(
        os.getenv("DEFAULT_APPOINTMENT_DURATION_MINUTES", "60")
    )
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Karachi")


settings = Settings()

"""ImageKit service for file uploads."""
from imagekitio import ImageKit
from app.core.config import settings

# Initialize the ImageKit client
imagekit = ImageKit(
    public_key=settings.IMAGEKIT_PUBLIC_KEY,
    private_key=settings.IMAGEKIT_PRIVATE_KEY,
    url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
)


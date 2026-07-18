import re
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import json

def validate_email(email: str) -> bool:
    """
    Validate email format using regex.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> Dict[str, Any]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        dict: Validation result with 'valid' and 'message' keys
    """
    if len(password) < 8:
        return {
            'valid': False,
            'message': 'Password must be at least 8 characters long'
        }
    
    if not re.search(r'[A-Z]', password):
        return {
            'valid': False,
            'message': 'Password must contain at least one uppercase letter'
        }
    
    if not re.search(r'[a-z]', password):
        return {
            'valid': False,
            'message': 'Password must contain at least one lowercase letter'
        }
    
    if not re.search(r'\d', password):
        return {
            'valid': False,
            'message': 'Password must contain at least one number'
        }
    
    return {'valid': True, 'message': 'Password is strong'}

def generate_token(length: int = 32) -> str:
    """
    Generate a secure random token.
    
    Args:
        length: Length of token in bytes
        
    Returns:
        str: Hexadecimal token string
    """
    return secrets.token_hex(length)

def hash_string(text: str) -> str:
    """
    Create SHA-256 hash of a string.
    
    Args:
        text: Text to hash
        
    Returns:
        str: Hexadecimal hash string
    """
    return hashlib.sha256(text.encode()).hexdigest()

def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing potentially harmful characters.
    
    Args:
        text: Input text to sanitize
        
    Returns:
        str: Sanitized text
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove special characters that could be used for injection
    text = re.sub(r'[<>"\']', '', text)
    
    return text.strip()

def format_datetime(dt: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format datetime object to string.
    
    Args:
        dt: Datetime object
        format_str: Format string
        
    Returns:
        str: Formatted datetime string
    """
    return dt.strftime(format_str)

def parse_datetime(date_str: str, format_str: str = '%Y-%m-%d %H:%M:%S') -> Optional[datetime]:
    """
    Parse datetime string to datetime object.
    
    Args:
        date_str: Datetime string
        format_str: Format string
        
    Returns:
        datetime or None: Parsed datetime object or None if invalid
    """
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None

def calculate_time_ago(dt: datetime) -> str:
    """
    Calculate human-readable time difference from now.
    
    Args:
        dt: Datetime to compare
        
    Returns:
        str: Human-readable time difference (e.g., "2 hours ago")
    """
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    else:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months > 1 else ''} ago"

def paginate_results(items: List[Any], page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """
    Paginate a list of items.
    
    Args:
        items: List of items to paginate
        page: Page number (1-indexed)
        per_page: Items per page
        
    Returns:
        dict: Paginated results with metadata
    """
    total_items = len(items)
    total_pages = (total_items + per_page - 1) // per_page
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    return {
        'items': items[start_idx:end_idx],
        'page': page,
        'per_page': per_page,
        'total_items': total_items,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text (simple implementation).
    
    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords to return
        
    Returns:
        list: List of keywords
    """
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    
    # Convert to lowercase and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter out stop words and short words
    keywords = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Count frequency
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_keywords[:max_keywords]]

def format_currency(amount: float, currency: str = 'INR', locale: str = 'en_IN') -> str:
    """
    Format amount as currency string.
    
    Args:
        amount: Amount to format
        currency: Currency code (INR, USD, etc.)
        locale: Locale for formatting
        
    Returns:
        str: Formatted currency string
    """
    if currency == 'INR':
        # Indian numbering system
        s = f"{amount:,.2f}"
        # Convert to Indian format (lakhs, crores)
        if amount >= 100000:
            parts = s.split('.')
            int_part = parts[0].replace(',', '')
            
            # Format with Indian numbering
            last_three = int_part[-3:]
            other = int_part[:-3]
            
            if other:
                formatted = ','.join([other[i:i+2] for i in range(0, len(other), 2)])
                return f"₹{formatted},{last_three}.{parts[1]}"
            else:
                return f"₹{last_three}.{parts[1]}"
        return f"₹{s}"
    else:
        return f"{currency} {amount:,.2f}"

def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)].strip() + suffix

def is_valid_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return pattern.match(url) is not None

def merge_dicts(*dicts: Dict) -> Dict:
    """
    Merge multiple dictionaries.
    
    Args:
        *dicts: Variable number of dictionaries
        
    Returns:
        dict: Merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """
    Safely load JSON string with error handling.
    
    Args:
        json_str: JSON string to parse
        default: Default value if parsing fails
        
    Returns:
        Parsed JSON or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

def generate_session_id() -> str:
    """
    Generate a unique session ID.
    
    Returns:
        str: Unique session ID
    """
    return f"session_{generate_token(16)}_{int(datetime.utcnow().timestamp())}"

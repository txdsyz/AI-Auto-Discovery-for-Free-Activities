"""
Data validation utilities
"""
import re
from typing import Dict, Any, List


def is_valid_email(email: str) -> bool:
    """
    Validate email format using regex.
    
    Args:
        email: Email address string
        
    Returns:
        True if valid email format, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_swedish_domain(url: str) -> bool:
    """
    Check if URL is a Swedish (.se) domain.
    
    Args:
        url: Website URL
        
    Returns:
        True if .se domain, False otherwise
    """
    return '.se' in url.lower()


def validate_age_range(age_range: str) -> bool:
    """
    Validate that age range is appropriate for youth (7-19).
    
    Args:
        age_range: Age range string (e.g., "8-14", "7-18")
        
    Returns:
        True if valid youth age range
    """
    if not age_range:
        return False
    
    # Extract numbers from age range
    numbers = re.findall(r'\d+', age_range)
    
    if len(numbers) < 2:
        return False
    
    min_age = int(numbers[0])
    max_age = int(numbers[1])
    
    # Check if range is within youth range (7-19)
    return 7 <= min_age <= 19 and 7 <= max_age <= 19 and min_age < max_age


def validate_organization_profile(profile: Dict[str, Any]) -> List[str]:
    """
    Validate organization profile data and return list of issues.
    
    Args:
        profile: Organization profile dictionary
        
    Returns:
        List of validation error messages (empty if valid)
    """
    issues = []
    
    # Check required fields
    if not profile.get('name'):
        issues.append("Missing organization name")
    
    if not profile.get('website'):
        issues.append("Missing website URL")
    
    # Check contact info
    contact = profile.get('contact', {})
    email = contact.get('email')
    phone = contact.get('phone')
    
    if not email and not phone:
        issues.append("Missing contact information (need email or phone)")
    
    if email and not is_valid_email(email):
        issues.append(f"Invalid email format: {email}")
    
    if email == "NOT_FOUND":
        issues.append("No email address found on website (CRITICAL)")
    
    # Check events
    events = profile.get('events', [])
    if len(events) == 0:
        issues.append("No events found (need at least 1)")
    
    # Validate each event
    for i, event in enumerate(events, 1):
        if not event.get('name'):
            issues.append(f"Event {i}: Missing name")
        
        age_range = event.get('age_range')
        if not age_range:
            issues.append(f"Event {i}: Missing age_range")
        elif not validate_age_range(age_range):
            issues.append(f"Event {i}: Invalid age range '{age_range}' (must be 7-19)")
    
    # Check location
    location = profile.get('location', '')
    if not location or location == 'Stockholm':
        issues.append("Location too generic (need specific neighborhood/district)")
    
    return issues


def validate_discovery_request(categories: List[str], max_orgs: int) -> List[str]:
    """
    Validate discovery request parameters.
    
    Args:
        categories: List of category names
        max_orgs: Maximum number of organizations
        
    Returns:
        List of validation error messages (empty if valid)
    """
    issues = []
    
    if not categories or len(categories) == 0:
        issues.append("At least one category is required")
    
    valid_categories = ['sports', 'youth_centers', 'scouts', 'cultural', 'educational']
    for cat in categories:
        if cat not in valid_categories:
            issues.append(f"Invalid category '{cat}'. Valid: {', '.join(valid_categories)}")
    
    if max_orgs < 1:
        issues.append("max_organizations must be at least 1")
    
    if max_orgs > 10:
        issues.append("max_organizations cannot exceed 10")
    
    return issues

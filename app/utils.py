def sanitize_text(text):
    """Sanitize text by stripping extra spaces and line breaks."""
    return ' '.join(text.split())

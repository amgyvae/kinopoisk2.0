from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(value):
    if not value:
        return ""
    
    # Регулярное выражение для поиска ID видео (11 символов) в любом типе ссылок
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(regex, value)
    
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    
    return value

@register.filter
def star_range(value):
    try:
        # Округляем рейтинг (например, 8.7 станет 9, а потом делим на 2, если у тебя 10-бальная шкала)
        # Или просто возвращаем диапазон до 10
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)
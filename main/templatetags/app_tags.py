from django import template

register = template.Library()

@register.filter
def rating_color(value):
    try:
        score = float(value)
        if score < 3:
            return "text-red-400"
        elif score < 7:
            return "text-yellow-500"
        elif score < 9:
            return "text-lime-500"
        else:
            return "text-lime-400"
    except (ValueError, TypeError):
        return "text-gray-400"
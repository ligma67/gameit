from django import template

register = template.Library()

@register.filter
def rating_color(value):
    try:
        score = float(value)
        if score == -1:
            return "text-stale-500"
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

@register.filter
def get_rating(value):
    return value if value > 0 else "??"

@register.filter
def get_text(value):
    if value <= 0:
        return "Оценок нет"
    value = value % 100
    n1 = value % 10
    res_str = f"{value} "
    if 10 < value < 20:
        res_str += "оценок"
    elif 1 > n1 or n1 > 4:
        res_str += "оценок"
    elif n1 == 1:
        res_str += "оценка"
    else:
        res_str += "оценки"
    return res_str
from django import template

register = template.Library()


@register.filter
def format_price(value):
    try:
        # Format w/ separators
        return (
            f"{float(value):,.2f}".replace(".", "X").replace(",", ",").replace("X", ".")
        )
    except (ValueError, TypeError):
        return value  # Return original value if conversion fails

def calculate_total_price(components, price_type='new'):
    """Calculate total price for the build"""
    total = 0
    for component in components.values():
        if isinstance(component, dict):
            total += component[f'price_{price_type}']
    return total

def get_price_rating(new_price, used_price):
    """Determine if the price is super, good, or bad"""
    price_diff = new_price - used_price
    if price_diff >= new_price * 0.4:
        return "Superpris! 🌟"
    elif price_diff >= new_price * 0.2:
        return "Bra pris 👍"
    else:
        return "Högt pris 😕"

def format_price(price):
    """Format price with SEK currency symbol"""
    return f"{int(price):,} kr".replace(",", " ")  # Swedish format uses space as thousand separator

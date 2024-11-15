from typing import Dict, List
import random

# Mock data for Tradera listings with SEK prices
dummy_data = {
    "gpu": [
        {
            "title": "NVIDIA GeForce RTX 4060 - Auktion",
            "current_bid": 3200,
            "time_remaining": "3 dagar",
            "num_bids": 7,
            "condition": "Begagnad",
            "listing_type": "auction",
            "link": "https://www.tradera.com/dummy-auction-gpu-1"
        },
        {
            "title": "NVIDIA GeForce RTX 4060 - Köp Nu",
            "fixed_price": 3800,
            "condition": "Ny",
            "listing_type": "buy_now",
            "link": "https://www.tradera.com/dummy-buy-now-gpu-1"
        }
    ],
    "motherboard": [
        {
            "title": "ASUS ROG Strix B450-F - Auktion",
            "current_bid": 1500,
            "time_remaining": "1 dag",
            "num_bids": 3,
            "condition": "Begagnad",
            "listing_type": "auction",
            "link": "https://www.tradera.com/dummy-auction-motherboard-1"
        },
        {
            "title": "ASUS ROG Strix B450-F - Köp Nu",
            "fixed_price": 1900,
            "condition": "Ny",
            "listing_type": "buy_now",
            "link": "https://www.tradera.com/dummy-buy-now-motherboard-1"
        }
    ],
    "cpu": [
        {
            "title": "Intel Core i7-9700K - Auktion",
            "current_bid": 2200,
            "time_remaining": "2 dagar",
            "num_bids": 5,
            "condition": "Begagnad",
            "listing_type": "auction",
            "link": "https://www.tradera.com/dummy-auction-cpu-1"
        },
        {
            "title": "Intel Core i7-9700K - Köp Nu",
            "fixed_price": 2800,
            "condition": "Ny",
            "listing_type": "buy_now",
            "link": "https://www.tradera.com/dummy-buy-now-cpu-1"
        }
    ],
    "ram": [
        {
            "title": "Corsair Vengeance LPX 16GB - Auktion",
            "current_bid": 800,
            "time_remaining": "4 timmar",
            "num_bids": 8,
            "condition": "Begagnad",
            "listing_type": "auction",
            "link": "https://www.tradera.com/dummy-auction-ram-1"
        },
        {
            "title": "Corsair Vengeance LPX 16GB - Köp Nu",
            "fixed_price": 1200,
            "condition": "Ny",
            "listing_type": "buy_now",
            "link": "https://www.tradera.com/dummy-buy-now-ram-1"
        }
    ],
    "psu": [
        {
            "title": "EVGA SuperNOVA 650 G3 - Auktion",
            "current_bid": 900,
            "time_remaining": "6 timmar",
            "num_bids": 4,
            "condition": "Begagnad",
            "listing_type": "auction",
            "link": "https://www.tradera.com/dummy-auction-psu-1"
        },
        {
            "title": "EVGA SuperNOVA 650 G3 - Köp Nu",
            "fixed_price": 1300,
            "condition": "Ny",
            "listing_type": "buy_now",
            "link": "https://www.tradera.com/dummy-buy-now-psu-1"
        }
    ],
    "case": [
        {
            "title": "NZXT H510 - Auktion",
            "current_bid": 600,
            "time_remaining": "1 dag",
            "num_bids": 2,
            "condition": "Begagnad",
            "listing_type": "auction",
            "link": "https://www.tradera.com/dummy-auction-case-1"
        },
        {
            "title": "NZXT H510 - Köp Nu",
            "fixed_price": 900,
            "condition": "Ny",
            "listing_type": "buy_now",
            "link": "https://www.tradera.com/dummy-buy-now-case-1"
        }
    ],
    "cooler": [
        {
            "title": "Cooler Master Hyper 212 - Auktion",
            "current_bid": 400,
            "time_remaining": "8 timmar",
            "num_bids": 3,
            "condition": "Begagnad",
            "listing_type": "auction",
            "link": "https://www.tradera.com/dummy-auction-cooler-1"
        },
        {
            "title": "Cooler Master Hyper 212 - Köp Nu",
            "fixed_price": 700,
            "condition": "Ny",
            "listing_type": "buy_now",
            "link": "https://www.tradera.com/dummy-buy-now-cooler-1"
        }
    ]
}

def _get_component_type(component: Dict) -> str:
    """Determine component type based on its properties"""
    if 'power' in component and 'length' in component:
        return 'gpu'
    elif 'socket' in component and 'power' in component:
        return 'cpu'
    elif 'socket' in component and 'form_factor' in component:
        return 'motherboard'
    elif 'watts' in component:
        return 'psu'
    elif 'max_gpu_length' in component:
        return 'case'
    elif 'type' in component and component['type'] in ['Air', 'AIO']:
        return 'cooler'
    elif 'type' in component and component['type'] == 'DDR5':
        return 'ram'
    return ''

def get_tradera_suggestions(component: Dict) -> List[Dict]:
    """
    Get Tradera suggestions for a specific component
    Returns list of suggestions with prices and links
    """
    component_name = component['name']
    component_type = _get_component_type(component)
    
    if not component_type:
        return []
        
    suggestions = dummy_data.get(component_type, [])
    
    # Add price comparison data
    for suggestion in suggestions:
        price = suggestion.get('fixed_price', suggestion.get('current_bid', 0))
        suggestion['price'] = price
        suggestion['price_difference'] = component['price_new'] - price
        suggestion['savings_percentage'] = (
            (suggestion['price_difference'] / component['price_new']) * 100
            if suggestion['price_difference'] > 0 else 0
        )
    
    return suggestions

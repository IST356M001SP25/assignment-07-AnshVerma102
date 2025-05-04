if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from menuitem import MenuItem
else:
    from code.menuitem import MenuItem


def clean_price(price: str) -> float:
    # Remove dollar sign and commas, then convert to float
    return float(price.replace("$", "").replace(",", ""))


def clean_scraped_text(scraped_text: str) -> list[str]:
    return [
        item for item in scraped_text.split("\n")
        if item.strip() and item not in {'GS', 'V', 'S', 'P'} and not item.startswith("NEW")
    ]


def extract_menu_item(title: str, scraped_text: str) -> MenuItem:
    cleaned_items = clean_scraped_text(scraped_text)
    name = cleaned_items[0] if cleaned_items else "Unnamed item"
    price = clean_price(cleaned_items[1]) if len(cleaned_items) > 1 else 0.0
    description = cleaned_items[2] if len(cleaned_items) > 2 else "No description available."
    return MenuItem(category=title, name=name, price=price, description=description)


if __name__ == '__main__':
    test_items = [
        '''
NEW!

Tully Tots

$11.79

Made from scratch with shredded potatoes, cheddar-jack cheese and Romano cheese all rolled up and deep-fried. Served with a spicy cheese sauce.
        ''',

        '''Super Nachos

$15.49
GS

Tortilla chips topped with a mix of spicy beef and refried beans, nacho cheese sauce, olives, pico de gallo, jalapeños, scallions and shredded lettuce. Sour cream and salsa on the side. Add guacamole $2.39

        ''',

        '''Veggie Quesadilla

$11.99
V

A flour tortilla packed with cheese, tomatoes, jalapeños, black olives and scallions. Served with sour cream and pico de gallo.
Add chicken $2.99 | Add guacamole $2.39
''',

        '''Kid's Burger & Fries

$6.99
'''
    ]

    title = "TEST"
    for scraped_text in test_items:
        item = extract_menu_item(title, scraped_text)
        print(item)

import re
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)  # Change to False if debugging
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://web.archive.org/web/20241111165815/https://www.tullysgoodtimes.com/menus/")

    extracted_items = []

    # Get all menu section headers
    section_titles = page.query_selector_all("h3.foodmenu__menu-section-title")

    for title in section_titles:
        title_text = title.inner_text().strip()
        print("MENU SECTION:", title_text)

        # Navigate to the corresponding sibling container
        section_container = title.evaluate_handle("el => el.nextElementSibling?.nextElementSibling")

        if section_container:
            menu_items = section_container.query_selector_all("div.foodmenu__menu-item")
            for item in menu_items:
                item_text = item.inner_text().strip()
                extracted_item = extract_menu_item(title_text, item_text)
                print(f"  MENU ITEM: {extracted_item.name}")
                extracted_items.append(extracted_item.to_dict())
        else:
            print(f"  WARNING: No menu items found for section: {title_text}")

    df = pd.DataFrame(extracted_items)
    import os
    os.makedirs("cache", exist_ok=True)  # Ensure the 'cache' directory exists
    df.to_csv("cache/tullys_menu.csv", index=False)
    os.makedirs("cache", exist_ok=True)  # Ensure the 'cache' directory exists
    df.to_csv("cache/tullys_menu.csv", index=False)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        tullyscraper(playwright)

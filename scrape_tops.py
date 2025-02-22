import re
import json
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScrapeTops:
    BASE_URL = "https://www.tops.co.th/en"
    CATEGORIES = [
        "OTOP", "Only At Tops", "Fruits & Vegetables", "Meat & Seafood", "Fresh Food & Bakery",
        "Pantry & Ingredients", "Snacks & Desserts", "Beverages", "Health & Beauty Care",
        "Mom & Kids", "Household & Merit", "PetNme"
    ]
    HEADERS = {"User-Agent": "Mozilla/5.0"}

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_soup(self, url, wait_selector=None, retries=3):
        for attempt in range(retries):
            try:
                self.driver.get(url)

                # Wait for full page load
                WebDriverWait(self.driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )

                # Wait for the selector (if provided) and ensure it's visible
                if wait_selector:
                    element = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector))
                    )
                    
                    # Ensure the element is actually visible
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of(element)
                    )

                    time.sleep(2)

                # Additional delay to allow dynamic content to load
                time.sleep(2)

                return BeautifulSoup(self.driver.page_source, "html.parser")

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"Failed to load {url} after {retries} attempts.")
                    return None

    def get_category_links(self):
        soup = self.get_soup(self.BASE_URL)
        if not soup:
            return {}
        
        sidebar = soup.find("div", class_="pc-sidenavbar")
        if not sidebar:
            return {}
        
        items = sidebar.find_all("div", class_="item sidebar-item")
        category_links = {}
        for item, category in zip(items, self.CATEGORIES):
            link_tag = item.find("a")
            if link_tag:
                link = link_tag.get("href", "")
                if "https://" not in link:
                    link = self.BASE_URL + link.replace("/en", "")
                category_links[category] = link
        return category_links

    def get_description(self, product_url):
        soup = self.get_soup(product_url)
        if not soup:
            return None
        try:
            div = soup.find("div", class_="accordion product-details-accordion")
            body = div.find("div", class_="accordion-body")
            description = body.find("span", class_= "text").text.strip().replace("\n", " ")
            return description
        except (AttributeError, ValueError) as e:
            print(f"No description found. Error: {e}")
        return None

    def extract_product_info(self, text):
        text = re.sub(r'[\(\[].*?[\)\]]', '', text).strip()  # Remove items like '.' (C, (B
        weight_pattern = r'(?i)\b(\d+\s*(?:g|kg|pcs|bags))\b'
        weight_range_pattern = r'(?i)\b(\d+to\d+\s*(?:g|kg))\b'
        volume_pattern = r'(?i)\b(\d+(?:\.\d+)?\s*(?:ml|L|litr|ltr|Litre|cc|sheets))\b'
        
        weight_match = re.search(weight_range_pattern, text) or re.search(weight_pattern, text)
        if weight_match:
            size = weight_match.group(1)
            remaining_text = re.sub(weight_match.re, '', text).strip()
        elif volume_match := re.search(volume_pattern, text):
            size = volume_match.group(1)
            remaining_text = re.sub(volume_pattern, '', text).strip()
        else:
            size = "N/A"
            remaining_text = text
        
        pack_match = re.search(r'\bPack\s*(\d+)\b', remaining_text, re.IGNORECASE)
        if pack_match:
            if size == "N/A":
                size = f"Pack {pack_match.group(1)}"
            else:
                size = (size + f" Pack {pack_match.group(1)}")
            remaining_text = re.sub(r'\bPack\s*\d+\b', '', remaining_text, flags=re.IGNORECASE).strip()
        
        if remaining_text.lower().endswith(" pack"):
            size = "Pack"
            remaining_text = remaining_text.rsplit(" ", 1)[0]
        
        product_name = re.sub(r'[\(\[].*?[\)\]]', '', remaining_text).replace(".", "").strip()
        return product_name, size

    def parse_product(self, category_url):
        print("CATEGORY URL:", category_url)
        soup = self.get_soup(category_url, wait_selector=".productlisting")
        
        product_list = []
        unique_barcodes = set()
        try:
            product_listing = soup.select_one(".productlisting")
            sliders = product_listing.find_all("div", class_="plp-carousel")

            for slider in sliders:
                articles = slider.find_all("article", class_="slider-items")
                
                for article in articles:
                    barcode = article.get("data-product-id", "").strip()
                    if barcode in unique_barcodes:
                        continue  # Skip duplicate barcode
                    unique_barcodes.add(barcode)
                    data = article.find("div", class_="product-item")

                    image_link = data.find("div", class_="product-item-image").find("img").get("src")

                    price_wrapper = data.find("div", class_="product-item-price-wrapper")
                    price = price_wrapper.find("span", class_="price-number").text.strip()

                    label_img = price_wrapper.find("div", class_="product-item--seasonal-badge")
                    label = label_img.find("img", class_="product-item-badge").get("alt") if label_img else None
                    if label == "":
                        label = None

                    product_name_text = data.find("div", class_="product-item-title").find("h3", class_="product-tile__name").text.strip()
                    print(product_name_text)
                    product_name, quantity = self.extract_product_info(product_name_text)
                    
                    product_url = data.find("a").get("href")
                    if product_url and "https://" not in product_url:
                        product_url = self.BASE_URL + product_url

                    description = self.get_description(product_url)

                    product_data = {
                        "product_name": product_name,
                        "product_images": image_link,
                        "quantity": quantity,
                        "barcode_number": barcode,
                        "product_details": description,
                        "price": price,
                        "label": label
                    }
                    print(product_data)
                    product_list.append(product_data)
        
        except AttributeError as e:
            print(f"Error parsing category: {category_url}. Error: {e}")
        
        return product_list

    def scrape_tops(self):
        category_links = self.get_category_links()
        all_products = {}
        for category, url in category_links.items():
            print(f"Scraping category: {category}")
            product_data = self.parse_product(url)
            all_products[category] = product_data
        
        with open("tops_products.json", "w", encoding="utf-8") as f:
            json.dump(all_products, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    scraper = ScrapeTops()
    scraper.scrape_tops()
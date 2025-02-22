# **Tops Online Product Scraper**  

## **Overview**  
This script scrapes product details from [Tops Online](https://www.tops.co.th/en) across multiple categories. It extracts:  
- **Product Name**  
- **Images**  
- **Quantity (Weight/Size/Packs)**  
- **Barcode**  
- **Description**  
- **Price**  
- **Labels (e.g., promotions, discounts, exclusive tags, etc.)**  

The scraped data is stored in **JSON format**.

---

## **Approach Used for Scraping**  
1. **Identifying Categories**:  
   - Extracted category links from the sidebar of the homepage.  
2. **Loading Category Pages**:  
   - Used Selenium to dynamically load JavaScript-rendered content.  
3. **Extracting Product Data**:  
   - Captured product information from the HTML structure.  
   - Cleaned product names, sizes, and extracted weight/volume details.  
4. **Handling Pagination**:  
   - Implemented a function to navigate multiple pages in a category.  
5. **Handling Bot Protection**:  
   - Used **headless Chrome** and **random delays** to avoid detection.  

---

## **Dependencies**  
To run this scraper, the following dependencies are needed:
- Python 3.10+
- Requests
- Beautifulsoup4
- Selenium


## **How to run**
In the projects' working directory execute the below command to create a virtual environment.

 
```python
$ py -m venv venv
```

To activate the virtual environment, execute the below command.

```python
$ source venv/Script/activate
```
Clone this repository in the projects' working directory by executing the command below.

```python
$ git clone https://github.com/ajaoooluseyi/tops-scraper.git
$ cd tops-scraper
```
Install the dependencies 
```sh
pip install -r requirements.txt
```
Run scraper
```sh
python scrape_tops.py
```

## **Sample output**
{
    "OTOP": [
        {
            "product_name": "Doikham Natural Honey",
            "product_images": "https://assets.tops.co.th/DOIKHAM-DoikhamNaturalHoney770g-8850773620033-1?$JPEG$",
            "quantity": "770g",
            "barcode_number": "8850773620033",
            "product_details": "The product received may be subject to package modification and quantity from the manufacturer. We reserve the right to make any changes without prior notice.  *The images used are for advertising purposes only.",
            "price": "199.00",
            "label": "OTOP Product"
        },
        {
            "product_name": "Doi Kham High Strawberry Spread Jam",
            "product_images": "https://assets.tops.co.th/DOIKHAM-DoiKhamHighStrawberrySpreadJam220g-8850773108197-1?$JPEG$",
            "quantity": "220g",
            "barcode_number": "8850773108197",
            "product_details": "The product received may be subject to package modification and quantity from the manufacturer. We reserve the right to make any changes without prior notice.  *The images used are for advertising purposes only.",
            "price": "85.00",
            "label": "OTOP Product"
        },
        {
            "product_name": "Doi Kham Mango with Passion Fruit Spread Jam",
            "product_images": "https://assets.tops.co.th/DOIKHAM-DoiKhamMangowithPassionFruitSpreadJam220g-8850773570123-1?$JPEG$",
            "quantity": "220g",
            "barcode_number": "8850773570123",
            "product_details": "The product received may be subject to package modification and quantity from the manufacturer. We reserve the right to make any changes without prior notice.  *The images used are for advertising purposes only.",
            "price": "85.00",
            "label": "OTOP Product"
        },
        {
            "product_name": "Doikham Natural Honey",
            "product_images": "https://assets.tops.co.th/DOIKHAM-DoikhamNaturalHoney230g-8850773620064-1?$JPEG$",
            "quantity": "230g",
            "barcode_number": "8850773620064",
            "product_details": "The product received may be subject to package modification and quantity from the manufacturer. We reserve the right to make any changes without prior notice.  *The images used are for advertising purposes only.",
            "price": "80.00",
            "label": "OTOP Product"
        },
        {
            "product_name": "Doi Kham Mulberry Spread Jam",
            "product_images": "https://assets.tops.co.th/DOIKHAM-DoiKhamMulberrySpreadJam220g-8850773108210-1?$JPEG$",
            "quantity": "220g",
            "barcode_number": "8850773108210",
            "product_details": "The product received may be subject to package modification and quantity from the manufacturer. We reserve the right to make any changes without prior notice.  *The images used are for advertising purposes only.",
            "price": "85.00",
            "label": "OTOP Product"
        },
   ]
}

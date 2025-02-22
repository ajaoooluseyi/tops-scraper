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
To run this scraper, install the following dependencies:

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

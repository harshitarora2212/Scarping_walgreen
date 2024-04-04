import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Initialize the webdriver
browser = webdriver.Firefox()

# Read URLs from Excel
urls_scrap = pd.read_excel('Walgreens_Master_2024-04-02.xlsx')
url_list = urls_scrap['URL'].tolist()

# Flag to check if header is written
write_header = True

# Loop through the URLs
for url in url_list:
    browser.get(url)

    # Lists to store data for each loop iteration
    pro_title = []
    pro_code = []
    pro_price = []
    master_url = [url]  # URL for the current iteration

    try:
        pro_title_temp =(WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="productTitle"]'))
        ).text)
        pro_title.append(pro_title_temp)
    except TimeoutException:
        pro_title.append('Unavailable')

    try:
        regular_price_element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="regular-price"]/span[1]'))
        )
        pro_price.append(regular_price_element.text)
    except TimeoutException:
        try:
            sales_price_element = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="sales-price-info"]'))
            )
            pro_price.append(sales_price_element.text)
        except TimeoutException:
            pro_price.append('Unavailable')

    try:
        code_temp_element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='prodSpecCont']/table/tbody/tr[contains(.,'Item Code')]"))
        )
        code_temp = code_temp_element.text
        if code_temp:
            temp = code_temp.split(':')[1].strip()
            pro_code.append(temp)
        else:
            pro_code.append('Unavailable')
    except TimeoutException:
        pro_code.append('Unavailable')


    # Create DataFrame for the current iteration
    df = pd.DataFrame({
        'Item Code': pro_code,
        'Product Name': pro_title,
        'Price': pro_price,
        'URL': master_url
    })

    # Write DataFrame to CSV
    with open('walgreen_pro.csv', 'a', newline='') as f:
        df.to_csv(f, header=write_header, index=False)

    # Update write_header flag to False after the first iteration
    write_header = False
    
browser.quit()

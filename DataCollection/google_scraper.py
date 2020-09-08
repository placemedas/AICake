import time
from selenium import webdriver
import requests
import io
from PIL import Image
from enum import Enum
import os
import argparse

def get_urls(query:str, driver, sleep_time:int=1):
    def scroll_to_page_end(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            #scroll to search end
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_time)

            new_height = driver.execute_script("return document.body.scrollHeight")
        
            if new_height == last_height:
                break
            last_height = new_height
            #class name for show more result button
            showmoreImages = driver.find_element_by_class_name("mye4qd")
            if showmoreImages.is_displayed():
                showmoreImages.click()
            # print("Element is visible? " + str(showmoreImages.is_displayed()))
        
    # build the google query 
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img" 
    
    # load the page 
    driver.get(search_url.format(q=query))
    
    image_urls = set() 
    image_count = 0 
    results_start_point = 0 
    # scroll all the way down
    scroll_to_page_end(driver) 
        
    # get all image thumbnails 
    thumbnail_results = driver.find_elements_by_css_selector("img.rg_i.Q4LuWd")
    num_thumbnails = len(thumbnail_results) 

    print(f"Found: {num_thumbnails} search results. Extracting links from {results_start_point}:{num_thumbnails}") 
    
    for img in thumbnail_results[results_start_point:10]: #num_thumbnails]:
        # click every thumbnail such that we can get the real image behind it 
        try: 
            img.click() 
            time.sleep(sleep_time) 
        except Exception: 
            continue 
        
        # extract image urls 
        fullSize_images = driver.find_elements_by_css_selector('img.n3VNCb') 
        for image in fullSize_images: 
            if image.get_attribute('src') and 'http' in image.get_attribute('src'): 
                image_urls.add(image.get_attribute('src')) 
                    
        image_count = len(image_urls) 
    
    return image_urls



def save_image(output_folder: str, url:str,count:int):
    try:
        url_content = requests.get(url).content
    except Exception as e:
        print(f"Download Error - Could not download {url} - {e}")
    try:
        image_file = io.BytesIO(url_content)
        image = Image.open(image_file)
        file_path = os.path.join(output_folder,'image{}.jpg'.format(count))
        with open(file_path, 'wb') as f:
            image.save(f,"JPEG",quality=90)
        print(f"saved-{url} as {file_path}")
    except Exception as e:
        print(f"Save Error - Could not save {url} - {e}")


def scrapeData(query, driverpath, outfolder):

    target = outfolder
    if not os.path.exists(target):
        os.makedirs(target)
    counter =0
    with webdriver.Chrome(executable_path=driverpath) as driver:
        urlList = get_urls(query,driver)
    
    for item in urlList:
        save_image(target, item, counter)
        counter+=1


if __name__ == "__main__":
    driver_path = r'C:\Users\Olay\Dev\chromedriver'
    ap = argparse.ArgumentParser(description="To help scrape images")
    ap.add_argument("query", help="search query")
    ap.add_argument("folder", help="path to output directory of images")

    args = ap.parse_args()
    query = args.query.lower()
    folder = args.folder.lower()
    scrapeData(query,driver_path,folder)
    
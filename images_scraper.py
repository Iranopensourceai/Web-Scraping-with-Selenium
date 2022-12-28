import os
import time
import urllib.request as request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager





class Image_Scraping:

      def __init__(self, query, search_engine, max_images, delay, high_reselotion):

            self.query = query
            self.search_engine = search_engine
            self.max_images = max_images
            self.delay = delay
            self.high_reselotion = high_reselotion


            if self.search_engine == "google":
                self.imgsLr_class = "Q4LuWd"
                self.imgsHr_class = "n3VNCb"
                self.load_more = ".mye4qd"
                self.xpath_nextImage = "//div[@class='tvh9oe BIB1wf']//a[@aria-label='Next Image']//div[@class='ZAxeoe']//*[name()='svg']"
                self.n_scroll = 3

            elif self.search_engine == "bing":
                self.imgsLr_class = "mimg"
                self.imgsHr_class = "nofocus"
                self.load_more = ".btn_seemore.cbtn.mBtn"
                self.id_nextImage = "navr"
                self.n_scroll = 3

                

            firefox_options = Options()
            firefox_options.add_argument("--headless")
            self.driver = webdriver.Firefox(GeckoDriverManager().install(), options=firefox_options)
            self.driver.set_window_size(1024, 768)



      def get_image_urls(self):

            self.driver.get(f"https://{self.search_engine}.com/")
            time.sleep(self.delay/2)

            search = self.driver.find_element(By.NAME, 'q')
            search.send_keys(self.query)
            search.send_keys(Keys.RETURN)
            time.sleep(self.delay)

            self.driver.find_element(By.XPATH, "//a[normalize-space()='Images']").click()
            time.sleep(self.delay)
            

            urls = set()
            img_count = 0
            results_start = 0  
            click = True



            if self.search_engine == "bing":
                try:
                    self.driver.find_element(By.CLASS_NAME, "bnp_btn_accept").click()
                    time.sleep(self.delay)
                except:
                    pass


            while img_count < self.max_images:

                    if self.high_reselotion:
                
                        if click:
                            img_lr = self.driver.find_element(By.XPATH, f"//img[contains(@class,'{self.imgsLr_class}')]")
                            img_lr.click()
                            if self.search_engine == "bing":
                                self.driver.switch_to.frame("OverlayIFrame")
                            time.sleep(self.delay)
                        click = False


                        img_hr = self.driver.find_element(By.CSS_SELECTOR, f"img.{self.imgsHr_class}")
                        if img_hr.get_attribute('src') and 'https' in img_hr.get_attribute('src'):
                                urls.add(img_hr.get_attribute('src'))


                        img_count = len(urls)
                        if img_count >= self.max_images:
                            print(f"Found: {img_count} image links")
                            break

                        else:
                            print("Found:", img_count, "looking for more image links ...")  
                            if self.search_engine == "google":              
                                self.driver.find_element(By.XPATH, self.xpath_nextImage).click()
                            elif self.search_engine == "bing":
                                self.driver.find_element(By.ID, self.id_nextImage).click()    
                            time.sleep(self.delay)



                    else:
                        self.scroll_down(2)
                        
                        imgResults_lr = self.driver.find_elements(By.XPATH, f"//img[contains(@class,{self.imgsLr_class})]")
                        totalResults = len(imgResults_lr)
                        print(f"Found: {totalResults} search results. Extracting links from {results_start}:{totalResults}")


                        for img_lr in imgResults_lr[results_start:totalResults]:
                                if img_lr.get_attribute('src') and 'https' in img_lr.get_attribute('src'):
                                    urls.add(img_lr.get_attribute('src'))


                        img_count = len(urls)
                        if img_count >= self.max_images:
                            print(f"Found: {img_count} image links")
                            break

                        else:
                            print("Found:", img_count, "looking for more image links ...")                
                            load_more_button = self.driver.find_element(By.CSS_SELECTOR, self.load_more)
                            self.driver.execute_script(f"document.querySelector('{self.load_more}').click();")
                            results_start = len(imgResults_lr)
    
            self.driver.quit()
            return urls



      def scroll_down(self, n):
            for _ in range(n):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.delay/2)



      def download_images(self, urls):

            if not os.path.isdir("Data"):
                os.mkdir("Data")

            urls = list(urls)
            for i in range(len(urls)):
                src = urls[i]

                try:
                    request.urlretrieve(src, f"Data/img{i+1}.jpg")
                except Exception as e:
                    print(f"Image {i+1} failed to download!")
                    continue       
            
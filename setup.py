import argparse
from images_scraper import *




parser = argparse.ArgumentParser(description='Process command line arguments.')
parser.add_argument("query", type=str)
parser.add_argument("max_images", type=int)
parser.add_argument("-e", "--search_engine", type=str, default="google")
parser.add_argument("-t", "--delay", type=int, default=4)
parser.add_argument("-r", "--High_reselotion", action='store_true')
args = parser.parse_args()




if __name__ == "__main__":

    scraper = Image_Scraping(query=args.query, max_images=args.max_images, search_engine=args.search_engine, delay=args.delay, high_reselotion=args.High_reselotion)

    urls = scraper.get_image_urls()
    scraper.download_images(urls)

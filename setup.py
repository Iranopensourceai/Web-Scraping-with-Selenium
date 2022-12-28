import argparse
from images_scraper import *




parser = argparse.ArgumentParser(description='Process command line arguments.')
parser.add_argument("q", help="query", type=str)
parser.add_argument("n", help="max_images", type=int)
parser.add_argument("-e", help="search_engine", type=str, default="google")
parser.add_argument("-t", help="delay", type=int, default=4)
parser.add_argument("-r", help="high_reselotion", action='store_true')
args = parser.parse_args()




if __name__ == "__main__":

    scraper = Image_Scraping(query=args.q, max_images=args.n, search_engine=args.e, delay=args.t, high_reselotion=args.r)

    urls = scraper.get_image_urls()
    scraper.download_images(urls)

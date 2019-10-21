from nameko.rpc import rpc
from nameko.timer import timer

from parser import add_posts_into_db
from settings import SCRAPING_INTERVAL


class Service:
    name = "scraper_service"

    @timer(interval=SCRAPING_INTERVAL, eager=True)
    def periodic_parse(self):
        add_posts_into_db()

    @rpc
    def parse(self):
        count = add_posts_into_db()
        return {'added': count}

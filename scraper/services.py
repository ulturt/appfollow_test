from nameko.rpc import rpc

from main import add_posts_into_db


class Service:
    name = "scraper_service"

    @rpc
    def parse(self):
        count = add_posts_into_db()
        return {'added': count}

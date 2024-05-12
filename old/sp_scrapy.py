import itertools
import scrapy
from old import database as db

from models import DataIdentifiersSelectedGeorge
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest
from scrapy.utils.project import get_project_settings


class SpeciesLink(scrapy.Spider):
    name = 'specieslink'
    base_url = 'https://specieslink.net/search/index'
    session = None
    query = None

    def __init__(self, query, session):
        self.query = query
        self.session = session

    def start_requests(self):
        for q in self.query:
            form_data = {
                'action': 'records',
                'graph_type': 'horizontalBar',
                'graph_sort': 'value',
                'from': '0',
                'recs_order_by': 'random_order',
                'dups_mode': 'collect_full_key',
                'coll_groups': '',
                'coll_networks': '',
                'catalognumber': q.catalog_number,
                'barcode': q.barcode
            }
            yield FormRequest(self.base_url,
                              formdata=form_data,
                              meta={'barcode': q.barcode, 'catalog_number': q.catalog_number, 'seq': q.seq},
                              callback=self.parse)

    def parse(self, response, **kwargs):
        barcode = response.meta.get('barcode')
        catalog_number = response.meta.get('catalog_number')
        seq = response.meta.get('seq')
        list_src = []
        list_title = []

        for url in response.xpath('//img'):
            list_src.append(url.xpath('@src').extract())
            list_title.append(url.xpath('@title').extract())

        list_src = list(itertools.chain(*list_src))
        list_title = list(itertools.chain(*list_title))
        list_src = [src for src in list_src if barcode in src or catalog_number in list_src]
        list_title = [title for title in list_title if barcode in title or catalog_number in list_title]

        if len(list_src) > 0 or len(list_title) > 0:
            self.session.query(DataIdentifiersSelectedGeorge) \
                .filter(DataIdentifiersSelectedGeorge.seq.__eq__(seq)) \
                .update(values={'list_src': list_src, 'list_title': list_title}, synchronize_session=False)
            self.session.commit()


def main():
    engine, session = db.connect()
    engine.echo = False

    query = session.query(DataIdentifiersSelectedGeorge) \
        .filter() \
        .all()

    process = CrawlerProcess(get_project_settings())
    process.crawl(SpeciesLink, query=query, session=session)
    process.start()

    session.close()
    engine.dispose()


if __name__ == '__main__':
    main()

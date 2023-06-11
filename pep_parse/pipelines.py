from datetime import datetime as dt
from collections import defaultdict
from csv import QUOTE_NONE, unix_dialect, writer
from pathlib import Path

from .settings import RESULTS

BASE_DIR = Path(__file__).parent.parent

RESULTS_DIR = BASE_DIR / RESULTS

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

FILE_NAME = 'status_summary_{}.csv'


class PepParsePipeline():

    def __init__(self):
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    def open_spider(self, spider):
        self.counter = defaultdict(int)

    def process_item(self, item, spider):
        self.counter[item['status']] += 1
        return item

    def close_spider(self, spider):
        with open(
            RESULTS_DIR / FILE_NAME.format(dt.now().strftime(DATETIME_FORMAT)),
            mode='w',
            encoding='utf-8',
        ) as f:
            writer(f, dialect=unix_dialect, quoting=QUOTE_NONE).writerows([
                ('Status', 'Count'),
                *self.counter.items(),
                ('Total', sum(self.counter.values()))
            ])

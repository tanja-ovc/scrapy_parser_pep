import datetime as dt

from .settings import BASE_DIR

count_statuses = {
    'Active': 0,
    'Accepted': 0,
    'Deferred': 0,
    'Final': 0,
    'Provisional': 0,
    'Rejected': 0,
    'Superseded': 0,
    'Withdrawn': 0,
    'Draft': 0,
}

now = dt.datetime.now()
current_time = now.strftime('%Y-%m-%d_%H-%M-%S')


class PepParsePipeline:
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        status = item['status']
        count_statuses[status] = count_statuses.get(status, 0) + 1
        all_peps_count = sum(count_statuses.values())
        filename = f'{BASE_DIR}/status_summary_{current_time}.csv'
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for status in count_statuses:
                amount = count_statuses[status]
                f.write(f'{status},{amount}\n')
            f.write(f'Total,{all_peps_count}\n')
        return item

    def close_spider(self, spider):
        pass

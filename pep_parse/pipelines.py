import csv
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


class PepParsePipeline:
    now = dt.datetime.now()
    current_time = now.strftime('%Y-%m-%d_%H-%M-%S')

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        status = item['status']
        count_statuses[status] = count_statuses.get(status, 0) + 1
        all_peps_count = sum(count_statuses.values())
        filename = f'{BASE_DIR}/status_summary_{self.current_time}.csv'
        with open(filename, 'w', newline='') as f:
            pep_csv_writer = csv.writer(f)
            pep_csv_writer.writerow(['Статус', 'Количество'])
            pep_table_rows = [
                [status, count_statuses[status]] for status in count_statuses
            ]
            pep_csv_writer.writerows(pep_table_rows)
            pep_csv_writer.writerow(['Total', all_peps_count])
        return item

    def close_spider(self, spider):
        pass

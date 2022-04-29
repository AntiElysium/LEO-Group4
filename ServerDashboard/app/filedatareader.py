import csv
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileDataReader:
    file: str

    def read_latest_data(self, data_type: str, n: int) -> list:
        data = []
        with open(self.file, "r") as data_file:
            cnt = 0
            for row in reversed(list(csv.reader(data_file))):
                if cnt == n:
                    break

                if row[1] == data_type:
                    data.append(row)
                    cnt += 1

        print(data_type + ": " + str(len(data)))
        return list(map(lambda x: (datetime.fromtimestamp(int(x[0]), tz=None), x[1], x[2], x[3]), data))
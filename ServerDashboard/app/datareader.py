from typing import Protocol

class DataReader(Protocol):
    def read_latest_data(self, data_type: str, n: int) -> list:
        raise NotImplementedError
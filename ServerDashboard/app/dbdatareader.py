from dataclasses import dataclass
from influxdb import InfluxDBClient

@dataclass
class DBDataReader:
    db_address: str
    db_user: str
    db_password: str

    client: InfluxDBClient = None
    close = None

    def connect(self):
        if ":" in self.db_address:
            tokens = self.db_address.split(":")
            self.client = InfluxDBClient(host=tokens[0], port=tokens[1], 
                                         username=self.db_user, password=self.db_password,
                                         ssl=True, verify_ssl=True)
        else:
            self.client = InfluxDBClient(host=self.db_address, port=8086,
                                         username=self.db_user, password=self.db_password,
                                         ssl=True, verify_ssl=True)
            
        self.client.switch_database("linux")
        self.close = self.client.close

    def read_latest_data(self, data_type: str, n: int) -> list:
        res = self.client.query(f"SELECT value, unit, time FROM {data_type} ORDER BY time DESC LIMIT {n}")
        return list(map(lambda x: (x["time"], data_type, x["value"], x["unit"]), res.get_points()))
import json, unittest, datetime

with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)

with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)

with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)

def parse_location(loc_string):
    parts = loc_string.split('/')
    return {
        "country": parts[0],
        "city": parts[1],
        "area": parts[2],
        "factory": parts[3],
        "section": parts[4]
    }

def parse_timestamp(timestamp):
    if isinstance(timestamp, str):
        dt = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        epoch = datetime.datetime.utcfromtimestamp(0)
        return int((dt - epoch).total_seconds() * 1000)
    return timestamp 

def normalize_input(data):
    try:
        return {
            "deviceID": data.get("deviceID"),
            "deviceType": data.get("deviceType"),
            "location": parse_location(data.get("location", "")),
            "data": {
                "status": data.get("operationStatus"),
                "temperature": data.get("temp")
            },
            "timestamp": parse_timestamp(data.get("timestamp"))
        }
    except Exception as e:
        print("Error normalizing input:", e)
        return None

result = normalize_input(jsonData1) or normalize_input(jsonData2)

class TestTelemetryData(unittest.TestCase):
    def test_combined_data_matches_expected(self):
        self.assertEqual(result, jsonExpectedResult)

unittest.main(argv=[''], exit=False)

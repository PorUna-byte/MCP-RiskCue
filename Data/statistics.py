import json
from pathlib import Path
from typing import List, Dict

ROOT         = Path(__file__).resolve().parent
QUERY_FILE    = ROOT / "queries_prin.json"
HISTORY_FILE = ROOT / "histories_prin.json"

query_map: Dict[str, List[str]] = json.loads(QUERY_FILE.read_text())
history_map: Dict[str, List[dict]] = json.loads(HISTORY_FILE.read_text())

def queries_statistics():
    queries_number = []
    for severName, queries in query_map.items():
        queries_number.append(len(queries))
    
    print("queries number distribution:\n", queries_number)


def histories_statistics():
    histories_number = []
    histories_min_max = []

    for severName, histories in history_map.items():
        histories_number.append(len(histories))
        min_len = 999
        max_len = -1
        for history in histories:
            min_len = min(len(history["history"]), min_len)
            max_len = max(len(history["history"]), max_len)

        histories_min_max.append((min_len, max_len))

    print("history numbers distribution:\n", histories_number)
    print("history length distribution:\n", histories_min_max)


queries_statistics()
histories_statistics()
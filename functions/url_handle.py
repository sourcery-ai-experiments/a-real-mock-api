import json
import logging
from typing import List

from fastapi import BackgroundTasks

logger = logging.getLogger(__name__)


tasks = BackgroundTasks()


class BuildUrlDict:
    path_dict = {}

    @classmethod
    def get_path_dict(cls):
        return cls.path_dict

    @classmethod
    def sync(cls):
        with open("files/openapi.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            path_dict = data["paths"]
        list_of_paths = []
        for key in path_dict.items():
            list_of_paths.append(key[0])
        cls.list_to_hierarchy_dict(list_of_paths)
        print("Paths Synced")

    @classmethod
    def list_to_hierarchy_dict(cls, url_patterns: List):
        url_patterns_list = []

        for pattern in url_patterns:
            pattern_parts = pattern.split("/")
            if pattern_parts[0] == "":
                del pattern_parts[0]
            url_patterns_list.append(pattern_parts)

        cls._build_dict(url_patterns_list)

    def linked_list(self, url_patterns: List, values: dict):
        if len(url_patterns) == 0:
            return {}
        values = url_patterns[0]
        del url_patterns[0]
        return self.linked_list(url_patterns, values)

    @classmethod
    def _build_dict(cls, url_patterns: List):
        result = {}
        for path in url_patterns:
            current_dict = result
            for element in path:
                if element not in current_dict:
                    current_dict[element] = {}
                current_dict = current_dict[element]
        cls.path_dict = result


class UrlHandler:

    @classmethod
    def sync(cls) -> None:
        tasks.add_task(BuildUrlDict.sync())

    @classmethod
    async def find_matching_url(cls, url_param: str):

        url_parts = url_param.split("/")
        if url_parts[0] == "":
            del url_parts[0]

        path = ""
        initial_path = BuildUrlDict.get_path_dict()
        keys_values = []

        for item in url_parts:
            try:
                _ = initial_path[item]
                if path == "":
                    path = item
                else:
                    path = path + "/" + item
                initial_path = initial_path[item]
            except KeyError:
                for key in initial_path.items():
                    if "{" in key[0]:
                        keys_values.append(item)
                        path = path + "/" + key[0]
                        initial_path = initial_path[key[0]]
                        break
        if path == {}:
            return "NOT FOUND"
        return str(path)


# Example usage
# url_patterns = [
#     "/applePay/sessions",
#     "/cancels",
#     "/paymentLinks/{linkId}",
#     "/paymentMethods/balance",
#     "/payments/{paymentPspReference}/amountUpdates",
#     "/payments/{paymentPspReference}/cancels",
#     "/payments/{paymentPspReference}/reversals",
# ]

# url = "/payments/Abdf/reversals"

# matching_pattern = find_matching_url(url, url_patterns)
# if matching_pattern:
#     print("Matching pattern:", matching_pattern)
# else:
#     print("No matching pattern found")

# # Example usage
# data = [
#     ["applePay", "sessions"],
#     ["cancels"],
#     ["paymentLinks", "{linkId}"],
#     ["paymentMethods", "balance"],
#     ["payments", "{paymentPspReference}", "amountUpdates"],
#     ["payments", "{paymentPspReference}", "cancels"],
#     ["payments", "{paymentPspReference}", "reversals"],
# ]

# url_dict = list_to_hierarchy_dict(data)
# print(url_dict)
a = {
    "applePay": {},
    "sessions": {"sessions": {}},
    "cancels": {"cancels": {}},
    "cardDetails": {},
    "donations": {},
    "orders": {},
    "cancel": {"cancel": {}},
    "originKeys": {},
    "paymentLinks": {},
    "{linkId}": {"{linkId}": {}},
    "paymentMethods": {},
    "balance": {"balance": {}},
    "paymentSession": {},
    "payments": {},
    "details": {"details": {}},
    "result": {"result": {}},
    "{paymentPspReference}": {"{paymentPspReference}": {}},
    "amountUpdates": {"amountUpdates": {}},
    "captures": {"captures": {}},
    "refunds": {"refunds": {}},
    "reversals": {"reversals": {}},
    "storedPaymentMethods": {},
    "{recurringId}": {"{recurringId}": {}},
}

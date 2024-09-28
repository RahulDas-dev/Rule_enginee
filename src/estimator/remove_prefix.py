from typing import Any, Dict, OrderedDict


class RemovePrefix:
    def __init__(self):
        pass

    def __str__(self):
        return "RemovePrefix"

    def __repr__(self):
        return "RemovePrefix"

    @staticmethod
    def remove_prefix_from_keys(
        obj: Dict[str, Any] | OrderedDict[str, Any],
        prefix: str = "sch:",
    ) -> Dict[str, Any] | OrderedDict[str, Any]:
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                new_key = key[len(prefix) :] if key.startswith(prefix) else key
                new_obj[new_key] = RemovePrefix.remove_prefix_from_keys(value, prefix)
        elif isinstance(obj, list):
            new_obj = [RemovePrefix.remove_prefix_from_keys(item, prefix) for item in obj]
        else:
            new_obj = obj
        return new_obj

    @staticmethod
    def add_prefix_to_keys(
        obj: Dict[str, Any] | OrderedDict[str, Any],
        prefix: str = "sch:",
    ) -> Dict[str, Any] | OrderedDict[str, Any]:
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                new_key = prefix + key if not key.startswith(prefix) else key
                new_obj[new_key] = RemovePrefix.add_prefix_to_keys(value, prefix)
        elif isinstance(obj, list):
            new_obj = [RemovePrefix.add_prefix_to_keys(item, prefix) for item in obj]
        else:
            new_obj = obj
        return new_obj

    def transform(
        self,
        data: Dict[str, Any] | OrderedDict[str, Any],
        prefix: str = "sch:",
    ) -> Dict[str, Any] | OrderedDict[str, Any]:
        # Transform JSON data by removing prefix
        return RemovePrefix.remove_prefix_from_keys(data, prefix)

    def inverse_transform(
        self,
        data: Dict[str, Any] | OrderedDict[str, Any],
        prefix: str = "sch:",
    ) -> Dict[str, Any] | OrderedDict[str, Any]:
        # Transform JSON data by adding prefix
        return RemovePrefix.add_prefix_to_keys(data, prefix)

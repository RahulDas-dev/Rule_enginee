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
        obj: Dict[str, Any] | OrderedDict[str, Any], prefix="sch:"
    ) -> Dict[str, Any] | OrderedDict[str, Any]:
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                new_key = key[len(prefix) :] if key.startswith(prefix) else key
                new_obj[new_key] = RemovePrefix.remove_prefix_from_keys(value, prefix)
            return new_obj
        elif isinstance(obj, list):
            return [RemovePrefix.remove_prefix_from_keys(item, prefix) for item in obj]
        else:
            return obj

    @staticmethod
    def add_prefix_to_keys(
        obj: Dict[str, Any] | OrderedDict[str, Any], prefix="sch:"
    ) -> Dict[str, Any] | OrderedDict[str, Any]:
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                new_key = prefix + key if not key.startswith(prefix) else key
                new_obj[new_key] = RemovePrefix.add_prefix_to_keys(value, prefix)
            return new_obj
        elif isinstance(obj, list):
            return [RemovePrefix.add_prefix_to_keys(item, prefix) for item in obj]
        else:
            return obj

    def transform(
        self, data: Dict[str, Any] | OrderedDict[str, Any], prefix="sch:"
    ) -> Dict[str, Any] | OrderedDict[str, Any]:
        # Transform JSON data by removing prefix
        return RemovePrefix.remove_prefix_from_keys(data, prefix)

    def inverse_transform(
        self, data: Dict[str, Any] | OrderedDict[str, Any], prefix="sch:"
    ) -> Dict[str, Any] | OrderedDict[str, Any]:
        # Transform JSON data by adding prefix
        return RemovePrefix.add_prefix_to_keys(data, prefix)


# Example usage:
# transformer = Transformer()
# input_data = {
#     "sch:name": "John",
#     "sch:details": {
#         "sch:age": 30,
#         "sch:city": "New York"
#     }
# }
# transformed_data = transformer.transform(input_data)
# print(transformed_data)
# inverse_transformed_data = transformer.inverse_transform(transformed_data)
# print(inverse_transformed_data)

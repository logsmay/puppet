def merge_range(ranges: list, start_key: str, end_key: str):
    # http://stackoverflow.com/a/36827622/137954
    ranges = sorted(ranges, key=lambda x: x[start_key])
    saved = dict(ranges[0])

    for range_set in sorted(ranges, key=lambda x: x[start_key]):
        if range_set[start_key] <= saved[end_key]:
            saved[end_key] = max(saved[end_key], range_set[end_key])
        else:
            yield dict(saved)
            saved[start_key] = range_set[start_key]
            saved[end_key] = range_set[end_key]
    yield dict(saved)


def remove_children(input_dict: dict):
    for item in dict(input_dict):
        if not isinstance(input_dict[item], (str, int, float)):
            del input_dict[item]

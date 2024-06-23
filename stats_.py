def mean(values: list) -> float:
    assert len(values) != 0, "<values> should not be empty"
    m = len(values)
    values_sum = sum(values)
    return values_sum / m


def var(values: list) -> float:
    assert len(values) != 0, "<values> should not be empty"
    m = len(values)
    v_mean = mean(values)
    ss = sum([(x - v_mean)**2 for x in values])
    return ss / m


def std(values: list) -> float:
    assert len(values) != 0, "<values> should not be empty"
    return var(values)**0.5


def max(values: list) -> float:
    assert len(values) != 0, "<values> should not be empty"
    v_max = values[0]
    for val in values:
        if val > v_max:
            v_max = val
    return v_max


def min(values: list) -> float:
    assert len(values) != 0, "<values> should not be empty"
    v_min = values[0]
    for val in values:
        if val < v_min:
            v_min = val
    return v_min


def median(values: list) -> float:
    assert len(values) != 0, "<values> should not be empty"
    m = len(values)

    if m % 2 != 0:
        return values[m // 2]
    else:
        med = (values[m // 2 - 1] + values[m // 2]) / 2
        return med


def quartiles(values: list) -> float:
    assert len(values) != 0, "<values> should not be empty"
    m = len(values)

    q1 = median(values[:m // 2])
    q3 = median(values[m // 2:])
    return (q1, q3)


def describe(data: dict):
    describe_dict = {
        "Feature": [],
        "Count": [],
        "Mean": [],
        "Std": [],
        "Min": [],
        "25%": [],
        "50%": [],
        "75%": [],
        "Max": []
    }
    if isinstance(data, dict):
        for key, values in data.items():
            q1, q3 = quartiles(values)
            describe_dict["Feature"].append(key)
            describe_dict["Count"].append(round(float(len(values)), 6))
            describe_dict["Mean"].append(round(mean(values), 6))
            describe_dict["Std"].append(round(std(values), 6))
            describe_dict["Min"].append(round(min(values), 6))
            describe_dict["25%"].append(round(q1, 6))
            describe_dict["50%"].append(round(median(values), 6))
            describe_dict["75%"].append(round(q3, 6))
            describe_dict["Max"].append(round(max(values), 6))

        for key, stat in describe_dict.items():
            print(f"{key:<10}", *stat, sep='         ')

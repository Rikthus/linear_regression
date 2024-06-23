import os
import sys
import csv
import matplotlib.pyplot as plt
import stats_ as st

PARAM_FILE_PATH = "./parameters.txt"


def load_data(path: str) -> dict:
    assert isinstance(path, str) and len(path) != 0, \
        "<path> should be a non empty string"
    assert os.path.exists(path) and os.path.isfile(path), \
        "<path> should be a valid file path"

    data = {
        'km': [],
        'price': []
    }
    with open(path, mode='r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            data['km'].append(float(line['km']))
            data['price'].append(float(line['price']))

    nb_km = len(data['km'])
    nb_price = len(data['price'])
    assert nb_km != 0 and nb_price != 0 and nb_km == nb_price, \
        "data should have the same non null number of km and price values"
    return data


def update_param_file(t1: float, t0: float):
    with open(PARAM_FILE_PATH, mode='w') as f:
        f.write(f"theta1 {t1}\n")
        f.write(f"theta0 {t0}")


def compute_r(t1: float, t0: float, data: dict):
    err_fit = 0
    err_mean = 0
    m = len(data['km'])
    for x, y in zip(data['km'], data['price']):
        err_fit += ((y - (t1*x + t0))**2)**0.5
        err_mean += y
    err_fit = err_fit / m
    err_mean = err_mean / m
    return (err_mean - err_fit) / err_mean


def min_max_scaling(values: list) -> list:
    x_min = st.min(values)
    x_max = st.max(values)
    assert x_max > x_min, "max and min_values are the same"

    scaled_values = []
    for val in values:
        scaled_val = (val - x_min) / (x_max - x_min)
        scaled_values.append(scaled_val)
    return scaled_values


def unscale_params(t1: float, t0: float, data: dict) -> tuple[float, float]:
    x_min = st.min(data['km'])
    x_max = st.max(data['km'])
    y_min = st.min(data['price'])
    y_max = st.max(data['price'])

    t1 = t1 * (y_max - y_min) / (x_max - x_min)
    t0 = (t0 * (y_max - y_min)) + y_min - t1 * x_min
    return (t1, t0)


def estimate_price(t1: float, t0: float, x: float) -> float:
    return t1 * x + t0


def gradient_descent(
    t1: float,
    t0: float,
    data: dict,
    l_rate: float,
) -> tuple[float, float]:
    t1_gradient = 0
    t0_gradient = 0
    m = len(data['km'])

    for x, y in zip(data['km'], data['price']):
        t1_gradient += ((estimate_price(t1, t0, x) - y) * x)
        t0_gradient += (estimate_price(t1, t0, x) - y)

    tmp_t1 = l_rate * (1 / m) * t1_gradient
    tmp_t0 = l_rate * (1 / m) * t0_gradient
    return tmp_t1, tmp_t0


def linear_regression(data: dict, l_rate: float = 0.01, epochs: int = 10000):
    t1 = 0
    t0 = 0
    norm_data = {}

    norm_data['km'] = min_max_scaling(data['km'])
    norm_data['price'] = min_max_scaling(data['price'])

    for _ in range(epochs):
        tmp_t1, tmp_t0 = gradient_descent(t1, t0, norm_data, l_rate)
        t1 -= tmp_t1
        t0 -= tmp_t0

    t1, t0 = unscale_params(t1, t0, data)
    bonus_data(t1, t0, data)
    update_param_file(t1, t0)


def bonus_data(t1: float, t0: float, data: dict):
    r = compute_r(t1, t0, data)
    print(f"theta1 = {t1}")
    print(f"theta0 = {t0}\n")
    print(f"R:    {r:.2f}")
    print(f"R^2:  {r**2:.2f}\n")
    st.describe(data)
    plt.scatter(data['km'], data['price'])
    plt.plot(data['km'], [estimate_price(t1, t0, x) for x in data['km']])
    plt.xlabel("Distance in km")
    plt.ylabel("Price in $")
    plt.show()


def main():
    try:
        args = sys.argv
        assert len(args) == 2, \
            "usage: train.py <data/path>"
        assert isinstance(args[1], str), \
            "<data/path> should be a string"
        data = load_data(args[1])
        assert data
        linear_regression(data)
    except Exception as e:
        print(f"{e.__class__.__name__}: {e.args[0]}")


if __name__ == "__main__":
    main()

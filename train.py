import os
import sys
import csv
import matplotlib.pyplot as plt

PARAM_FILE_PATH = "./parameters.txt"


def load_data(path: str) -> dict:
    assert isinstance(path, str) and len(path) != 0, \
        "<path> should be a non empty string"
    assert os.path.exists(path) and os.path.isfile(path), \
        "<path> should be a valid file path"

    dataset = {
        'km': [],
        'price': []
    }
    with open(path, mode='r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            dataset['km'].append(float(line['km']))
            dataset['price'].append(float(line['price']))

    nb_km = len(dataset['km'])
    nb_price = len(dataset['price'])
    assert nb_km != 0 and nb_price != 0 and nb_km == nb_price, \
        "dataset should have the same non null number of km and price values"
    return dataset


def update_param_file(t1: float, t0: float):
    with open(PARAM_FILE_PATH, mode='w') as f:
        f.write(f"theta1 {t1}\n")
        f.write(f"theta0 {t0}")


def loss_function(t1: float, t0: float, dataset: dict):
    err_sum = 0
    m = len(dataset['km'])
    for x, y in zip(dataset['km'], dataset['price']):
        err_sum += (y - (t1*x + t0))**2
    return err_sum / m


def estimate_price(t1: float, t0: float, x: float) -> float:
    return t1 * x + t0


def min_max_ft_scaling(values: list) -> list:
    min_val = min(values)
    max_val = max(values)
    
    scaled_values = []
    
    for val in values:
        scaled_val = (val - min_val) / (max_val - min_val)
        scaled_values.append(scaled_val)
    
    return scaled_values


def gradient_descent(
    t1: float,
    t0: float,
    dataset: dict,
    l_rate: float,
) -> tuple[float, float]:
    t0_gradient = 0
    t1_gradient = 0
    m = len(dataset['km'])

    for x, y in zip(dataset['km'], dataset['price']):
        t0_gradient += (1 / m) * (estimate_price(t1, t0, x) - y)
        t1_gradient += (1 / m) * (estimate_price(t1, t0, x) - y) * x

    t1 = t1 - l_rate * t1_gradient
    t0 = t0 - l_rate * t0_gradient
    return t1, t0


def linear_regression(dataset, l_rate: float = 0.0001, epochs: int = 1000000):
    t1 = 0
    t0 = 0

    dataset['km'] = min_max_ft_scaling(dataset['km'])
    err_rate = 0
    for i in range(epochs):
        t1, t0 = gradient_descent(t1, t0, dataset, l_rate)
        err_rate = loss_function(t1, t0, dataset)

    print(f"Error rate: {err_rate}")
    print(f"theta1 = {t1}")
    print(f"theta0 = {t0}")
    update_param_file(t1, t0)


def main():
    try:
        args = sys.argv
        assert len(args) == 2, \
            "usage: train.py <dataset/path>"
        assert isinstance(args[1], str), \
            "<dataset/path> should be a string"
        dataset = load_data(args[1])
        assert dataset
        # plt.scatter(dataset['km'], dataset['price'])
        # plt.show()
        linear_regression(dataset)
    except Exception as e:
        print(f"{e.__class__.__name__}: {e.args[0]}")


if __name__ == "__main__":
    main()

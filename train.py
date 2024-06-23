import os
import sys
import csv
import matplotlib.pyplot as plt
from math_ import mean


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


def loss_function(a: float, b: float, dataset: dict):
    err_sum = 0
    m = len(dataset['km'])
    for x, y in zip(dataset['km'], dataset['price']):
        err_sum += (y - (a*x + b))**2
    return err_sum / m


def estimate_price(t0: float, t1: float, x: float) -> float:
    return t0 + t1 * x


def linear_regression(a: float, b: float, dataset: dict, l_rate: float):
    t0 = 0
    t1 = 0
    m = len(dataset['km'])

    err_sum_t0 = 0
    err_sum_t1 = 0
    for x, y in zip(dataset['km'], dataset['price']):
        err_sum_t0

        t0 += tmp_t0
        t1 += tmp_t1


def main():
    try:
        args = sys.argv
        assert len(args) == 2, \
            "usage: train.py <dataset/path>"
        assert isinstance(args[1], str), \
            "<dataset/path> should be a string"
        dataset = load_data(args[1])
        assert dataset
        plt.scatter(dataset['km'], dataset['price'])
        plt.show()
        # train_model(df)
    except Exception as e:
        print(f"{e.__class__.__name__}: {e.args[0]}")


if __name__ == "__main__":
    main()

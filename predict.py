PARAM_FILE_PATH = "./parameters.txt"


def estimate_price(t0: float, t1: float, x: float) -> float:
    return t0 + t1 * x


def retrieve_parameters() -> tuple[float, float]:
    try:
        t0 = 0
        t1 = 0
        with open(PARAM_FILE_PATH, mode='r') as f:
            for line in f:
                key, val = line.split()
                if key == "theta0" and t0 == 0:
                    t0 = float(val)
                elif key == "theta1" and t1 == 0:
                    t1 = val
                else:
                    raise Exception("Uncorrect file format")
    except Exception as e:
        print(f"{e.__class__.__name__}: {e.args[0]}")
    return t0, t1


def main():
    try:
        t0, t1 = retrieve_parameters()
        mileage = float(input("Enter the car mileage:  "))
        price_estimate = estimate_price(t0, t1, mileage)
        print(f"Estamed price is {price_estimate:.2f}$")
    except Exception as e:
        print(f"{e.__class__.__name__}: {e.args[0]}")


if __name__ == "__main__":
    main()

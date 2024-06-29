PARAM_FILE_PATH = "./weights.txt"


def estimate_price(t1: float, t0: float, x: float) -> float:
    return t1 * x + t0


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
                    t1 = float(val)
                else:
                    raise Exception("Uncorrect file format")
    except Exception as e:
        print(f"{e.__class__.__name__}: {e.args[0]}")
    return t1, t0


def main():
    try:
        t1, t0 = retrieve_parameters()
        kilometers = float(input("Enter the car kilometers:  "))
        assert kilometers >= 0, "kilometers cannot be negative"
        price_estimate = estimate_price(t1, t0, kilometers)
        print(f"Estamed price is {price_estimate:.2f}$")
    except Exception as e:
        print(f"{e.__class__.__name__}: {e.args[0]}")


if __name__ == "__main__":
    main()

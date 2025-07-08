from src.loader import load_file


def print_data(data):
    print(data)


if __name__ == "__main__":
    data = load_file("data/test.csv")
    print_data(data)

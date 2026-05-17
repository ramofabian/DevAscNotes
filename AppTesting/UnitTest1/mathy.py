#mathy.py
def add_numbers(a: int, b: int) -> int:
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both arguments must be integers")
    return a + b

if __name__ == "__main__":
    print(add_numbers(1, 2))
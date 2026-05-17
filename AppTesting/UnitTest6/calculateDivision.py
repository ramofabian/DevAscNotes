#calculateDevision.py
def calculateDivision(a: int|float, b: int|float) -> float:
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numbers")
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return f"The result of the division is: {a / b}" 

if __name__ == "__main__":
    num1 = float(input("Enter the numerator: "))
    num2 = float(input("Enter the denominator: "))
    result = calculateDivision(num1, num2)
    print(result)
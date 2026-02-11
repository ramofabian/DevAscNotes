# Flow Control Examples
print("Flow Control Examples:", "\n" + "=" * 30)
# 1. if/elif/else statement
print("\nif/elif/else statement:")
age = 25
if age < 13:
    print(f"Age {age} is a Child")
elif age < 18:
    print(f"Age {age} is a Teenager")
else:
    print(f"Age {age} is an Adult")

# 2. for loop
print("\nFor loop:")
for i in range(5):
    print(f"Iteration {i}")

# 3. while loop
print("\nWhile loop:")
count = 0
while count < 3:
    print(f"Count: {count}")
    count += 1

# 4. break and continue
print("\nBreak and continue:")
for i in range(10):
    if i == 3:
        continue  # Skip iteration when i is 3
    if i == 7:
        break  # Exit loop when i is 7
    print(i)

# 5. Nested loops
print("\nNested loops:")
for row in range(3):
    for col in range(3):
        print(f"({row},{col})", end=" ")
    print()

# 6. try/except for error handling
print("\nError handling:")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
finally:
    print("Operation completed")

# 7. match statement (Python 3.10+)
print("\nMatch statement:")
http_code = 404
match http_code:
    case 200:
        print("OK - Request successful")
    case 201:
        print("Created - Resource created")
    case 400:
        print("Bad Request - Invalid request")
    case 401:
        print("Unauthorized - Authentication required")
    case 404:
        print("Not Found - Resource not found")
    case 500:
        print("Internal Server Error")
    case 503:
        print("Service Unavailable")
    case _:
        print(f"Unknown HTTP code: {http_code}")


print("""\n
Challenge:
----------
1) Create a loop to iterate over the list of cars so that you can 
2) TRY to see 
3) IF the price is over $100,000. Print out to the terminal which cars ARE over $100,000 only.
      
Results:
--------""")
favorite_cars = [
    {
        "make": "Tesla",
        "model": "Model S",
        "year": 2022,
        "price": 79999.99,
        "features": ["Autopilot", "Electric", "All-Wheel Drive"],
        "is_electric": True,
        "owner": None
    },
    {
        "make": "Porsche",
        "model": "911 Carrera",
        "year": 2023,
        "price": 106500.00,
        "features": ["Sport Mode", "Rear-Wheel Drive", "Turbocharged"],
        "is_electric": False,
        "owner": None
    },
    {
        "make": "Ford",
        "model": "Mustang",
        "year": 2022,
        "price": 27995.00,
        "features": ["Rear-Wheel Drive", "V8 Engine", "Fastback"],
        "is_electric": False,
        "owner": None
    },
    {
        "make": "Chevrolet",
        "model": "Corvette",
        "year": 2023,
        "price": 62995.00,
        "features": ["Supercharged", "V8 Engine", "Fastback"],
        "is_electric": False,
        "owner": None
    },
    {
        "make": "Audi",
        "model": "R8",
        "year": 2023,
        "price": 144195.00,
        "features": ["All-Wheel Drive", "V10 Engine", "Convertible"],
        "is_electric": False,
        "owner": None
    }
]

for car in favorite_cars:
    try:
        if car["price"] > 100000:
            print(f"{car['make']} {car['model']} is over $100,000 with a price of ${car['price']:.2f}")
    except KeyError as e:
        print(f"Key error: {e} - Missing key in car data")
#Functions, Methods, and Classes
"""Functions are reusable blocks of code that perform a specific task. 
They can take inputs (called parameters) and return outputs. 
Methods are functions that are associated with an object and can operate on that object's data. 
Classes are blueprints for creating objects, which can have attributes (data) and methods (functions)."""
print(f"Functions, Methods, and Classes\n{'#'*40}")
#################################

#Functions
from funcs.my_module import cube_number, greet_person

print(f"Functions\n{'-'*20}")
result = cube_number(input_number=3)
print(result)  # Output: 27
greeting = greet_person(name="Alice")
print(greeting)  # Output: Hello, Alice!

#Classes
from classess.my_clasess import Car

print(f"\nClasses\n{'-'*20}")
my_clasess = Car(make="Toyota", model="Camry", year=2020, mileage=15000, condition="Good", color="Blue")
print(f"Make: {my_clasess.make}")   
print(f"Dict: {my_clasess.__dict__}")   
my_wife_clasess = Car(make="Honda", model="Civic", year=2018, mileage=30000, condition="Fair", color="Red")
print(f"Make: {my_wife_clasess.make}")
print(f"Dict: {my_wife_clasess.__dict__}")

#Methods
print(f"\nMethods\n{'-'*20}")
my_clasess.start()  # Output: The Toyota Camry is starting.     
my_clasess.accelerate(increase_speed=30)  # Output: The Toyota Camry is accelerating. Current speed: 30 mph.
my_clasess.accelerate(increase_speed=20)  # Output: The Toyota Camry is accelerating. Current speed: 50 mph.
my_clasess.stop()  # Output: The Toyota Camry is stopping.
my_wife_clasess.start()  # Output: The Honda Civic is starting.
my_wife_clasess.accelerate(increase_speed=20)  # Output: The Honda Civic is accelerating. Current speed: 20 mph.
my_wife_clasess.accelerate(increase_speed=10)  # Output: The Honda Civic is accelerating. Current speed: 30 mph.
my_wife_clasess.stop()  # Output: The Honda Civic is stopping.  


#Challenge:
print(f"\nChallenge\n{'-'*20}")
from classess.my_clasess import Human

my_human = Human()
person1 = my_human.create_human(first_name="John", last_name="Doe", age=30, sex="Male", height=5.9, weight=180, occupation="Engineer", hobbies=["Reading", "Hiking"], country="USA")
print(f"Person 1: {person1}")
my_human.add_human(person1)
my_human.show_humans()
person2 = my_human.create_human(first_name="Jane", last_name="Smith", age=28, sex="Female", height=5.5, weight=150, occupation="Designer", hobbies=["Painting", "Traveling"], country="USA")
print(f"Person 2: {person2}")
my_human.add_human(person2)
my_human.show_humans()

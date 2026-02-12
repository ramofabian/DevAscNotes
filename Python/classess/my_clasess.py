class Car:
    """A class representing a car with attributes and methods to start, stop, and accelerate."""
    def __init__(self, make: str, model: str, year: int, mileage: int, condition: str, color: str) -> None:
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.condition = condition
        self.color = color
        self.running = False
        self.speed = 0        
    
    def start(self) -> None:
        """Starts the car if it's not already running."""
        if not self.running:
            self.running = True
            print(f"The {self.make} {self.model} is starting.")
        else:
            print(f"The {self.make} {self.model} is already running.")

    def stop(self) -> None:
        """Stops the car if it's currently running."""
        if self.running:
            self.running = False
            print(f"The {self.make} {self.model} is stopping.")
        else:
            print(f"The {self.make} {self.model} is already stopped.")

    def accelerate(self, increase_speed: int) -> None:
        """Increases the car's speed by a specified amount."""
        if self.running:
            self.speed += increase_speed
            print(f"The {self.make} {self.model} is accelerating. Current speed: {self.speed} mph.")
        else:
            print(f"Cannot accelerate. The {self.make} {self.model} is not running.")

class Human:
    """A class representing a human with attributes and methods to eat, sleep, and work."""
    def __init__(self) -> None:
        self.human_list = []
    
    def create_human(self, first_name: str, last_name: str, age: int, sex: str, height: float, weight: float,
                     occupation: str, hobbies: list, country: str) -> dict:
        """Creates a human with the specified attributes and returns a dictionary representation."""
        human = {
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "sex": sex,
            "height": height,
            "weight": weight,
            "occupation": occupation,
            "hobbies": hobbies,
            "country": country
        }
        print(f"Created human: {human['first_name']} {human['last_name']}")
        return human
    
    def add_human(self, human: dict) -> None:
        """Adds a human to the human list."""
        self.human_list.append(human)
        print(f"Added human: {human['first_name']} {human['last_name']} to the human list.")
    
    def show_humans(self) -> None:
        """Prints all humans in the human list."""
        print("Humans in the list:")
        for human in self.human_list:
            print(human)
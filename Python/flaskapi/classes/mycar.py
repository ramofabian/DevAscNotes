class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def to_dict(self):
        return {
            'make': self.make,
            'model': self.model,
            'year': self.year
        }
    def display_info(self):
        return f"{self.year} {self.make} {self.model}"
    
    def drive(self):
        return f"The {self.make} {self.model} is driving."
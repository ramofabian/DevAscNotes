class ingesthuman:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age
        }
    def display_info(self):
        return f"{self.name} is {self.age} years old."
    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."
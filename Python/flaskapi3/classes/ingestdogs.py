class ingestdogs:
    def __init__(self):
        self.name = ""
        self.age = ""
        self.breed = ""
        self.inventory = []
    
    def add_to_list(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed
        self.inventory.append({"name": self.name, "age": self.age, "breed": self.breed})
        return True
    def display_info(self):
        return f"{self.name} is {self.age} years old and is a {self.breed}."
    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."
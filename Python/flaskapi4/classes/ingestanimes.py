class ingestanimes:
    def __init__(self):
        self.tile = ""
        self.genre = ""
        self.rating = ""
        self.release_year = ""
        self.studio = ""
        self.inventory = []
    
    def add_to_list(self, title, genre, rating, release_year, studio):
        self.title = title
        self.genre = genre
        self.rating = rating
        self.release_year = release_year
        self.studio = studio
        self.inventory.append({
            "title": self.title,
            "genre": self.genre,
            "rating": self.rating,
            "release_year": self.release_year,
            "studio": self.studio
        })
        return True
    def display_info(self):
        return f"{self.title} is a {self.genre} anime with a rating of {self.rating}."
    def greet(self):
        return f"Hello, my name is {self.title} and I am an anime."
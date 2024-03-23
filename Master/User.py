# Class of the User object
class User:
    '''
        This is a local class that represents the User object, here can be implemented user-related methods
    '''
    def __init__(self, name, surname, age, features, favorite_game = "tic tac toe", id = None):

        self.id = id
        self.name = name
        self.surname = surname
        self.age = age
        self.favorite_game = favorite_game
        self.features = features

    def get_profile(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'age': self.age,
            'favorite_game': self.favorite_game,
            'features': self.features
        }

    def __str__(self):
        return f'{self.name} {self.surname} ({self.age})'
    

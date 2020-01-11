class Dog:
    def __init__(self):  # Called whenever the object is created
        print("Woof, woof!")

    def pee(self):
        print("I will pee!")


class Puppy(Dog):
    def __init__(self):
        super().__init__()
        print("I'm puppy")

    def pee(self):
        print("Let's go to the park")
        super().pee()  # This allows the child class to access to the parent class.


pug = Puppy()
pug.pee()

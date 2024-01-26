class Shape:
    def __init__(self, name):
        self.name = name
    def perimiter(self):
        raise NotImplementedError("perimeter")
    def area(self):
        raise NotImplementedError("area")

class Square(Shape):
    def __init__(self, name, side):
        super().__init__(name)
        self.side = side
        
    def perimeter(self):
        return 4 * self.side
    
    def area(self):
        return self.side ** 2

class Circle(Shape):
    def __init__(self, name, radius):
        super().__init__(name)
        self.radius = radius
        
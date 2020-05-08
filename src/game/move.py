class Move():
    
    def __init__(self, color, column):
        self.color = color
        self.column = column
        
    def render(self):
        template = "color : {}, column: {}."
        print(template.format(self.color, self.column))
        
        
    def equals(self, otherMove):
        if (otherMove.color == self.color) & (otherMove.column == self.column) :
            return True
        else:
            return False
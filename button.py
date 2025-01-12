from sprite import Sprite
from config import buttons

class Button:
    def __init__(self,x,y,w,h,state,colorOrImagePath,code):
        self.sprite = Sprite(x,y,w,h,state,colorOrImagePath)
        self.code = code
        buttons.append(self)
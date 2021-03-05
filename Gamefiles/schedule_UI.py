def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(screen, text, input, size = 30, color = (0, 0, 0)):
    import pygame as pg
    font = None
    largeText = pg.font.Font(font, size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.topleft = (input.mx + 50, input.my)
    screen.blit(TextSurf, TextRect)
    dimension = largeText.render(text, True, color).get_rect()
    return(TextRect)

class schedule_block:
    def __init__(self, tag_dict):
        from random import randint as rhombus
        self.color = (rhombus(0, 125), rhombus(0, 125), rhombus(0, 125))
        self.name = tag_dict['Name']
        self.x, self.y = 100, 0
        self.grabbed = False
    def display(self, screen, input):
        message_display(screen, self.name, input)
    def be(self, screen, input):
        import pygame as py
        rect = py.draw.rect(screen, self.color, (self.x, self.y, 100, 100))
        if not self.grabbed:
            if rect.collidepoint(input.mx, input.my): input.mouse.rect_list.append(self.name)
            if input.mouse.rect_over == self.name:
                self.display(screen, input)
                if input.t1:
                    self.grabbed = True
                    self.snap_x, self.snap_y = input.mx - self.x, input.my - self.y
            if self.x % 100:
                self.x /= 100
                self.x = round(self.x)
                self.x = 100*self.x
                if self.x < 0:
                    self.x += 200
            if self.x == 0:
                self.x += 100
            if self.y % 100:
                self.y /= 100
                self.y = round(self.y)
                self.y = 100*self.y
                if self.y < 0:
                    self.y += 100
        if self.grabbed:
            self.x, self.y = input.mx - self.snap_x, input.my - self.snap_y
            self.display(screen, input)
            if not input.m1:
                self.grabbed = False

class schedule_UI_obj:
    def __init__(self, jsondata):
        self.red = schedule_block({'Name': 'tutorial'})
        self.blue = schedule_block({'Name': 'carnival_offer'})
    def go(self, screen, inpt, jsondata):
        self.red.be(screen, inpt)
        self.blue.be(screen, inpt)

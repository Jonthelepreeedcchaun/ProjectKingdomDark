def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class duskscroll_obj:
    def __init__(self):
        from Gamefiles.ass_processing import ass
        self.font = 1; self.ticktrack = 1
        self.arrow_ass = ass(['arrow_be1.png', 'arrow_be2.png', 'arrow_be3.png'], path = 'Ass/DuskScroll/', name = 'arrow')
        #self.scroll_ass = ass(['duskscroll_be1.png', 'duskscroll_be2.png', 'duskscroll_be3.png'], path = 'Ass/DuskScroll/', name = 'duskscroll');
    def message_display(self, screen, text, x, y, size, tick = None, color = (185, 185, 185)):
        import pygame as pg
        font = None
        if tick != None:
            if tick != self.ticktrack:
                self.font += 1
                self.ticktrack += 1
                if self.font == 3:
                    self.font = 1
                if self.ticktrack == 4:
                    self.ticktrack = 1
            font = 'Ass/Textbox/Drawnfont' + str(self.font) + '.ttf'
        largeText = pg.font.Font(font, size)
        TextSurf, TextRect = text_objects(text, largeText, color)
        TextRect.center = (x, y)
        screen.blit(TextSurf, TextRect)
        dimension = largeText.render(text, True, color).get_rect()
        return(TextRect)
    def show(self, screen, oxygen, input, jsondata, tick):
        if self.arrow_ass.pose(screen, oxygen, 'be', (765, 720), tick, -8).collidepoint(input.mx, input.my) and input.t1:
            return True
        self.message_display(screen, 'Day ' + str(jsondata.day), 1920/2, 200, 250, tick)
        number = 0
        for this in jsondata.stats:
            number += 1
            self.message_display(screen, this + ' - ' + str(jsondata.stats[this]), 1920/2, 300 + 100*number, 100, tick)

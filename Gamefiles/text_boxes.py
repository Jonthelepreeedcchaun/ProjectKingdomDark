def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class text_box:
    def __init__(self):
        from Gamefiles.ass_processing import ass, speech_obj; import os
        self.linedict = None; self.browse = 0; self.dialength = 1
        self.font = 1; self.ticktrack = 1; self.decision = False; self.key = None
        self.scroll_ass = ass(['scroll_be1.png', 'scroll_be2.png', 'scroll_be3.png'], path = 'Ass/Textbox/', name = 'scroll');
        self.face_ass_dict = {}; self.face_ass_back_dict = {}
        character_list = ['hatlor']
        for this in os.listdir(os.path.join('Ass','Textbox')):
            if this[-8:] == "_be3.png" and not this[:6] == "scroll":
                if not 'back' in this:
                    self.face_ass_dict.update({this[:-8]: ass([this[:-5] + '1.png', this[:-5] + '2.png', this[:-5] + '3.png'], 'Ass/Textbox/', this[:-8])})
                else:
                    self.face_ass_back_dict.update({this[:-12]: ass([this[:-5] + '1.png', this[:-5] + '2.png', this[:-5] + '3.png'], 'Ass/Textbox/', this[:-8])})
        self.bubble = speech_obj(); self.bubble_pose = None
    def reset(self):
        self.browse = 0
        self.decision = False
        self.donewriting = False
        self.key = None
    def message_display(self, screen, text, x, y, size, color, tick = None):
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
    def box(self, screen, oxygen, jsondata, input, text_dict, x, y, x_len, time, tick, speed = 0.1, size = 45, color = (0, 0, 0)):
        paralax_x, paralax_y = oxygen.paralax_x, oxygen.paralax_y
        self.dialength = len(text_dict)
        character = text_dict[str(self.browse)]['Char']
        if character != 'hatlor':
            alt_character = character
        if self.key == None:
            self.key = jsondata.dialogues[character]['Dialogue_List'][0]
        if self.decision == False:
            self.scroll_ass.pose(screen, oxygen, 'be', (x - 100, y - 100), tick, 2)
            self.RnD(screen, input, text_dict[str(self.browse)]['Message'], x + 230 + paralax_x/2, y + 30 + paralax_y/2, x_len, time, tick, speed, size, color)
            self.face_ass_back_dict[character].pose(screen, oxygen, 'be', (x - 420, y - 150), tick, 2)
            self.face_ass_dict[character].pose(screen, oxygen, 'be', (x - 420, y - 150), tick, 5)
            if input.t1 and input.mouse.rect_over == None:
                if self.donewriting:
                    self.clear()
                    if self.browse < self.dialength - 1:
                        self.browse += 1
                    else:
                        if self.key in jsondata.dialogues[character]['Ask_Line']:
                            character = alt_character
                            self.decision = 'True'
                        else:
                            self.browse += 1
                        self.frame = 0
                else:
                    if self.line < len(self.linelist) - 1:
                        self.line += 1
                    else:
                        self.donewriting = True
                        self.line += 1
            if input.t2 and input.mouse.rect_over == None:
                self.clear()
                if self.browse > 0:
                    self.browse -= 1
        if self.decision == 'True':
            self.scroll_ass.pose(screen, oxygen, 'be', (x - 250, y - 100), tick, 2)
            self.render(jsondata.dialogues[character]['Ask_Line'][self.key], 0, 0, x_len + 100, 69, (69, 69, 69))
            self.RnD(screen, input, jsondata.dialogues[character]['Ask_Line'][self.key], x + 80 + paralax_x/2, y + 30 + paralax_y/2, x_len, time, tick, speed, size, color)
            if not self.frame == 0:
                if input.t1 and input.mouse.rect_over == None:
                    if self.line < len(self.linelist) - 1:
                        self.line += 1
                    else:
                        self.donewriting = True
                        self.line += 1
            self.frame = 1
            if self.bubble_pose == None:
                self.bubble_pose = 'idle'
            rect, mid_y = self.bubble.waiting(screen, oxygen, self.bubble_pose, (400, 400), tick, 2)
            if rect.collidepoint(input.mx, input.my): input.mouse.rect_list.append('bubble')
            if input.mouse.rect_over == 'bubble':
                if input.my > mid_y:
                    self.bubble_pose = 'down'
                    if input.t1:
                        self.decision = 'No'
                        self.frame = 0
                else:
                    self.bubble_pose = 'up'
                    if input.t1:
                        self.decision = 'Yes'
                        self.frame = 0
            else:
                self.bubble_pose = 'idle'
        if self.decision != 'True' and self.decision != False:
            self.scroll_ass.pose(screen, oxygen, 'be', (x - 100, y - 100), tick, 2)
            self.render(jsondata.dialogues[character][self.decision + '_Line'][self.key]['Line'], 0, 0, x_len + 100, 69, (69, 69, 69))
            try:
                jsondata.events[jsondata.dialogues[character][self.decision + '_Line'][self.key]['Result'][0]] = jsondata.dialogues[character][self.decision + '_Line'][self.key]['Result'][1]
                jsondata.save('events')
            except:
                pass
            self.RnD(screen, input, jsondata.dialogues[character][self.decision + '_Line'][self.key]['Line'], x + 230 + paralax_x/2, y + 30 + paralax_y/2, x_len, time, tick, speed, size, color)
            self.face_ass_back_dict[character].pose(screen, oxygen, 'be', (x - 420, y - 150), tick, 2)
            self.face_ass_dict[character].pose(screen, oxygen, 'be', (x - 420, y - 150), tick, 5)
            if input.t1 and input.mouse.rect_over == None:
                self.browse += 1
    def clear(self):
        self.linedict = None
    def RnD(self, screen, input, text, x, y, x_len, time, tick, speed, size, color):
        if self.linedict == None:
            self.render(text, x, y, x_len, size, color)
            self.timestart = time; self.timelist = []; self.line = 0; self.word = "arbitrary string :)"
            self.donewriting = False
        else:
            self.display(screen, input, x, y, time, tick, speed, size, color)
    def render(self, text, x, y, x_len, size, color):
        import pygame as paygay
        test_screen = paygay.Surface((1920, 1080))
        wordlist = []; word = ""
        for this in text:
            if this != " ":
                word += this
            else:
                word += " "
                wordlist.append(word); word = ""
        wordlist.append(word)
        linedict = {}; word = ""; line = 0 # note to self: the variable word is not a word, but the line of words being displayed
        for thing in wordlist:
            word += thing
            local_x = self.message_display(test_screen, word, x, y, size, color).right
            if (local_x - x) >= x_len:
                word = word[:-len(thing)] # this is madness
                linedict[word] = line
                line += 1; word = thing
        linedict[word] = line
        self.linedict = linedict # {"im mr worldwide": 0, "star thats so cool": 1}
        self.linelist = []
        for this in self.linedict:
            self.linelist.append(this)
    def display(self, screen, input, x, y, time, tick, speed, size, color):
        localtime = time - self.timestart
        if not int(int(localtime * 10)/speed) in self.timelist:
            self.timelist.append(int(int(localtime * 10)/speed))
            try:
                self.word = self.linelist[self.line]
                self.writing_line = self.word[: -(len(self.word) - len(self.timelist))]
            except:
                self.line += 1
                self.donewriting = True
            if len(self.word) == len(self.timelist) and len(self.linelist) > self.line:
                self.timelist = []; self.line += 1
        for this in self.linedict:
            if self.line > self.linedict[this]:
                self.message_display(screen, this, x, y + self.linedict[this] * size, size, color, tick)
        if not self.donewriting:
            self.message_display(screen, self.writing_line, x, y + self.line * size, size, color, tick)

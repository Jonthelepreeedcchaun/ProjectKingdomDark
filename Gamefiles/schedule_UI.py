def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(screen, text, xy_tuple, size = 30, color = (255, 255, 255)):
    import pygame as pg
    font = None
    largeText = pg.font.Font(font, size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.topleft = xy_tuple
    screen.blit(TextSurf, TextRect)
    dimension = largeText.render(text, True, color).get_rect()
    return(TextRect)

class terminal:
    def __init__(self, name, big_obj):
        self.big = big_obj
        self.block = self.big.block_dict[name]
        self.name = name
        self.barcolor = []; self.boxcolor = []
        for inte in self.block.color:
            self.barcolor.append(int(2*inte/3))
            self.boxcolor.append(int(inte/3))
        self.init = False
        self.grabbed = False
        self.type_event = False
    def be(self, screen, inpt, jsondata):
        import pygame as py
        if not hasattr(self, 'x'):
            self.x = inpt.mx + 50
            self.y = inpt.my
        if self.init:
            bar = py.draw.rect(screen, self.barcolor, (self.x, self.y - 20, 200, 20))
            if bar.collidepoint(inpt.mx, inpt.my):
                inpt.mouse.rect_list.append(self.name + '_tbar')
            box = py.draw.rect(screen, self.boxcolor, (self.x, self.y, 200, 180))
            if box.collidepoint(inpt.mx, inpt.my):
                inpt.mouse.rect_list.append(self.name + '_tbox')
            if inpt.t1 or inpt.t2:
                if not inpt.mouse.rect_over == self.name + '_tbar' and not inpt.mouse.rect_over == self.name + '_tbox':
                    self.big.terminal_del = self.name
            message_display(screen, self.name, (self.x, self.y - 20), 30)
            if 'chance' in self.block.info:
                text_lag = 20
                type_rect = message_display(screen, 'Type: Random', (self.x, self.y), 30)
                chance_rect = message_display(screen, 'Chance: ' + str(len(self.block.info['chance'])) + '0%', (self.x, self.y + 20), 30)
                if chance_rect.collidepoint(inpt.mx, inpt.my) and inpt.t1:
                    if len(self.block.info['chance']) < 9:
                        self.block.info['chance'].append(len(self.block.info['chance']))
                    else:
                        self.block.info['chance'] = [0]
                    self.block.block_event = 'chancechange'
            else:
                text_lag = 0
                type_rect = message_display(screen, 'Type: Scheduled', (self.x, self.y), 30)
            if type_rect.collidepoint(inpt.mx, inpt.my) and inpt.t1:
                if 'chance' in self.block.info:
                    del self.block.info['chance']
                else:
                    self.block.info['chance'] = [0, 1, 2, 3]
                self.block.block_event = 'typechange'
            if inpt.t1 and inpt.mouse.rect_over == self.name + '_tbar':
                self.grabbed = True
                self.snap_x, self.snap_y = inpt.mx - self.x, inpt.my - self.y
            if self.grabbed:
                self.x, self.y = inpt.mx - self.snap_x, inpt.my - self.snap_y
                if not inpt.m1:
                    self.grabbed = False
            if 'event' in self.block.info:
                event_list = self.block.info['event']
                text_lag += 20
                message_display(screen, 'Req Events:', (self.x, self.y + text_lag), 30)
            else:
                event_list = []
            if not 'Add Req Event +' in event_list:
                event_list.append('Add Req Event +')
            event_rect_list = []; rect_def = {}; count = 0
            for string in event_list:
                count += 1
                rect = message_display(screen, string, (self.x, self.y + text_lag + (count*20)), 30)
                if string == 'Add Req Event +':
                    add_event = rect
                else:
                    event_rect_list.append(rect)
                    rect_def.update({str(rect): string})
            if add_event.collidepoint(inpt.mx, inpt.my) and inpt.t1:
                self.type_event = True
                self.event_string = ''
            if 'event' in self.block.info and 'Add Req Event +' in self.block.info['event']:
                self.block.info['event'].remove('Add Req Event +')
            for rect in event_rect_list:
                if rect.collidepoint(inpt.mx, inpt.my) and inpt.t1:
                    event = rect_def[str(rect)]
                    if self.name in jsondata.dialogue_event and event in jsondata.dialogue_event[self.name]:
                        jsondata.dialogue_event[self.name].remove(event)
                        if event in self.block.info['event']:
                            self.block.info['event'].remove(event)
                        if len(jsondata.dialogue_event[self.name]) == 0:
                            del self.block.info['event']
                            del jsondata.dialogue_event[self.name]
                        jsondata.save('dialogue_event')
            if self.type_event:
                if not inpt.char == None:
                    if inpt.char == 'enter':
                        if not 'event' in self.block.info:
                            self.block.info['event'] = []
                        self.block.info['event'].append(self.event_string)
                        if not self.name in jsondata.dialogue_event:
                            jsondata.dialogue_event[self.name] = []
                        jsondata.dialogue_event[self.name].append(self.event_string)
                        jsondata.save('dialogue_event')
                        self.type_event = False
                    else:
                        char = inpt.char
                        if inpt.char == 'space':
                            char = ' '
                        if inpt.char == 'backspace':
                            char = ''
                            self.event_string = self.event_string[:-1]
                        if inpt.char == 'F11':
                            char = ''
                        self.event_string += char.translate({ord(i): '' for i in "<>:\"/\\|?*"})
                message_display(screen, self.event_string, (self.x, self.y + (count*20) + text_lag + 20), 30)
        if self.init == False:
            self.init = True

class schedule_block:
    def __init__(self, name, big_obj, jsondata):
        from random import randint as rhombus
        info_dict = big_obj.block_init_dict[name]
        color_list = [rhombus(0, 42), rhombus(42, 84), rhombus(84, 126)]; pick = rhombus(0, 2)
        self.color = (color_list[rhombus(0, 2)], color_list[2 - pick], color_list[pick])
        self.name = name; self.info = info_dict
        self.big = big_obj
        if 'day' in info_dict:
            if 'chance' in info_dict:
                self.x = (len(jsondata.schedule[str(info_dict['day'])]) + big_obj.r_dict_list[info_dict['day']].index(self.name) + 1)*100
                self.y = 100*int(info_dict['day'])
            else:
                self.x = (jsondata.schedule[info_dict['day']].index(self.name) + 1)*100
                self.y = 100*int(info_dict['day'])
        else:
            self.x, self.y = rhombus(100, 820), 0
        if not 'day' in self.info and self.y > 0:
            self.info['day'] = int(self.y/100)
        self.grabbed = False
        self.block_event = None
    def display(self, screen, inpt):
        if inpt.mouse.rect_over == self.name or self.grabbed == True:
            message_display(screen, self.name, (inpt.mx + 50, inpt.my))
            message_display(screen, self.info['char'], (inpt.mx + 50, inpt.my + 30))
    def be(self, screen, inpt, jsondata):
        import pygame as py
        rect = py.draw.rect(screen, self.color, (self.x, self.y + self.big.y_scroll, 100, 100))
        if self.block_event == None:
            if 'chance' in self.info:
                message_display(screen, 'R', (self.x + 10, self.y + 5 + self.big.y_scroll), 60)
            if 'event' in self.info:
                message_display(screen, 'E', (self.x + 60, self.y + 5 + self.big.y_scroll), 60)
            if not self.grabbed:
                if rect.collidepoint(inpt.mx, inpt.my): inpt.mouse.rect_list.append(self.name)
                if inpt.mouse.rect_over == self.name and inpt.t1:
                    if self.y >= 100:
                        if 'chance' in self.info:
                            del jsondata.schedule_r[self.name]
                            jsondata.save('schedule_r')
                        else:
                            day = int(self.y / 100); pos = int((self.x / 100) - 1)
                            jsondata.schedule[str(day)].pop(pos)
                            jsondata.save('schedule')
                    day = int(self.y / 100)
                    if day:
                        inpt.schedule_arrange = {'day': day, 'obj': self.name, 'event': 'grabbed'}
                    self.grabbed = True
                    self.snap_x, self.snap_y = inpt.mx - self.x, inpt.my - (self.y + self.big.y_scroll)
                if inpt.mouse.rect_over == self.name and inpt.t2 and self.y >= 100:
                    self.big.terminal_list.append(self.name)
            else:
                self.x, self.y = inpt.mx - self.snap_x, inpt.my - self.snap_y - self.big.y_scroll
                if not inpt.m1:
                    if self.x % 100:
                        self.x /= 100
                        self.x = 100*round(self.x)
                        if self.x < 0:
                            self.x += 200
                    if self.x == 0:
                        self.x += 100
                    if self.y % 100:
                        self.y /= 100
                        self.y = 100*round(self.y)
                        if self.y < 0:
                            self.y += 100
                    day = int(self.y / 100)
                    self.info['day'] = day
                    if day:
                        inpt.schedule_arrange = {'day': day, 'obj': self.name, 'event': 'dropped'}
                    self.grabbed = False
        elif self.block_event == 'typechange':
            other_block_list = []; block = self.big.block_dict[self.name]
            for block_name in self.big.block_dict:
                other_block = self.big.block_dict[block_name]
                if not block == other_block:
                    other_block_list.append(other_block)
            if 'chance' in self.info:
                jsondata.schedule[str(self.info['day'])].remove(self.name)
                jsondata.schedule_r[self.name] = [self.info['chance'], int(self.info['day'])]
                displacement = 0
                for other_block in other_block_list:
                    if not 'chance' in other_block.info and other_block.y == block.y and other_block.x > block.x:
                        displacement += 1
                        other_block.x -= 100
                block.x += 100 * displacement
            else:
                del jsondata.schedule_r[self.name]
                jsondata.schedule[str(self.info['day'])].append(self.name)
                displacement = 0
                for other_block in other_block_list:
                    if other_block.y == block.y and other_block.x < block.x and 'chance' in other_block.info:
                        displacement += 1
                        other_block.x += 100
                block.x -= 100 * displacement
            for jsonfile in ['schedule', 'schedule_r']:
                jsondata.save(jsonfile)
            self.block_event = None
        elif self.block_event == 'chancechange':
            jsondata.schedule_r[self.name][0] = self.info['chance']
            jsondata.save('schedule_r')
            self.block_event = None

class schedule_UI_obj:
    def __init__(self, jsondata):
        self.block_init_dict = {}; self.r_dict_list = {}; self.terminal_list = []; self.terminal_del = None; self.terminal_dict = {}; day_list = []
        self.y_scroll = 0
        for char in jsondata.dialogues:
            for dial in jsondata.dialogues[char]['Dialogues']:
                self.block_init_dict.update({dial: {'char': char}})
                if dial in jsondata.dialogue_event:
                    self.block_init_dict[dial].update({'event': jsondata.dialogue_event[dial]})
        for day in jsondata.schedule:
            for dial in jsondata.schedule[day]:
                self.block_init_dict[dial].update({'day': day})
                day_list.append(str(day))
        for dial in jsondata.schedule_r:
            day = jsondata.schedule_r[dial][1]
            day_list.append(str(day))
            if not day in self.r_dict_list:
                self.r_dict_list.update({day: []})
            self.r_dict_list[day].append(dial)
            self.block_init_dict[dial].update({'day': day, 'chance': jsondata.schedule_r[dial][0]})
        self.block_dict = {}
        self.block_dict.update({dial: schedule_block(dial, self, jsondata) for dial in self.block_init_dict})
        del_list = []
        for day in jsondata.schedule:
            if not day in day_list:
                del_list.append(day)
        for day in del_list:
            del jsondata.schedule[day]
        jsondata.save('schedule')
    def marginlabels(self, screen, jsondata):
        list = ['X']
        for day in jsondata.schedule:
            list.append(str(day))
        list.append(str(len(list)))
        for this in list:
            message_display(screen, this, (10, 100*list.index(this) + self.y_scroll), 180 - len(str(this))*60)
    def go(self, screen, inpt, jsondata):
        self.test_var = 'Yes'
        self.marginlabels(screen, jsondata)
        if not hasattr(inpt, 'schedule_arrange'):
            inpt.schedule_arrange = False
        if inpt.my < 980 and self.y_scroll <= 0:
            self.y_scroll += 2
        if inpt.my > 100:
            self.y_scroll -= 2
        if self.y_scroll >  0:
            self.y_scroll = 0
        block_render_order = []
        for block in self.block_dict:
            if not self.block_dict[block].grabbed:
                block_render_order.append(self.block_dict[block])
        for block in self.block_dict:
            if self.block_dict[block].grabbed:
                block_render_order.append(self.block_dict[block])
        for block in block_render_order:
            block.be(screen, inpt, jsondata)
        for block in self.block_dict:
            self.block_dict[block].display(screen, inpt)
        for block_name in self.terminal_list:
            if not block_name in self.terminal_dict:
                self.terminal_dict.update({block_name: terminal(block_name, self)})
        for title in self.terminal_dict:
            self.terminal_dict[title].be(screen, inpt, jsondata)
        if not self.terminal_del == None:
            self.terminal_list.remove(self.terminal_del)
            del self.terminal_dict[self.terminal_del]
            self.terminal_del = None
        if inpt.schedule_arrange:
            day = inpt.schedule_arrange['day']
            block = self.block_dict[inpt.schedule_arrange['obj']]
            event = inpt.schedule_arrange['event']
            if event == 'grabbed':
                for block_name in self.block_dict:
                    other_block = self.block_dict[block_name]
                    if 'day' in other_block.info and int(other_block.info['day']) == int(day) and other_block.x > block.x:
                        other_block.x -= 100
            elif event == 'dropped':
                block_x_list = []; blocks_disturbed = False
                if 'chance' in block.info:
                    for block_name in self.block_dict:
                        other_block = self.block_dict[block_name]
                        if 'day' in other_block.info and int(other_block.info['day']) == int(day) and not block == other_block:
                            block_x_list.append(other_block.x)
                    block.x = (len(block_x_list) * 100) + 100
                else:
                    for block_name in self.block_dict:
                        other_block = self.block_dict[block_name]
                        if 'day' in other_block.info and int(other_block.info['day']) == int(day) and not block == other_block:
                            block_x_list.append(other_block.x)
                            if other_block.x >= block.x:
                                blocks_disturbed = True
                                other_block.x += 100
                if not blocks_disturbed:
                    x_sup = 0
                    for x_val in block_x_list:
                        if x_val > x_sup:
                            x_sup = x_val
                    block.x = x_sup + 100
                chance_block_left_list = []
                if not 'chance' in block.info:
                    for block_name in self.block_dict:
                        other_block = self.block_dict[block_name]
                        if 'day' in other_block.info and int(other_block.info['day']) == int(day) and not block == other_block and 'chance' in other_block.info and other_block.x < block.x:
                            chance_block_left_list.append(other_block)
                    block.x -= len(chance_block_left_list) * 100
                    for other_block in chance_block_left_list:
                        other_block.x += 100
                for block_name in self.block_dict:
                    block = self.block_dict[block_name] # block is overwritten here
                    if 'chance' in block.info:
                        jsondata.schedule_r[block.name] = [block.info['chance'], int(block.info['day'])]
                        jsondata.save('schedule_r')
                    elif 'day' in block.info and int(block.info['day']): # ensures that only nonzero days are used here
                        if not str(block.info['day']) in jsondata.schedule:
                            jsondata.schedule.update({str(block.info['day']): []})
                        day_sche = jsondata.schedule[str(block.info['day'])] # day_sche (schedule) is a list
                        list_pos = int((block.x/100) - 1)
                        try_madness_boolean = False
                        while not try_madness_boolean:
                            try:
                                jsondata.schedule[str(block.info['day'])][list_pos] = block.name
                                try_madness_boolean = True
                            except:
                                jsondata.schedule[str(block.info['day'])].append(None)
                        jsondata.save('schedule')
            inpt.schedule_arrange = False

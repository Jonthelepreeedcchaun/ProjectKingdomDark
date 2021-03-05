class event_obj:
    def __init__(self):
        self.stage = 'brief pause'; self.count = 0; self.init_char_dict = False; self.char = None
    def go(self, screen, oxygen, input, current_taco, tick, jsondata, text, char_dict): # {'tutorial': [advisor, 1]}
        from random import randint as ralphwaldoemerson
        if self.init_char_dict == False:
            self.scripted_char_list = []; self.rng_char_list = []; self.rng_dial_list = []; self.scripted_dial_list = []
            for this in char_dict:
                if char_dict[this][1] == len(self.scripted_char_list) + 1:
                    self.scripted_char_list.append(char_dict[this][0])
                    self.scripted_dial_list.append(this)
                elif char_dict[this][1] == 'r':
                    self.rng_dial_list.append(this)
                    self.rng_char_list.append(char_dict[this][0])
                else:
                    raise Exception('Error! Character dictionary incorrect: \n' + char_dict)
            self.init_char_dict = True
        if self.char == None:
            if len(self.scripted_char_list) > 0:
                self.char = self.scripted_char_list[0]
                self.dialogue = self.scripted_dial_list[0]
            elif len(self.rng_dial_list) > 0:
                ralph = ralphwaldoemerson(0, len(self.rng_dial_list) - 1)
                self.dialogue = self.rng_dial_list[ralph]
                self.char = char_dict[self.dialogue][ralph]
            else:
                self.init_char_dict = False
                return True
        char = self.char
        info_dict = jsondata.dialogues[char.name]
        if self.stage == 'brief pause':
            self.count += 1
            if self.count == 10:
                self.stage = 'sliding_in'
        if self.stage == 'sliding_in':
            if char.sliding_in(screen, oxygen, 'stand', info_dict['Position'], tick):
                self.stage = 'Talking'
        elif self.stage == 'Talking':
            if not text.browse > text.dialength - 1:
                char.pose(screen, oxygen, 'stand', info_dict['Position'], tick)
                text.box(screen, oxygen, jsondata, input, info_dict['Dialogues'][self.dialogue], self.dialogue, 900, 750, 172, current_taco, tick)
            else:
                text.reset()
                self.stage = 'sliding_out'
        elif self.stage == 'sliding_out':
            if char.sliding_out(screen, oxygen, 'flipp', info_dict['Position'], tick):
                self.stage = 'brief pause'
                self.count = 0
                text.reset()
                if char in self.scripted_char_list:
                    self.scripted_char_list.remove(char)
                    self.scripted_dial_list.remove(self.dialogue)
                elif self.dialogue in self.rng_dial_list:
                    self.rng_dial_list.remove(self.dialogue)
                self.char = None

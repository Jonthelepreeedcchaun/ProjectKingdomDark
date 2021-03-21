class character_event_obj:
    def __init__(self):
        pass
    def render(self, char_list, jsondata):
        from random import randint as randal
        self.dict = {}; int = 1
        dialogue_list = jsondata.schedule[str(jsondata.day)]
        for dial in dialogue_list:
            for char in char_list:
                if dial in jsondata.dialogues[char.name]["Dialogues"]:
                    if not dial in jsondata.dialogue_event:
                        self.dict.update({dial: [char, int]})
                        int += 1
                    else:
                        for event in jsondata.dialogue_event[dial]:
                            if jsondata.events[event]:
                                self.dict.update({dial: [char, int]})
                                int += 1
                            else:
                                jsondata.schedule[str(jsondata.day)].remove(dial)
                                int = 1
                                if not str(jsondata.day + 4) in jsondata.schedule:
                                    while not str(jsondata.day + 4) in jsondata.schedule:
                                        if not str(jsondata.day + int) in jsondata.schedule:
                                            jsondata.schedule.update({str(jsondata.day + int): []})
                                        int += 1
                                jsondata.schedule[str(jsondata.day + 4)].append(dial)
                                jsondata.save('schedule')
        for dial in jsondata.schedule_r:
            if jsondata.day >= jsondata.schedule_r[dial][1] and randal(0, 9) in jsondata.schedule_r[dial][0]:
                for char in char_list:
                    if dial in jsondata.dialogues[char.name]["Dialogues"]:
                        if not dial in jsondata.dialogue_event:
                            self.dict.update({dial: [char, 'r']})
                        else:
                            for event in jsondata.dialogue_event[dial]:
                                if jsondata.events[event]:
                                    self.dict.update({dial: [char, 'r']})
                                else:
                                    day = jsondata.schedule_r[dial][1]; day += 4
                                    jsondata.schedule_r[dial][1] = day
                                    jsondata.save('schedule_r')

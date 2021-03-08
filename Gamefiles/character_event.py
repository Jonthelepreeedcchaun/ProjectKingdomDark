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
                    self.dict.update({dial: [char, int]})
                    int += 1
        for dial in jsondata.schedule_r:
            if jsondata.day >= jsondata.schedule_r[dial][1] and randal(0, 9) in jsondata.schedule_r[dial][0]:
                for char in char_list:
                    if dial in jsondata.dialogues[char.name]["Dialogues"]:
                        self.dict.update({dial: [char, 'r']})

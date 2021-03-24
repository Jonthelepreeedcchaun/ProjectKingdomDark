from cursesmenu import *
from cursesmenu.items import *

def clear():
    import os
    if os.name == 'nt': _ = os.system('cls')
    else: _ = os.system('clear')

def makemenu(list, title='Please Select One'):
    list.append('Exit')
    menu = SelectionMenu(list, title=title, show_exit_option=False)
    return list[menu.get_selection(list, title=title, exit_option=False)]

def check_dict(jsondata, character):
    dict = jsondata.dialogues[character]
    checkdict = {"Immutable_Dialogue_List": [], "Dialogue_List": [], "Position": [1500, 650], "Dialogues": {}, "Ask_Line": {}, "Yes_Line": {}, "No_Line": {}}
    if not dict.keys() == checkdict.keys():
        print("The dialogues dictionary for " + character + " is incomplete:")
        print("    Current keys - " + str(dict.keys())[11:len(str(dict.keys()))  - 1])
        print("    Correct keys - " + str(checkdict.keys())[11:len(str(checkdict.keys())) - 1])
        answer = input('Would you like the current keys overwritten with the correct keys? (y/n) \n')
        if answer == 'y':
            empty = []
            for this in dict.keys():
                if not this in checkdict.keys():
                    empty.append(this)
            for this in empty:
                del dict[this]
            for this in checkdict.keys():
                if not this in dict.keys():
                    dict.update({this: checkdict[this]})
            jsondata.dialogues[character] = dict; jsondata.save('dialogues')
            input('\nDictionary overwritten successfully. (Enter)')
            clear()
        elif answer == 'n':
            raise Exception('\nTo fix the dictionary without overwriting, go to Storage/dialogues.json and find the key/value pair.')
        else:
            write_mode(jsondata)

def position_access(jsondata, character):
    clear()
    value = jsondata.dialogues[character]['Position']
    print('The x-position is ' + str(value[0]))
    print('The y-position is ' + str(value[1]))
    answer = input('To change one of these values, specify which. (x/y)\n')
    if answer == 'x': number = 0
    elif answer == 'y': number = 1
    else:
        access_character_attributes(jsondata, character)
    jsondata.dialogues[character]['Position'][number] = int(input('Enter the new value.\n'))
    jsondata.save('dialogues')
    clear()
    input('Value saved successfully. Returning to access menu. (Enter)')
    access_character_attributes(jsondata, character)

def add_question(jsondata, character, dialogue, scroll):
    jsondata.dialogues[character]['Yes_Line'][dialogue] = {'Line': 'NoneType'}
    jsondata.dialogues[character]['No_Line'][dialogue] = {'Line': 'NoneType'}
    clear()
    print('Type the question that ' + character + ' asks at the end of the dialogue "' + dialogue + '".')
    print('Ex: Do you accept, Lord Hatlor?\n')
    answer = input()
    jsondata.dialogues[character]['Ask_Line'][dialogue] = answer
    clear()
    print('What does ' + character + ' say if the player accepts?')
    print('Ex: Thank you, my Lord.\n')
    answer = input()
    jsondata.dialogues[character]['Yes_Line'][dialogue]["Line"] = answer
    clear()
    answer = input('Does saying yes cause an event? (y/n)\n')
    if answer == 'y':
        answer = input('What event?\n')
        if not answer in jsondata.events:
            jsondata.events.update({answer: 0})
            jsondata.save('events')
        jsondata.dialogues[character]['Yes_Line'][dialogue].update({'Result': [answer, 1]})
        jsondata.save('dialogues')
    answer = input('Does saying yes change any stats? (y/n)\nStats are Gold, Morale, and Subjects.\n')
    if answer == 'y':
        stat_leave = False
        while not stat_leave:
            clear()
            answer = makemenu(['gold', 'morale', 'subjects'], 'Which stat do you want to change?')
            clear()
            if answer in ['gold', 'morale', 'subjects']:
                stat = answer
                print('How much does this stat change by?')
                answer = input('Enter a negative number if the effect is negative. \n')
                amount = int(answer)
                jsondata.dialogues[character]['Yes_Line'][dialogue].update({'stats': [stat, amount]})
                jsondata.save('dialogues')
            clear()
            answer = input('Are you done changing the stats? (y/n) \n')
            if answer == 'y':
                stat_leave = True
    clear()
    print('What does ' + character + ' say if the player does not accept?')
    print('Ex: I understand, my Lord.\n')
    answer = input()
    jsondata.dialogues[character]['No_Line'][dialogue]["Line"] = answer
    clear()
    answer = input('Does saying no cause an event? (y/n)\n')
    if answer == 'y':
        answer = input('What event?\n')
        if not answer in jsondata.events:
            jsondata.events.update({answer: 0})
            jsondata.save('events')
        jsondata.dialogues[character]['No_Line'][dialogue].update({'Result': [answer, 1]})
        jsondata.save('dialogues')
    answer = input('Does saying no change any stats? (y/n)\nStats are Gold, Morale, and Subjects.\n')
    if answer == 'y':
        stat_leave = False
        while not stat_leave:
            clear()
            answer = makemenu(['gold', 'morale', 'subjects'], 'Which stat do you want to change?')
            clear()
            if answer in ['gold', 'morale', 'subjects']:
                stat = answer
                print('How much does this stat change by?')
                answer = input('Enter a negative number if the effect is negative. \n')
                amount = int(answer)
                if not 'stats' in jsondata.dialogues[character]['No_Line'][dialogue]:
                    jsondata.dialogues[character]['No_Line'][dialogue].update({'stats': {stat: amount}})
                else:
                    jsondata.dialogues[character]['No_Line'][dialogue]['stats'].update({stat: amount})
                jsondata.save('dialogues')
            clear()
            answer = input('Are you done changing the stats? (y/n) \n')
            if answer == 'y':
                stat_leave = True
    clear()
    jsondata.save('dialogues')
    input('Question and responses saved. Returning to dialogue writing menu. (Enter)')
    write_dialogue(jsondata, character, dialogue, scroll)

def write_dialogue(jsondata, character, dialogue, scroll):
    clear()
    dialogue_dict = jsondata.dialogues[character]['Dialogues'][dialogue]
    print(dialogue_dict[str(scroll)]['Char'] + ': ' + dialogue_dict[str(scroll)]['Message'])
    print('Dialogue piece (' + str(scroll + 1) + '/' + str(len(dialogue_dict)) + ')')
    answer = input()
    try:
        answer = int(answer)
        clear()
        if answer > 0 and answer <= len(dialogue_dict): scroll = answer - 1
        write_dialogue(jsondata, character, dialogue, scroll)
    except:
        if answer == 'next':
            clear()
            if scroll < len(dialogue_dict) - 1: scroll += 1
            write_dialogue(jsondata, character, dialogue, scroll)
        elif answer == 'prev':
            clear()
            if scroll > 0: scroll -= 1
            write_dialogue(jsondata, character, dialogue, scroll)
        elif answer == 'edit':
            clear()
            print('Type "hatlor/' + character + ': dialogue", as seen below.')
            print(dialogue_dict[str(scroll)]['Char'] + ': ' + dialogue_dict[str(scroll)]['Message'])
            print('Dialogue piece (' + str(scroll + 1) + '/' + str(len(dialogue_dict)) + ')\n')
            speaker, new_dialogue = input('').split(': ')
            jsondata.dialogues[character]['Dialogues'][dialogue][str(scroll)]['Char'] = speaker
            jsondata.dialogues[character]['Dialogues'][dialogue][str(scroll)]['Message'] = new_dialogue
            jsondata.save('dialogues')
            clear()
            input('Dialogue saved successfully. Returning to edit menu. (Enter)')
            write_dialogue(jsondata, character, dialogue, scroll)
        elif answer == 'add_next':
            piece = str(dialogue_dict[str(scroll)]['Char']) + ': ' + str(dialogue_dict[str(scroll)]['Message'])
            scroll += 1; splint_dict = {}
            if scroll in dialogue_dict:
                for this in dialogue_dict:
                    if int(this) >= scroll:
                        splint_dict[str(int(this) + 1)] = dialogue_dict[this]
                        if int(this) == scroll:
                            dialogue_dict[this] = {'Char': 'hatlor', 'Message': 'This dialogue (' + dialogue + ') is incomplete.'}
                for this in splint_dict:
                    dialogue_dict[this] = splint_dict[this]
            else:
                dialogue_dict[str(scroll)] = {'Char': 'hatlor', 'Message': 'This dialogue (' + dialogue + ') is incomplete.'}
            clear()
            print('Type "hatlor/' + character + ': dialogue", as seen below.')
            print(piece)
            print('Dialogue piece (' + str(scroll + 1) + '/' + str(len(dialogue_dict)) + ')\n')
            speaker, new_dialogue = input('').split(': ')
            jsondata.dialogues[character]['Dialogues'][dialogue] = dialogue_dict
            jsondata.dialogues[character]['Dialogues'][dialogue][str(scroll)]['Char'] = speaker
            jsondata.dialogues[character]['Dialogues'][dialogue][str(scroll)]['Message'] = new_dialogue
            jsondata.save('dialogues')
            clear()
            input('Dialogue saved successfully. Returning to edit menu. (Enter)')
            write_dialogue(jsondata, character, dialogue, scroll)
        elif answer == 'add_prev':
            piece = str(dialogue_dict[str(scroll)]['Char']) + ': ' + str(dialogue_dict[str(scroll)]['Message'])
            splint_dict = {}
            for this in dialogue_dict:
                if int(this) >= scroll:
                    splint_dict[str(int(this) + 1)] = dialogue_dict[this]
                    if int(this) == scroll:
                        dialogue_dict[this] = {'Char': 'hatlor', 'Message': 'This dialogue (' + dialogue + ') is incomplete.'}
            for this in splint_dict:
                dialogue_dict[this] = splint_dict[this]
            clear()
            print('Type "hatlor/' + character + ': dialogue", as seen below.')
            print(piece)
            print('Dialogue piece (' + str(scroll + 1) + '/' + str(len(dialogue_dict)) + ')\n')
            speaker, new_dialogue = input('').split(': ')
            jsondata.dialogues[character]['Dialogues'][dialogue] = dialogue_dict
            jsondata.dialogues[character]['Dialogues'][dialogue][str(scroll)]['Char'] = speaker
            jsondata.dialogues[character]['Dialogues'][dialogue][str(scroll)]['Message'] = new_dialogue
            jsondata.save('dialogues')
            clear()
            input('Dialogue saved successfully. Returning to edit menu. (Enter)')
            write_dialogue(jsondata, character, dialogue, scroll)
        elif answer == 'del':
            clear()
            if not scroll == 0:
                answer = input('Are you certain you want to delete this piece of dialogue? (y/n)\n')
                clear()
                if answer == 'y':
                    del dialogue_dict[str(scroll)]
                    shift_dict = {}
                    for this in dialogue_dict:
                        if int(this) > scroll:
                            shift_dict.update({this: dialogue_dict[this]})
                    for this in shift_dict:
                        dialogue_dict.update({str(int(this) - 1): shift_dict[this]})
                        del dialogue_dict[this]
                    jsondata.dialogues[character]['Dialogues'][dialogue] = dialogue_dict
                    jsondata.save('dialogues')
                    print('Dialogue piece deleted successfully.')
                else:
                    pass
                print('Returning to dialogue edit menu.')
                input('(Enter)\n')
                write_dialogue(jsondata, character, dialogue, scroll - 1)
            else:
                print('You cannot delete the first piece of dialogue.')
                print('To replace this piece of dialogue, use edit.')
                print('Returning to dialogue edit menu.')
                input('(Enter)\n')
                write_dialogue(jsondata, character, dialogue, scroll)
        elif answer == 'add_q':
            if dialogue in jsondata.dialogues[character]['Ask_Line']:
                clear()
                print('There is already a question for this dialogue:')
                print('Question - ' + jsondata.dialogues[character]['Ask_Line'][dialogue])
                print('Yes_Line - ' + jsondata.dialogues[character]['Yes_Line'][dialogue]["Line"])
                print('No_Line - ' + jsondata.dialogues[character]['No_Line'][dialogue]["Line"])
                answer = input('Do you want to overwrite this question? (y/n)\n')
                if answer == 'y':
                    add_question(jsondata, character, dialogue, scroll)
                else:
                    write_dialogue(jsondata, character, dialogue, scroll)
            else:
                add_question(jsondata, character, dialogue, scroll)
        elif answer == 'del_q':
            if dialogue in jsondata.dialogues[character]['Ask_Line']:
                clear()
                print('This dialogue question is as follows:')
                print('Question - ' + jsondata.dialogues[character]['Ask_Line'][dialogue])
                print('Yes_Line - ' + jsondata.dialogues[character]['Yes_Line'][dialogue]["Line"])
                print('No_Line - ' + jsondata.dialogues[character]['No_Line'][dialogue]["Line"])
                answer = input('Are you sure you want to delete this question? (y/n)\n')
                if answer == 'y':
                    del jsondata.dialogues[character]['Ask_Line'][dialogue]
                    del jsondata.dialogues[character]['Yes_Line'][dialogue]
                    del jsondata.dialogues[character]['No_Line'][dialogue]
                    jsondata.save('dialogues')
                    clear()
                    input('Question deleted from dialogue. (Space)')
                    write_dialogue(jsondata, character, dialogue, scroll)
                else:
                    write_dialogue(jsondata, character, dialogue, scroll)
            else:
                clear()
                print('Question does not exist for dialogue ' + dialogue + '.')
                input('Returning to write menu. (Space)')
                write_dialogue(jsondata, character, dialogue, scroll)
        else:
            write_dialogue_instruction(jsondata, character, dialogue, scroll)

def write_dialogue_instruction(jsondata, character, dialogue, scroll = 0):
    clear()
    print('Instruction: ')
    print('Type next to advance to the next piece of dialogue.')
    print('Type prev to go backwards.')
    print('You can also type a number to reach that number in the dialogue.')
    print('Type edit to edit the current piece of dialogue.')
    print('To create a new piece of dialogue ahead of the current, type add_next.')
    print('To create one before, type add_prev.')
    print('To add or edit a question to the end of the dialogue, type add_q.')
    print('To remove a question from a dialogue, type del_q.')
    answer = input('(Enter)\n')
    if answer != 'back':
        write_dialogue(jsondata, character, dialogue, scroll)
    else:
        edit(jsondata, character)

def edit(jsondata, character):
    clear()
    save_list = jsondata.dialogues[character]['Dialogue_List']
    immu_list = jsondata.dialogues[character]['Immutable_Dialogue_List']
    if len(immu_list) > 0:
        print('The dialogues for ' + character + ' are:')
        for this in immu_list:
            print('\n    ' + this)
        answer = input('\nType the dialogue you want to edit.\n')
        if answer in immu_list:
            write_dialogue_instruction(jsondata, character, answer)
        else:
            dialogue_access(jsondata, character)
    else:
        input(character + 'has no dialogues; press (Enter) to go and create one.\n')
        create(jsondata, character)

def create(jsondata, character):
    clear()
    save_list = jsondata.dialogues[character]['Dialogue_List']
    immu_list = jsondata.dialogues[character]['Immutable_Dialogue_List']
    if len(immu_list) > 0:
        print('The dialogues for ' + character + ' are:')
        for this in immu_list:
            print('\n    ' + this)
    else:
        print('There are currently no dialogues for ' + character + '.')
    answer = input('\nType the name of the dialogue you want to create.\n')
    if answer == 'back':
        access_character_attributes(jsondata, character)
    elif not answer in immu_list:
        jsondata.dialogues[character]['Dialogue_List'].append(answer)
        jsondata.dialogues[character]['Immutable_Dialogue_List'].append(answer)
        jsondata.dialogues[character]['Dialogues'].update({answer: {"0": {"Char": "hatlor", "Message": "This message in " + answer + " is to be overwritten."}}})
        jsondata.save('dialogues')
        clear()
        print('New dialogue entered in the dictionary for ' + character + '.')
        input('Press (Enter) to go on and edit it.\n')
        write_dialogue_instruction(jsondata, character, answer)
    else:
        print('This dialogue already exists.')
        input('Press (Enter) to go back to the dialogue creation screen.\n')
        create(jsondata, character)

def delete(jsondata, character):
    clear()
    save_list = jsondata.dialogues[character]['Dialogue_List']
    immu_list = jsondata.dialogues[character]['Immutable_Dialogue_List']
    if len(immu_list) > 1:
        print('The dialogues for ' + character + ' are:')
        for this in immu_list:
            print('\n    ' + this)
        print('\nWhich one would you like to delete?')
        answer = input('')
        if answer in immu_list:
            clear()
            dialogue = answer
            answer = input('Are you ABSOLUTELY sure you want to delete this? (y/n)\n')
            if answer == 'y':
                jsondata.dialogues[character]['Dialogue_List'].remove(dialogue)
                jsondata.dialogues[character]['Immutable_Dialogue_List'].remove(dialogue)
                del jsondata.dialogues[character]['Dialogues'][dialogue]
                if dialogue in jsondata.dialogues[character]['Ask_Line']:
                    del jsondata.dialogues[character]['Ask_Line'][dialogue]
                    del jsondata.dialogues[character]['Yes_Line'][dialogue]
                    del jsondata.dialogues[character]['No_Line'][dialogue]
                jsondata.save('dialogues')
                for day in jsondata.schedule:
                    for dial in jsondata.schedule[day]:
                        if dial == dialogue:
                            jsondata.schedule[day].remove(dialogue)
                jsondata.save('schedule')
                if dialogue in jsondata.schedule_r:
                    del jsondata.schedule_r[dialogue]
                jsondata.save('schedule_r')
                dialogue_access(jsondata, character)
            else:
                dialogue_access(jsondata, character)
        else:
            dialogue_access(jsondata, character)
    else:
        print('There are currently no dialogues for ' + character)
        input('Press (Enter) to go back to the dialogue access screen.\n')
        dialogue_access(jsondata, character)

def dialogue_access(jsondata, character):
    clear()
    answer = input('Type an action. (edit/create/delete)\n')
    if answer in ['edit', 'create', 'delete']:
        exec(answer + '(jsondata, character)')
    else:
        access_character_attributes(jsondata, character)

def access_character_attributes(jsondata, character):
    clear()
    dict = jsondata.dialogues[character]
    check_dict(jsondata, character)
    print('Type one of the following access keys:')
    for this in ['position', 'dialogue']:
        print('\n    ' + this.lower())
    answer = input('\n')
    if answer in ['position', 'dialogue']:
        exec(answer + '_access(jsondata, character)')
    else:
        write_mode(jsondata)

def write_mode(jsondata):
    clear()
    print('-- WRITE MODE -- \n')
    print('Type "back" to go back a screen.\n')
    print('The current characters with dialogue are:')
    for this in jsondata.dialogues:
        print('\n    ' + this)
    menulist = []
    for this in jsondata.dialogues.keys():
        menulist.append(this)
    menulist.append('Add Character')
    character = makemenu(menulist, title="Enter the character you want to access")
    if character in jsondata.dialogues:
        access_character_attributes(jsondata, character)
    if character == 'Add Character':
        clear()
        answer = input('Are you sure you want to add a new character? (y/n) \n')
        if answer == 'y':
            clear()
            character = input('What is the name of this character?\n')
            jsondata.dialogues.update({character: {"Position": [1500, 650], "Immutable_Dialogue_List": [], "Dialogue_List": [], "Dialogues": {}, "Ask_Line": {}, "Yes_Line": {}, "No_Line": {}}})
            jsondata.save('dialogues')
            clear()
            input('Default position assigned.\nPress (Enter) to proceed to creating the first dialogue for this character.\n')
            create(jsondata, character)
        else:
            write_mode(jsondata)

def pyexit():
    pass

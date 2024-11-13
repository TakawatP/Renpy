init python:
    def list_completed_saves(columns = 2, rows = 5):
        list = renpy.list_slots()
        r = []
        for save in list:
            if "c" in save:
                r += [save]
        return r
        
    def available_slot(columns = 2, rows = 5):
        available = False
        i = 1
        while not available:
            page = 1 + (i / (columns*rows))
            name = "{}-c{}".format(page, FileSlotName(i, columns * rows))
            
            available = not renpy.can_load(name)
            i += 1
        renpy.say("", str(name)) ##Prints the name of the available slot
        return name
label start():
    "Beginning."
label new_game:
    "Starting new game."
    $ exp = 0
#    $ game_cycle = 0
    jump play_game
    
label new_game_plus:
    "Starting New Game Plus."
    if list_completed_saves():
        $ renpy.call_in_new_context("_game_menu", _game_menu_screen = "load", completed_mode = True)
    else:
        "No completed save files, starting normal new game."
        jump play_game

label play_game:
    "Defeat goblin. Gain 10 exp."
    $ exp += 10
    "Total exp: [exp]"
    "Ending"
    $ save_name = "Completed with flying colors"
    $ persistent.completed = True
    
    menu:
            "You have won, would you like to start New Game Plus?"
            "Yes":
                jump play_game
            "No":
                pass
    $game_plus = False
    menu:
        "Would you like to save the completed game?"
        "Yes":
            if not game_plus:
                python:
                    game_plus = True
                    renpy.retain_after_load()
                    renpy.save(available_slot(), save_name)
            else:
                jump play_game
            return
        "No":
            pass
    
    
    return
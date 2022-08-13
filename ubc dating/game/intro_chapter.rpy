# The script of the game goes in this file.

# Declarations of audio, images, constants etc are in variables.rpy



# The game starts here.

label intro_chapter:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    $ mc = renpy.input("What will your character name be?")

    $ mc = mc.strip()

    menu: 
      "She/Her":
            $ pronoun1 = "She"
            $ pronoun2 = "Her"
            $ pronoun3 = "Hers"
            jump nameDone

      "He/Him":
            $ pronoun1 = "He"
            $ pronoun2 = "Him"
            $ pronoun3 = "His"
            jump nameDone

      "They/Them":
            $ pronoun1 = "They"
            $ pronoun2 = "Them"
            $ pronoun3 = "Their"
            jump nameDone
            
            #add optiont to get custom pronouns 
label nameDone:

    scene water_fountain with fade

    "You sigh as you listen to the footsteps of people rushing to their next classes."
    "The sound of the water spewing out of the fountain is just what you need at the moment."

    "It's been a long while since you had time to sit down and enjoy the campus for it's beauty. Sometimes, it's easy to forget."

    "To be honest"
    
    mc "tester"



    show eileen happy

    # These display lines of dialogue

    f "Hey, are you going to the party next week? I heard it's going to be pretty fun actually."

    $ name = renpy.input("What is your name?", "Joe User", length=20)

    f "Pleased to meet you, %(name)s."


    k "hello there"

    # This ends the game.

    return

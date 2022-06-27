﻿# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")

define f = Character("your friend - pick name")

define u = Character()

# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    # These display lines of dialogue.

    f "Hey, are you going to the party next week? I heard it's going to be pretty fun actually."

    $ name = renpy.input("What is your name?", "Joe User", length=20)

    f "Pleased to meet you, %(name)s."


    k "hello there"

    # This ends the game.

    return
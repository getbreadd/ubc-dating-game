# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.


# -------- Audio Declaration ---------
define audio.talkingSounds = "cafe talking sound.mp3"




# -------- Character Declaration ---------
define u = Character("User")

define cassie = Character("Cassie") # best friendo 



# -------- Image Declaration ---------





# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene totem_poll with fade

    "You sigh as you listen to the footsteps of people rushing to their next classes."
    "The sound of the water spewing out of the fountain is just what you need at the moment."

    "It's been a long while since you had time to sit down and enjoy the campus for it's beauty. Sometimes, it's easy to forget."

    "To be honest"









    show eileen happy

    # These display lines of dialogue

    f "Hey, are you going to the party next week? I heard it's going to be pretty fun actually."

    $ name = renpy.input("What is your name?", "Joe User", length=20)

    f "Pleased to meet you, %(name)s."


    k "hello there"

    # This ends the game.

    return

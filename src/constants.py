from enum import Enum


class Constants:
    # True/False,
    #   if True, overwrites files in output path if they already exist.
    OVERWRITE_MODE = False

    # Regex for common prefixes to get code.
    CODE_REGEX = '^\d\d\d'

    # True/False,
    #   if True, mixes faces background (works sloppy with hair),
    #   if False, all background is transparent.
    MIX_BACKGROUNDS = False

    # Integer,
    #   how many morphing levels should be generated,
    #   (more than 3, because first and last levels skipped).
    MORPHING_LEVELS = 11

    # Possible image extensions.
    #   Not sure that you can add something new to this.
    IMAGE_EXTENSIONS = ('.png', '.jpg', 'jpeg')


# Person and mood tags used in pictures naming.
class Person(Enum):
    YOURSELF = 'I'
    FRIEND = 'f'
    STRANGER = 's'


class Mood(Enum):
    HAPPY = 'h'
    NORMAL = 'n'
    SAD = 's'

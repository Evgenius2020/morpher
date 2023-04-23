import contextlib
import itertools
import os

import facemorpher
from tqdm import tqdm

from constants import Person, Mood, Constants


def run_facemorpher(paths):
    # Make morphing files, first person is always YOURSELF.
    progress_bar = tqdm(
        list(itertools.product((Person.FRIEND, Person.STRANGER), Mood)))
    for opposite, mood in progress_bar:
        progress_bar.set_description(f'{opposite.value}_{mood.value}')
        # Create morphing files.
        with contextlib.redirect_stdout(None):
            facemorpher.morpher(
                imgpaths=(paths.input_paths[Person.YOURSELF, mood],
                          paths.input_paths[opposite, mood]),
                num_frames=max(Constants.MORPHING_LEVELS, 3),
                out_frames=paths.output_folder,
                background=
                'average' if Constants.MIX_BACKGROUNDS else 'transparent')

        # Rename them (after morpher() called,
        #   files with names frameXXX.png will be created,
        #   where XXX is 3-digit number, starts with 1, ends with
        #   MORPHING_LEVELS-2)
        for frame_number in range(1, Constants.MORPHING_LEVELS - 1):
            frame_right_filename = os.path.join(
                paths.output_folder,
                f'{opposite.value}_{mood.value}_{frame_number}.png')
            os.rename(
                os.path.join(
                    paths.output_folder,
                    f'frame{frame_number:03}.png'),
                frame_right_filename
            )

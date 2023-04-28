import contextlib
import itertools
import os

import facemorpher
from tqdm import tqdm

from constants import Person, Mood, Constants
from processing_stages.working_paths import WorkingPaths


def run_facemorpher(working_paths: WorkingPaths):
    """
    Run facemorpher.morpher(),
        rename result images and
        initialize working_paths.output_paths.
    """
    working_paths.output_paths = {}

    # Make morphing files, first person is always YOURSELF.
    progress_bar = tqdm(
        list(itertools.product((Person.FRIEND, Person.STRANGER), Mood)))
    for opposite, mood in progress_bar:
        progress_bar.set_description(f'{opposite.value}_{mood.value}')
        # Create morphed faces.
        #   By some reason morpher generates (num_frames-2) frames.
        num_frames = max(Constants.MORPHING_LEVELS + 2, 3)
        with contextlib.redirect_stdout(None):
            facemorpher.morpher(
                height=Constants.MORPHING_RESULT_HEIGHT,
                width=Constants.MORPHING_RESULT_WIDTH,
                imgpaths=(working_paths.input_paths[Person.YOURSELF, mood],
                          working_paths.input_paths[opposite, mood]),
                num_frames=num_frames,
                out_frames=working_paths.output_folder,
                background=
                'average' if Constants.MIX_BACKGROUNDS else 'transparent')

        # Save all paths of generated images
        #   (but without first and last frames).
        working_paths.output_paths[opposite, mood] = []

        # Rename them (after morpher() called,
        #   files with names frameXXX.png will be created,
        #   where XXX is 3-digit number, starts with 1, ends with num_frames-1).
        for frame_number in range(1, num_frames - 1):
            frame_generated_filename = os.path.join(
                working_paths.output_folder,
                f'frame{frame_number:03}.png')
            # It's not obvious but first and last frames
            #   are a copies of original photos.
            if (frame_number == 1) or \
                    (frame_number == Constants.MORPHING_LEVELS):
                os.remove(frame_generated_filename)
                continue
            # Right filename contains short tags of opposite person and mood.
            #   Also frame numbers should be started from 1.
            frame_right_filename = os.path.join(
                working_paths.output_folder,
                f'{opposite.value}_{mood.value}_{frame_number - 1}.png')
            if os.path.exists(frame_right_filename):
                os.remove(frame_right_filename)
            os.rename(
                frame_generated_filename,
                frame_right_filename
            )

            working_paths.output_paths[opposite, mood].append(
                frame_right_filename)

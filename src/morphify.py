import os

from processing_stages.run_facemorpher import run_facemorpher
from processing_stages.scramble_picture import scramble_picture
from processing_stages.validate_dirs_and_get_paths import \
    validate_dirs_and_get_paths
from processing_stages.working_paths import WorkingPaths


def morphify(input_dir: str,
             stranger_dir: str,
             output_dir: str) -> WorkingPaths:
    """
    Makes a morphing pictures for
        I/Friend/Stranger photos in different mood types.
    """
    working_paths = validate_dirs_and_get_paths(input_dir,
                                                stranger_dir,
                                                output_dir)
    run_facemorpher(working_paths)
    for morphing_frames in working_paths.output_paths.values():
        # Scramble every middle frame of mood-opposite frames.
        middle_frame_index = len(morphing_frames) // 2
        middle_frame_path = morphing_frames[middle_frame_index]
        scrambled_middle_frame_path = scramble_picture(middle_frame_path)

        # Original frame should be removed.
        morphing_frames.remove(middle_frame_path)
        morphing_frames.insert(middle_frame_index, scrambled_middle_frame_path)
        os.remove(middle_frame_path)

    return working_paths

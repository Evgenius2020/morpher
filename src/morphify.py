from processing_stages.run_facemorpher import run_facemorpher
from processing_stages.validate_dirs_and_get_paths import \
    validate_dirs_and_get_paths


def morphify(input_dir: str,
             stranger_dir: str,
             output_dir: str):
    """
    Makes a morphing pictures for
        I/Friend/Stranger photos in different mood types.
    """
    paths = validate_dirs_and_get_paths(input_dir,
                                        stranger_dir,
                                        output_dir)
    run_facemorpher(paths)
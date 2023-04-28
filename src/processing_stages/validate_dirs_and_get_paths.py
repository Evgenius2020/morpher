import os
import pathlib
import re

from constants import Constants, Person, Mood
from processing_stages.working_paths import WorkingPaths


def validate_dirs_and_get_paths(input_dir: str,
                                stranger_dir: str,
                                output_dir: str) -> WorkingPaths:
    """
    Checks that all input files are exists and valid.
        For disabled OVERWRITE_MODE, checks that output_dir is not exists.
        Returns paths of original photos and output_folder (output_dir/<code>).
    """
    # Check input_dir, get code.
    assert os.path.exists(input_dir), \
        f'input_dir "{input_dir}" is not exists!'
    input_files_names = os.listdir(input_dir)
    assert len(input_files_names) == 6, \
        f'input_dir "{input_dir}" contains not 6 (3+3) files!' \
        f'Files found: {input_files_names}.'
    # Check code exist in every string.
    code_founds = [re.search(Constants.CODE_REGEX, input_file_name)
                   for input_file_name in input_files_names]
    assert all(code_founds), \
        f'Not all prefixes of files in {input_dir})' \
        f'matches {Constants.CODE_REGEX} regex.'
    # Get first regex entry from every string, check that all codes are equal.
    unique_codes = list(set([str(code.group()) for code in code_founds]))
    assert len(unique_codes) == 1, \
        f'Find more that one unique codes in {input_dir}: {unique_codes}.'
    code = unique_codes[0]

    # Check Stranger dir.
    assert os.path.exists(stranger_dir), \
        f'stranger_dir "{stranger_dir}" is not exists!'
    stranger_files_names = os.listdir(stranger_dir)
    assert len(stranger_files_names) == 3, \
        f'stranger_dir "{stranger_dir}" contains not 3 files!' \
        f'Files found: {stranger_dir}.'

    # Check all files is pictures (by extension).
    all_photos_files = input_files_names + stranger_files_names
    picture_extensions = Constants.IMAGE_EXTENSIONS
    assert all(pathlib.Path(file_name).suffix.lower() in picture_extensions
               for file_name in all_photos_files), \
        f'Not every input (I/Friend/Strange) photo has ' \
        f'picture extension (should be one of {list(picture_extensions)}): ' \
        f'{all_photos_files}.'

    # Check all needed person-mood pictures are exist.
    input_files_names_no_extension = \
        [pathlib.Path(input_file_name).stem
         for input_file_name in input_files_names]
    reference_input_filenames = \
        {f'{code}_{person.value}_{mood.value}'
         for person in (Person.YOURSELF, Person.FRIEND)
         for mood in Mood}
    assert set(input_files_names_no_extension) == reference_input_filenames, \
        f'In input_dir, files {reference_input_filenames} expected, ' \
        f'but found {input_files_names_no_extension}.'
    stranger_files_names_no_extension = \
        [pathlib.Path(stranger_file_name).stem
         for stranger_file_name in stranger_files_names]
    reference_stranger_filenames = \
        {f'{Person.STRANGER.value}_{mood.value}' for mood in Mood}
    assert set(
        stranger_files_names_no_extension) == reference_stranger_filenames, \
        f'In stranger_dir, files {reference_stranger_filenames} expected, ' \
        f'but found {stranger_files_names_no_extension}.'

    # Check output_dir.
    output_folder_with_code = os.path.join(output_dir, code)
    assert not (Constants.OVERWRITE_MODE and
                os.path.exists(output_folder_with_code)), \
        f'Rewrite mode is "off", ' \
        f'but output_dir "{output_folder_with_code}" exists!. Aborting...'
    pathlib.Path(output_folder_with_code).mkdir(exist_ok=True, parents=True)

    # Pack paths: for every person-mood pair get path to picture.
    #   (And output folder is also needed).
    return WorkingPaths(
        input_paths={
            (person, mood):
                os.path.join(
                    input_dir if person != Person.STRANGER else stranger_dir,
                    list(filter(
                        lambda filename:
                        f'{person.value}_{mood.value}' in filename,
                        all_photos_files))[0])
            for person in Person
            for mood in Mood
        },
        output_folder=output_folder_with_code
    )

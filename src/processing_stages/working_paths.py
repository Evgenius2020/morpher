from dataclasses import dataclass
from typing import Union

from constants import Person, Mood


@dataclass
class WorkingPaths:
    # All pictures paths (person, mood) -> path.
    input_paths: dict[(Person, Mood), str]

    # Path of output folder (created catalog with code already)
    output_folder: str

    # Path of output morphing frames.
    #   Will be initialized after run_facemorpher.
    output_paths: Union[None, dict[(Person, Mood), list[str]]] = None

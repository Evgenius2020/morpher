import os.path
import random

import click as click
import cv2
import numpy as np

from constants import Constants


def scramble_picture(img_path: str, add_noise=True) -> str:
    assert os.path.exists(img_path), f'File not found {img_path}'

    img_src = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    img_dest = np.zeros(img_src.shape, np.uint8)

    img_height, img_width = img_src.shape[0], img_src.shape[1]
    fragment_height = img_height // Constants.SCRAMBLING_SQUARES_VERTICAL
    fragment_width = img_width // Constants.SCRAMBLING_SQUARES_HORIZONTAL

    # Map img_src fragments into img_dest in random order.
    fragments_count = \
        Constants.SCRAMBLING_SQUARES_VERTICAL * \
        Constants.SCRAMBLING_SQUARES_HORIZONTAL
    scrambled_indexes = \
        random.sample(range(fragments_count), fragments_count)
    for original_index, scrambled_index in enumerate(scrambled_indexes):
        # Calculate fragment coordinates for fragment index.
        original_index_x = \
            original_index % Constants.SCRAMBLING_SQUARES_HORIZONTAL
        original_index_y = \
            original_index // Constants.SCRAMBLING_SQUARES_VERTICAL
        scrambled_index_x = \
            scrambled_index % Constants.SCRAMBLING_SQUARES_HORIZONTAL
        scrambled_index_y = \
            scrambled_index // Constants.SCRAMBLING_SQUARES_VERTICAL

        # Copy pixels from img_src into img_dest
        img_dest[
        fragment_height * scrambled_index_y:
        fragment_height * (scrambled_index_y + 1),
        fragment_width * scrambled_index_x:
        fragment_width * (scrambled_index_x + 1),
        :] = \
            img_src[
            fragment_height * original_index_y:
            fragment_height * (original_index_y + 1),
            fragment_width * original_index_x:
            fragment_width * (original_index_x + 1),
            :]

    if add_noise:
        # Add some noise to img_dest
        img_dest[:, :, 3] += \
            np.random.normal(0, Constants.NOISE_LEVEL, img_src.shape). \
                astype(np.uint8)[:, :, 3]

    # Save image, return path.
    img_path_filename, img_path_extension = os.path.splitext(img_path)
    img_dest_path = f'{img_path_filename}_s{img_path_extension}'
    cv2.imwrite(img_dest_path, img_dest)
    return img_dest_path


@click.command()
@click.option('--img-path',
              type=click.Path(dir_okay=False, exists=True, readable=True),
              prompt='Specify image to scramble',
              help='Image path to scramble.')
def scramble_picture_cli(img_path: str):
    scramble_picture(img_path)


if __name__ == '__main__':
    scramble_picture_cli()

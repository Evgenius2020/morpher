import click

from processing_stages.run_facemorpher import run_facemorpher
from processing_stages.validate_dirs_and_get_paths import \
    validate_dirs_and_get_paths


@click.command()
@click.option('--input-dir',
              type=click.Path(exists=True),
              prompt='Specify input path',
              help='Folder path with I/Friend photos.')
@click.option('--stranger-dir',
              type=click.Path(exists=True),
              prompt='Specify input path',
              help='Folder path with Stranger photos.')
@click.option('--output-dir',
              type=click.Path(),
              prompt='Specify output path',
              help='Folder path for morphed photos.')
def morphify_cli(input_dir: str,
                 stranger_dir: str,
                 output_dir: str):
    morphify(input_dir, stranger_dir, output_dir)


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


if __name__ == '__main__':
    morphify_cli()

import click

from morphify import morphify


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


if __name__ == '__main__':
    morphify_cli()

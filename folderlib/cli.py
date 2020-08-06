"""Console script for folder_wonder."""
# Standard library imports
import sys
import pathlib
import logging

# Third party imports
import click
import click_help_colors

# Local application imports
from .workers import Populator, Cleaner


@click.group(

    cls=click_help_colors.HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green',
    name="Populator",
    context_settings={
        "help_option_names":      ['-h', '--help'],
        "ignore_unknown_options": True
    },
    no_args_is_help=True,
    options_metavar="<options>"
)
def main():
    pass


class ConvertStrToList(click.Option):

    def type_cast_value(self, ctx, value):
        if not value:
            return None
        try:
            value = str(value)
            assert value.count('[') == 1 and value.count(']') == 1
            list_as_str = value.replace('"', "'").split('[')[1].split(']')[0]
            list_of_items = [item.strip().strip("'") for item in list_as_str.split(',')]
            return list_of_items
        except Exception:
            raise click.BadParameter(value)


# region Click Options
# region command settings
@main.command(
    cls=click_help_colors.HelpColorsCommand,
    help_headers_color='green',
    help_options_color='red',
    name="populator",
    context_settings={
        "help_option_names":      ['-h', '--help'],
        "ignore_unknown_options": True
    },
    no_args_is_help=True,
    options_metavar="<options>"
)
# endregion
# region amount option
@click.option(
    "-a",
    "--amount",
    default=10,
    metavar="<integer>",
    type=click.INT,
    help="Populate a folder with random file(s) of different type(s)"
)
# endregion
# region folder option
@click.option(
    "-f",
    "--folder",
    metavar="<Path>",
    type=click.Path(dir_okay=True, file_okay=False),
    help="Folder path where the files will be generated"
)
# endregion
# region verbose option
@click.option(
    "--verbose",
    metavar="<boolean>",
    is_flag=True,
    help="Enables verbose logging messages"
)
# endregion
@click.option(
    "-s",
    "--supported",
    metavar="<Path>",
    type=click.Path(dir_okay=False, file_okay=True),
    help="JSON file with supported files to produce"
)
@click.option(
    "--filters",
    metavar="<List>",
    cls=ConvertStrToList,
    help="Comma separated List of filters to be applied in the files supported e.g [audio, video, ...]"
)
# endregion
def populator_cli(amount, folder, supported, verbose, filters):
    if verbose:
        import workers.populator
        workers.populator.logger.setLevel(logging.DEBUG)
        for handler in workers.populator.logger.handlers:
            handler.setLevel(logging.DEBUG)

    folder = pathlib.Path(folder)
    populator = Populator(path=folder, amount=amount, supported_files=supported, filters=filters)
    populator()


# region Click Options
# region command settings
@main.command(
    cls=click_help_colors.HelpColorsCommand,
    help_headers_color='green',
    help_options_color='red',
    name="cleaner",
    context_settings={
        "help_option_names":      ['-h', '--help'],
        "ignore_unknown_options": True
    },
    no_args_is_help=True,
    options_metavar="<options>"
)
# endregion
# region folder option
@click.option(
    "-f",
    "--folder",
    metavar="<Path>",
    type=click.Path(dir_okay=True, file_okay=False),
    help="Folder path where the files will be processed for cleaning"
)
# endregion
# region save option
@click.option(
    "-s",
    "--save",
    metavar="<Path>",
    default="clean-folder",
    type=click.Path(dir_okay=True, file_okay=False),
    help="Folder path where the files will be stored after cleanup"
)
# endregion
# region verbose option
@click.option(
    "--verbose",
    metavar="<boolean>",
    is_flag=True,
    help="Enables verbose logging messages"
)
# endregion
@click.option(
    "-p",
    "--pool",
    metavar="<Path>",
    type=click.Path(dir_okay=False, file_okay=True),
    help="JSON file with file types to produce"
)
# endregion
def cleaner_cli(folder, save, verbose, pool):
    if verbose:
        import workers.cleaner
        workers.cleaner.logger.setLevel(logging.DEBUG)
        for handler in workers.cleaner.logger.handlers:
            handler.setLevel(logging.DEBUG)

    folder = pathlib.Path(folder)
    cleaner = Cleaner(path=folder, save_to=save)
    cleaner()


if __name__ == '__main__':
    main()

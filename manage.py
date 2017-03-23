import argparse

from aiohttp import web

from todo.app import create_app
from todo.storage import create_tables


def custom_args():
    parser = argparse.ArgumentParser(
        description='demo aio project')

    parser.add_argument('program', choices=['runserver', 'migrate'])
    return parser


if __name__ == "__main__":
    parser = custom_args()
    args = parser.parse_args()
    program = args.program

    if program == 'runserver':
        app = create_app()
        web.run_app(app)
    elif program == 'migrate':
        create_tables()
    else:
        parser.print_help()

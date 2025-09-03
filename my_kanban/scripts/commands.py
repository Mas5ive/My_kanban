import os
import sqlite3

import click
from flask import current_app


@click.command('load-data')
@click.argument('sql_file', type=click.Path(exists=True, dir_okay=False, readable=True), required=False)
def load_data(sql_file=None):
    if sql_file:
        sql_file_path = sql_file
    else:
        sql_file_path = os.path.join(current_app.root_path, 'demo_data.sql')

    db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']

    if not db_uri.startswith('sqlite:///'):
        raise ValueError('This command only supports SQLite databases.')

    db_path = db_uri.replace('sqlite:///', '')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(sql_file_path, 'r') as f:
        sql_script = f.read()

    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    click.echo(f'The data from {os.path.basename(sql_file_path)} has been loaded into the database {db_path}')


def init_app(app):
    app.cli.add_command(load_data)

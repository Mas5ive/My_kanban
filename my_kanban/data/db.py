import os
import sqlite3

import click
from flask import current_app


@click.command('init-db')
def init_db_command():
    instance_dir = current_app.instance_path
    data_dir = os.path.dirname(os.path.abspath(__file__))

    conn = sqlite3.connect(os.path.join(instance_dir, 'db.sqlite3'))
    cursor = conn.cursor()

    with open(os.path.join(data_dir, 'db.sql'), 'r') as sql_file:
        sql_script = sql_file.read()

    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)

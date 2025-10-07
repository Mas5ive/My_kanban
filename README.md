# My-kanban

## Description

A simple multi-user kanban application written in python 3.10 using the Flask 3.0 web framework. This is a learning project, not intended to be deployed on a server.

### Available features

- create Kanban boards
- different functionality depending on the user's relationship to the board
- invite/exclude other users to your projects
- create/edit/move/delete task cards
- comment on cards

### Technical features

- SQLite3 database is used
- JWT technology is used
- frontend is written in vanilla JS
- there are no unit tests

## Installation

```bash
git clone https://github.com/Mas5ive/My_kanban
```

```bash
cd My_kanban/
```

### Using Poetry

Install:

```bash
poetry install
```

### Using pip

- сreate a virtual environment
- activate it
- and run the command:

```bash
pip install -r requirements.txt
```

## Demo mode

To run the demo, use the **VS Code launcher**. When the application starts, it will already have data loaded that will help you quickly evaluate all of its features.

In this example, 3 users are created:

| User      | Password |
|-----------|----------|
| demo_user | 0000     |
| user1     | 1111     |
| user2     | 2222     |

Use them to get a peek behind the scenes!

## Development

Before launching the app in this mode for the first time, you must initialise the DB based on the latest migration:

```bash
export FLASK_CONFIG=development && flask --app my_kanban db upgrade
```

Run the app using the **VS code launcher**.

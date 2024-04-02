# My-kanban

## Description

A simple multi-user kanban application written on the Flask web framework.

### Available features

- create Kanban boards
- different functionality depending on the user's relationship to the board
- invite/exclude other users to your projects
- create/edit/move/delete task cards
- comment on cards

### Technical features

- SQLite3 database is used
- JWT technology is used
- frontend is written in a minimalistic way, without using JS
- REST architecture is followed as much as possible
- there are no unit tests
- basic configuration settings are designed for the development stage. Be sure to write your own configuration file for safe and complete use!
- time and date are counted from UTC 0

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

## Turn on the demo (optional)

```bash
flask --app my_kanban init-db
```

This command will create a database file that contains a schema and some content that allows you to evaluate all the functions of the application.

In this example, 3 users are created:

| User      | Password |
|-----------|----------|
| demo_user | 0000     |
| user1     | 1111     |
| user2     | 2222     |

Use them to get a peek behind the scenes!

## Run

If you haven't skipped the demo step, create your own database file. Take the already existing code in the data folder as a basis.

Now everything is ready to run!

```bash
flask --app my_kanban run
```

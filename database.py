from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import event, types
from sqlalchemy.engine import Engine

db = SQLAlchemy()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
    """
    Activate foreign key functionality under sqlite.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class DatabaseEnum(types.TypeDecorator):
    impl = types.Integer

    def __init__(self, statusEnum, *args, **kwargs):
        self._statusEnum = statusEnum
        super(DatabaseEnum, self).__init__(self, *args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = self._statusEnum(value)
        return value

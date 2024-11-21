from config import db, app
from sqlalchemy import text

table_name = "citations"


def table_exists(name):
    sql_table_existence = text(
        "SELECT EXISTS ("
        "  SELECT 1"
        "  FROM information_schema.tables"
        f" WHERE table_name = '{name}'"
        ")"
    )

    print(f"Checking if table {name} exists")
    print(sql_table_existence)

    result = db.session.execute(sql_table_existence)
    return result.fetchall()[0][0]


def reset_db():
    print(f"Clearing contents from table {table_name}")
    sql = text(f"DELETE FROM {table_name}")
    db.session.execute(sql)
    db.session.commit()


def setup_db():
    if table_exists(table_name):
        print(f"Table {table_name} exists, dropping")
        sql = text(f"DROP TABLE {table_name}")
        db.session.execute(sql)
        db.session.commit()

    print(f"Creating table {table_name}")
    sql = text(
        f"CREATE TABLE {table_name} ("
        "  id SERIAL PRIMARY KEY, "
        "  citation_type TEXT NOT NULL CHECK (char_length(author) >= 1),"
        "  author TEXT DEFAULT NULL CHECK (char_length(author) >= 1),"
        "  title TEXT NOT NULL CHECK (char_length(title) >= 1),"
        "  year TEXT DEFAULT NULL,"
        "  address TEXT DEFAULT NULL,"
        "  annote TEXT DEFAULT NULL,"
        "  booktitle TEXT DEFAULT NULL,"
        "  chapter TEXT DEFAULT NULL,"
        "  crossref TEXT DEFAULT NULL,"
        "  doi TEXT DEFAULT NULL,"
        "  edition TEXT DEFAULT NULL,"
        "  editor TEXT DEFAULT NULL,"
        "  email TEXT DEFAULT NULL,"
        "  howpublished TEXT DEFAULT NULL,"
        "  institution TEXT DEFAULT NULL,"
        "  journal TEXT DEFAULT NULL,"
        "  month TEXT DEFAULT NULL,"
        "  note TEXT DEFAULT NULL,"
        "  number TEXT DEFAULT NULL,"
        "  organization TEXT DEFAULT NULL,"
        "  pages TEXT DEFAULT NULL,"
        "  publisher TEXT DEFAULT NULL,"
        "  school TEXT DEFAULT NULL,"
        "  series TEXT DEFAULT NULL,"
        "  volume TEXT DEFAULT NULL"
        ")"
    )

    db.session.execute(sql)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        setup_db()

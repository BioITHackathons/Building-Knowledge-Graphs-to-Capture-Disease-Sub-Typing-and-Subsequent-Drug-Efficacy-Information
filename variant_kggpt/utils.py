def split_text(text, max_line_length=20):
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 > max_line_length:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word) + 1
    if current_line:
        lines.append(" ".join(current_line))
    return "\n".join(lines)


def view_sqlitedb(cursor):
    # Get a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Print table names and their schema
    for table_name in tables:
        table_name = table_name[0]
        print(f"Table name: {table_name}")

        # Get the schema for the table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        # Print column names and their data types
        print("Columns:")
        for column in columns:
            print(f"    {column[1]} ({column[2]})")

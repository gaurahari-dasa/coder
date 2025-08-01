import mysql.connector


def get_columns_with_foreign_keys(
    db_config, table_name, skip_tables: list[str], skip_columns: list[str]
):
    def column_names():
        return filter(lambda x: x[0] not in skip_columns, cursor.fetchall())

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get columns of the given table
    cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
    columns = [f"{table_name}.{row[0]}" for row in column_names()]

    # Get foreign key relationships
    cursor.execute(
        f"""
        SELECT COLUMN_NAME, REFERENCED_TABLE_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND REFERENCED_TABLE_NAME IS NOT NULL
    """,
        (db_config["database"], table_name),
    )

    foreign_keys = cursor.fetchall()

    # Get columns from referenced tables
    for _, ref_table in foreign_keys:
        if ref_table in skip_tables:
            continue
        cursor.execute(f"SHOW COLUMNS FROM `{ref_table}`")
        ref_columns = [f"{ref_table}.{row[0]}" for row in column_names()]
        columns.extend(ref_columns)

    cursor.close()
    conn.close()
    return columns


# Example usage
# db_config = {
#     "host": "localhost",
#     "user": "your_username",
#     "password": "your_password",
#     "database": "your_database",
# }

# table_name = "your_table_name"
# columns = get_columns_with_foreign_keys(db_config, table_name)
# print(columns)

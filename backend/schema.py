from database import get_connection
from psycopg import sql

TEXT_TYPES = {
    "text",
    "character varying",
    "character",
}

def get_tables() -> list[str]:
    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)

            return [row[0] for row in cur.fetchall()]

def get_columns(table_name: str) -> list[tuple[str, str]]:
    query = """
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    AND table_name = %s
    ORDER BY ordinal_position;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (table_name,))

            return cur.fetchall()

def get_example_values(table: str, column: str) -> list[str]:
    query = sql.SQL("""
        SELECT DISTINCT {column}
        FROM {table}
        WHERE {column} IS NOT NULL
        LIMIT 5;
    """).format(
        table=sql.Identifier(table),
        column=sql.Identifier(column),
    )

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)

            return [str(row[0]) for row in cur.fetchall()]

def get_foreign_keys() -> list[tuple[str, str, str, str]]:
    query = """
    SELECT
        tc.table_name,
        kcu.column_name,
        ccu.table_name AS foreign_table,
        ccu.column_name AS foreign_column
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage ccu
        ON ccu.constraint_name = tc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY'
    ORDER BY tc.table_name;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)

            return cur.fetchall()

def build_database_context() -> str:
    context = []

    context.append("Database schema")
    context.append("================")
    context.append("")

    for table in get_tables():
        context.append(f"Table: {table}")
        context.append("Columns:")

        columns = get_columns(table)

        for column_name, column_type in columns:
            context.append(f"- {column_name} ({column_type})")

            if column_type in TEXT_TYPES:
                values = get_example_values(table, column_name)

                if values:
                    context.append(
                        f"  Example values: {', '.join(values)}"
                    )

        context.append("")

    context.append("Relationships:")
    for table, column, foreign_table, foreign_column in get_foreign_keys():
        context.append(
            f"- {table}.{column} -> {foreign_table}.{foreign_column}"
        )

    context.append("")

    return "\n".join(context)
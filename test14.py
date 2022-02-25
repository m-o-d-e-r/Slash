import psycopg2

conn = psycopg2.connect(
    dbname="Slash",
    user="test",#"postgres",
    password="test",
    host="127.0.0.1",
    port=5432
)
curr = conn.cursor()

#curr.execute("CREATE ROLE test WITH LOGIN PASSWORD 'test' NOCREATEDB;")
#curr.execute("DROP ROLE test")
#curr.execute("SELECT rolname FROM pg_roles")
#print(curr.fetchall())


curr.execute("CREATE TABLE IF NOT EXISTS testtb (name TEXT)")


conn.commit()

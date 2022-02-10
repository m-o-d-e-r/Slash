from Slash.Core.core import Logger, Connection

log = Logger(__name__, __file__)

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

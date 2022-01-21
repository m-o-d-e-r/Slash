from Slash.Core.core import SQLConditions

SQLConditions.where(
    "author", SQLConditions.EQ, "M_O_D_E_R", SQLConditions.AND, "rowid",  SQLConditions.EQ, 10
)
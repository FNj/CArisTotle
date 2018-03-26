import pandas as pd
from collections import namedtuple
from ..config import db

engine = db.engine


def get_df_from_sql(sql: str):
    return pd.read_sql_query(sql, con=engine)


BokehFragments = namedtuple('BokehFragments', ['script', 'div'])

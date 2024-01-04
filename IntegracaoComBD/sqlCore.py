from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, create_engine

engine = create_engine('engine://:memory')

metadata_obj = MetaData(schema='teste')

user = Table(
    'user', metadata_obj, Column('user_id', Integer, primary_key=True),
    Column('user_name', String(40), nullable=False),
    Column('email_address', String(60)),
    Column('nickname', String(50), nullable=False)
)

user_prefs = Table(
    'user_prefs', metadata_obj, 
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', String(40), ForeignKey("user.user_id"), nullable=False),
    Column('pref_name', String(60), nullable=False),
    Column('pref_value', String(100))
)

for table in metadata_obj.sorted_tables:
    print(table)
    
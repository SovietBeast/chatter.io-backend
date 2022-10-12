from sqlalchemy import create_engine, MetaData

#engine = create_engine('mysql+pymysql://root:password@db:3306/chatterio')
engine = create_engine('postgresql://postgres:password@dawn-water-5378.internal:5432/chatterio')

meta = MetaData()
conn = engine.connect()
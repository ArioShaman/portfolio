from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
projects = Table('projects', post_meta,
    Column('uid', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('review', String(length=1000), default=ColumnDefault('not text')),
    Column('link', String(length=128)),
    Column('prev_link', String(length=128)),
    Column('desktop', SmallInteger),
    Column('mobile_version', SmallInteger),
    Column('interactive', SmallInteger),
    Column('inter_map', SmallInteger),
    Column('using', SmallInteger),
    Column('cover', String(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['projects'].columns['prev_link'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['projects'].columns['prev_link'].drop()

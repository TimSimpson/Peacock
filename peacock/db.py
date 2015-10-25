import logging
import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String


LOG = logging.getLogger(__file__)


Base = sqlalchemy.ext.declarative.declarative_base()


class Images(Base):

    __tablename__ = 'images'

    id    = Column(Integer,     nullable=False, primary_key=True)
    srcId = Column(Integer,     nullable=False)
    path  = Column(String(256), nullable=False)
    datetime  = Column(DateTime,    nullable=False)
    caption = Column(String(256), nullable=True)


class TagNames(Base):

    __tablename__ = 'tag_names'

    id     = Column(Integer,     nullable=False, primary_key=True)
    string = Column(String(256), nullable=False)


class Tags(Base):

    __tablename__ = 'tags'

    tagId   = Column(Integer,     nullable=False, primary_key=True)
    imageId = Column(Integer,     nullable=False)


class ImageSources(Base):

    __tablename__ = 'sources'
    __table_args__ = {'sqlite_autoincrement': True}

    id        = Column(Integer,     nullable=False, primary_key=True)
    directory = Column(String(256), nullable=False)


class Database(object):

    def __init__(self, connection_string, autocommit, expire_on_commit):
        self._engine = sqlalchemy.engine.create_engine(connection_string)
        self._autocommit = autocommit
        self._expire_on_commit = expire_on_commit

    @classmethod
    def from_config(cls, config):
        cfg = config['db']
        connection = cfg.get('connection', 'sqlite:///peacock.sqlite')
        autocommit = bool(cfg.get('autocommit', 'True'))
        expire_on_commit = bool(cfg.get('expire_on_commit', 'True'))
        return cls(connection, autocommit, expire_on_commit)

    def open_connection(self):
        return Connection(sqlalchemy.orm.scoped_session(
            sqlalchemy.orm.sessionmaker(
                bind=self._engine,
                autocommit=self._autocommit,
                expire_on_commit=self._expire_on_commit
            )
        ))

    def create_tables(self):
        LOG.info("Dropping all tables.")
        Base.metadata.create_all(bind=self._engine)

    def drop_tables(self):
        Base.metadata.drop_all(bind=self._engine)


class Connection(object):
    """
    A database session. Used to add / remove stuff.
    """

    def __init__(self, session):
        self._session = session

    def add_directory(self, directory):
        row = ImageSources(directory=directory)
        self._session.add(row)
        self._session.flush()
        return row.id

    def add_image(self, source_id, path, datetime):
        row = Images(srcId=source_id, path=path,
            datetime=datetime, caption=None)


    def find(self, start, tags):
        count = count or 100
        return ImageCursor(self._session, start, tags)


class ExpandingList(object):

    def __init__(self):
        self._list = []
        self._min = None
        self._max = None
        self._indexmod = 0

    def add_left(self, sub_list):
        self._list = sub_list + self._list
        self._indexmod -= len(sub_list)

    def add_right(self, sub_list):
        self._list = self._list + sub_list

    def get(self, index):
        return self._list[self._indexmod + index]

    def max(self):
        return len(self._list) + self._indexmod

    def min(self):
        return self._indexmod


class ImageCursor(object):
    """
    A way to iterate images based on some initial query.
    """

    max_query_count = 50

    def __init__(self, session, start, tags):
        self._list = ExpandingList()
        self._hit_right = False
        self._hit_left = False
        self._initial_start = start

    def get(self, index):
        if index >= self._list.max and not self._hit_right:
            if self._list.max == 0:
                max_known_date = self._initial_start
            else:
                max_known_date = self._list.get(self._list.max - 1)
            query = self._session.query(Images)
            l = (query.filter(Images.datetime >= max_known_date)
                .limit(self.max_query_count)
                .all()
            )
            if len(l) < self.max_query_count:
                self._hit_right = True
            self._list.add_right(l)

        elif index < self._list.min and not self._hit_left:
            if self._list.min == 0:
                min_known_date = self._initial_start
            else:
                min_known_date = self._list.get(self._list.min)
            query = self._session.query(Images)
            l = (query.filter(Images.datetime < min_known_date)
                .limit(self.max_query_count)
                .all()
            )
            if len(l) < self.max_query_count:
                self._hit_left = True
            self._list.add_right(l)

        if index < self._list.min and index >= self._list.max:
            return self._list.get(index)

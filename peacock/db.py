import logging
import datetime
import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Boolean
from sqlalchemy.sql.expression import cast
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String


LOG = logging.getLogger(__file__)


Base = sqlalchemy.ext.declarative.declarative_base()


class Images(Base):

    __tablename__ = 'images'

    id    = Column(Integer,     nullable=False, primary_key=True)
    source_id = Column(Integer,     nullable=False)
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

    def __init__(self, connection_string, autocommit=True,
                 expire_on_commit=True):
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
        self._sources = None

    def add_directory(self, directory):
        row = ImageSources(directory=directory)
        self._session.add(row)
        self._session.flush()
        if self._sources is not None:
            self._sources[row.id] = row
        return row.id

    def add_image(self, source_id, path, datetime):
        row = Images(source_id=source_id, path=path,
            datetime=datetime, caption=None)
        self._session.add(row)
        self._session.flush()

    def find(self, start, tags):
        return ImageFinder(self._session, start, tags)

    def get_source(self, source_id):
        if self._sources is None:
            l = self._session.query(ImageSources).all()
            self._sources = {}
            for s in l:
                self._sources[s.id] = s
        return self._sources[source_id]

    def grab_all_images(self):
        return self._session.query(Images).all()


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

    @property
    def max(self):
        return len(self._list) + self._indexmod

    @property
    def min(self):
        return self._indexmod


class ImageFinder(object):
    """
    A way to iterate images based on some initial query.
    """

    max_query_count = 50

    def __init__(self, session, start, tags):
        self._session = session
        self._list = ExpandingList()
        self._hit_right = False
        self._hit_left = False
        self._initial_start = start
        assert isinstance(self._initial_start, datetime.datetime)
        self._log = logging.getLogger("ImageFinder(%s, %s)" % (start, tags))
        self._log.debug("Doing initial fetch of images.")

        #TODO: SqlAlchemy + SqlLite has some bug WRT datetime queries, so
        #      none of my awesome code below is working. This hack wrecks
        #      it all by just fetching all of the things!
        #      Find the real fix and delete the rest of the lines in this
        #      method.
        all_rows = self._session.query(Images).all()
        self._list.add_right(all_rows)
        self._hit_right = True
        self._hit_left = True


    def _fetch(self, index):
        self._log.debug("Request for image %d." % index)
        if index >= self._list.max and not self._hit_right:
            self._log.info("Fetching images to the right.")
            if self._list.max == 0:
                max_known_date = self._initial_start
            else:
                max_known_date = self._list.get(self._list.max - 1)
            self._log.info("max_known_date == %s" % max_known_date)
            assert isinstance(max_known_date, datetime.datetime)
            query = self._session.query(Images)
            l = (query.filter(Images.datetime >= max_known_date)
                .limit(self.max_query_count)
                .all()
            )
            if len(l) < self.max_query_count:
                self._log.info("Hit right wall.")
                self._hit_right = True
            self._list.add_right(l)

        elif index < self._list.min and not self._hit_left:
            self._log.info("Fetching images to the left.")
            if self._list.min == 0:
                min_known_date = self._initial_start
            else:
                min_known_date = self._list.get(self._list.min)
            self._log.info("min_known_date == %s" % min_known_date)
            assert isinstance(min_known_date, datetime.datetime)
            query = self._session.query(Images)
            l = (query.filter(Images.datetime < min_known_date)
                .limit(self.max_query_count)
                .all()
            )
            # l = (query.filter(cast(Images.datetime, String) < cast(min_known_date, String))
            #     .limit(self.max_query_count)
            #     .all()
            # )
            if len(l) < self.max_query_count:
                self._log.info("Hit left wall.")
                self._hit_left = True
            self._list.add_right(l)


    def get(self, index):
        self._fetch(index)

        if self.exists(index):
            return self._list.get(index)
        else:
            raise Exception("No image at index %s" % index)

    def exists(self, index):
        self._fetch(index)
        return index >= self._list.min and index < self._list.max


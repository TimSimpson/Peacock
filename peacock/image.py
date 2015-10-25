class Image(object):

    def __init__(self, id, full_path):
        self._id = id
        self._full_path = full_path

    @property
    def path(self):
        return self._path



class ImageCursor(object):

    def __init__(self, connection, image_finder):
        self._finder = image_finder
        self._index = 0

    def current(self):
        db_info = self._finder.get(self._index)
        src = self._connection.get_source(db_info.source_id)
        return Image(db_info.id, os.path.join(src.directory, db_info.path))

    def left(self):
        if self._finder.exists(self._index - 1):
            self._index -= 1

    def right(self):
        if self._finder.exists(self._index + 1):
            self._index += 1

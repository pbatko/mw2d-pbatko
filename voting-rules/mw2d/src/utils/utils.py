from pathlib2 import Path


class PathValidator:

    def __init__(self, path, name):
        # type: (Path or str, str) -> None
        if isinstance(path, str):
            self.path = Path(path)
        elif isinstance(path, Path):
            self.path = path
        else:
            raise Exception("'{0}' is neither a string or Path!".format(path))

        self.name = name
        self.msg_prefix = "{0} '{1}' ".format(name, path)

    def exists(self):
        if not self.path.exists():
            print self.__create_errmsg("doesn't exist!")
            exit(1)
        return self

    def is_file(self):
        if not self.path.is_file():
            print self.__create_errmsg("is not a regular file!")
            exit(1)
        return self

    def is_dir(self):
        if not self.path.is_dir():
            print self.__create_errmsg("is not a directory!")
            exit(1)
        return self

    def get_path(self):
        return self.path

    def __create_errmsg(self, suffix):
        return self.msg_prefix + suffix


class SimplePickler():

    TYPES = []

    @classmethod
    def registerType(cls, type):
        cls.TYPES.append(type)

    def serialize(self, obj):
        # type: (object) -> str

        obj.to_dict()

        return ""

    def deserialize(self, string):
        # type: (str) -> object

        return ""


pluck = lambda dict, *args: (dict[arg] for arg in args)
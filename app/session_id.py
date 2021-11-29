class SessionID:
    """id generator for process
    Max. 500 processes, and this way max. 500 unique files
    will be allowed.
    After that the process will start overwriting from 0."""
    _id = -1

    @classmethod
    def generate(cls) -> int:
        """increments id and and returns it"""
        if cls._id < 10000:
            cls._id += 1
            id = cls._id
            return id
        else:
            cls._id = 0
            return cls._id

class User(object):
    """
    class User

    Generic user class, nothing more than name.
    """
    def __init__(self, name=""):
        self.name = name
        self._internal_cache = {} # this is a dummy variable to test the __repr__ method

    def __str__(self):
        # 1. Grab the dynamic class name
        header = f"=== {self.__class__.__name__} Details ==="

        # 2. Dynamically format public attributes into clean, user-friendly lines
        lines = [
            f"{k.title()}: {v}"
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        ]

        # 3. Combine them into a single, clean text block
        return "\n".join([header] + lines)

    def __repr__(self):
        # Filter out keys that start with an underscore
        attrs = ", ".join(
            f"{k}={v!r}"
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        )
        return f"{self.__class__.__name__}({attrs})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        # Filter out keys that start with an underscore for both objects
        self_attrs = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        other_attrs = {k: v for k, v in other.__dict__.items() if not k.startswith('_')}

        return self_attrs == other_attrs
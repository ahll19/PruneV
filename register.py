class Register:
    _id: int = None
    _value: int = None

    def __init__(self, id: int, value: int = 0):
        self.id = id
        self.value = value

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Register):
            return self.id == __value.id
        else:
            return False

    def __str__(self) -> str:
        return f"x{self.id}=0x{self.value:08x}"

    def __repr__(self) -> str:
        return f"{self.__str__()}"

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if id < 0 or id > 31 or not isinstance(id, int):
            raise ValueError("Register id must be between 0 and 31")

        self._id = id

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value < 0 or value > 2**32 or not isinstance(value, int):
            raise ValueError("Register value must be between 0 and 2^32")

        self._value = value

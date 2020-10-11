
class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self._genre_name = None
        else:
            self._genre_name = genre_name.strip()

    @property
    def genre_name(self):
        return self._genre_name

    @genre_name.setter
    def genre_name(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self._genre_name = None
        else:
            self._genre_name = genre_name.strip()

    def __repr__(self):
        return f"<Genre {self.genre_name}>"

    def __eq__(self, other):
        if isinstance(other, Genre):
            return self.genre_name.lower() == other.genre_name.lower()
        elif isinstance(other, str):
            return self.genre_name.lower() == other.lower()
        else:
            return False

    def __lt__(self, other):
        return sorted((self.genre_name, other.genre_name))[0] == self.genre_name

    def __hash__(self):
        return hash(self._genre_name)

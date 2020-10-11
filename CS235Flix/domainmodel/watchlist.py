from CS235Flix.domainmodel.movie import Movie


class WatchList:
    def __init__(self):
        self._movie_list = []
        self._current_movie_index = None

    def add_movie(self, movie: Movie):
        if type(movie) is Movie and movie not in self._movie_list:
            self._movie_list.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self._movie_list:
            self._movie_list.remove(movie)

    def select_movie_to_watch(self, index: int):
        if type(index) is not int or index >= len(self._movie_list):
            return None
        else:
            return self._movie_list[index]

    def size(self):
        return len(self._movie_list)

    def first_movie_in_watchlist(self):
        if len(self._movie_list) > 0:
            return self._movie_list[0]
        else:
            return None

    def contains_movie(self, movie: Movie) -> bool:
        return movie in self._movie_list

    def __iter__(self):
        self._current_movie_index = 0
        return self

    def __next__(self):
        if self._current_movie_index < len(self._movie_list):
            movie = self._movie_list[self._current_movie_index]
            self._current_movie_index += 1
            return movie
        else:
            raise StopIteration

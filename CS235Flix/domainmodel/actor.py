
class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self._actor_full_name = None
        else:
            self._actor_full_name = actor_full_name.strip()

        self._colleagues = []

    @property
    def actor_full_name(self):
        return self._actor_full_name

    @actor_full_name.setter
    def actor_full_name(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self._actor_full_name = None
        else:
            self._actor_full_name = actor_full_name.strip()

    def add_actor_colleague(self, colleague: "Actor"):
        if type(colleague) is Actor and colleague not in self._colleagues:
            self._colleagues.append(colleague)
            colleague.add_actor_colleague(self)

    def check_if_this_actor_worked_with(self, colleague: "Actor") -> bool:
        return colleague in self._colleagues

    def __repr__(self):
        return f"<Actor {self.actor_full_name}>"

    def __eq__(self, other):
        if isinstance(other, Actor):
            return self.actor_full_name.lower() == other.actor_full_name.lower()
        elif isinstance(other, str):
            return self._actor_full_name.lower() == other.lower()
        else:
            return False

    def __lt__(self, other):
        return sorted((self.actor_full_name, other.actor_full_name))[0] == self.actor_full_name

    def __hash__(self):
        return hash(self._actor_full_name)

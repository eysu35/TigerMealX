# container class for students
class Students:
    pass


class Student:

    def __init__(self, puid, netid, name, club):
        self._puid = puid
        self._netid = netid
        self._name = name
        self._club = club
        # other fields?

    def get_puid(self):
        return self._puid

    def set_studentid(self, puid):
        self._puid = puid

    def get_netid(self):
        return self._netid

    def set_netid(self, netid):
        self._netid = netid

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_club(self):
        return self._club

    def set_club(self, club):
        self._club = club

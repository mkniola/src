"""Class representation of employee."""


class Employee:
    """Holds basic data for single employee."""

    def __init__(self, name, lastname, eid):
        """Initialize method."""
        self.name = name
        self.lastname = lastname
        self.eid = eid

    def who_am_i(self):
        """Return employee full name."""
        return [f'{self.name} {self.lastname}', f"{self.eid}"]

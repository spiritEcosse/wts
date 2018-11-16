"""Analyze html structure."""

from apps.css.models import Value


class Analyze:
    """Analyze html structure."""

    DISPLAYS = Value.pd_name_by_pr('display')

    def __init__(self, display, windows_width=1904):
        """Init ."""
        self.display = display
        self.windows_width = windows_width

    def append(self):
        """Find target component."""
        append = False

        if self.display == self.DISPLAYS[0]:
            append = False
        elif self.display in list(self.DISPLAYS[1:]):
            append = True

        return append

"""Analyze html structure."""


class Analyze:
    """Analyze html structure."""

    def __init__(self, windows_width=1024):
        """Init ."""
        self.full_width = windows_width

    def is_component(self, width):
        """Find target component."""
        return self.full_width == width

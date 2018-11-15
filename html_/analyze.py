"""Analyze html structure."""


class Analyze:
    """Analyze html structure."""

    CSS_DISPLAYS = (
        'block',
        'inline',
        'inline-block',
    )

    def __init__(self, css_display, windows_width=1904):
        """Init ."""
        self.css_display = css_display
        self.windows_width = windows_width

    def append(self):
        """Find target component."""
        append = False

        if self.css_display == self.CSS_DISPLAYS[0]:
            append = False
        elif self.css_display in self.CSS_DISPLAYS[1:]:
            append = True

        return append

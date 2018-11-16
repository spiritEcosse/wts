"""Test analyze html structure."""

import pytest
from apps.html.analyze import Analyze


class TestAnalyze:
    """Test analyze html structure."""

    @pytest.mark.parametrize("input,expected", (
        ("block", False),
        ("inline", True),
        ("inline-block", True),
    ))
    def test_append(self, input, expected):
        """Test find target component."""
        analyze = Analyze(input)
        assert analyze.append() == expected

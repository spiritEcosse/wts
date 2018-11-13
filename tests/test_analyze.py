"""Test analyze html structure."""

import pytest
from html_.analyze import Analyze


class TestAnalyze:
    """Test analyze html structure."""

    @pytest.mark.parametrize("input,expected", (
        (1024, True),
        (700, False),
    ))
    def test_is_component(self, input, expected):
        """Test find target component."""
        analyze = Analyze()
        assert analyze.is_component(input) == expected

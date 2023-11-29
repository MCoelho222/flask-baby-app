from __future__ import annotations

import data_api


def test_data_api():
    """Test import data_api correctly."""
    assert isinstance(data_api.__version__, str)

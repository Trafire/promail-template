"""Package-wide test fixtures."""


def pytest_configure(config):
    """Configure pytest cli."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")

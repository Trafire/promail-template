[![Tests](https://github.com/trafire/promail-template/workflows/Tests/badge.svg)](https://github.com/trafire/promail-template/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/trafire/promail-template/branch/main/graph/badge.svg)](https://codecov.io/gh/trafire/promail)
[![PyPI](https://img.shields.io/pypi/v/promail-template.svg)](https://pypi.org/project/promail/)

# Promail-Template

## Basic Usage

```python
from promail_template.templates.full import HelloWorld

template = HelloWorld()
template.preview_html()
template.print("html")


```

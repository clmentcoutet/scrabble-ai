mypy --explicit-package-bases --check-untyped-defs .
ruff check --fix
ruff format
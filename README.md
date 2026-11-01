# CEAww

[English](README.md) · [العربية](README_AR.md) · [File index](docs/INDEX.md)

Flask academic results dashboard with charts, recommendations, and Supabase access.

## Repository contents

- [app.py](app.py)
- [requirements.txt](requirements.txt)
- [templates](templates)
- [static](static)
- [.env.example](.env.example)

## Setup and use

Create a Python virtual environment and install the listed dependencies. Copy `.env.example` to `.env`, then configure `SUPABASE_URL`, `SUPABASE_KEY`, and `SECRET_KEY`.

```sh
python -m venv .venv
# Activate the virtual environment for your shell.
python -m pip install -r requirements.txt
python app.py
```

The default development port is 5000; `PORT` can override it.

## License

The repository currently has no root license file. This documentation does not assign a new license.

## Contributing and navigation

[CONTRIBUTING.md](CONTRIBUTING.md) · [Documentation index](docs/INDEX.md) · [Public project index](https://github.com/InfoSecNazir/InfoSecNazir/blob/main/PROJECTS.md)

## Verification scope

Repository organization checked file paths, documentation links, and available dependency manifests. This update did not run or deploy the application.

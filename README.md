# Songs CLI

## Pre-requisites

This project requires to have [pipenv](https://pipenv.pypa.io/en/latest/) installed. You can install it with:

```bash
pip install pipenv
```

## Gettings started

To get started, clone this repository and install the dependencies using pipenv:

```bash
python -m pipenv install
```

To start the virtual environment, run:

```bash
python -m pipenv shell
```

## Usage

To use the CLI run the following command

```bash
python -m pipenv run cli [COMMAND] [OPTIONS]
```

For example:

```bash
python -m pipenv run cli artist list
```

You can pass the flag `--help` at any point in the cli to see more command options

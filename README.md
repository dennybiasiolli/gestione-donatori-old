# Gestione Donatori - API Server

[![Updates](https://pyup.io/repos/github/dennybiasiolli/blood-donor-management/shield.svg)](https://pyup.io/repos/github/dennybiasiolli/blood-donor-management/) [![Python 3](https://pyup.io/repos/github/dennybiasiolli/blood-donor-management/python-3-shield.svg)](https://pyup.io/repos/github/dennybiasiolli/blood-donor-management/)


## Initializing project

- Install requirements or development requirements, based on your preferences.

    ```sh
    pip install -r requirements.txt
    # or
    pip install -r requirements_dev.txt
    ```

- Create settings file, for example starting from development settings

    `cp website/settings_dev.py website/settings.py`

- Define a `SECRET_KEY` in `website/settings.py` file


## Running server

- Apply all missing database migration

    `python manage.py migrate`

- Collecting all static files
    (for production purposes only, non required in development mode)

    `python manage.py collectstatic --noinput`

- Running server

    `python manage.py runserver`

- Configure a cron job for flushing expired tokens daily

    `python manage.py flushexpiredtokens`


## Tests

Launch simple tests with `python manage.py test`, or launch test with coverage
results with:

```
coverage run manage.py test --settings=website.settings_test && coverage report -m && coverage html
```

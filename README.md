# Analytics Pipeline

This repo contains the code for creating a data pipeline to calculate metrics for a fake webserver:

* `log_generator.py` -- generates fake webserver logs.
* `store_logs.py` -- parses the logs and stores them in a SQLite database.
* `count_visitors.py` -- pulls from the database to count visitors to the site per day.

This is an update of the original code to appeal better to my tastes.

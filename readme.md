
# setup

requires python 3 with lxml
create a venv and install requirements.txt


# ckantoiso101153.py

This will pull ckan metadata records from a server and output a minimal iso 10115-3 dataset to `output/ckan`

For development it is setup to process of number of datasets from catalogue.data.wa.gov.au


# dbcatoiso101153.py

This will process dbca metadata records from and ouput a minimal iso 10115-3 dataset to `output/dbca`

For development it is setup to process any files it finds at `input/dbca/*.xml`



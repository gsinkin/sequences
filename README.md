# sequences
Atomic, threadsafe, sequences as a service


1. `virtualenv --no-site-packages venv-sequences`
1. `source venv-sequences/bin/activate`
1. `pip install -r requirements.txt -r test_requirements.txt`
1. `psql -U postgres`
1. `create database sequences_db`
1. `create database sequences_db_test`
1. `\q`
1. `psql -U YOUR_POSTGRES_USER sequences_db < schema/001_sequences.sql`
1. `psql -U YOUR_POSTGRES_USER sequences_db_test < schema/001_sequences.sql`
1. `cp sample_env .env`
1. Edit the .env file with your DB connection credentials
1. `py.test test/unit`

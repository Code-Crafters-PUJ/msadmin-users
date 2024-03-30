# msadmin-users

To run the microservice, you need to have the .env file created.

To do that:
1. Copy the example.env file and rename it to .env.
2. Then complete the environment variables with your own credentials.
3. To create the database, run the following command:
```bash
python manage.py makemigrations
python manage.py migrate
```
4. To run the microservice, run the following command:
```bash
python manage.py runserver
```
5. To run the tests, run the following command:
```bash
python manage.py test
```




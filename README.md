# Dodgy Brothers (Dealership App)

In the wake of the COVID pandemic, Dodgy Brothers (a car dealership) has decided to try its hand at selling used cars online. The dealership principal - Mike "Iron" Smith wants users to be able to submit their used cars for sale online for free.
Buyers will then search for the cars online and apply to buy. When the car is marked as "sold", Mike will receive an email.


## Run DB & Web Server

- Run Docker Compose in parent directory: `dodgy_brothers`
> $ docker-compose up

- Open http://localhost:80 in browser

## Code Test & Coverage

- Run Test cases with coverage
> $ coverage run --source='.' manage.py test dealership_app -v 2

- Show coverage report
> $ coverage report
```
Name                                              Stmts   Miss  Cover
---------------------------------------------------------------------
dealership_app/__init__.py                            0      0   100%
dealership_app/admin.py                               1      0   100%
dealership_app/apps.py                                4      0   100%
dealership_app/constants.py                           9      0   100%
dealership_app/exceptions.py                          9      0   100%
dealership_app/features/__init__.py                   0      0   100%
dealership_app/features/list_car_steps.py             5      5     0%
dealership_app/forms.py                              25      0   100%
dealership_app/management/commands/initadmin.py      26      2    92%
dealership_app/migrations/0001_initial.py             7      0   100%
dealership_app/migrations/__init__.py                 0      0   100%
dealership_app/models.py                             25      0   100%
dealership_app/tests/__init__.py                      0      0   100%
dealership_app/tests/test_models.py                  20      0   100%
dealership_app/tests/test_views.py                  120      0   100%
dealership_app/urls.py                                4      0   100%
dealership_app/views.py                              84      5    94%
dodgy_brothers/__init__.py                            0      0   100%
dodgy_brothers/asgi.py                                4      4     0%
dodgy_brothers/settings.py                           24      0   100%
dodgy_brothers/urls.py                                3      0   100%
dodgy_brothers/wsgi.py                                4      4     0%
manage.py                                            12      2    83%
---------------------------------------------------------------------
TOTAL                                               386     22    94%
```

- Generate coverage report in html
> $ coverage html

### Basic ERD

![ERD](DodgyBrothersERD.jpg?raw=true)

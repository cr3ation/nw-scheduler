
# Nordic Wellness Scheduler

Or `nw-scheduler` is a Django based application running in docker to manage scheduling of booking of group activities. So you can spend your time drinking beer. 

Group activities is being fetched automatically from Nordic Wellness every 15 min. It can also be manually updated with the blue `Refresh` button on the bottom of `http://server:8000`

*Nordic Wellness Scheduler* consists of 3 docker containers  
`db` – Postgresql database  
`app` – Django-app doing the heavy lifting  
`infinite-loop` – Checks every 5 min if a booking is scheduled. If yes, it checks every second if booking has opened.

## Installation
You need docker and docker-compose to be installed before continue.

 1. Edit `docker-compose.yml`. See *Environment Variables* section below
 2. Build and run docker images
```shell
docker-compose build && docker-compose up
```
 3. Open a shell in to the docker container `nw-scheduler-app` and create a superuser to access the `http://server:8000/admin` interface. Then then start workers to fetch data from Nordic Wellness every 15 min
 ````shell
python manage.py createsuperuser
... 
python manage.py runworkers
````


### Environment Variables
Open `docker-compose.yml` and edit the mandatory `ALLOWED_HOSTS`, `NW_CLUB_ID`, `NW_USER_ID`.

Optional environment variables:
`SECRET_KEY`, `DEBUG`, `NW_EMPLOYE_ID`, `DB_NAME`, `DB_USER`, `DB_PASS`, `POSTGRES_DB`, `DB_NAME`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `PUSHOVER_USER`, `PUSHOVER_TOKEN`

#### Description
* `SECRET_KEY` – Used by django. Can be whatever *(secretkey is default)*
* `DEBUG` – `0` is False, `1` is True *(0 is default)*
* `ALLOWED_HOSTS` – `127.0.0.1,*,localhost` *(127.0.0.1 is default)*
* `NW_CLUB_ID` – ID of a Nordic Wellness club. Use Chrome developer tools to filter requests from https://nordicwellness.se/boka/ to find your club *(mandatory)*
* `NW_USER_ID` – ID of your Nordic Wellness user. Is always a numeric id *(mandatory)*
* `NW_EMPLOYE_ID` – Filter group activity by your favorite leader. Is always a numeric id *(optional)*
* `DB_NAME` – Database name *(db is default)*
* `DB_USER` – Database user *(devuser is default)*
* `DB_PASS` – Database password *(changeme is default)*
* `POSTGRES_DB` – Same as `DB_NAME` *(db is default)*
* `POSTGRES_USER` – Same as `DB_USER` *(devuser is default)*
* `POSTGRES_PASSWORD` Same as `DB_PASS` *(changeme is default)*
* `DEBUG` – `0` is False, `1` is True *(0 is default)*
* `PUSHOVER_USER` – Used for push notifications *(optional)*
* `PUSHOVER_TOKEN` – Used for push notification *(optional)*


### Volumes
*  `./django/app:/app` - Main application

### URLs
`http://localhost:8000` – homepage
`http://localhost:8000/admin` – admin page. Use credentials created in step 3 during installation
`http://localhost:8000/fetch`– fetch data on demand from Nordic Wellness API

### Useful File Locations (inside container)
*  `/app/` - Django application
  
## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code of conduct, and the process for submitting pull requests.

## Authors
*  **Henrik Engström** - *Initial work* - [cr3ation](https://github.com/cr3ation)
* See also the list of [contributors](https://github.com/cr3ation/epidemic-sound/contributors) who participated in this project.

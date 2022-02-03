
# Nordic Wellness Scheduler

Or `nw-scheduler` is a Django based application running in docker to manage scheduling of booking of group activities. So you can spend your time drinking beer and need the extra exercise. 

Group activities is being fetched automatically every 15 min. They can also be fetched using 

## Installation
You need docker and docker-compose to be installed before continue.

 1. Open and update `docker-compose.yml`. See *Environment Variables* section below
 2. Build and run docker images
```shell
docker-compose build && docker-compose up
```
 3. Open shell in `nordic-wellness-app` and create a superuser. Then then start workers to fetch data from Nordic Wellness every 15 min
 ````shell
python manage.py createsuperuser
... 
python manage.py runworkers
````


### Environment Variables
Open `docker-compose.yml` and edit `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `NW_CLUB_ID`, `NW_USER_ID`, `NW_EMPLOYE_ID`, `PUSHOVER_USER` and `PUSHOVER_TOKEN`

* `SECRET_KEY` – Used by django. Can be whatever *(mandatory)*
* `DEBUG` – `0` is False, `1` is True *(mandatory)*
* `ALLOWED_HOSTS` – `127.0.0.1,*,localhost` *(mandatory)*
* `NW_CLUB_ID` – ID of a Nordic Wellness club. Use Chrome developer tools to filter requests from https://nordicwellness.se/boka/ to find your club *(mandatory)*
* `NW_USER_ID` – ID of your Nordic Wellness user. Is always a numeric id *(mandatory)*
* `NW_EMPLOYE_ID` – Filter group activity by your favorite leader. Is always a numeric id *(optional)*
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
# Nordic Wellness Scheduler

**Or `nw-scheduler`**, a Django-based application running in Docker to manage scheduling and booking of group activities—so you can spend more time drinking beer. 🍻

Group activities are fetched from Nordic Wellness every 30 minutes and stored in a local database. If needed, fetching new data can be manually initiated using the blue **Refresh** button at the bottom of `http://server:8000`.

## **Architecture**
The *Nordic Wellness Scheduler* consists of three Docker containers:

- `db` – PostgreSQL database  
- `app` – Django application handling core logic  
- `infinite-loop` – A process that checks every 10 minutes if a booking is scheduled. If less then 10 min until a scheduled booking, it checks every second to see if the booking has opened.

---

## **Installation**
Ensure you have **Docker** and **Docker Compose** installed before proceeding.

### **1. Download this repo**
```sh
git clone https://github.com/cr3ation/nw-scheduler.git
cd nw-scheduler
```

### **2. Copy Sample Settings**
```sh
cp docker-compose-sample.yml docker-compose.yml
```

### **3. Edit `docker-compose.yml`**
Modify the environment variables as needed (see the *Environment Variables* section below).

### **4. Build and Run Docker Images**
```sh
docker-compose build && docker-compose up
```

---

## **Environment Variables**
Open `docker-compose.yml` and configure the mandatory variables:  
`ALLOWED_HOSTS`, `NW_CLUB_ID`, `NW_USER_ID`

### **Optional Environment Variables:**
- `SECRET_KEY`, `DEBUG`, `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`
- `DB_NAME`, `DB_USER`, `DB_PASS`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `NW_EMPLOYE_ID`
- `PUSHOVER_USER`, `PUSHOVER_TOKEN`

### **Description of Environment Variables**
| Variable                      | Description | Default Value |
|--------------------------------|-------------|--------------|
| `SECRET_KEY`                  | Used by Django. Can be any string. | `secretkey` |
| `DEBUG`                       | `0` for False, `1` for True | `0` |
| `DJANGO_SUPERUSER_USERNAME`    | Django admin username | `admin` |
| `DJANGO_SUPERUSER_EMAIL`       | Superuser email | `admin@example.com` |
| `DJANGO_SUPERUSER_PASSWORD`    | Superuser password | `password` |
| `ALLOWED_HOSTS`                | Allowed hosts for Django | `127.0.0.1,*,localhost` |
| `CSRF_TRUSTED_ORIGINS`         | App URL when using reverse proxy | `https://subdomain.example.com` |
| `NW_CLUB_ID`                   | ID of a Nordic Wellness club (mandatory) | _None_ |
| `NW_USER_ID`                   | ID of your Nordic Wellness user (mandatory) | _None_ |
| `NW_EMPLOYE_ID`                | ID of a preferred group activity leader (optional) | _None_ |
| `DB_NAME`                      | Database name | `db` |
| `DB_USER`                      | Database username | `devuser` |
| `DB_PASS`                      | Database password | `changeme` |
| `POSTGRES_DB`                  | Same as `DB_NAME` | `db` |
| `POSTGRES_USER`                | Same as `DB_USER` | `devuser` |
| `POSTGRES_PASSWORD`            | Same as `DB_PASS` | `changeme` |
| `PUSHOVER_USER`                | User key for push notifications (optional) | _None_ |
| `PUSHOVER_TOKEN`               | Token for push notifications (optional) | _None_ |

---

## **Volumes**
The following volume is mounted in the container:

- `./django/app:/app` – Main application directory

---

## **URLs**
`http://localhost:8000` – homepage  
`http://localhost:8000/admin` – admin page. Use superuser credentials created in step 3 of the installation instructions  
`http://localhost:8000/fetch`– fetch data on demand from Nordic Wellness API  

---

## **Useful File Locations (Inside Container)**
- `/app/` – Django application directory

---

## **Contributing**
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

---

## **Authors**
- **Henrik Engström** – *Initial work* – [cr3ation](https://github.com/cr3ation)
- See the full list of [contributors](https://github.com/cr3ation/epidemic-sound/contributors) who have participated in this project.

# Parking-Reservation



## Getting Started

Clone the repository

```bash
git clone https://github.com/iSabbuGiri/Parking-Reservation.git
```
Activate the virtual environment

Install dependencies:
```bash
pip install -r requirements.txt
```

Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
Now you can run the server:
```bash
python manage.py runserver
```

## Overview

The project is a car park booking system that consists of 4 bays numbered 1 to 4. A customer can book all-day parking for a single car on a given date if there is an available bay. A customer can only make one booking per day and bookings must be made at least 24 hours in advance.


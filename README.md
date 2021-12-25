# Theater Seating API

This repo contains a Flask API for seating groups of attendees to a given rank

## Environment
Before running the application you will need to create a `.env` file at the root of the project with the following values:

```bash
PORT=8080

MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_NAME=theater_seating_db
MONGO_CONNECT_ON_STARTUP=True
```

## Running locally

To run the basic server, you'll need to install a few requirements. First, run:

```bash
virtualenv venv
source venv/bin/activate
```

Then:

```bash
pip install -r requirements/common.txt
```

This will install only the dependencies required to run the server. To boot up the 
default server, you can run:

```bash
bash bin/run.sh
```

Alternatively the following `make` commands will perform the setup for you:

```bash
make venv
make install
make start
```

This will start a [Gunicorn](https://gunicorn.org/) server that wraps the Flask app 
defined in `src/app.py`. Note that [this is one of the recommended ways of deploying a
Flask app 'in production'](https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/). 
The server shipped with Flask is [intended for development
purposes only](https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment).  

You should now be able to send:

```bash
curl localhost:5000/health
```

And receive the response `OK` and status code `200`. This also has the added benefit of spinning up/checking the connection to the DB if no requests have been made yet.

## Running with `docker`

You'll need [Docker](https://www.docker.com/products/docker-desktop) 
installed to run this project with Docker. To build a containerized version of the API, 
run:

```bash
docker compose up --build -d
```

You should see the db image downloaded, the server boot up, and should be accessible as before.

# Design Considerations and Decisions

Beyond this point I will discuss various design decisions that were made as the application was being built.

## Data Structures
To solve the problem in the problem statement we will need several data structures stored across several collections.

### Theater Info
The data structure to represent an event venue will be broken up and stored in the `venue-layout` collection within mongoDB. The top level document will contain the sections and the section metadata. An example layout is below:

```py
{
  _id: '',
  venue_name: 'name',
  main_hall: [{
    floor: 0,
    curved: False,
    total_seats: 10,
    layout: [] # layout is empty within the database, populated in the api
    ... // additional params
  }, ...],
  balcony1:[{...}],
  balcony2:[{...}],
  ...
}
```

#### Querying
This document would be pulled by ID when the user clicks "buy tickets" on a given site. It would display the entire layout of the venue as an image, and clicking on a various section would query for the documents below.

#### Writing
In a real-life implementation you would need a role-secured endpoint to POST new venue data to. There could be an admin panel that the sales department uses or shares with the venue to define their venue.

### Seat Layout
The next step is to have a collection that is relatively static representing each possible seat within a given venue. The documents are returned via the venue ID and section and an accumulator places them within the above data structure. Example below:

```py
{
  _id: '',
  venue_id: '',
  section: 'main_hall',
  rank: '1', # refers to value/placement of seat selection, e.g. rank 1 is better seating than 3.
  seat_number: '1',
  row: '1', # String, some venues may use letters for rows
  aisle_seat: True
}
```

#### Querying
These documents would be pulled as the user drills into a given section in the venue while going through the ticket purchasing process. In this site, a user can only view one section at a time to calls to the DB would be minimal. However, to ensure speed, we can apply an ascending index on the `row` field to return the seats sorted by row. If desired, a compound sort can sort first by row, then by seat.

### User Ticket
Once we've pulled the layout from the DB into the app to send to the user, we want to allow the user to purchase and thereby "lock" a seat to that user. The process of locking is not something that is an ask of this project so we will only worry about issuing tickets and not checking if a ticket can be issued. Example document:

```py
{
  _id: '',
  user_id: '',
  event_id: '',
  venue_id: '',
  group_size: '',
  rank: '',
  preference: '',
  created_at: '',
  redeemed_at: ''
}
```

#### Querying 
When a user clicks into their wallet on the site, a request is made to the DB to return tickets based on `user_id`. Additionally a date range could be placed on the query if the user has many tickets.
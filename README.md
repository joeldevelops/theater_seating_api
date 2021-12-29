# Theater Seating API

This repo contains a Flask API for seating groups of attendees to a given rank

- [Theater Seating API](#theater-seating-api)
  - [Environment](#environment)
  - [Running locally](#running-locally)
  - [Running with `docker`](#running-with-docker)
  - [Activating the Seating Algorithm](#activating-the-seating-algorithm)
    - [Swagger](#swagger)
    - [Extra Step](#extra-step)
- [Design Considerations and Decisions](#design-considerations-and-decisions)
  - [Flask and Quart](#flask-and-quart)
  - [Database](#database)
  - [Data Structures](#data-structures)
    - [Theater Info](#theater-info)
      - [Querying](#querying)
      - [Writing](#writing)
    - [Seat Layout](#seat-layout)
      - [Querying](#querying-1)
    - [User Ticket](#user-ticket)
      - [Querying](#querying-2)
- [Testing](#testing)

## Environment
Before running the application you will need to create a `.env` file at the root of the project with the following values:

```bash
QUART_APP=src
HOST=0.0.0.0
PORT=8080
WORKERS=4

LOG_LEVEL=debug

MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_NAME=theater_seating_db
MONGO_CONNECT_ON_STARTUP=False
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
export QUART_APP=src && quart run
```

Alternatively the following `make` commands will perform the setup for you:

```bash
make venv
make install
make start
```

This will start a Hypercorn ASGI server that wraps the Flask app 
defined in `src/app.py`.

You should now be able to send:

```bash
curl localhost:8080/health
```

And receive the response `OK` and status code `200`. This also has the added benefit of spinning up/checking the connection to the DB if no requests have been made yet.

## Running with `docker`

This is the preferred way of running this application.

You'll need [Docker](https://www.docker.com/products/docker-desktop) 
installed to run this project with Docker. To build a containerized version of the API, 
run:

```bash
docker compose up --build -d
```

You should see the db image downloaded, the server boot up, and should be accessible as before.

## Activating the Seating Algorithm

### Swagger
All the below requests can also be activated by Swagger, pasting in the bodies from the cURL commands will work fine. Start the server and visit [the Swagger URL.](http://localhost:8080/apidocs/#/)

As this codebase interacts with a MongoDB database there is an initial step required for a quick test run of the code. However this step is easy with the `make` command:

```bash
make init-db
```

If you have your docker container running then the above command will run the `initdb` command within Quart to set up for the test run. This creates the 24 seats in 3 rows from the problem statement.

Next, we need to find the ObjectID of the venue that was created in the DB for us:

```bash
curl localhost:8080/venue
```

This will display an `oid` that you will need to copy. Next we will use this `oid` to kick off the seating/ticketing algorithm:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"groups":[1,3,4,4,5,1,2,4],"rank":"1","venue_id":"<venue_id_here>"}' localhost:8080/seats/order
```

You should see the following displayed on screen:

```bash
[1, 2, 2, 2, 3, 3, 3, 3]
[8, 8, 8, 8, 4, 4, 4, 4]
[5, 5, 5, 5, 5, 6, 7, 7]
```

Finally, you can take a user's group ID and get a list of their tickets from the wallet endpoint:

```bash
curl localhost:8080/wallet/2
```

### Extra Step

The application also supports seating users with various preferences. Which can be tested with:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"groups":[1,3,4,4,5,1,2,4],"rank":"1","venue_id":"61c95f272ae66f3472c7f6e4", "prefs":{"2":"aisle"}}' localhost:8080/seats/order
```

All of the above curls can be found in the `.curls` file in this repo.

# Design Considerations and Decisions

Beyond this point I will discuss various design decisions that were made as the application was being built.

## Flask and Quart

To solve the non-blocking ask for this project I've written the original service in Flask, then migrated to Quart based on the [Flask Docs recommendation.](https://flask.palletsprojects.com/en/2.0.x/async-await/#when-to-use-quart-instead)

## Database

For this project I selected MongoDB. For a given event the number of tickets could average 20,000+, which is a relatively small amount of documents. Even at hundreds of those events a day we would barely scratch the performance on Mongo and with NoSQL we get the benefit of flexible collection/table structure.

## Data Structures
To solve the problem in the problem statement we will need several data structures stored across several collections.

### Theater Info
The data structure to represent an event venue will be broken up and stored in the `venue-layout` collection within mongoDB. The top level document will contain the sections and the section metadata. This collection is the main reason for MongoDB, as we are free to define the section names at will. An example layout is below:

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
This document would be pulled by ID when the user clicks "buy tickets" on a given site. It would enable display of the entire layout of the venue as an image, and clicking on a various section would query a separate collection for the documents below.

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


# Testing

To run the unit tests, activate the virtual environment and then run the below commands:

```bash
pip install -r requirements/develop.txt
pytest
```
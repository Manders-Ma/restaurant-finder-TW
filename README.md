# FoodSearchService-TW

## Brief Introduction
- A simplified google map that considers traffic costs based on current location and provides more appropriate search functions.
- Different from the past that only displayed the distance, it is changed to use a more intuitive traffic time.

## System Component
 - Frontend : HTML, CSS, Bootstrap
 - Backend : Flask, sqlAlchemy
 - Database : google cloud sql (postgreSQL)
 - Service : google map API (Distance Matrix API, Places API)

## Prerequisite
**1. Prepare Python Environment**

Create a virtual environment : 
    
    python -m venv <environment path>

Download library : 

    pip install -r requirement.txt

**2. Create google cloud sql instances**

Read Reference 1, Section : Create and manage---instances.

**3. Setup google map API**

Read [Reference](##Reference) 2, Section : setup.

Read [Reference](##Reference) 3, Section : setup.

## Reference
1. [Use python to connect cloud sql (postgreSQL)](https://cloud.google.com/sql/docs/postgres/connect-connectors?hl=zh-tw)
2. [Distance API document](https://developers.google.com/maps/documentation/distance-matrix)
3. [Place AP document](https://developers.google.com/maps/documentation/places/web-service)

## ER diagram
![ER](./img/ER-diagram.png)

## Relational schema diagram
![Relational](./img/RelationalSchema.png)


## Example
![show](./img/show.PNG)

![park](./img/park.PNG)
# Post trade processing kit

This kit can calculate combined exposure or reconcile order info with Karaken exchange based on an order dump file.

## Docker setup

After building image

`docker build . -t kraken_test`

Launch docker in detach and foreground mode

`docker run -t -d kraken_test`

## Running application

Logon to container

`docker exec -it [container_id] bash`

To calculate the combined exposure based on order input file

`python main.py calcuateExposure --t [PATH TO ORDER FILE]`

---
**NOTE**

If order file is not defined, it will use `data/kraken_tradefile1.csv` by default.

---
To reconcile the order data with exchange

* Configure environment variables `API_KEY` and `API_SECRET`
* `python main.py reconcile --t [PATH TO ORDER FILE]`


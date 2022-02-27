# escalante-flows


## TODO:
- use prefect or cronjob to schedule new data retrieval. (Airflow?)
- data storage? [sqlite on droplet, file w/ append util]

## Design Goals:
- Setup CI with Github actions
- mypy, precommit, black etc.
- codecov


## Goals:
 - Determine the best 5 day interval to do the float in question (meaning of best tbd)
 - target flows: supposed minimum 10-30cfm, 0.7 known minimum
 - Test model on test years (test years tbd)
 - Potentially generalize to other trips
 - calculate drainage basin from input flow gauge and get snotel sites
## data we need:
 - historical usgs gauge data data for escalante (09337500) + more in basin?
 - snotel SWE historical data
 - watershed data?

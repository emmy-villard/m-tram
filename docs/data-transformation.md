# Data Transformation - Explanatory Document
This document outlines the logic behind the transformations and cleansing applied to the data. For each table in the database, I will explain:
1. the source(s)
2. the transformations applied
3. the business rationale for these transformations
4. the assumptions made
5. the expected impact
6. the tests covering the rule

## Dynamic MData (trr, ligne)
1. The data comes from [MData](https://data.mobilites-m.fr/), a collection of datasets related to travel within the Grenoble area. The URLs follow the format 'https://data.mobilites-m.fr/api/dyn/{type}/json'. These dynamic data are updated every 5 minutes or so. Old data is lost if not captured
2. From a messy json, we process the data by keeping only the columns we're interested in: the ID, the date (time), and the traffic level (nsv_id). The traffic level ranges from 1 (smooth) to 4 (at a standstill). A value of 0 means there is no data; therefore, we remove the rows with an nsv_id of 0.
3. row with an nsv_id of 0 are removed because they do not provide any information.
4. I assume that none of the three columns is empty or missing.
5. We end up with a database that tracks how these dynamic data points have changed over time. This historical data is not available anywhere else, making this database the only historical record of traffic trends in the Grenoble area.
6. The exclusion of rows where nsv_id = 0 is tested in the [tests/etl](../tests/etl/transform/) directory, in the transform_{type}_test.py files.

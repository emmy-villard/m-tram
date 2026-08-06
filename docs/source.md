# Sources
This document provides a complete list of the data sources used, along with their terms of reuse.

## Dynamic MData
These data from [MData](https://data.mobilites-m.fr/donnees) are freely available under the [ODbL licence](https://spdx.org/licenses/ODbL-1.0.html#licenseText).

### Urls
- trr : https://data.mobilites-m.fr/api/dyn/trr/json
- ligne : https://data.mobilites-m.fr/api/dyn/ligne/json

### Data description
This data is in JSON format. I use the json key as the ID, as it represents a unique location (tram line, bus line, road section)

The two named fields are "time" (date in milliseconds) and "nsv_id," which represents the traffic level:
- 0 : Information not available
- 1 : Smooth traffic
- 2 : Slow traffic
- 3 : Traffic jam / congestion
- 4 : Closed
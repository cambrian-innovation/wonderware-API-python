# wonderware-API-python
Unofficial Python wrapper for the AVEVA Insight, formerly Wonderware Online InSight, Historian Data REST API. 

Response data is returned as a `pandas` DataFrame for quicker, easier manipulation and analysis. 

Full documentation for the API can be found [here](https://online.wonderware.com/help/#273809.htm).

## Getting Started
### Installation
1.  Fork/Clone/Download this repo:

`https://github.com/dpkilcoyne/wonderware-API-python.git`

2.  Navigate to the directory:

`cd wonderware-API-python`

3. Install the dependencies:

`pip install -r requirements.txt`

### Authentication
1.  From [AVEVA Insight](https://online.wonderware.com), go to [administration portal](https://online.wonderware.com/AdministrationPortal)
then select **REST API** under the **Integration Settings** cell.
2.  Select **Basic Authentication** and copy the endpoint URL.
3.  Enter your endpoint and account credentials into the WonderwareAPI constructor:
```python
from wonderware import WonderwareAPI
endpoint = "YOUR_ENDPOINT"
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
wonderware = WonderwareAPI(endpoint, username, password)
```

## Example Use
More examples can be found in the [examples directory]()
```python
wonderware = WonderwareAPI(endpoint, username, password)
start_time = "2019-11-23T00:00:00.000Z"
end_time = "2019-11-26T00:00:00.000Z"
resolution = 60000
tags = ['YOUR_TAG_1', 'YOUR_TAG_2']

df = wonderware.analog_summary(tags, start_time, end_time, resolution)
wonderware.dir = r'C:\Users\home\target_directory' # Use this directory for the entire project, otherwise, will use working dir
wonderware.save_to_csv(df, 'YOUR_FILENAME.csv')
```

## Current Features
* Analog summary requests
* Process values requests

## Notes
* Historian Data REST API responses are paginated with a maximum of of 5000 records. wonderware-API-python makes all 
the requests from `start_time` to `end_time` and returns a single DataFrame that's appended all the paginated responses.
* DateTime values are formatted as `pandas.Timestamp` objects with ns units.
* All DateTime values are returned in UTC, then non-localized so reading/writing from storage remains consistent.
* `resolution` is in milliseconds. `resolution=86400000` will return data with a resolution of 1 day 
(useful to get the min, max, avg, etc. of the day)

## Contact
Daniel Kilcoyne
[dkilcoyne@cambrianinnovation.com]()

## License
- The source code is licensed under GPL v3. License is available [here](https://github.com/cambrian-innovation/wonderware-API-python/blob/master/LICENSE)
- Copyright 2019 © <a href="https://cambrianinnovation.com/" target="_blank">Cambrian Innovation</a>.

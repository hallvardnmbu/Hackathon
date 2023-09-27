import requests
import pandas as pd


class WeatherData:
    def __init__(self, stations, elements, time, client_id,
                 url='https://frost.met.no/observations/v0.jsonld'):
        """
        Fetch weather data from the Frost API.

        Parameters
        ----------
        stations : list
            List of station IDs.
        elements : list
            List of elements to fetch.
        time : str
            Time to fetch data from.
        client_id : str
            Client ID for the Frost API.
        url : str, optional
            URL to the Frost API.
        """
        self.stations = stations
        self.elements = elements
        self.time = time
        self.client_id = client_id
        self.url = url

        self.data = None
        self.fetch()

    def fetch(self):
        """Fetch weather data."""
        parameters = {
            'sources': ",".join(self.stations),
            'elements': self.elements,
            'referencetime': self.time,
        }

        _response = requests.get(self.url, parameters, auth=(self.client_id, ''))
        response = _response.json()

        self.data = pd.json_normalize(response['data'], record_path='observations',
                                      meta=['sourceId', 'referenceTime'])

    def clean(self, remove=None):
        """
        Remove unnessecary columns of the data.

        Parameters
        ----------
        remove : list, optional
            List of columns to remove.

        Notes
        -----
        The following columns are removed by default:
        - timeSeriesId
        - performanceCategory
        - exposureCategory
        - qualityCode
        - level.unit
        - level.levelType
        - level.value
        """
        if remove is None:
            remove = ["timeSeriesId", "performanceCategory", "exposureCategory",
                      "qualityCode", "level.unit", "level.levelType", "level.value"]
        self.data.drop(columns=remove, inplace=True)

    def save(self, path):
        """Save the data to a CSV file."""
        self.data.to_csv(path, index=False)

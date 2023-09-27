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

    def save(self, path=None):
        """
        Fetch and save the data.

        Parameters
        ----------
        path : str, optional

        Returns
        -------
        data : pd.DataFrame
            The data if no path is given.
        """
        parameters = {
            'sources': ",".join(self.stations),
            'elements': self.elements,
            'referencetime': self.time,
        }

        _response = requests.get(self.url, parameters, auth=(self.client_id, ''))
        response = _response.json()

        data = pd.json_normalize(response['data'], record_path='observations',
                                 meta=['sourceId', 'referenceTime'])

        if path is not None:
            data.to_csv(path, index=False)
            return
        return data

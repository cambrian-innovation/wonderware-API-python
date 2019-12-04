import requests as requests
from requests.auth import HTTPBasicAuth
import os
import numpy as np
import pandas as pd


class WonderwareAPI:
    def __init__(self, endpoint, email, password):
        self.endpoint = endpoint
        self.email = email
        self.password = password
        self.dir = os.getcwd()
        self._df = None
        self._url = None
        self._response = None

    def analog_summary(self, tags, start_time, end_time, resolution):
        tags_string = self._tags_string(tags)
        self._url = "{0}AnalogSummary?$filter={1}'+and+StartDateTime+ge+{2}+and+EndDateTime+le+{3}&RetrievalMode=Cyclic&Resolution={4}"\
            .format(self.endpoint, tags_string, start_time, end_time, resolution)
        return self._wonderware_request()

    def process_values(self, tags, start_time, end_time, resolution, retrieval_mode):
        tags_string = self._tags_string(tags)
        self._url = "{0}ProcessValues?$filter=FQN+eq+'{1}'+and+DateTime+ge+{2}+and+DateTime+le+{3}&RetrievalMode={4}&Resolution={5}"\
            .format(self.endpoint, tags_string, start_time, end_time, retrieval_mode, resolution)
        return self._wonderware_request()

    def _wonderware_request(self):
        '''
        Wonderware Request
        Appends paginated process or analog requests and formats datetime:
        coerce to NaN, drops bad start date rows - FIX, drops tz
        :return: dataframe
        '''
        self._df = pd.DataFrame()
        self._df = self._loop_requests()
        self._df = self._format_datetime(self._df)
        return self._df

    def _loop_requests(self):
        while True:
            self._paginated_request()
            self._df = self._df.append(pd.DataFrame(self._response['value']))
            if '@odata.nextLink' not in self._response:
                break
            else:
                self._url = self._response['@odata.nextLink']
        self._df = self._df.reset_index(drop=True)
        return self._df

    def _paginated_request(self):
        r = requests.get(
            url=self._url,
            auth=HTTPBasicAuth(username=self.email, password=self.password))
        self._response = r.json()
        return self

    def _format_datetime(self, df):
        # Bad date values are coerced, np.nan dropped
        df = df.apply(lambda x: pd.to_datetime(x, errors='coerce') if 'Date' in x.name else x)
        df = df.replace(['NaN', ''], np.nan).dropna(subset=['StartDateTime'])
        df = df.apply(lambda x: x.dt.tz_localize(None) if 'Date' in x.name else x)
        return df

    def _tags_string(self, tags):
        tags_string = "FQN+eq+'"
        if isinstance(tags, str):
            tags_string += tags
        else:
            tags_string += "'+or+FQN+eq+'".join([tag for tag in tags])
        return tags_string

    def save_to_hdf(self, df, filename, directory=None):
        if directory is None:
            directory = self.dir
        return df.to_hdf(os.path.join(directory, filename), key='df')

    def save_to_csv(self, df, filename, directory=None):
        if directory is None:
            directory = self.dir
        return df.to_csv(os.path.join(directory, filename), index=False, na_rep='')

    def load_csv(self, filename, directory=None):
        if directory is None:
            directory = self.dir
        df = pd.read_csv(os.path.join(directory, filename))
        return self._format_datetime(df)
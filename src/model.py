import pandas as pd
import xgboost as xgb
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit


class Model:
    def __init__(self, data_path, price_area="NO2"):
        """
        Initialize the model for predicting spot price.

        Parameters
        ----------
        data_path : str
            Path to the data.
        price_area : str, optional
            Price area to predict.
        """
        self.data = pd.read_csv(data_path)
        self.price_area = price_area

        self.preprocess()

    def preprocess(self):
        """Preprosess the data."""
        drop = {"NO1", "NO2", "NO3", "NO4", "NO5"} - {self.price_area}
        self.data.drop(columns=list(drop), inplace=True)

        self.data.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
        self.data["Date"] = pd.to_datetime(self.data["Date"])

    def validate(self):
        """Check the performance of a simple XGBoostRegressor model. Returns a plot."""
        self.data = self.data.dropna(subset=[self.price_area])
        splitter = TimeSeriesSplit(n_splits=5)

        fig = make_subplots(rows=5, cols=1)
        for i, (train_index, test_index) in enumerate(splitter.split(self.data)):
            train = self.data.iloc[train_index]
            test = self.data.iloc[test_index]

            if len(test) > 24:
                test = test[:24]

            model = xgb.XGBRegressor(objective="reg:squarederror")
            model.fit(train.drop(columns=[self.price_area, "Date"]),
                      train[self.price_area])

            predictions = model.predict(test.drop(columns=[self.price_area, "Date"]))
            error = mean_absolute_error(test[self.price_area], predictions)

            fig.add_trace(
                go.Scatter(x=test['Date'], y=test[self.price_area],
                           name='Actual', row=i + 1))
            fig.add_trace(
                go.Scatter(x=test['Date'], y=predictions,
                           name='Predicted', row=i + 1,
                           line=dict(dash='dash')))
            fig.update_xaxes(tickangle=45, tickformat='%Y-%m-%d %H:%M', row=i + 1, col=1)
            fig.update_yaxes(title_text=self.price_area, row=i + 1, col=1)
            fig.update_layout(title=f"Fold {i + 1} - Mean Absolute Error: {error:.4f}")

        return fig

    def train(self, until=-1):
        """
        Trains a model on the 'whole' dataset and returns it.

        Parameters
        ----------
        until : int, optional
            Index to train the model until.

        Returns
        -------
        xgboost.XGBRegressor
        """
        data = self.data.drop(columns=[self.price_area, "Date"])
        data = data.iloc[:until]
        y = self.data[self.price_area]
        y = y.iloc[:until]

        model = xgb.XGBRegressor(objective="reg:squarederror")
        model.fit(data, y)

        return model

    def predict(self, model=None, startpoint=-1):
        """Returns a plot of the predicted prices."""
        if not model:
            model = self.train(until=startpoint)

        data = self.data.drop(columns=[self.price_area, "Date"])
        data = data.iloc[startpoint:]
        y = self.data[self.price_area]
        y = y.iloc[startpoint:]

        predictions = model.predict(data, y)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=self.data['Date'], y=y,
                       name='Actual'))
        fig.add_trace(
            go.Scatter(x=self.data['Date'], y=predictions,
                       name='Predicted',
                       line=dict(dash='dash')))
        fig.update_xaxes(tickangle=45, tickformat='%Y-%m-%d %H:%M')
        fig.update_yaxes(title_text=self.price_area)
        fig.update_layout(title=f"Predictions from {self.data['Date'].iloc[startpoint]}")

        return fig

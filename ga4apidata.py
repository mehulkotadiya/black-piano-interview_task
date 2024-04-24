# Import modules

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account
import pandas as pd

# Set credentials and define the right GA4 property

credentials = service_account.Credentials.from_service_account_file('/content/gcp-credentials.json') 
client = BetaAnalyticsDataClient(credentials=credentials)
property_id="305482976"

# Get the data from the API

request = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[Dimension(name="city"), Dimension(name="country"),Dimension(name="date")],
    metrics=[Metric(name="totalUsers"), Metric(name="sessions")],
    date_ranges=[DateRange(start_date="2023-09-20", end_date="2024-04-22")],
    )

response = client.run_report(request)

# Turn the raw data into a Table

def ga4_result_to_df(response):
    result_dict = {dimensionHeader.name: [] for dimensionHeader in response.dimension_headers}
    result_dict.update({metricHeader.name: [] for metricHeader in response.metric_headers})

    for row in response.rows:
        for i, dimension_value in enumerate(row.dimension_values):
            dimension_name = response.dimension_headers[i].name
            result_dict[dimension_name].append(dimension_value.value)
        for i, metric_value in enumerate(row.metric_values):
            metric_name = response.metric_headers[i].name
            result_dict[metric_name].append(metric_value.value)

    return pd.DataFrame(result_dict)

df = ga4_result_to_df(response)

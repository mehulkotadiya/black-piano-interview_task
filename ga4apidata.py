# Import modules

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account
import csv

# Set credentials and define the right GA4 property

credentials = service_account.Credentials.from_service_account_file('/content/gcp-credentials.json') 
client = BetaAnalyticsDataClient(credentials=credentials)
property_id="309591865"

# Get the data from the API

try:
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="city"), Dimension(name="country"),Dimension(name="date")],
        metrics=[Metric(name="activeUsers"), Metric(name="sessions")],
        date_ranges=[DateRange(start_date="2023-01-01", end_date="2023-12-31")],
        )
    
    response = client.run_report(request)
    
    # Turn the raw data into a csv file
    
    with open('ga4_data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Writing headers
        headers = [dimension.name for dimension in response.dimension_headers] + [metric.name for metric in response.metric_headers]
        csvwriter.writerow(headers)
        
        # Writing rows
        for row in response.rows:
            dimension_values = [dimension.value for dimension in row.dimension_values]
            metric_values = [metric.value for metric in row.metric_values]
            csvwriter.writerow(dimension_values + metric_values)
except Exception as e:
    print(f"An error occurred while fetching data from the API: {e}"

# Stock Price Streaming and Querying

AWS Kinesis Data Firehose was used with two AWS Lambda functions to stream the stock data 
from Yahoo Finance API for May 14th 2020. The stocks involved were Facebook (FB), 
Shopify (SHOP), Beyond Meat (BYND), Netflix (NFLX), Pinterest (PINS), Square (SQ),
The Trade Dest (TTD), Okta (OKTA), Snap (SNAP), and Datadog (DDOG). The lambda functions are
*data_collector.py*, and *data_transformer.py*, *data_transformer.py* has a API Gateway trigger, 
which can be replaced with CloudWatch Events to stream data periodically. All data was 
delivered to AWS S3 bucket. 

API Gateway trigger:  

https://wqtv96egtc.execute-api.us-east-2.amazonaws.com/default/data_collector

AWS Lambda Function: data_collector

<img src="/img/img1.png" width="400">

AWS Kinesis Delivery Stream Monitoring

<img src="/img/img2.png" width="400">

AWS Athena was used to query the data collected with kinesis. The query was for the 
highest hourly price for each stock (results.csv). 
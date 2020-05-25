import json
import os                                                                                                                                                                    
import subprocess                                                                                                                                                            
import sys                                                                                                                                                                  
from string import Template                                                                                                                                                  
import boto3                                                                                                                                                                
subprocess.check_call([sys.executable, "-m", "pip", "install", "--target",                                                                                                  
"/tmp", 'yfinance'])                                                                                                                                                        
sys.path.append('/tmp')                                                                                                                                                      
import yfinance as yf                                                                                                                                                        
                                                                                                                                                                             
fh = boto3.client("firehose", "us-east-2")                                                                                                                                  
                                                                                                                                                                             
def download_intraday_data(stockname,fromdate,todate):                                                                                                                      
    resp = yf.download(stockname,start=fromdate,end=todate,interval="1m")                                                                                                    
    return resp;                                                                                                                                                            
                                                                                                                                                                             
def push_data_item(jsonData):    
 
    fh.put_record(                                                                                                                                                          
        DeliveryStreamName="datacollector-stream",                                                                                                                          
        Record={"Data": jsonData.encode('utf-8')})                                                                                                                          
                                                                                                                                                                             
def send_stock_kinesis(name):                                                                                                                                                
    print("Downloading Data For "+name)
    stockData= download_intraday_data(name,"2020-05-14","2020-05-15")                                                                                                        
    jsonKinesis=Template('{"high" : $high , "low" : $low, "ts" : "$ts" , "name" :"$stock"}')                                                                                    
    for tick in stockData.itertuples(index=True, name="Pandas"):
        highValue = "%.2f" % tick.High
        lowValue  = "%.2f" % tick.Low
        push_data_item(jsonKinesis.substitute(high=highValue,low=lowValue,ts=tick.Index,stock=name))                                                                        
    return stockData                                                                                                                                                                        
                                                                                                                                                                             
def lambda_handler(event, context):
    # TODO implement
    totalCount = 0
    allStocksForAnalysis = ["FB","SHOP","BYND","NFLX","PINS","SQ","TTD","OKTA","SNAP","DDOG"]
    for stk in allStocksForAnalysis:
        stockData = send_stock_kinesis(stk)
        totalCount = totalCount + len(stockData)
    responseMessage = "Total Count  ::  "+str(totalCount)
    return {
        'statusCode': 200,
        'body': json.dumps(responseMessage)
    }
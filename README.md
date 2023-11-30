# Walmart ETL Pipeline
This project aims to get data from an API, structure it into a table/dataframe, load it into a storage system and then analyze it. Instead of locally running this pipeline, I have deployed it onto Amazon Web Services (AWS), a clould service provider. The reason for doing so is to account for any scalabilioty or flexibility issues. As data always grows more and more, running it on one computer locally becomes a tedious task. The s3 storage buckets as well as the computing engine on AWS (known as EC2) are strongly capable of processing and storing large datasets. This ReadMe file will split the tasks into 3 sections: Extract, Transform, Load to better understand how I used different services to prepare the data for analysis.

## But First, the Data:
The Data used in this project comes from RapidAPI, a publicly available online service for thousands of API's. The one we're interested in for this project is the Axesso - Walmart Data Service 
 




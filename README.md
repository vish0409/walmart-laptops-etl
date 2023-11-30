# Walmart ETL Pipeline

## Summary
This project aims to get data from an API, structure it into a table/dataframe, load it into a storage system and then analyze it. This pipeline is deployed onto Amazon Web Services (AWS), a clould service provider. The reason for doing so is to account for any scalability or flexibility issues that may arise by running it locally on a single computer. As data  grows more and more, running programs on one computer locally becomes a tedious task. The S3 storage buckets as well as the computing engine (known as EC2) on AWS are highly capable for processing and storing large datasets.

## But First, the Data:
The project leverages data sourced from the Axesso - Walmart Data Service API, conveniently hosted on RapidAPI. RapidAPI stands as a widely accessible online platform, providing access to thousands of API's. 
The Axesso - Walmart Data Service provides real time data listed on the **Walmart** website. This includes search results, product information, deals, prices, ratings, reviews and more. For this project, the search results for "Laptops" are extracted from the first 5 pages to determine different measures and dimensions.

## Project Outline:
The steps taken to process and analyze this data will be detailed in three steps: Extract, Transform, Load.

### Extract:
The python script **walmart_etl.py** contains the code necessary to perform the following steps:
 * Request the necessary variables from the API and upload the initial JSON documents into the **walmart-extracted-data** S3 bucket.
 * Transform the JSON documents into a Dataframe and clean the data.
 * Upload the clean data onto the **walmart-transformed-data** bucket as a .csv file.

This script will run on the AWS EC2 engine using the Command Line Interface (the **ec2.sh** shell script demonstrates this). Exeption Handling is imbedded into the script to account for any errors that may come up. 





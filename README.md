# Walmart ETL Pipeline

## Summary
This project aims to get data from an API, structure it into a table/dataframe, load it into a storage system and then analyze it. This pipeline is deployed onto Amazon Web Services (AWS), a clould service provider. The reason for doing so is to account for any scalability or flexibility issues that may arise by running it locally on a single computer. As data  grows more and more, running programs on one computer locally becomes a tedious task. The S3 storage buckets as well as the computing engine (known as EC2) on AWS are highly capable for processing and storing large datasets.

## But First, the Data:
The project leverages data sourced from the Axesso - Walmart Data Service API, conveniently hosted on RapidAPI. RapidAPI stands as a widely accessible online platform, providing access to thousands of API's. 
The Axesso - Walmart Data Service provides real time data listed on the **Walmart** website. This includes search results, product information, deals, prices, ratings, reviews and more. For this project, the search results for "Laptops" are extracted from the first 5 pages to determine different measures and dimensions.

## Project Goals &  Outline:
The goal of this project is to see what Laptops from Walmart are popular and in demand with regards to their **brand, price, ratings and savings**.Running this pipeline frequently will let us know any real-time shifts in customer preferences.
The methods taken to process and analyze the data will be detailed in three steps : Extract, Transform, Load.


### Extract:
The python script **walmart_etl.py** contains the code necessary to perform the following steps:
 * Request the necessary variables from the API and upload the initial JSON documents into the **walmart-extracted-data** S3 bucket.
 * The variables extracted are: **Item Id & US Item Id, Product Name, Flag, Current & Previous Price, Savings, Seller  Id & Name, Offer Count, Average Rating, Number of Reviews, Product Variants, Brand**
 * Transform the JSON documents into a Dataframe and clean the data.
 * Upload the cleaned table, **transformed_laptop_data.csv**, onto the **walmart-transformed-data** bucket

*NOTE:This script will run on the AWS EC2 engine using the Command Line Interface (the **ec2.sh** shell script demonstrates this). Exception Handling is imbedded into the script to account for any errors that may come up.* 


### Transform:
The Transformation is done on AWS Glue, an event-driven ETL Service. Two components of the AWS Glue service are used for this project: **Glue Data Catalog** (which contains Glue Crawlers and Databases) & **Glue ETL Jobs**. 
The crawlers are useful for importing data from S3 buckets into the data catalog databses. Whereas, the ETL Jobs are made to adjust datatypes, schema and drop any unnecessary columns. 

  * The **s3-to-walmart-laptops**  Glue Crawler takes the .csv file from the previous step and uploads it onto a database named **walmart-laptops**
  * The ETL Glue Job is then designed to source the table from the database, adjust necessary datatypes and **drop** the following columns: *Seller Id* and *Product Variants*. After which, it uploads the transformed dataset into the **walmart-output-data** S3 bucket. It is exported as a CSV using GZIP compression. 
  

### Load:
The Loading section is triggered with another Crawler, which is set up to take the CSV file from the walmart-output-data bucket and upload it onto the **walmart-laptops-clean** database.
This database is then used in AWS Athena, a service that helps us analyze data suing SQL. All query results are saved in the **walmart-output-data** S3 bucket.

*NOTE: The queries performed can be found in the athena_sql_queries.txt file*

## Findings:
As of **December 2023**, the insights gained from the first 5 pages of search results for Laptops on the Walmart onine retail store are:
 * **Basic Statistics:-** Average Price: $465; Max Price: $2009; Average savings: $87; Max savings: $1140; Average rating: 3.5
 * **Brand and Rating Analysis:**
     * Most number of laptops: HP (30% of laptops were from this brand)
     * Highest average price: MSI
     * Highest savings: SGIN
     * Top brands (with a rating of 3.8 or higher) include: HP, Lenovo, SGIN,Windows, MSI, Asus and Dell.
  * **Price and Savings Analysis**:
     * 72% of laptops are prices below $500
     * Samsung laptops are the most frequent when the price is between >$500 but <$1000
     * MSI laptops are the most frequent when the price is >$1000
     * The average savings are >$100 when the laptops are price >$700
     * SGIN Official Store seller had the most savings, summing upto $4620 with an average price of $311
     * The official Walmart seller was the 4th highest in terms of savings, with the savings summing upto $1500 and an average price of $394
     * The Black Friday deal offered the highest savings (total sum: $3345) and showed up for 20 laptops in total.
     * However, the Flash Deal offered the highest average savings (average: $430).
       
   *NOTE: The points mentioned above are subjected to change with time*

## References:
The following two articles have been used to gain basic knowledge of the services offered by AWS for this project:
https://medium.com/@aimee.tang0317/beginners-guide-to-aws-how-to-run-a-python-script-stored-in-s3-on-ec2-f05730c500e7

https://medium.com/@aimee.tang0317/how-to-create-a-powerful-etl-data-pipeline-with-python-and-aws-services-6ad8ddd7ca1b








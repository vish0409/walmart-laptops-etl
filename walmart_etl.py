import requests
import pandas as pd
import json
import boto3

# EXTRACT

def upload_data(url, headers, params, bucket_name, s3_key):
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Checking for HTTP errors

        if response.status_code == 200:
            response_data = response.json()
            s3_client = boto3.client('s3',
            aws_access_key_id="########",aws_secret_access_key="######")  # Initialize the S3 client

            # Uploading the JSON data to a S3 bucket
            s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=json.dumps(response_data, indent=4).encode('utf-8')
            )

            print(f'Successfully uploaded data to S3://{bucket_name}/{s3_key}')
        else:
            print(f'Error: Status code {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

def get_data(bucket_name,page_num):
	url = "https://axesso-walmart-data-service.p.rapidapi.com/wlm/walmart-search-by-keyword"

	querystring = {"keyword":"laptops","page":page_num,"sortBy":"best_seller"}

	headers = {
		"X-RapidAPI-Key": "##########",
		"X-RapidAPI-Host": "axesso-walmart-data-service.p.rapidapi.com"
	}
	s3_key = f'laptops_{page_num}.json'
	upload_data(url, headers, querystring, bucket_name, s3_key)

s3_bucket_name="walmart-extracted-data"
for page in range(1,6):
	get_data(s3_bucket_name,page)
     
def extract_data(data):
    #Getting to the nested "items" key that contains all the variables
    item = data.get('item', {})
    props = item.get('props', {})
    page_props = props.get('pageProps', {})
    initial_data = page_props.get('initialData', {})
    search_result = initial_data.get('searchResult', {})
    item_stacks = search_result.get('itemStacks', [])
    items=item_stacks[0].get('items',[])
    lst = []

    # Getting all the necessary variables
    for item in items:
        info_dict = {}
        
        # Item info
        info_dict['item_id'] = item.get('id')
        info_dict['usItemId'] = item.get('usItemId')
        info_dict['name'] = item.get('name')
        info_dict['availability'] = item.get('availabilityStatusDisplayValue')
        info_dict['out_of_stock'] = item.get('isOutOfStock')
        info_dict['flag']=item.get('flag',"")
        
        # Price info
        info_dict['current_price'] = item.get('price')
        price_info = item.get("priceInfo")  # Get the "priceInfo" dictionary or None if it doesn't exist
        info_dict['previous_price'] = price_info.get('wasPrice', '') if price_info else ''
        info_dict['savings'] = price_info.get('savingsAmt') if price_info else 0
    
        # Seller info
        info_dict['seller_id'] = item.get("sellerId")
        info_dict['seller_name'] = item.get("sellerName")
        info_dict['unit_type'] = item.get("salesUnitType")
        info_dict['offer_count'] = item.get("additionalOfferCount", 0)
        
        # Ratings info
        ratings = item.get('rating')
        info_dict['avg_rating'] = ratings.get('averageRating') if ratings else 0
        info_dict['reviews'] = ratings.get('numberOfReviews') if ratings else 0
        
        # Variants
        variants_lst=item.get("variantList")
        if variants_lst is not None:
            info_dict['variant_1']=variants_lst[0].get('name',"") if variants_lst else ""
            info_dict['variant_2']=variants_lst[1].get('name',"") if variants_lst else ""
            if len(variants_lst) > 2:
                    info_dict['variant_3'] = variants_lst[2].get('name', "")
            else:
                info_dict['variant_3'] =""
        else:
                info_dict['variant_1'] = ""
                info_dict['variant_2'] = ""
                info_dict['variant_3'] = ""

        lst.append(info_dict)
    df=pd.DataFrame(lst)
    return df

# Getting the data for all the 5 pages
data_pages=[]

s3_client = boto3.client('s3',aws_access_key_id="##########",aws_secret_access_key="######")

for i in range(1,6):
    filename=f'laptops_{i}.json'
    s3_client.download_file("walmart-extracted-data",filename,filename)

    with open(filename,'r') as laptops:
        data_page=json.load(laptops)
        data_pages.append(data_page)


df_page1=extract_data(data=data_pages[0])
df_page2=extract_data(data=data_pages[1])
df_page3=extract_data(data=data_pages[2])
df_page4=extract_data(data=data_pages[3])
df_page5=extract_data(data=data_pages[4])

# Creating a DataFrame that contains the raw data from all pages
final_df = pd.concat([df_page1, df_page2, df_page3, df_page4, df_page5], ignore_index=True)
print("Final df created successfully")

# TRANSFORM
def transform(table):
    try:
        table['offer_count'] = table['offer_count'].fillna(0)
    except Exception as e:
        print(f"Error in offer_count and previous_price transformation: {e}")

    try:
        table[['avg_rating', 'reviews']] = table[['avg_rating', 'reviews']].astype(float)
    except Exception as e:
        print(f"Error in avg_rating and reviews transformation: {e}")

    try:
        table['variants'] = table['variant_1'] + ',' + table['variant_2'] + ',' + table['variant_3']
        table['variants'] = table['variants'].str.rstrip(",")
    except Exception:
        print("Error in variants transformation: variants_1 column does not exist or has been dropped")

    try:
        table['previous_price'] = pd.to_numeric(table['previous_price'].str.replace('$', ''), errors='coerce')
        table['previous_price'] = table['previous_price'].fillna(0)
    except Exception:
        print("Error in previous_price transformation: previous_price column has already been transformed")

    try:
        table.drop(columns=['unit_type', 'out_of_stock', 'availability', 'variant_1', 'variant_2', 'variant_3'], inplace=True)
    except Exception:
        print("Error in dropping columns: Columns already dropped")

    try:
        table['brand'] = table['name'].str.split().str.get(0)
        table.loc[table['brand'] == '15.6"','brand'] = 'KUU'
        table.loc[table['brand'] == '2023','brand'] = 'ASUS'
        table.loc[table['brand'] == 'Newest','brand'] = 'HP'
        table.loc[table['flag']=="",'flag']="None"

    except Exception as e:
        print(f"Error in brand transformation: {e}")
    
    try:
        table['name']=table['name'].str.split(',').str[0]
    except:
        print(f"Error in brand name column: {e}")

    return table


# LOAD

new_table=transform(final_df)
new_table['name']=new_table['name'].str.replace('"','') #to avoid any quote related issues 
walmart_csv=new_table.to_csv(index=False)
s3_client.put_object(Body=walmart_csv,Bucket="walmart-transformed-data",Key="transformed_laptop_data.csv")
print("File uploaded successfully")
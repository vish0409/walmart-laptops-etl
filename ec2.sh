sudo su
sudo yum update
yum install python3-pip
python3 pip install pandas
python3 pip install requests
python3 pip install json
python3 pip install boto3
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws s3 cp s3://walmart-extracted-data/walmart_etl.py ./walmart_etl.py
python3 walmart_etl.py

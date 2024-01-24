# @Author Satish Utnal

import os
import time
import directory_setup as ds
from dataquality_check import rule_validation as val
import datetime as dt
import csv
import shutil as cp
import smtplib

def get_orders(file, src_file_path, order_schema):
    dict_order = {}
    with open(src_file_path + file, mode='r') as src_csv_file:
        header = src_csv_file.readline().strip('\n')
        header = header.split(',')
        header.sort()
        order_schema.sort()
        if header == order_schema:  # proceed to process only if required schema present
            for src_rows in src_csv_file:
                row_data = src_rows.split(",")
                dict_order.update({row_data[0]: {"order_date": row_data[1], "product_id": row_data[2],
                                                 "quantity": row_data[3], "sales": row_data[4],
                                                 "city": row_data[5].replace('\n', ''), "file_name": file}})
        else:
            print(f"Required schema is not present for file : {file} ")
    return dict_order


def get_products(file, src_file_path, product_schema):
    dict_product = {}
    with open(src_file_path + file, mode='r') as src_csv_file:
        header = src_csv_file.readline().strip('\n').split(',')
        header.sort()
        product_schema.sort()
        if header == product_schema:
            for src_rows in src_csv_file:
                row_data = src_rows.split(",")
                dict_product.update({row_data[0]: {"product_name": row_data[1], "price": row_data[2],
                                                   "category": row_data[3].replace('\n', '', )}})
        else:
            print(f"Required schema is not present for file : {file} ")
    return dict_product

def sendmail(sndr, rcvr, pswd, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sndr, pswd)
        server.sendmail(sndr, rcvr, msg)
    except Exception as e:
        print(f"Enter Valid EMail details to receive the mail failed with Exception {e}")



ds.create_dir() # create required directory structure
src_file_path = 'incoming_files/' + dt.datetime.now().strftime('%Y%m%d') + '/'
rej_file_path = 'rejected_files/'  + dt.datetime.now().strftime('%Y%m%d') + '/'
success_file_path = 'success_files/' + dt.datetime.now().strftime('%Y%m%d') + '/'
file_list = os.listdir(src_file_path)
EMAIL_SENDER = 'abc@gmail.com'  # Required Valid email id to run this code
EMAIL_PASSWORD = input(f"Enter password for {EMAIL_SENDER} : ")
EMAIL_RECIEVER = EMAIL_SENDER  # Required Valid email id to send mail
try:
    file_list.remove("product_master.csv")
except ValueError:
    print("Product master file required to proceed")
    exit()
file_list_orders = file_list
file_list_products = 'product_master.csv'
order_schema=['order_id','order_date','product_id','quantity','sales','city']
product_schema=['product_id','product_name','price','category']
if len(file_list) >= 1 and os.path.exists(src_file_path+'product_master.csv'):
    for file in file_list:
        dict_orders = get_orders(file, src_file_path,order_schema)
        dict_products = get_products(file_list_products, src_file_path,product_schema)
        rej_dict = {}
    if len(dict_orders) >= 1 and len(dict_products) >= 1:
        rej_dict = val.check_product_id(dict_orders, dict_products, rej_dict)  # Business rule 1- product id should be present in product master table
        rej_dict = val.check_sales_amt(dict_orders, dict_products, rej_dict) # Business rule 2- total sales amount should be (product price from product master table * quantity)
        rej_dict = val.check_future_orders(dict_orders, rej_dict) # Business rule 3- the order date should not be in future
        rej_dict = val.check_empty_fields(dict_orders, rej_dict) # Business rule 4- any field should not be empty
        order_city = ['Bangalore', 'Mumbai']
        rej_dict = val.check_order_city(dict_orders, order_city, rej_dict) # Business rule 5- The orders should be from Mumbai or Bangalore only.
        if len(rej_dict) >= 1:
            with open(rej_file_path + "error_"+file, "w", newline="") as fp:
                fields = ['order_id', 'order_date', 'product_id', 'quantity', 'sales', 'city', 'Error']
                writer = csv.writer(fp)
                writer.writerow(['order_id', 'order_date', 'product_id', 'quantity', 'sales', 'city', 'Error'])
                for row in rej_dict:
                    line = row, rej_dict[row]['order_date'], rej_dict[row]['product_id'], rej_dict[row]['quantity'], \
                        rej_dict[row]['sales'], rej_dict[row]['city'], rej_dict[row]['Error']
                    writer.writerow(line)
                cp.copy(src_file_path+file, rej_file_path+file)
        else:
            cp.copy(src_file_path+file,success_file_path+file)
    print(f'Data quality check completed for the files received')


else:
    if len(file_list) < 1:
        print(f" Required order and product master files not exists in path : {src_file_path}")
        exit()
    else:
        pass

try:
    subject = 'validation email '+ dt.datetime.now().strftime('%Y-%m-%d')

    count=0
    for file in file_list:
        if file in os.listdir(rej_file_path):
           count = count + 1
    body = f' Total {len(file_list)} incoming files, {len(os.listdir(success_file_path))} successful files and {count} rejected files for the day'
    msg = f'Subject : {subject}\n\n {body}'
    sendmail(EMAIL_SENDER, EMAIL_RECIEVER, EMAIL_PASSWORD, msg)
finally:
    print(f'Completed execution')

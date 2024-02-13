"""

main module script for performing some data quality tests the files from /data/incoming_files

"""

import os
import datetime as dt
import logging
import sys
import pandas as pd
import configparser
import validate_business_rule as br
import shutil
import subprocess


if __name__ == "__main__":
    folder_suffix = dt.datetime.utcnow().strftime('%Y%m%d')
    file_suffix = dt.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    EXIT_CODE = False
    SUCCESS_COUNTER = 0
    FAILED_COUNTER = 0
    CURRENT_DATE = dt.datetime.utcnow().strftime('%Y-%m-%d')
    config = configparser.ConfigParser()
    config.read('../config/config.ini')
    paths = config['Schema']
    order_schema = paths['order_file']
    product_schema = paths['product_file']
    order_schema = order_schema.split(',')
    file_stat = {}
    logging.basicConfig(filename='../logs/data_quality_' + file_suffix + '.log',
                        encoding='utf-8', level=logging.DEBUG)
    try:
        output = subprocess.check_output(['python', '../utility/setup_project_structure.py'])
        logging.info(f"{dt.datetime.utcnow()} : {output}")
    except Exception as e:
        logging.error(f"{dt.datetime.utcnow()} : {e.output}")

    """
    Do not make changes to the order of required_folders list content, append for any new enhancement
    """
    required_folders = [
        '../data',
        '../data/incoming_files/' + folder_suffix,
        '../data/rejected_files/' + folder_suffix,
        '../data/success_files/' + folder_suffix,
        '../logs'
    ]
    for folder in required_folders:
        if not os.path.isdir(folder):
            logging.error(f"{dt.datetime.utcnow()} : Required directory structure not found to proceed execute "
                          f"file_validations/utility/setup_project_structure.py and place files to proceed")
            EXIT_CODE = True
    if EXIT_CODE:
        logging.info("Exiting the program due to missing required folders.")
        sys.exit()
    raw_files = os.listdir(required_folders[1])
    if len(raw_files) == 0:
        logging.error(f"{dt.datetime.utcnow()} : At-least single file required to proceed "
                      f"make sure files are present at {required_folders[1]}")
        EXIT_CODE = True
        sys.exit()
    if not os.path.exists(required_folders[0] + '/product_master.csv'):
        logging.error(f"{dt.datetime.utcnow()} : product master file not found at {required_folders[0]}")
        EXIT_CODE = True
        sys.exit()
    pd.options.display.width = None
    pd.options.display.max_rows = 10
    product_master = pd.read_csv(required_folders[0] + '/product_master.csv')
    for raw_file in raw_files:
        order_raw = pd.read_csv(required_folders[1]+'/'+raw_file)
        if not br.validate_schema(order_raw.columns.to_list(), order_schema):
            logging.error(f"{dt.datetime.utcnow()} : Failed to process the file {raw_file} schema not matched"
                          f" Expected schema {order_schema} and actual schema is {order_raw.columns.values}")
            file_stat['Failed'] = FAILED_COUNTER + 1
            continue
        product_order = pd.merge(left=order_raw, right=product_master, on="product_id", how='left')
        product_order["order_date"] = pd.to_datetime(product_order["order_date"], format='%d/%m/%Y')
        product_order = br.product_id_check(product_order)
        product_order = br.sales_amount_check(product_order)
        product_order = br.order_date_check(product_order, CURRENT_DATE)
        product_order = br.null_check(product_order)
        product_order = br.order_city_check(product_order)
        error_cols = product_order.filter(like='error_reason_')
        error_cols = error_cols.astype(str)
        product_order['conError'] = error_cols.apply(lambda x: ','.join(x), axis=1)
        product_order.drop(error_cols.columns, axis=1, inplace=True)
        product_order['conError'] = product_order['conError'].str.replace('nan,', '')
        product_order['conError'] = product_order['conError'].str.replace(',nan', '')
        product_order['conError'] = product_order['conError'].str.replace('nan', '')
        product_order['conError'] = product_order['conError'].str.strip()
        order_failed = product_order[product_order['conError'].str.len() != 0]
        if not order_failed.empty:
            order_failed.to_csv(required_folders[2]+'/error_'+raw_file, index=False)
            shutil.copy2(required_folders[1]+'/'+raw_file, required_folders[2]+'/')
            os.remove(required_folders[1] + '/' + raw_file)
        else:
            shutil.copy2(required_folders[1] + '/' + raw_file, required_folders[3] + '/')
            os.remove(required_folders[1] + '/'+raw_file)

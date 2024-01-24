import time
import datetime as dt


def check_product_id(src_dict, lkp_dict, rej_dict):
    for src_key, src_val in src_dict.items():
        if not src_dict[src_key]['product_id'] in lkp_dict.keys():
            rej_dict[src_key] = src_dict[src_key].copy()
            rej_dict.setdefault(src_key, {}).setdefault('Error', 'Product key not found')
    return rej_dict


def check_sales_amt(src_dict, lkp_dict, rej_dict):
    for src_key, src_val in src_dict.items():
        if src_dict[src_key]['product_id'] in lkp_dict.keys():
            if not float(int(src_dict[src_key]['quantity']) * float(
                    lkp_dict[src_dict[src_key]['product_id']]['price'])) == float(src_dict[src_key]['sales']):
                rej_dict[src_key] = src_dict[src_key].copy()
                rej_dict.setdefault(src_key, {}).setdefault('Error', 'Sales amount not matched')
    return rej_dict


def check_future_orders(src_dict, rej_dict):
    for src_key, src_val in src_dict.items():
        if time.strptime(src_dict[src_key]['order_date'], "%d/%m/%Y") > time.strptime(
                dt.datetime.now().strftime('%d/%m/%Y'), "%d/%m/%Y"):
            try:
                if 'Error' in rej_dict[src_key].keys():
                    error_message = rej_dict[src_key]['Error'] + ', order date is future'
                    rej_dict[src_key]['Error'] = error_message
                else:
                    rej_dict[src_key] = src_dict[src_key].copy()
                    rej_dict.setdefault(src_key, {}).setdefault('Error', 'order date is future')
            except KeyError:
                rej_dict[src_key] = src_dict[src_key].copy()
                rej_dict.setdefault(src_key, {}).setdefault('Error', 'order date is future')
    return rej_dict


def check_order_city(src_dict, order_city, rej_dict):
    for src_key, src_val in src_dict.items():
        if src_dict[src_key]['city'] not in order_city:
            try:
                if 'Error' in rej_dict[src_key].keys():
                    error_message = rej_dict[src_key]['Error'] + ', orders should be from Mumbai or Bangalore only'
                    rej_dict[src_key]['Error'] = error_message
                else:
                    rej_dict[src_key] = src_dict[src_key].copy()
                    rej_dict.setdefault(src_key, {}).setdefault('Error',
                                                                'orders should be from Mumbai or Bangalore only')
            except KeyError:
                rej_dict[src_key] = src_dict[src_key].copy()
                rej_dict.setdefault(src_key, {}).setdefault('Error', 'orders should be from Mumbai or Bangalore only')
    return rej_dict


def check_empty_fields(src_dict, rej_dict):
    for src_key, src_val in src_dict.items():
        if len(src_dict[src_key]['order_date']) == 0:
            rej_dict[src_key] = src_dict[src_key].copy()
            try:
                error_message = rej_dict[src_key]['Error'] + ', order_date field should not be null'
                rej_dict[src_key]['Error'] = error_message
            except KeyError:
                rej_dict.setdefault(src_key, {}).setdefault('Error', 'order_date field should not be null')
        if len(src_dict[src_key]['product_id']) == 0:
            rej_dict[src_key] = src_dict[src_key].copy()
            try:
                error_message = rej_dict[src_key]['Error'] + ', product_id field should not be null'
                rej_dict[src_key]['Error'] = error_message
            except KeyError:
                rej_dict.setdefault(src_key, {}).setdefault('Error', 'product_id field should not be null')
        if len(src_dict[src_key]['quantity']) == 0:
            rej_dict[src_key] = src_dict[src_key].copy()
            try:
                error_message = rej_dict[src_key]['Error'] + ', quantity field should not be null'
                rej_dict[src_key]['Error'] = error_message
            except KeyError:
                rej_dict.setdefault(src_key, {}).setdefault('Error', 'quantity field should not be null')
        if len(src_dict[src_key]['sales']) == 0:
            rej_dict[src_key] = src_dict[src_key].copy()
            try:
                error_message = rej_dict[src_key]['Error'] + ', sales field should not be null'
                rej_dict[src_key]['Error'] = error_message
            except KeyError:
                rej_dict.setdefault(src_key, {}).setdefault('Error', 'sales field should not be null')
        if len(src_dict[src_key]['city']) == 0:
            rej_dict[src_key] = src_dict[src_key].copy()
            try:
                error_message = rej_dict[src_key]['Error'] + ', city field should not be null'
                rej_dict[src_key]['Error'] = error_message
            except KeyError:
                rej_dict.setdefault(src_key, {}).setdefault('Error', 'city field should not be null')
    return rej_dict

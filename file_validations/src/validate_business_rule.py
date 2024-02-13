"""
Given set of files this module helps to validate below-mentioned business rules

1- product id should be present in product master table

2- total sales amount should be (product price from product master table * quantity)

3- the order date should not be in future

4- any field should not be empty

5- The orders should be from Mumbai or Bangalore only.

"""


def validate_schema(input_file_schema, required_schema):
    if input_file_schema == required_schema:
        return True
    else:
        return False


def product_id_check(product_order):
    product_order.loc[product_order["product_name"].isna(), "error_reason_pid"] = 'Product_id not found'
    return product_order


def sales_amount_check(product_order):
    product_order.loc[product_order["price"] * product_order["quantity"] !=
                      product_order["sales"], "error_reason_amt"] = 'Amount not matched'
    return product_order


def order_date_check(product_order, CURRENT_DATE):
    product_order.loc[product_order["order_date"] > CURRENT_DATE, "error_reason_date"] = 'order date is future'
    return product_order


def null_check(product_order):
    product_order.loc[
        product_order["order_id"].isnull() |
        product_order["order_date"].isnull() |
        product_order["product_id"].isnull() |
        product_order["quantity"].isnull() |
        product_order["sales"].isnull() |
        product_order["city"].isnull(), "error_reason_null"] = 'Null in field'
    return product_order


def order_city_check(product_order):
    product_order.loc[(product_order["city"].str.lower() != 'mumbai') &
                      (product_order["city"].str.lower() != 'bangalore'), "error_reason_city"] = 'invalid city name'
    return product_order

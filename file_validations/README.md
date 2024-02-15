# About Project Description

Assume there is an online shopping mall, and every day, all transaction/order files are generated and delivered to you for validation.
You must verify all files and tell the business if there are any issues.


Read all the files from current date folder data/incoming_files-/YYYYMMDD

My project's folders will have directories with "config, data, logs, scripts, src, utility



## Business use cases 

1. The product ID should be present in the product master table.
2. The total sales amount should be (product price from product master table * quantity).
3. The order date should not be in the future.
4. Any field should not be empty.
5. Orders should only come from Mumbai or Bangalore.

## Main file of the project

executing Main file for the project is :- [file_validations/src/data_quality.py]

Files with no difficulties should go to the data>success_files->YYYYMMDD folder. 
If any single order validation fails, the entire file should be denied and moved to the data->rejected_files->YYYYMMDD folder. 
For each rejected file, create a new file in the data->rejected_files->YYYYMMDD folder with the name error_{rejected_file_name}. 
This file should only contain order records that failed validation, with an additional column for each record describing the reason for rejection.
If there are more than one cause for rejecting a certain order, both should be there, separated.


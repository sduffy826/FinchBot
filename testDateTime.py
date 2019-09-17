import datetime
some_datetime_obj = datetime.datetime.now()  # Store current datetime
datetime_str = some_datetime_obj.isoformat()  # Convert to ISO 8601 string
print(datetime_str)  # Print the string
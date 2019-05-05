"""
# Let's Build a Vendor Availability system

## Problem

We need to know if a vendor (restaurant) is available to deliver a meal. 
So given a list of upcoming meals, build a function that will tell us if 
the vendor (restaurant) is available to take the order.

## Requirements

- input: take a vendor_id and a date
- output: True if the vendor is available, False if not
- A vendor is available if:
  - They have enough drivers for a concurrent delivery
  - As long as the delivery blackout period doesn't overlap (30 minutes before, 10 minutes after)
"""
import pytest
from datetime import datetime

# A list of meals to be delivered
meals = {
    "results": [
    {
        "vendor_id": 1,                    # Vendor 1 will be serving
        "client_id": 10,                   # Client 10 on
        "datetime": "2017-01-01 13:30:00"  # January 1st, 2017 at 1:30 pm
    },
    {
        "vendor_id": 1,
        "client_id": 40,
        "datetime": "2017-01-01 14:30:00"
    },
    {
        "vendor_id": 2,
        "client_id": 20,
        "datetime": "2017-01-01 13:30:00"
    }
  ]
}

# Driver information per vendor.
vendors = {
    "results": [
    {
        "vendor_id": 1,
        "drivers": 1
    },
    {
        "vendor_id": 2,
        "drivers": 3
    }
  ]
}



# you can write the function here.
def is_vendor_available(vendor_id, date_time):

  _vendor = list(filter(lambda v : True if v['vendor_id'] == vendor_id else False, vendors['results']))

  if len(_vendor) != 1 or _vendor[0]['drivers'] < 1: 
    return False

  _meal_delivery_dates = []
  for m in meals['results']:
    if m['vendor_id'] == vendor_id :
      _meal_delivery_dates.append(datetime.timestamp(datetime.strptime(m['datetime'], '%Y-%m-%d %H:%M:%S')))

  _unix_time = datetime.timestamp(datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S'))

  if len(_meal_delivery_dates) == 0 :
    return True
  if _meal_delivery_dates.count(_unix_time) > 0 and _meal_delivery_dates.count(_unix_time) + 1 > _vendor[0]['drivers'] :
    return False

  _meal_delivery_dates.sort()
  _len = len(_meal_delivery_dates)

  # finding the time range and calculating blackout period overlap
  for t in range( _len ):
    if _unix_time > _meal_delivery_dates[t] :
      if t+1 == _len : # at end of list
        if _unix_time-1800 > _meal_delivery_dates[t]+600 :
          return True
        else :
          return False
      elif _unix_time < _meal_delivery_dates[t+1] :
        if _unix_time-1800 > _meal_delivery_dates[t]+600 and _unix_time + 600 < _meal_delivery_dates[t+1]-1800 :
          return True
        else :
          return False
    else: # at t = 0
      if _unix_time + 600 < _meal_delivery_dates[t]-1800 :
        return True
      else :
        return False

  return True
  





"""
Here's some tests to get you started
"""
def test_unavailable_vendor():
    assert is_vendor_available(1, "2017-01-01 14:30:00") == False
    assert is_vendor_available(1, "2017-01-01 14:40:00") == False
    assert is_vendor_available(1, "2017-01-01 14:50:00") == False
    assert is_vendor_available(1, "2017-01-01 15:00:00") == False
    
def test_available_vendor():
    assert is_vendor_available(1, "2017-01-02 14:30:00") == True
    assert is_vendor_available(1, "2017-01-01 15:11:00") == True

"""
Sanity tests
""" 
def test_exceptions_get_caught():
    with pytest.raises(Exception) as e_info:
        x = 1 / 0

def test_sanity():
    assert 2 + 2 == 4
    
pytest.main()


from __future__ import absolute_import
from django import template  
import time
import datetime 
register = template.Library()    

@register.filter('timestamp_to_time')
def convert_timestamp_to_time(timestamp):
 
    return datetime.date.fromtimestamp(int(timestamp))
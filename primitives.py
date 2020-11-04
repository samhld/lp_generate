import random
import string
import datetime

letters = string.ascii_lowercase

def _gen_string(num):
    result_str = ''.join(random.choice(letters) for i in range(num))
    return(result_str)

def _gen_int(num):
    lower_bound = 10 ** (num - 1)
    upper_bound = 10 ** num - 1
    return(random.randint(lower_bound,upper_bound))

def gen_tag(tag_key_size, tag_value_size):
    # return string Tag key-value pair
    key = 'tag_' + _gen_string((tag_key_size-4))
    val = _gen_string(tag_value_size)
    pair = f",{key}={val}"
    return(pair)

def gen_str_field(field_key_size, field_value_size):
    # return string Tag key-value pair
    key = 'str_' + _gen_string(field_key_size-4)
    val = _gen_string(field_value_size)
    pair = f",{key}='{val}'"
    return(pair)

def gen_int_field(field_key_size, int_value_size):
    # return int Field key-value pair
    key = 'int_' + _gen_string(field_key_size-4)
    val = _gen_int(int_value_size)
    pair = f",{key}={val}i"
    return(pair)

def gen_float_field(field_key_size, float_value_size):
    # return float Field key-value pair
    key = 'fl_' + _gen_string(field_key_size-3)
    val = round(random.uniform(10,99), float_value_size-2)
    pair = f",{key}={val}"
    return(pair)

def gen_ts(precision = 's'):
    now  = datetime.datetime.now()
    ts = now.timestamp()
    if precision == ('s' or 'S'):
        ts = round(ts)
        return(ts*1000000000)
    elif precision == ('ms' or 'MS'):
        ts = round(ts*1000)
        return(ts*1000000)
    elif precision == ('us' or 'US'):
        ts = round(ts*1000000)
        return(ts*1000)
    elif precision == ('ns' or 'NS'):
        ts = round(ts*1000000000)
        return(ts)
    else:
        print("Warn: gen_ts() only takes `s`, `ms`, `us`, or `ns` as inputs")
        return ts
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

def gen_tag_key(tag_key_size, key=''):
    '''
    Generates a string that will be a Tag key in a LP line.
    The `key` argument determines if the key has already been set
    or if this function should create it.
    '''
    if key:
        held_key = 'tag_' + key
        held_key = held_key[:-4]
        return held_key
    else:
        key = 'tag_' + _gen_string((tag_key_size-4))
        return key

def gen_tag_value(tag_value_size, val=''):
    '''
    Generates a Tag value.  Behaves like `gen_tag_key`.
    '''
    if val:
        held_val = val
        return held_val
    else:
        val = _gen_string((tag_value_size))
        return val

def gen_str_field(field_key_size, field_value_size, key=''):
    '''
    Generates string key-value pair that will be a Field in a LP line.
    '''
    if key:
        held_key = 'str_' + key
        held_key = held_key[:-4]
        val = _gen_string(field_key_size)
        pair = f',{held_key}="{val}"'
    else:
        key = 'str_' + _gen_string(field_key_size-4)
        val = _gen_string(field_value_size)
        pair = f',{key}="{val}"'

    return(pair)

def gen_int_field(field_key_size, int_value_size, key=''):
    '''
    Generates int key-value pair that will be a Field in a LP line
    '''
    if key:
        held_key = 'int_' + key
        held_key = held_key[:-4]
        val = _gen_int(int_value_size)
        pair = f",{held_key}={val}"
    else:
        key = 'int_' + _gen_string(field_key_size-4)
        val = _gen_int(int_value_size)
        pair = f",{key}={val}i"
    return(pair)

def gen_float_field(field_key_size, float_value_size, key=''):
    '''
    Generates float key-value pair that will be a Field in a LP line
    '''
    if key:
        held_key = 'fl_' + key
        held_key = held_key[:-3]
        val = _gen_int(float_value_size)
        pair = f",{held_key}={val}"
    else:
        key = 'fl_' + _gen_string(field_key_size-3)
        val = round(random.uniform(10,99), float_value_size-2)
        pair = f",{key}={val}"
    return(pair)

def gen_ts(precision = 's'):
    '''
    Generates a timestamp to be used at end of line of Line Protocol.
    The precision can be set to seconds, milliseconds, microseconds, or nanoseconds.
    Less precision is achieved with rounding the timestamp to the passed precison
    and then adding zeros as  necessary to keep the timestamp length constant.
    '''
    now  = datetime.datetime.now()
    ts = now.timestamp()
    if precision == ('s' or 'S'):
        ts = round(ts)
        return(ts*10**9)
    elif precision == ('ms' or 'MS'):
        ts = round(ts*10**3)
        return(ts*10**6)
    elif precision == ('us' or 'US'):
        ts = round(ts*10**6)
        return(ts*10**3)
    elif precision == ('ns' or 'NS'):
        ts = round(ts*10**9)
        return(ts)
    else:
        raise ValueError("Warn: gen_ts() only takes `s`, `ms`, `us`, or `ns` as inputs")
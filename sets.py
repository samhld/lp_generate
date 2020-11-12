import random
import string
import time
import primitives

# Return set of Tag key-value pairs with trailing space
def gen_tagset(tag_keys, **kwargs):
    if tag_keys:
        tagset = ''.join(primitives.gen_tag(kwargs['tag_key_size'],kwargs['tag_value_size'], key=i) for i in tag_keys) + ' ' 
    else:
        tagset = ''.join(primitives.gen_tag(kwargs['tag_key_size'],kwargs['tag_value_size']) for i in range(kwargs['num_tags'])) + ' '
    
    return(tagset[1:]) # remove leading comma

# Following 3 functions are helper functions for `gen_fieldset()`
def _gen_int_fieldset(int_field_keys, **kwargs):
    if int_field_keys:
        int_fieldset = ''.join(primitives.gen_int_field(kwargs['field_key_size'],kwargs['int_value_size'], key=i) for i in int_field_keys)       
    else:
        int_fieldset = ''.join(primitives.gen_int_field(kwargs['field_key_size'],kwargs['int_value_size']) for i in range(kwargs['int_fields']))

    return(int_fieldset[1:])

def _gen_float_fieldset(float_field_keys, **kwargs):
    if float_field_keys:
        float_fieldset = ''.join(primitives.gen_float_field(kwargs['field_key_size'],kwargs['float_value_size'], key=i) for i in float_field_keys) 
    else:
        float_fieldset = ''.join(primitives.gen_float_field(kwargs['field_key_size'],kwargs['float_value_size']) for i in range(kwargs['float_fields']))
    
    return(float_fieldset[1:])

def _gen_str_fieldset(str_field_keys, **kwargs):
    if str_field_keys:
        str_fieldset = ''.join(primitives.gen_str_field(kwargs['field_key_size'],kwargs['str_value_size'], key=i) for i in str_field_keys)
    else:
        str_fieldset = ''.join(primitives.gen_str_field(kwargs['field_key_size'],kwargs['str_value_size']) for i in range(kwargs['str_fields']))
    return(str_fieldset[1:])

# Use fieldset helper functions to generate a full fieldset
def gen_fieldset(int_field_keys, float_field_keys, str_field_keys, **kwargs):
    int_fieldset = _gen_int_fieldset(int_field_keys, **kwargs)
    float_fieldset = _gen_float_fieldset(float_field_keys, **kwargs)
    str_fieldset = _gen_str_fieldset(str_field_keys, **kwargs)

    fieldset = ''
    if int_fieldset:
        fieldset += f"{int_fieldset},"
    if float_fieldset:
        fieldset += f"{float_fieldset},"
    if str_fieldset:
        fieldset += f"{str_fieldset},"

    return(fieldset[:-1]+' ') # remove leading and trailing comma

import random
import string
import time
import primitives

# Return set of Tag key-value pairs with trailing space
def gen_tagset(num_tags, tag_key_size, tag_value_size, tag_keys):
    if tag_keys:
        tagset = ''.join(primitives.gen_tag(tag_key_size,tag_value_size, key=i) for i in tag_keys) + ' ' 
    else:
        tagset = ''.join(primitives.gen_tag(tag_key_size,tag_value_size) for i in range(num_tags)) + ' '
    
    return(tagset[1:]) # remove leading comma

# Following 3 functions are helper functions for `gen_fieldset()`
def _gen_int_fieldset(int_fields, field_key_size, int_value_size, int_field_keys):
    if int_field_keys:
        int_fieldset = ''.join(primitives.gen_int_field(field_key_size,int_value_size, key=i) for i in int_field_keys)       
    else:
        int_fieldset = ''.join(primitives.gen_int_field(field_key_size,int_value_size) for i in range(int_fields))

    return(int_fieldset[1:])

def _gen_float_fieldset(float_fields, field_key_size, float_value_size, float_field_keys):
    if float_field_keys:
        float_fieldset = ''.join(primitives.gen_float_field(field_key_size,float_value_size, key=i) for i in float_field_keys) 
    else:
        float_fieldset = ''.join(primitives.gen_float_field(field_key_size,float_value_size) for i in range(float_fields))
    
    return(float_fieldset[1:])

def _gen_str_fieldset(str_fields, field_key_size, str_value_size, str_field_keys):
    if str_field_keys:
        str_fieldset = ''.join(primitives.gen_str_field(field_key_size,str_value_size, key=i) for i in str_field_keys)
    else:
        str_fieldset = ''.join(primitives.gen_str_field(field_key_size,str_value_size) for i in range(str_fields))
    return(str_fieldset[1:])

# Use fieldset helper functions to generate a full fieldset
def gen_fieldset(int_fields, 
                float_fields, 
                str_fields, 
                field_key_size,
                int_value_size,
                float_value_size,
                str_value_size,
                int_field_keys,
                float_field_keys,
                str_field_keys):
    int_fieldset = _gen_int_fieldset(int_fields, field_key_size, int_value_size, int_field_keys)
    float_fieldset = _gen_float_fieldset(float_fields, field_key_size, float_value_size, float_field_keys)
    str_fieldset = _gen_str_fieldset(str_fields, field_key_size, str_value_size, str_field_keys)

    fieldset = ''
    if int_fieldset:
        fieldset += f"{int_fieldset},"
    if float_fieldset:
        fieldset += f"{float_fieldset},"
    if str_fieldset:
        fieldset += f"{str_fieldset},"

    return(fieldset[:-1]+' ') # remove leading and trailing comma

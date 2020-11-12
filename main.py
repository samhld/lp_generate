import primitives
import sets
import time
import argparse

def gen_line(tag_keys, int_field_keys, float_field_keys, str_field_keys, **kwargs):

    tagset = sets.gen_tagset(tag_keys, **kwargs)
    fieldset = sets.gen_fieldset(int_field_keys, float_field_keys, str_field_keys, **kwargs)
    timestamp = primitives.gen_ts(kwargs['precision'])
    line = f"{kwargs['measurement']},{tagset}{fieldset}{timestamp}"

    return(line)

def gen_batch(tag_keys, int_field_keys, float_field_keys, str_field_keys, **kwargs):
    
    # Generate keys at batch level if `hold_keys` is True. 
    # This will keep Tag keys constant per line, reducing Series creation at database level.
    if kwargs['keep_keys_session']:
        tag_keys         = tag_keys
        int_field_keys   = int_field_keys
        float_field_keys = float_field_keys
        str_field_keys   = str_field_keys
    elif kwargs['keep_keys_batch']:
        tag_keys         = [primitives._gen_string(kwargs['tag_key_size']) for i in range(kwargs['num_tags'])]
        int_field_keys   = [primitives._gen_string(kwargs['tag_key_size']) for i in range(kwargs['int_fields'])]
        float_field_keys = [primitives._gen_string(kwargs['tag_key_size']) for i in range(kwargs['float_fields'])]
        str_field_keys   = [primitives._gen_string(kwargs['tag_key_size']) for i in range(kwargs['str_fields'])]
    else:
        tag_keys         = []
        int_field_keys   = []
        float_field_keys = []
        str_field_keys   = []
        
    batch = []
    for i in range(kwargs['batch_size']):
        line = gen_line(tag_keys, int_field_keys, float_field_keys, str_field_keys, **kwargs)
        batch.append(line)

    return(batch)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a batch of Line Protocol points of a specified shape")
    parser.add_argument('measurement', type=str, default='cpu')
    parser.add_argument('--batch_size', type=int, default=10)
    parser.add_argument('--num_tags', type=int, default=3)
    parser.add_argument('--int_fields', type=int, default=2)
    parser.add_argument('--float_fields', type=int, default=1)
    parser.add_argument('--str_fields', type=int, default=1)
    parser.add_argument('--tag_key_size', type=int, default=8)
    parser.add_argument('--tag_value_size', type=int, default=10)  
    parser.add_argument('--field_key_size', type=int, default=8)
    parser.add_argument('--int_value_size', type=int, default=4)
    parser.add_argument('--float_value_size', type=int, default=4)
    parser.add_argument('--str_value_size', type=int, default=8)
    parser.add_argument('--precision', type=str, choices = ['s','S','ms','MS','us','US','ns','NS'], default='s')
    parser.add_argument('--keep_keys_batch', action='store_true')
    parser.add_argument('--keep_keys_session', action='store_true', help="")


    kwargs = vars(parser.parse_args())

    if kwargs['keep_keys_session']:
        tag_keys         = [primitives._gen_string(kwargs['tag_key_size']) for i in range(kwargs['num_tags'])]
        int_field_keys   = [primitives._gen_string(kwargs['tag_key_size']) for i in range(kwargs['int_fields'])]
        float_field_keys = [primitives._gen_string(kwargs['tag_key_size']) for i in range(kwargs['float_fields'])]
        str_field_keys   = [primitives._gen_string(kwargs['tag_key_size']) for i in range(kwargs['str_fields'])]
        kwargs['keep_keys_batch']  = True
    else:
        tag_keys         = [] 
        int_field_keys   = []
        float_field_keys = []
        str_field_keys   = []

    batch = gen_batch(tag_keys, int_field_keys, float_field_keys, str_field_keys, **kwargs)

    for line in batch:
        print(line)
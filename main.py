import primitives
import sets
import time
import argparse
import config

def gen_keys_vals(kwargs):
    '''
    Function used to generate keys and values directly (without calling primitive/set functions). 
    Used for when the keys/values need to be constant for all batches/lines.
    In those cases, keys/values must be passed from the entry point of the script. 
    '''
    tag_keys         = [primitives._gen_string(kwargs['tag_key_size']) for i in range(kwargs['num_tags'])]
    tag_values       = [primitives._gen_string(kwargs['tag_value_size']) for i in range(kwargs['num_tags'])]
    int_field_keys   = [primitives._gen_string(kwargs['field_key_size']) for i in range(kwargs['int_fields'])]
    float_field_keys = [primitives._gen_string(kwargs['field_key_size']) for i in range(kwargs['float_fields'])]
    str_field_keys   = [primitives._gen_string(kwargs['field_key_size']) for i in range(kwargs['str_fields'])]

    return tag_keys, tag_values, int_field_keys, float_field_keys, str_field_keys

def gen_line(tag_keys, tag_values, int_field_keys, float_field_keys, str_field_keys, **kwargs):
    '''
    Generates a single line of Line Protocol out of the args passed to it.
    '''
    tagset = sets.gen_tagset(tag_keys, tag_values, kwargs)
    fieldset = sets.gen_fieldset(int_field_keys, float_field_keys, str_field_keys, kwargs)
    timestamp = primitives.gen_ts(kwargs['precision'])
    line = f"{kwargs['measurement']},{tagset} {fieldset}{timestamp}"

    return line

def gen_batch(kwargs, distinct_sets=[], tag_keys=None, tag_values=None, int_field_keys=None, float_field_keys=None, str_field_keys=None):
    '''
    Generates a single batch of lines of Line Protocol.
    This will keep Tag keys constant per line, reducing Series creation at database level.
    '''
    if distinct_sets:
        print(f"distinct_sets: {distinct_sets}")
        batch = []
        for tag_keys, tag_values, int_field_keys, float_field_keys, str_field_keys in distinct_sets:
            line = gen_line(tag_keys, tag_values, int_field_keys, float_field_keys, str_field_keys, **kwargs)
            batch.append(line)
        return batch

    elif kwargs['keep_keys_session']:
        tag_keys         = tag_keys
        int_field_keys   = int_field_keys
        float_field_keys = float_field_keys
        str_field_keys   = str_field_keys
    # Generate keys at batch level if `keep_keys_batch` is True. 
    # This will keep Tag keys constant per line, reducing Series creation at database level.
    elif kwargs['keep_keys_batch']:
        tag_keys, tag_values, int_field_keys, float_field_keys, str_field_keys = gen_keys_vals(kwargs)

    else:
        tag_keys         = []
        int_field_keys   = []
        float_field_keys = []
        str_field_keys   = []

    batch = []
    for i in range(kwargs['batch_size']):
        line = gen_line(tag_keys, tag_values, int_field_keys, float_field_keys, str_field_keys, **kwargs)
        batch.append(line)

    return batch

# Expected entry point to script
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
    parser.add_argument('--keep_keys_batch', action='store_true', help="Keep Tag/Field keys constant for each line in a batch")
    parser.add_argument('--keep_keys_session', action='store_true', help="Keep Tag/Field keys constant for each line in all batches; only relevant when `--loop` is True")
    parser.add_argument('--keep_tags_batch', action='store_true', help="Superset of `--keep_keys_batch`; keeps Tag values constant as well")
    parser.add_argument('--keep_tags_session', action='store_true', help="Superset of `--keep_keys_session`; keeps Tag values constant as well; only relevant when `--loop` is True")
    parser.add_argument('--loop', action='store_true', help="If True, script runs in infinit loop; used with Telegraf `execd` input plugin")

    kwargs = vars(parser.parse_args())

    if kwargs["loop"]:

        if kwargs["keep_tags_session"]:

            # Instantiate all keys/values before loops starts so they remain constant
            tag_keys, tag_values, int_field_keys, float_field_keys, str_field_keys = gen_keys_vals(kwargs)
            kwargs["keep_keys_session"] = True

            if kwargs["keep_keys_batch"]:
                while True:

                    batch = gen_batch(kwargs,
                                        tag_keys=tag_keys,
                                        tag_values=tag_values, 
                                        int_field_keys=int_field_keys, 
                                        float_field_keys=float_field_keys, 
                                        str_field_keys=str_field_keys)
                    for line in batch:
                        print(line)

                    time.sleep(config.sample_interval)
            else: # not keep_keys_batch --> keys will be different in the batch but repeated across batches
                distincts = {}
                distincts["tag_keys"], distincts["tag_values"], distincts["int_field_keys"], distincts["float_field_keys"], distincts["str_field_keys"] = [], [], [], [], []
                distinct_sets = [gen_keys_vals(kwargs) for i in range(kwargs["batch_size"])]
                batch = gen_batch(kwargs, distinct_sets=distinct_sets)

                while True:
            
                    for line in batch:
                        print(line)

                    time.sleep(config.sample_interval)

        elif kwargs["keep_tags_batch"]:
            while True:
                print(kwargs)
                # Instantiate keys/values in loop so they change different each iteration
                tag_keys, tag_values, int_field_keys, float_field_keys, str_field_keys = gen_keys_vals(kwargs)
                kwargs["keep_keys_batch"] = True
                batch = gen_batch(kwargs, tag_keys, tag_values, int_field_keys, float_field_keys, str_field_keys)

                for line in batch:
                    print(line)

                time.sleep(config.sample_interval)

        elif kwargs['keep_keys_session']:
            tag_keys, _, int_field_keys, float_field_keys, str_field_keys = gen_keys_vals(kwargs)
            kwargs['keep_keys_batch'] = True
            while True:
                batch = gen_batch(kwargs,
                                tag_keys=tag_keys,
                                int_field_keys=int_field_keys, 
                                float_field_keys=float_field_keys, 
                                str_field_keys=str_field_keys)
                    
                for line in batch:
                    print(line)

                time.sleep(config.sample_interval)
        else:
            while True:
                batch = gen_batch(kwargs)
                for line in batch:
                    print(line)

                time.sleep(config.sample_interval)
    else:
        batch = gen_batch(kwargs)

        for line in batch:
            print(line)
import primitives
import sets
import time
import argparse

def gen_line(measurement,
                num_tags,
                int_fields,
                float_fields,
                str_fields,
                tag_key_size,
                tag_value_size,
                field_key_size,
                int_value_size,
                float_value_size,
                str_value_size,
                precision,
                tag_keys,
                int_field_keys,
                float_field_keys,
                str_field_keys):


    tagset = sets.gen_tagset(num_tags, tag_key_size, tag_value_size, tag_keys)
    fieldset = sets.gen_fieldset(int_fields, float_fields, str_fields, field_key_size, int_value_size, float_value_size, str_value_size, int_field_keys, float_field_keys, str_field_keys)
    timestamp = primitives.gen_ts(precision)
    line = f"{measurement},{tagset}{fieldset}{timestamp}"

    return(line)

def gen_batch(measurement, 
                batch_size,
                num_tags,
                int_fields,
                float_fields,
                str_fields,
                tag_key_size,
                tag_value_size,
                field_key_size,
                int_value_size,
                float_value_size,
                str_value_size,
                precision,
                keep_keys_batch,
                keep_keys_session,
                tag_keys,
                int_field_keys,
                float_field_keys,
                str_field_keys):

    # Generate keys at batch level if `hold_keys` is True. 
    # This will keep Tag keys constant per line, reducing Series creation at database level.
    if keep_keys_session:
        tag_keys         = tag_keys
        int_field_keys   = int_field_keys
        float_field_keys = float_field_keys
        str_field_keys   = str_field_keys
    elif keep_keys_batch:
        tag_keys         = [primitives._gen_string(tag_key_size) for i in range(num_tags)]
        int_field_keys   = [primitives._gen_string(tag_key_size) for i in range(int_fields)]
        float_field_keys = [primitives._gen_string(tag_key_size) for i in range(float_fields)]
        str_field_keys   = [primitives._gen_string(tag_key_size) for i in range(str_fields)]
    else:
        tag_keys         = []
        int_field_keys   = []
        float_field_keys = []
        str_field_keys   = []
        
    batch = []
    for i in range(batch_size):
        line = gen_line(measurement, 
                            num_tags,
                            int_fields,
                            float_fields,
                            str_fields,
                            tag_key_size,
                            tag_value_size,
                            field_key_size,
                            int_value_size,
                            float_value_size,
                            str_value_size,
                            precision,
                            tag_keys,
                            int_field_keys,
                            float_field_keys,
                            str_field_keys)
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


    args = parser.parse_args()

    if args.keep_keys_session:
        tag_keys         = [primitives._gen_string(args.tag_key_size) for i in range(args.num_tags)]
        int_field_keys   = [primitives._gen_string(args.tag_key_size) for i in range(args.int_fields)]
        float_field_keys = [primitives._gen_string(args.tag_key_size) for i in range(args.float_fields)]
        str_field_keys   = [primitives._gen_string(args.tag_key_size) for i in range(args.str_fields)]
        args.keep_keys_batch  = True
    else:
        tag_keys         = [] 
        int_field_keys   = []
        float_field_keys = []
        str_field_keys   = []

    batch = gen_batch(args.measurement, 
                args.batch_size,
                args.num_tags,
                args.int_fields,
                args.float_fields,
                args.str_fields,
                args.tag_key_size,
                args.tag_value_size,
                args.field_key_size,
                args.int_value_size,
                args.float_value_size,
                args.str_value_size,
                args.precision,
                args.keep_keys_batch,
                args.keep_keys_session,
                tag_keys,
                int_field_keys,
                float_field_keys,
                str_field_keys)

    for line in batch:
        print(line)

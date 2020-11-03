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
                field_key_size,
                int_value_size,
                float_value_size,
                str_value_size,
                precision):

    tagset = sets.gen_tagset()
    fieldset = sets.gen_fieldset()
    timestamp = primitives.gen_ts(precision)
    line = f"{measurement},{tagset}{fieldset}{timestamp}"

    return(line)

def gen_batch(measurement, 
                batch_size=10,
                num_tags=3,
                int_fields=2,
                float_fields=1,
                str_fields=1,
                tag_key_size=8,
                field_key_size=8,
                int_value_size=4,
                float_value_size=4,
                str_value_size=8,
                precision='s'):

    batch = []
    for i in range(batch_size):
        line = gen_line(measurement, 
                            num_tags,
                            int_fields,
                            float_fields,
                            str_fields,
                            tag_key_size,
                            field_key_size,
                            int_value_size,
                            float_value_size,
                            str_value_size,
                            precision)
        batch.append(line)

    return(batch)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a batch of Line Protocol points of a specified shape")
    parser.add_argument('measurement', default='cpu', type=str)
    parser.add_argument('--batch_size', default=100, type=int)
    parser.add_argument('--num_tags', type=int)
    parser.add_argument('--int_fields', type=int)
    parser.add_argument('--float_fields', type=int)
    parser.add_argument('--str_fields', type=int)
    parser.add_argument('--tag_key_size', type=int)
    parser.add_argument('--field_key_size', type=int)
    parser.add_argument('--int_value_size', type=int)
    parser.add_argument('--float_value_size', type=int)
    parser.add_argument('--str_value_size', type=int)
    parser.add_argument('--precision', type=str, choices = ['s','S','ms','MS','us','US','ns','NS'], default='s')

    args = parser.parse_args()
    measurement = args.measurement
    batch_size = args.batch_size
    num_tags = args.num_tags
    int_fields = args.int_fields
    float_fields = args.float_fields
    str_fields = args.str_fields
    tag_key_size = args.tag_key_size
    field_key_size = args.field_key_size
    int_value_size = args.int_value_size
    float_value_size = args.float_value_size
    str_value_size = args.str_value_size
    precision = args.precision

    print(gen_batch(measurement, 
                batch_size,
                num_tags,
                int_fields,
                float_fields,
                str_fields,
                tag_key_size,
                field_key_size,
                int_value_size,
                float_value_size,
                str_value_size,
                precision))
import primitives
import sets
import time


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
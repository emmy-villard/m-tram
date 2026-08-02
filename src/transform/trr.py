import pandas as pd

def raw_to_pandas_trr(response_dict_ttr):
    data = [[
        k,
        value[0]['time'],
        value[0]['nsv_id']
    ] for k, value in response_dict_ttr.items()]

    dataframe_trr = pd.DataFrame(data,
    columns=('id', 'time', 'nsv_id')
    ).set_index('id')

    return dataframe_trr
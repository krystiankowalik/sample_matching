import pandas as pd

raw = pd.read_csv('raw.csv')

raw['abs_my_vs_brk'] = abs(raw['my_qty'] - raw['brk_qty'])

mask = raw['abs_my_vs_brk'] != 0
diffs_to_brk = raw[mask]

no_brk_filter = diffs_to_brk['brk_qty'] == 0
diffs_to_brk_missing_brk = diffs_to_brk[no_brk_filter]
diffs_to_brk_existing_brk = diffs_to_brk[~no_brk_filter]

diffs_to_brk_missing_brk['status'] = 'unmatched'
matched = []

for existing_index, existing_row in diffs_to_brk_existing_brk.iterrows():
    for missing_index, missing_row in \
            diffs_to_brk_missing_brk[
                diffs_to_brk_missing_brk['abs_my_vs_brk'] == existing_row['abs_my_vs_brk']].iterrows():
        if missing_row['my_qty'] == existing_row['brk_qty'] and missing_row['my_curr'] == existing_row['brk_curr'] and \
                missing_index not in matched:
            raw.loc[missing_index, 'brk_qty'] = existing_row['brk_qty']
            print(missing_index)
            print(raw.loc[missing_index, 'brk_qty'])
            raw.loc[missing_index, 'brk_curr'] = existing_row['brk_curr']
            print(missing_index)
            print(raw.loc[missing_index, 'brk_curr'])
            raw.drop(existing_index, inplace=True)
            matched.append(missing_index)
            diffs_to_brk_missing_brk['status'] = 'matched'
            break

raw['my_vs_brk'] = raw['my_qty'] - raw['brk_qty']
raw['my_vs_client'] = raw['my_qty'] - raw['client_qty']
raw['abs_my_vs_brk'] = abs(raw['my_qty'] - raw['brk_qty'])

print(raw)

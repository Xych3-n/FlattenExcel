import os
import pandas as pd

from core.xlsx_handler import process_xlsx
from core.xls_handler import process_xls
from core.postprocess import (
    process_processed_files,
    remove_empty_columns,
    deduplicate_column_names
)
from core.collapsed_column import generate_collapsed_column


def main():
    input_dir = os.path.join(os.getcwd(), '待处理')
    base_output_dir = os.path.join(os.getcwd(), '已处理')
    os.makedirs(base_output_dir, exist_ok=True)

    for fname in os.listdir(input_dir):
        if not fname.lower().endswith(('.xlsx', '.xls')):
            continue

        fullpath = os.path.join(input_dir, fname)
        base_name = os.path.splitext(fname)[0]
        output_dir = os.path.join(base_output_dir, base_name)
        os.makedirs(output_dir, exist_ok=True)

        tables = process_xlsx(fullpath) if fname.lower().endswith('.xlsx') else process_xls(fullpath)

        count = 1
        for sheet_name, tbl in tables:
            out_path = os.path.join(output_dir, f"{base_name}_分表{count:03d}.xlsx")
            df = pd.DataFrame(tbl)
            with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=f'_分表{count}', index=False, header=False)
            count += 1

        process_processed_files(output_dir)
        remove_empty_columns(output_dir)
        deduplicate_column_names(output_dir)
        generate_collapsed_column(output_dir)


if __name__ == '__main__':
    main()

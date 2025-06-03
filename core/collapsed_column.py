import os
import pandas as pd


def generate_collapsed_column(directory):
    """
    在指定目录的_xlsx_文件中，寻找文件名中带“_分表”的Excel文件，
    遍历所有表，拼接每行各列数据和列名，生成单列格式。
    最终合并所有表的数据，保存为目录下/table/目录中的_csv_文件。
    """
    table_dir = os.path.join(directory, 'table')
    os.makedirs(table_dir, exist_ok=True)

    all_output_data = []
    base_name = None

    # 寻找包含“_分表”的xlsx文件
    xlsx_files = [f for f in os.listdir(directory) if f.lower().endswith('.xlsx') and '_分表' in f]
    if not xlsx_files:
        print("没有找到分表文件。")
        return

    base_name = xlsx_files[0].split('_分表')[0]

    for fname in xlsx_files:
        file_path = os.path.join(directory, fname)
        try:
            xl = pd.ExcelFile(file_path)
            for sheet_name in xl.sheet_names:
                df = xl.parse(sheet_name)
                if df.empty:
                    continue

                headers = df.columns.tolist()

                for _, row in df.iterrows():
                    parts = []
                    for col in headers:
                        val_str = str(row[col]) if pd.notna(row[col]) else ''
                        header_str = str(col)
                        # 如果列值和列名完全相同，拼接列名一次；否则拼接 列名:值
                        if val_str == header_str:
                            parts.append(header_str)
                        else:
                            parts.append(f"{header_str}:{val_str}")
                    combined_str = ';'.join(parts)
                    all_output_data.append([combined_str, ""])  # 第二列为空

        except Exception as e:
            print(f"处理 {fname} 时出错：{e}")
            continue

    if all_output_data:
        final_df = pd.DataFrame(all_output_data, columns=["index", "content"])
        output_path = os.path.join(table_dir, f"{base_name}_table.csv")
        final_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"{output_path}")

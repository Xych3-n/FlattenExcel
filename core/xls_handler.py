import xlrd
from .table_utils import extract_tables_from_rows, transform_table

def process_xls(path):
    """
    处理xls文件，使用xlrd读取，手动填充合并单元格内容，
    然后提取表格块并转换表头，返回所有表格及其对应工作表名。
    """
    book = xlrd.open_workbook(path, formatting_info=True)
    all_tables = []
    for sheet in book.sheets():
        merged_map = {}
        # 生成合并单元格映射，合并区域内所有单元格值相同
        for (rlow, rhigh, clow, chigh) in sheet.merged_cells:
            val = sheet.cell_value(rlow, clow)
            for r in range(rlow, rhigh):
                for c in range(clow, chigh):
                    merged_map[(r, c)] = val
        rows = []
        # 按行按列填充单元格值，优先使用合并映射
        for r in range(sheet.nrows):
            row = []
            for c in range(sheet.ncols):
                row.append(merged_map.get((r, c), sheet.cell_value(r, c)))
            rows.append(row)
        tables = extract_tables_from_rows(rows)
        for tbl in tables:
            processed = transform_table(tbl)
            all_tables.append((sheet.name, processed))
    return all_tables

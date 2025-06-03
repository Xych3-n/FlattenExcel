def extract_tables_from_rows(rows):
    """
    从连续的行数据中提取独立的表格块。
    空白行作为表格的分隔符，将非空行聚集为一个表格。
    返回：列表，包含多个表格（每个表格是行的列表）。
    """
    tables = []
    current = []
    for row in rows:
        # 判断该行是否全为空或空字符串
        if all(cell is None or str(cell).strip() == '' for cell in row):
            # 遇到空行，且当前有积累的表格，存储并重置
            if current:
                tables.append(current)
                current = []
        else:
            # 非空行，加入当前表格
            current.append(row)
    # 最后一组非空行也加入
    if current:
        tables.append(current)
    return tables


def transform_table(tbl):
    """
    处理表格数据，将多层表头转化为首列多标签的形式。
    通过寻找第一个含数字的行，判定数据起始行，向上合并前几行表头为标签。
    返回转化后的行列表。
    """
    rows = [list(r) for r in tbl]
    pure_row = None  # 记录第一个数字行的索引
    for i, row in enumerate(rows):
        for cell in row:
            # 找到第一个含数字的单元格所在行
            if cell is not None and str(cell).strip().isdigit():
                pure_row = i
                break
        if pure_row is not None:
            break
    # 如果找不到数字行，或数字行太靠前，不做转换，直接返回原始行
    if pure_row is None or pure_row < 2:
        return rows

    labels = []
    header_indices = []
    # 从纯数据行的上方两行开始倒序检查，寻找单标签行（只有一段非空连续内容）
    for k in range(pure_row - 2, -1, -1):
        row_k = rows[k]
        runs = []
        prev_val = None
        prev_empty = True
        for idx, cell in enumerate(row_k):
            if cell is not None and str(cell).strip() != '':
                if prev_empty or cell != prev_val:
                    runs.append((idx, cell))
                prev_empty = False
                prev_val = cell
            else:
                prev_empty = True
                prev_val = None
        # 如果该行只有一个有效标签段，记录下来
        if len(runs) == 1:
            header_indices.append(k)
            labels.append(runs[0][1])
    # 如果没找到标签，返回原始行
    if not labels:
        return rows
    # 删除被提取为标签的表头行
    for k in sorted(header_indices, reverse=True):
        rows.pop(k)
    # 将每个标签插入为每行的首列
    for label in labels:
        rows = [[label] + r for r in rows]
    return rows


def merge_and_deduplicate(table):
    """
    将多行多层表头合并为单行表头，去除重复的标签。
    通过查找首个含数字的行确定数据起始行，合并起始行以上的表头。
    返回处理后的新表格。
    """
    rows = table.copy()
    digit_row_index = None

    # 查找首个含数字的行索引
    for i, row in enumerate(rows):
        for cell in row:
            if isinstance(cell, (int, float)) or (isinstance(cell, str) and cell.strip().isdigit()):
                digit_row_index = i
                break
        if digit_row_index is not None:
            break

    # 如果无数字行或数字行太靠前，返回原表
    if digit_row_index is None or digit_row_index < 1:
        return rows

    num_cols = max(len(r) for r in rows)
    merged_header = []
    # 对每列，按行依次合并非空且不重复的表头单元格值
    for col_idx in range(num_cols):
        merged_parts = []
        seen = set()
        for r in range(digit_row_index):
            if col_idx < len(rows[r]):
                val = rows[r][col_idx]
                if val not in [None, '']:
                    val_str = str(val).strip()
                    if val_str and val_str not in seen:
                        merged_parts.append(val_str)
                        seen.add(val_str)
        merged_header.append(''.join(merged_parts))

    # 生成新表，第一行为合并后的表头，后续为数据行
    new_rows = [merged_header] + rows[digit_row_index:]
    return new_rows

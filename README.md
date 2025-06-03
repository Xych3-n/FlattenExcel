
# 📊 FlattenExcel

`FlattenExcel` 是一个用于批量处理结构化 Excel 报表的工具，能够自动清洗、标准化表格内容，并将其转换为类似 [RAGFlow](https://github.com/infiniflow/ragflow) 中经过table方法分块解析后的 `index-content` 结构文本，方便用于如 [FastGPT](https://github.com/labring/FastGPT) 的知识库构建任务。

---

## ✅ 项目亮点

- 自动识别 Excel 文件中的表格区域（兼容 `.xlsx` 和 `.xls`）
- 清洗与标准化表格：填充合并单元格、移除空列、重复列及噪音行
- 拆分单个 Excel 文件中的多个独立表格，支持多 sheet 处理
- 支持将多列信息拼接为单列 `content` 字符串（用于 RAG）
- 自动导出为 index-content 格式 CSV，适合文本向量化与知识库构建
- 支持 CLI 一键处理整个目录下所有文件（递归子目录）

---

## 📁 项目结构

```

flatten_excel/
├── core/                    # 核心模块（表格处理、清洗、拼接等）
│   ├── table_utils.py
│   ├── xlsx_handler.py
│   ├── xls_handler.py
│   ├── postprocess.py
│   └── collapsed_column.py
│
├── main.py                  # 主入口脚本
├── requirements.txt
├── README.md
└── example_data/     

````

---

## 📦 安装依赖

建议使用 Python 3.10 环境：

```bash
pip install -r requirements.txt
````

---

## 🚀 快速开始

### Step 1: 准备 Excel 文件

将你的 `.xlsx` 或 `.xls` 报表放入项目根目录下的 `待处理/` 文件夹（支持递归子目录）。

### Step 2: 执行处理流程

```bash
python main.py
```

### Step 3: 查看输出结果

处理后的文件将保存至 `已处理/` 目录：

* 清洗后的标准 Excel 表格（无合并单元格，表头规范）
* 生成的 index-content 格式 `.csv` 文件，命名规则：

  ```
  [原始文件名]_表N_合并列.csv
  ```

---

## 🧪 样例演示

### 输入示例（Excel 表格部分）：

| 财务报表 |     |       |
| ---- | --- | ----- |
| 部门   | 项目  | 金额    |
| 市场部  | 宣传费 | 10000 |
| 市场部  | 差旅费 | 8000  |
| 销售部  | 差旅费 | 6000  |

### 清洗后的 DataFrame：

| 财务报表 | 部门  | 项目  | 金额    |
| --- | --- | --- | ----- |
| 财务报表 | 市场部 | 宣传费 | 10000 |
| 财务报表 | 市场部 | 差旅费 | 8000  |
| 财务报表 | 销售部 | 差旅费 | 6000  |

### 转换输出（index-content CSV）：

| index | content | 
| --- | --- |
| 财务报表；0,部门：市场部；项目：宣传费；金额：10000 |  | 
| 财务报表；1,部门：市场部；项目：差旅费；金额：8000 |  | 
| 财务报表；2,部门：销售部；项目：差旅费；金额：6000 |  | 

---

## 🧠 应用场景

* 企业文档结构化知识库构建
* 面向文本向量化的内容预处理（RAG / FastGPT / LangChain 等）
* 多表合并、数据迁移前的预清洗与规范化
* 自动化报表标准化和归一化内容生成

---

## 🛠 依赖列表

主要依赖（详见 `requirements.txt`）：

* `pandas==2.1.4`
* `openpyxl==3.1.2`
* `xlrd==1.2.0`
* `numpy==1.26.4`

---

## 📮 联系与反馈

欢迎通过 issue 或 PR 贡献功能与优化！
企业定制需求请联系作者团队，支持模板适配和集成扩展。

---

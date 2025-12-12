```markdown
# NB

这是一个“企业数字化转型指数查询系统”的示例应用，基于 Streamlit 构建。主要文件：

- `digital_transformation_query_app.py`：主应用程序，包含数据加载、字段映射、查询、可视化与统计分析功能。

运行方法（需要 Python 3.8+）：

1. 创建虚拟环境并激活（可选但推荐）：

```bash
python -m venv .venv
source .venv/bin/activate
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 启动应用：

```bash
streamlit run digital_transformation_query_app.py
```

示例数据：应用会尝试加载 `两版合并后的年报数据_完整版.xlsx`，如果不存在会使用内置示例数据。你也可以将自己的 Excel 文件放在仓库根目录，或在侧边栏选择字段映射。

如需在 Linux 上用脚本一键启动：运行 `./run_app.sh`（确保已 `chmod +x run_app.sh`）

如需在 Windows 上，运行现有的 `run_app.bat`。

更多信息请查看 `digital_transformation_query_app.py` 中的注释。
```

部署到 Streamlit Cloud：

1. 确保仓库已推送到 GitHub（本仓库远程为 `origin`）。
2. 在 https://share.streamlit.io 登录并选择 "New app" → 连接你的 GitHub 仓库。
3. 选择分支 `main` 和应用入口 `digital_transformation_query_app.py`，点击部署。
4. Streamlit Cloud 会自动安装 `requirements.txt` 中列出的依赖并启动应用。

注意：如果你上传了 Excel 数据到仓库根目录（文件名 `两版合并后的年报数据_完整版.xlsx`），应用会自动加载它；否则可在侧边栏上传文件。

# NB
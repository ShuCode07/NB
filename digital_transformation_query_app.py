import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import plotly.express as px
import plotly.graph_objects as go
import time

# 应用配置设置
st.set_page_config(
    page_title="企业数字化转型指数查询系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置中文字体以确保中文正常显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 设置Plotly字体
import plotly.io as pio
pio.templates.default = "plotly_white"

# 自定义CSS样式 - 增强版
st.markdown("""
<style>
    /* 主样式 */
    .main-header {
        color: #1a5276;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    .sub-header {
        color: #2874a6;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* 信息框 */
    .info-box {
        background-color: #f4f9fd;
        border-left: 4px solid #3498db;
        padding: 1.2rem;
        margin: 1.2rem 0;
        border-radius: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* 统计卡片 */
    .stats-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1.2rem;
        margin: 1.5rem 0;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 0.8rem;
        padding: 1.5rem;
        flex: 1;
        min-width: 180px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
        color: white;
    }
    .stat-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: white;
    }
    .stat-label {
        font-size: 0.95rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.3rem;
    }
    
    /* 选择框样式 */
    div[data-baseweb="select"] > div {
        background-color: white;
        border-color: #d1d5db;
        border-radius: 0.5rem;
        padding: 0.4rem;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.8rem;
        font-size: 1.05rem;
        font-weight: 600;
        border-radius: 0.5rem;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a418d 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* 卡片样式 */
    .card {
        background-color: white;
        border-radius: 0.8rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    /* 输入框样式 */
    .stTextInput > div > input {
        border-radius: 0.5rem;
        border: 1px solid #d1d5db;
        padding: 0.6rem;
    }
    
    /* 滑块样式 */
    .stSlider > div > div > div > div {
        background-color: #667eea;
    }
    
    /* 加载动画 */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    /* 错误和警告样式 */
    .stAlert {
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* 页脚样式 */
    .footer {
        text-align: center;
        color: #666;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid #eee;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .stats-container {
            flex-direction: column;
        }
        .stat-box {
            min-width: auto;
        }
    }
</style>
""", unsafe_allow_html=True)

# 应用标题和说明
st.markdown('<div class="main-header">企业数字化转型指数查询系统</div>', unsafe_allow_html=True)
st.markdown('通过股票代码和年份查询企业数字化转型指数，并查看变化趋势')

# 应用介绍卡片
with st.container():
    st.markdown("""
    <div class='card'>
        <h3 style='color: #1a5276; margin-bottom: 1rem;'>📊 系统功能简介</h3>
        <div style='display: flex; flex-wrap: wrap; gap: 1rem;'>
            <div style='flex: 1; min-width: 200px;'>
                <h4 style='color: #2874a6;'>数据管理</h4>
                <p>支持Excel文件导入，灵活的字段映射配置</p>
            </div>
            <div style='flex: 1; min-width: 200px;'>
                <h4 style='color: #2874a6;'>智能查询</h4>
                <p>快速搜索股票代码，灵活的年份范围选择</p>
            </div>
            <div style='flex: 1; min-width: 200px;'>
                <h4 style='color: #2874a6;'>可视化分析</h4>
                <p>多种图表类型（折线图、柱状图、面积图、散点图）</p>
            </div>
            <div style='flex: 1; min-width: 200px;'>
                <h4 style='color: #2874a6;'>统计分析</h4>
                <p>关键指标统计，增长率计算，趋势分析</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Excel文件路径
file_path = '两版合并后的年报数据_完整版.xlsx'
export_dir = 'exports'

if not os.path.exists(export_dir):
    try:
        os.makedirs(export_dir, exist_ok=True)
    except Exception:
        pass

# 数据加载函数
def format_stock_code(code):
    """将股票代码格式化为6位字符串"""
    try:
        code_str = str(code).strip()
        # 移除可能存在的'.0'后缀
        if code_str.endswith('.0'):
            code_str = code_str[:-2]
        # 如果是数字，格式化为6位
        if code_str.isdigit():
            return '{:06d}'.format(int(code_str))
        return code_str
    except:
        return str(code)

@st.cache_data
def load_data():
    try:
        # 检查文件是否存在
        # 优先读取指定文件路径；如果不存在会返回示例数据
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
        else:
            # 返回一个示例数据框以便应用能够运行
            return pd.DataFrame({
                '股票代码': ['000001', '000002', '000003'],
                '年份': [2019, 2020, 2021],
                '数字化转型指数': [35.2, 42.5, 50.8]
            })
        
        # 数据预处理
        # 移除全为空的列
        df = df.dropna(axis=1, how='all')
        # 移除全为空的行
        df = df.dropna(axis=0, how='all')
        
        # 自动检测股票代码列并格式化
        for col in df.columns:
            if any(keyword in col.lower() or keyword in col for keyword in ['股票代码', 'stock', 'code', 'symbol']):
                df[col] = df[col].apply(format_stock_code)

        # 对列进行初步类型修正：年份转为整数，数值列尝试转换为浮点
        for col in df.columns:
            try:
                # 年份列识别
                if any(k in col.lower() for k in ['年', '年份']):
                    df[col] = df[col].astype(str).str.extract(r'(\d{4})')[0]
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
                else:
                    # 其他列尝试转为数值（保留原有非数值）
                    df[col] = pd.to_numeric(df[col], errors='ignore')
            except Exception:
                pass
        
        return df
    except Exception as e:
        st.error(f"加载数据时出错: {str(e)}")
        # 返回一个示例数据框以便应用能够运行
        return pd.DataFrame({
            '股票代码': ['000001', '000002', '000003'],
            '年份': [2019, 2020, 2021],
            '数字化转型指数': [35.2, 42.5, 50.8]
        })

# 侧边栏设置
with st.sidebar:
    st.title("设置")
    
    # 应用主题设置
    with st.expander("🎨 主题设置", expanded=False):
        theme = st.radio(
            "选择主题",
            options=["默认", "暗黑", "蓝色"],
            index=0
        )
    
    # 根据主题设置调整样式
    if theme == "暗黑":
        st.markdown("""
        <style>
            body {background-color: #1e1e1e; color: white;}
            .main-header {color: #64b5f6;}
            .sub-header {color: #42a5f5;}
            .card {background-color: #2d2d2d; color: white;}
            .info-box {background-color: #1e3a5f;}
        </style>
        """, unsafe_allow_html=True)
    elif theme == "蓝色":
        st.markdown("""
        <style>
            .main-header {color: #0d47a1;}
            .sub-header {color: #1565c0;}
            .stButton > button {background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);}
            .stButton > button:hover {background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);}
        </style>
        """, unsafe_allow_html=True)

# 自动加载数据（启动时显示查询界面，无需手动点击）
try:
    with st.spinner('正在加载数据，请稍候...'):
        df = load_data()
        time.sleep(0.2)
    data_loaded = not df.empty

    if data_loaded:
        st.sidebar.success(f"已加载数据，共 {len(df)} 条记录（可在侧边重新加载）")
    else:
        st.sidebar.warning('未检测到外部数据，使用内置示例数据')

    # 尝试自动检测关键字段（如果存在）
    def detect_column(df, keywords):
        for col in df.columns:
            for keyword in keywords:
                if keyword in col.lower() or keyword in col:
                    return col
        return None

    stock_code_col = detect_column(df, ['股票代码', 'stock', 'code', 'symbol'])
    year_col = detect_column(df, ['年份', '年', 'year'])
    index_col = detect_column(df, ['数字化转型指数', '指数', 'index', 'digit', 'transformat'])

    # 显示数据概览（可折叠）
    with st.expander('📊 数据概览', expanded=False):
        st.markdown("**数据预览（前10行）**")
        try:
            st.dataframe(df.head(10), width='stretch', height=300)
        except Exception:
            st.write(df.head(10))
        st.markdown('**数据类型**')
        st.write(df.dtypes)

except Exception as e:
    st.error(f"加载数据时出错: {e}")
    df = pd.DataFrame()
    data_loaded = False
    stock_code_col = None
    year_col = None
    index_col = None

# 侧边栏提供手动重新加载按钮
with st.sidebar:
    if st.button('🔄 重新加载数据'):
        st.experimental_rerun()
    # 文件上传支持：允许用户上传新的 Excel 文件并覆盖默认文件
    uploaded = st.file_uploader('上传 Excel 文件（可覆盖默认数据）', type=['xlsx', 'xls'])
    if uploaded is not None:
        try:
            # 保存上传文件到工作目录并重启以加载
            with open(file_path, 'wb') as f:
                f.write(uploaded.getbuffer())
            st.success('已上传并保存文件，页面将刷新以加载新数据。')
            time.sleep(0.5)
            st.experimental_rerun()
        except Exception as e:
            st.error(f'保存上传文件失败: {e}')

# 如果数据加载成功，继续处理
if data_loaded:
    
    # 如果自动检测失败，让用户手动选择
    st.sidebar.header('字段映射设置')
    
    # 股票代码列选择 - 修复选择功能
    try:
        # 尝试找到最合适的默认索引
        default_stock_index = 0
        for i, col in enumerate(df.columns):
            if any(keyword in col.lower() or keyword in col for keyword in ['股票代码', 'stock', 'code', 'symbol']):
                default_stock_index = i
                break
    except:
        default_stock_index = 0
    
    stock_code_col = st.sidebar.selectbox(
        '选择股票代码列', 
        df.columns, 
        index=default_stock_index,
        key="stock_code_select"
    )
    
    # 年份列选择 - 修复选择功能
    try:
        # 尝试找到最合适的默认索引
        default_year_index = 0
        for i, col in enumerate(df.columns):
            if any(keyword in col.lower() or keyword in col for keyword in ['年份', '年', 'year']):
                default_year_index = i
                break
    except:
        default_year_index = 0
    
    year_col = st.sidebar.selectbox(
        '选择年份列', 
        df.columns, 
        index=default_year_index,
        key="year_select"
    )
    
    # 指数列选择 - 修复选择功能
    try:
        # 尝试找到最合适的默认索引
        default_index_index = 0
        for i, col in enumerate(df.columns):
            if any(keyword in col.lower() or keyword in col for keyword in ['数字化转型指数', '指数', 'index', 'digit', 'transformat']):
                default_index_index = i
                break
    except:
        default_index_index = 0
    
    index_col = st.sidebar.selectbox(
        '选择数字化转型指数列', 
        df.columns, 
        index=default_index_index,
        key="index_select"
    )

    # 选择用于可视化和统计的指标列（支持多指标）
    try:
        candidate_cols = []
        seen = set()
        for col in df.columns:
            if col in (stock_code_col, year_col):
                continue
            low = col.lower()
            is_numeric = pd.api.types.is_numeric_dtype(df[col])
            if is_numeric or any(k in low for k in ['数字化', '指数', '指标', 'score', 'index', 'value']):
                if col not in seen:
                    candidate_cols.append(col)
                    seen.add(col)

        if not candidate_cols:
            candidate_cols = [index_col] if index_col in df.columns else list(df.columns)

        default_metric = index_col if index_col in candidate_cols else candidate_cols[0]
        metric_col = st.sidebar.selectbox('选择展示指标列', candidate_cols, index=candidate_cols.index(default_metric) if default_metric in candidate_cols else 0)
    except Exception:
        metric_col = index_col
    
    # 获取唯一的股票代码和年份
    try:
        # 对股票代码进行排序，确保股票代码格式一致并补全为6位
        df[stock_code_col] = df[stock_code_col].astype(str).apply(format_stock_code)

        # 检测可能的公司名称列（用于改进搜索展示）
        name_col = None
        for col in df.columns:
            if any(keyword in col.lower() or keyword in col for keyword in ['公司', '简称', 'name', 'company']):
                name_col = col
                break

        # 构建展示用选项：'代码 — 名称'（如果没有名称则仅显示代码）
        unique_codes = sorted(df[stock_code_col].dropna().unique())
        display_options = []
        code_to_display = {}
        for code in unique_codes:
            display = code
            if name_col is not None:
                # 尝试取第一个匹配该代码的公司名称
                try:
                    name_val = df.loc[df[stock_code_col] == code, name_col].dropna().astype(str)
                    if not name_val.empty:
                        display = f"{code} — {name_val.iloc[0]}"
                except Exception:
                    pass
            display_options.append(display)
            code_to_display[display] = code

        # 处理年份数据并标准化为整数列表
        years_raw = df[year_col].dropna().unique()
        years = []
        for year in years_raw:
            try:
                if isinstance(year, (int, float)):
                    years.append(int(year))
                else:
                    year_str = str(year)
                    year_num = re.search(r'\d{4}', year_str)
                    if year_num:
                        years.append(int(year_num.group()))
                    else:
                        years.append(int(float(year_str)))
            except Exception:
                continue
        years = sorted(list(set(years)))
    except Exception as e:
        st.error(f"处理数据时出错: {str(e)}")
        display_options = ['000001']
        code_to_display = { '000001': '000001' }
        years = [2021]
    
    # 用户输入部分
    st.markdown("## 查询参数设置")
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 股票代码输入 - 改进的搜索/选择（支持按代码或名称搜索）
        search_term = st.text_input("搜索股票代码或公司名称", "")
        if st.button('清除搜索'):
            search_term = ""

        query = search_term.strip().lower()

        # 过滤显示选项（在 '代码 — 名称' 或 仅代码 中进行匹配）
        filtered = display_options
        if query:
            try:
                # 尝试使用模糊匹配（如果 rapidfuzz 可用）获取前20项
                from rapidfuzz import process, fuzz
                # 构建候选键（显示文字与代码）
                candidates = display_options
                results = process.extract(query, candidates, scorer=fuzz.WRatio, limit=50)
                # 过滤相似度阈值 50
                filtered = [r[0] for r in results if r[1] >= 50]
                if not filtered:
                    # 退回到简单包含匹配
                    filtered = [opt for opt in display_options if query in opt.lower() or query in code_to_display.get(opt, '').lower()]
            except Exception:
                # rapidfuzz 不可用时回退到包含匹配
                filtered = [opt for opt in display_options if query in opt.lower() or query in code_to_display.get(opt, '').lower()]

        if not filtered:
            st.warning(f"未找到匹配 '{search_term}' 的股票代码或名称，显示全部选项")
            filtered = display_options

        # 使用 selectbox 让用户选择（显示为 '代码 — 名称'）
        selected_display = st.selectbox('请选择股票代码', options=filtered, index=0)
        # 从显示文本解析出实际股票代码
        selected_code = code_to_display.get(selected_display, None)

        # 允许用户直接输入股票代码并使用按钮查询
        manual_code = st.text_input('或直接输入股票代码（例如 000001）', '')
        if manual_code:
            if st.button('按代码查询', key='manual_query'):
                selected_code = format_stock_code(manual_code)
                # 同步 selected_display 显示为代码形式（或名称如果存在）
                # 如果有对应名称，更新展示文本
                found_display = None
                for disp, code in code_to_display.items():
                    if code == selected_code:
                        found_display = disp
                        break
                if found_display:
                    selected_display = found_display
                else:
                    selected_display = selected_code
    
    with col2:
        # 年份范围选择
        st.markdown("### 年份范围")
        
        # 如果年份数量较多，使用滑块选择
        if len(years) > 5:
            year_range = st.slider(
                '选择年份范围',
                min_value=min(years),
                max_value=max(years),
                value=(min(years), max(years)),
                step=1
            )
            start_year, end_year = year_range[0], year_range[1]
        else:
            # 否则使用选择框
            start_year = st.selectbox(
                '起始年份',
                options=years,
                index=0
            )
            end_year = st.selectbox(
                '结束年份',
                options=years,
                index=len(years)-1 if years else 0
            )
    
    # 验证年份输入
    if start_year > end_year:
        st.warning('起始年份不能大于结束年份，请重新选择。')
    else:
        # 执行查询
        if st.button('执行查询', type="primary"):
            if not selected_code:
                st.error("请先选择有效的股票代码")
            else:
                with st.spinner(f"正在查询 {selected_code} 的数据..."):
                    filtered_df = None
                    try:
                        # 筛选数据
                        # 使用全局的format_stock_code函数来确保一致性
                        # 应用格式化函数并创建掩码
                        code_mask = df[stock_code_col].apply(format_stock_code) == format_stock_code(selected_code)
                        year_mask = (df[year_col] >= start_year) & (df[year_col] <= end_year)
                        
                        filtered_df = df[code_mask & year_mask]
                        
                        # 按年份排序
                        filtered_df = filtered_df.sort_values(by=year_col)
                        
                        # 显示查询结果
                        if not filtered_df.empty:
                            st.markdown(f"## 查询结果: {selected_code}")
                            
                            # 使用expander来折叠/展开详细数据
                            with st.expander("查看详细数据", expanded=False):
                                st.dataframe(filtered_df, width='stretch')
                        
                    except Exception as e:
                        st.error(f"查询过程中出现错误: {e}")
                    
                    # 准备可视化数据
                    if filtered_df is not None:
                        years_data = filtered_df[year_col]
                        index_data = filtered_df[metric_col]
                        
                        # 可视化选项
                        st.subheader('📊 可视化选项')
                        chart_type = st.radio(
                            '选择图表类型',
                            options=['折线图', '柱状图', '面积图', '散点图'],
                            horizontal=True
                        )
                        
                        # 初始化图表对象
                        fig = None
                        
                        # 使用Plotly创建交互式图表
                        if chart_type == '折线图':
                            fig = px.line(
                                filtered_df,
                                x=year_col,
                                y=metric_col,
                                title=f'{selected_code} {metric_col} 趋势',
                                labels={year_col: '年份', metric_col: metric_col},
                                markers=True,
                                line_shape='linear'
                            )
                            
                            # 自定义图表样式
                            fig.update_layout(
                                font=dict(family="SimHei, WenQuanYi Micro Hei, Heiti TC"),
                                plot_bgcolor='white',
                                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
                                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
                                hovermode='x unified',
                                margin=dict(t=60, b=40, l=40, r=20)
                            )
                            
                            # 添加趋势线
                            if len(filtered_df) >= 2:  # 确保有足够数据点
                                fig.add_traces(go.Scatter(
                                    x=filtered_df[year_col],
                                    y=filtered_df[metric_col].rolling(window=2).mean(),
                                    mode='lines',
                                    name='移动平均',
                                    line=dict(color='red', dash='dash')
                                ))
                        
                        elif chart_type == '柱状图':
                            fig = px.bar(
                                filtered_df,
                                x=year_col,
                                y=metric_col,
                                title=f'{selected_code} {metric_col}',
                                labels={year_col: '年份', metric_col: metric_col},
                                color_discrete_sequence=['#667eea'],
                                text=metric_col
                            )
                            
                            # 自定义图表样式
                            fig.update_layout(
                                font=dict(family="SimHei, WenQuanYi Micro Hei, Heiti TC"),
                                plot_bgcolor='white',
                                xaxis=dict(showgrid=False),
                                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
                                hovermode='x unified',
                                margin=dict(t=60, b=40, l=40, r=20)
                            )
                            
                            # 添加数据标签
                            fig.update_traces(texttemplate='%{text:.2f}', textposition='auto', textfont=dict(size=10))
                            
                            # 添加移动平均线（可选）
                            if len(filtered_df) >= 2:  # 确保有足够数据点
                                fig.add_traces(go.Scatter(
                                    x=filtered_df[year_col],
                                    y=filtered_df[metric_col].rolling(window=2).mean(),
                                    mode='lines',
                                    name='移动平均',
                                    line=dict(color='red', dash='dash'),
                                    yaxis='y'
                                ))
                        
                        elif chart_type == '面积图':
                            fig = px.area(
                                filtered_df,
                                x=year_col,
                                y=metric_col,
                                title=f'{selected_code} {metric_col} 趋势',
                                labels={year_col: '年份', metric_col: metric_col},
                                color_discrete_sequence=['rgba(102, 126, 234, 0.3)']
                            )
                            
                            # 自定义图表样式
                            fig.update_layout(
                                font=dict(family="SimHei, WenQuanYi Micro Hei, Heiti TC"),
                                plot_bgcolor='white',
                                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
                                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
                                hovermode='x unified',
                                margin=dict(t=60, b=40, l=40, r=20)
                            )
                            
                            # 添加移动平均线
                            if len(filtered_df) >= 2:  # 确保有足够数据点
                                fig.add_traces(go.Scatter(
                                    x=filtered_df[year_col],
                                    y=filtered_df[metric_col].rolling(window=2).mean(),
                                    mode='lines',
                                    name='移动平均',
                                    line=dict(color='red', dash='dash')
                                ))
                        
                        else:  # 散点图
                            fig = px.scatter(
                                filtered_df,
                                x=year_col,
                                y=metric_col,
                                title=f'{selected_code} {metric_col} 散点图',
                                labels={year_col: '年份', metric_col: metric_col},
                                color_discrete_sequence=['#764ba2']
                            )
                            
                            # 自定义图表样式
                            fig.update_layout(
                                font=dict(family="SimHei, WenQuanYi Micro Hei, Heiti TC"),
                                plot_bgcolor='white',
                                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
                                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
                                hovermode='closest',
                                margin=dict(t=60, b=40, l=40, r=20)
                            )
                            
                            # 添加数据标签
                            fig.add_traces(go.Scatter(
                                x=filtered_df[year_col],
                                y=filtered_df[metric_col],
                                mode='markers+text',
                                text=filtered_df[metric_col].round(2),
                                textposition='top center',
                                showlegend=False,
                                marker=dict(color='#764ba2', size=6),
                                textfont=dict(size=10)
                            ))
                            
                            # 添加移动平均线
                            if len(filtered_df) >= 2:  # 确保有足够数据点
                                fig.add_traces(go.Scatter(
                                    x=filtered_df[year_col],
                                    y=filtered_df[metric_col].rolling(window=2).mean(),
                                    mode='lines',
                                    name='移动平均',
                                    line=dict(color='red', dash='dash')
                                ))
                            
                            # 添加数据标签
                            fig.add_traces(go.Scatter(
                                x=filtered_df[year_col],
                                y=filtered_df[metric_col],
                                mode='markers+text',
                                text=filtered_df[metric_col].round(2),
                                textposition='top right',
                                showlegend=False,
                                marker=dict(color='#764ba2', size=8),
                                textfont=dict(size=10)
                            ))
                            
                            # 添加趋势线
                            if len(filtered_df) >= 2:  # 确保有足够数据点
                                z = np.polyfit(filtered_df[year_col], filtered_df[metric_col], 1)
                                p = np.poly1d(z)
                                fig.add_traces(go.Scatter(
                                    x=filtered_df[year_col],
                                    y=p(filtered_df[year_col]),
                                    mode='lines',
                                    name='趋势线',
                                    line=dict(color='red', dash='dash')
                                ))
                    
                    # 确保图表对象已创建并且数据不为空
                    if fig is not None and not filtered_df.empty:
                        # 显示图表
                        st.plotly_chart(fig, width='stretch')
                    else:
                        st.warning("无法生成图表，请检查数据是否足够或格式是否正确。")
                    
                    # 添加静态Matplotlib备用图表
                    if not filtered_df.empty:
                        st.markdown("### 备用图表")
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.plot(years_data, index_data, marker='o', linewidth=2, markersize=8)
                        
                        # 设置图表属性
                        ax.set_title(f'{selected_code} 数字化转型指数趋势', fontsize=16)
                        ax.set_xlabel('年份', fontsize=12)
                        ax.set_ylabel('数字化转型指数', fontsize=12)
                        ax.grid(True, linestyle='--', alpha=0.7)
                        
                        # 优化坐标轴
                        ax.tick_params(axis='both', labelsize=10)
                        
                        # 添加数据标签
                        for i, value in enumerate(index_data):
                            ax.text(years_data.iloc[i], value + max(index_data) * 0.01,
                                    f'{value:.2f}', ha='center', fontsize=9)
                        
                        # 自动调整布局
                        plt.tight_layout()
                        
                        # 显示图表
                        st.pyplot(fig)
                        
                        # 显示统计信息
                        st.subheader('📈 统计信息')
                        
                        # 使用卡片式布局显示统计信息
                        stats_container = ""
                        stats_container += f"<div class='stats-container'>"
                        
                        # 数据条数
                        stats_container += f"<div class='stat-box'>"
                        stats_container += f"<div class='stat-value'>{len(filtered_df)}</div>"
                        stats_container += f"<div class='stat-label'>数据条数</div>"
                        stats_container += f"</div>"
                        
                        # 最小指数值
                        min_val = index_data.min()
                        stats_container += f"<div class='stat-box'>"
                        stats_container += f"<div class='stat-value'>{min_val:.2f}</div>"
                        stats_container += f"<div class='stat-label'>最小指数值</div>"
                        stats_container += f"</div>"
                        
                        # 最大指数值
                        max_val = index_data.max()
                        stats_container += f"<div class='stat-box'>"
                        stats_container += f"<div class='stat-value'>{max_val:.2f}</div>"
                        stats_container += f"<div class='stat-label'>最大指数值</div>"
                        stats_container += f"</div>"
                        
                        # 平均指数值
                        avg_val = index_data.mean()
                        stats_container += f"<div class='stat-box'>"
                        stats_container += f"<div class='stat-value'>{avg_val:.2f}</div>"
                        stats_container += f"<div class='stat-label'>平均指数值</div>"
                        stats_container += f"</div>"
                        
                        stats_container += f"</div>"
                        st.markdown(stats_container, unsafe_allow_html=True)
                    
                    # 导出功能（导出并在界面中提供下载）
                    with st.expander('导出数据与图表', expanded=False):
                        if not filtered_df.empty:
                            csv_path = os.path.join(export_dir, f"{format_stock_code(selected_code)}_{start_year}_{end_year}.csv")
                            excel_path = os.path.join(export_dir, f"{format_stock_code(selected_code)}_{start_year}_{end_year}.xlsx")
                            if st.button('导出 CSV'):
                                try:
                                    filtered_df.to_csv(csv_path, index=False)
                                    st.success(f'已导出 CSV: {csv_path}')
                                except Exception as e:
                                    st.error(f'导出失败: {e}')
                            if st.button('导出 Excel'):
                                try:
                                    filtered_df.to_excel(excel_path, index=False)
                                    st.success(f'已导出 Excel: {excel_path}')
                                except Exception as e:
                                    st.error(f'导出失败: {e}')

                            # 列出 exports 目录中文件并提供下载
                            files = []
                            try:
                                files = sorted([f for f in os.listdir(export_dir) if os.path.isfile(os.path.join(export_dir, f))])
                            except Exception:
                                files = []

                            if files:
                                st.markdown('**已导出文件**')
                                for fn in files:
                                    fp = os.path.join(export_dir, fn)
                                    try:
                                        with open(fp, 'rb') as fh:
                                            btn = st.download_button(label=f'下载 {fn}', data=fh.read(), file_name=fn)
                                    except Exception:
                                        st.write(fn)
                            else:
                                st.info('尚无导出文件')
                        else:
                            st.info('没有可导出的数据')

                    # 计算增长率
                    if len(index_data) >= 2:
                        # 创建增长率卡片
                        growth_rate = (index_data.iloc[-1] - index_data.iloc[0]) / index_data.iloc[0] * 100
                        growth_text = f"{growth_rate:.2f}%"
                        growth_color = "#28a745" if growth_rate > 0 else "#dc3545" if growth_rate < 0 else "#6c757d"
                        
                        growth_card = ""
                        growth_card += f"<div class='card'>"
                        growth_card += f"<div style='display: flex; align-items: center; justify-content: space-between;'>"
                        growth_card += f"<div>"
                        growth_card += f"<h4 style='margin: 0; color: #1a5276;'>指数增长率</h4>"
                        growth_card += f"<p style='margin: 0.2rem 0; color: #666;'>从 {years_data.iloc[0]} 到 {years_data.iloc[-1]}</p>"
                        growth_card += f"</div>"
                        growth_card += f"<div style='font-size: 2rem; font-weight: bold; color: {growth_color};'>{growth_text}</div>"
                        growth_card += f"</div>"
                        growth_card += f"</div>"
                        
                        st.markdown(growth_card, unsafe_allow_html=True)
                        
                        # 添加趋势分析
                        trend_analysis = ""
                        trend_analysis += f"<div class='card'>"
                        trend_analysis += f"<h4 style='margin-top: 0; color: #1a5276;'>📊 趋势分析</h4>"
                        
                        if growth_rate > 10:
                            trend_analysis += f"<p style='color: #28a745;'>📈 <strong>快速增长</strong>: 数字化转型指数呈现显著上升趋势</p>"
                        elif growth_rate > 0:
                            trend_analysis += f"<p style='color: #28a745;'>📈 <strong>稳定增长</strong>: 数字化转型指数逐步提升</p>"
                        elif growth_rate == 0:
                            trend_analysis += f"<p style='color: #6c757d;'>➡️ <strong>保持稳定</strong>: 数字化转型指数无明显变化</p>"
                        elif growth_rate > -10:
                            trend_analysis += f"<p style='color: #dc3545;'>📉 <strong>轻微下降</strong>: 数字化转型指数略有下滑</p>"
                        else:
                            trend_analysis += f"<p style='color: #dc3545;'>📉 <strong>显著下降</strong>: 数字化转型指数大幅下滑</p>"
                        
                        # 计算波动率
                        if len(index_data) > 1:
                            volatility = index_data.std() / index_data.mean() * 100 if index_data.mean() != 0 else 0
                            trend_analysis += f"<p>📊 <strong>指数波动率</strong>: {volatility:.2f}% (数据波动程度)</p>"
                        
                        trend_analysis += f"</div>"
                        st.markdown(trend_analysis, unsafe_allow_html=True)
                    else:
                        st.info("需要至少2个数据点来计算增长率和趋势分析")
                    
                    # 检查是否没有数据
                    if filtered_df.empty:
                        st.info(f'未找到股票代码 {selected_code} 在 {start_year} 至 {end_year} 年间的数据。')
                        
                        # 提供可能的解决方案
                        st.markdown("""
                        <div class="info-box">
                        <strong>可能的原因：</strong>
                        <ul>
                        <li>该股票代码在所选年份范围内没有数据</li>
                        <li>股票代码格式不匹配，请检查是否输入正确</li>
                        <li>字段映射设置可能不正确，请在左侧重新选择</li>
                        </ul>
                        </div>
                        "", unsafe_allow_html=True""")

# 应用说明
with st.sidebar.expander("使用说明", expanded=False):
    st.markdown("""
    ## 使用步骤
    1. 在左侧设置字段映射，确保正确识别股票代码、年份和指数列
    2. 在主界面使用搜索框快速找到目标股票代码
    3. 设置查询的年份范围（可使用滑块或下拉选择框）
    4. 点击"执行查询"按钮获取结果
    5. 查看统计信息和可视化图表
    
    ## 功能说明
    - **数据概览**：显示数据的基本统计信息
    - **字段映射**:灵活适配不同格式的Excel文件
    - **股票搜索**：快速定位目标股票代码
    - **多图表类型**：支持折线图、柱状图和面积图
    - **统计分析**：提供关键指标的统计数据
    
    ## 注意事项
    - 如果数据加载失败,请检查Excel文件是否存在且格式正确
    - 确保Excel文件与应用在同一目录下
    - 对于较大的数据集，首次加载可能需要较长时间
    """)

# 页脚信息
st.markdown("""---
<div class='footer'>
    <div style='margin-bottom: 1rem;'>
        <h3 style='margin: 0; color: #1a5276;'>企业数字化转型指数查询系统</h3>
        <p style='margin: 0.3rem 0; color: #666;'>v1.0</p>
    </div>
    <div style='display: flex; flex-wrap: wrap; justify-content: center; gap: 2rem; margin-bottom: 1rem;'>
        <div>
            <h4 style='margin: 0; color: #1a5276;'>技术栈</h4>
            <p style='margin: 0.3rem 0; color: #666;'>Python | Streamlit | Plotly | Pandas</p>
        </div>
        <div>
            <h4 style='margin: 0; color: #1a5276;'>功能特色</h4>
            <p style='margin: 0.3rem 0; color: #666;'>数据可视化 | 统计分析 | 趋势预测</p>
        </div>
        <div>
            <h4 style='margin: 0; color: #1a5276;'>支持</h4>
            <p style='margin: 0.3rem 0; color: #666;'>Excel数据导入 | 多主题切换 | 响应式设计</p>
        </div>
    </div>
    <p style='color: #999; font-size: 0.9rem;'>© 2024 企业数字化转型指数查询系统. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
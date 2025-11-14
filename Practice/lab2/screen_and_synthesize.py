import pandas as pd
import os
import re

# 文件路径
input_file = '/workspaces/Comm2026/Practice/lab2/input/AI_mental_health.csv'
output_dir = '/workspaces/Comm2026/Practice/lab2/output'
output_csv = os.path.join(output_dir, 'AI_mental_health_with_genai.csv')
output_report = os.path.join(output_dir, 'GenAI_Usage_Report.md')

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 读取CSV
df = pd.read_csv(input_file)

# 定义生成式AI技术关键词
genai_keywords = {
    'ChatGPT': ['chatgpt', 'gpt-3', 'gpt-4', 'gpt4', 'openai', 'chat gpt'],
    'Gemini': ['gemini', 'bard', 'google'],
    'Claude': ['claude', 'anthropic'],
    'DeepSeek': ['deepseek'],
    'GPT': ['generative pre-trained transformer', 'large language model', 'llm'],
    'Other LLM': ['language model', 'transformer', 'bert', 'gpt-', 'llama']
}

def detect_genai(text):
    """检测摘要中使用的生成式AI技术"""
    if pd.isna(text):
        return 'None'
    
    text_lower = str(text).lower()
    detected = []
    
    for ai_type, keywords in genai_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                if ai_type not in detected:
                    detected.append(ai_type)
                break
    
    return ', '.join(detected) if detected else 'None'

# 添加GenAI列
print("正在检测生成式AI技术...")
df['GenAI_Used'] = df['Abstract'].apply(detect_genai)

# 保存CSV文件
df.to_csv(output_csv, index=False)
print(f"✓ CSV文件已保存: {output_csv}")

# 生成报告
report_content = "# GenAI Usage Report\n\n"
report_content += "## Summary\n\n"

# 统计信息
genai_count = (df['GenAI_Used'] != 'None').sum()
total_count = len(df)
report_content += f"Total studies analyzed: **{total_count}**\n\n"
report_content += f"Studies using Generative AI: **{genai_count}** ({genai_count/total_count*100:.1f}%)\n\n"

# 详细分析前20条
report_content += "## Detailed Analysis of First 20 Studies\n\n"

for idx, row in df.head(20).iterrows():
    report_content += f"### Study {idx + 1}: {row['Title']}\n\n"
    report_content += f"**Authors:** {row['Authors']}\n\n"
    report_content += f"**Year:** {row['Year']}\n\n"
    report_content += f"**GenAI Tools Used:** {row['GenAI_Used']}\n\n"
    
    if row['GenAI_Used'] != 'None':
        report_content += f"**Analysis:** This study employs generative AI technology in its research. "
        report_content += f"The abstract mentions the use of {row['GenAI_Used'].lower()} for mental health applications.\n\n"
    else:
        report_content += f"**Analysis:** This study does not explicitly mention the use of generative AI tools in the abstract.\n\n"
    
    abstract_text = str(row['Abstract']) if pd.notna(row['Abstract']) else "No abstract available"
    report_content += f"**Abstract Summary:** {abstract_text[:200]}...\n\n"
    report_content += "---\n\n"

# 保存报告
with open(output_report, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"✓ 报告已保存: {output_report}")
print(f"\n统计信息:")
print(f"  - 总研究数: {total_count}")
print(f"  - 使用生成式AI的研究: {genai_count}")
print(f"  - 使用比例: {genai_count/total_count*100:.1f}%")

# 显示GenAI技术使用分布
print(f"\n生成式AI技术使用分布:")
genai_dist = df['GenAI_Used'].value_counts()
for tech, count in genai_dist.items():
    print(f"  - {tech}: {count}")

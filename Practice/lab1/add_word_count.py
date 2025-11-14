import pandas as pd
import os

# 读取输入CSV文件
input_file = '/workspaces/Comm2026/Practice/lab1/input/AI_mental_health.csv'
output_dir = '/workspaces/Comm2026/Practice/lab1/output'

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 读取CSV
df = pd.read_csv(input_file)

# 创建新列来计算每个摘要的字数
def count_words(abstract):
    if pd.isna(abstract):
        return 0
    return len(str(abstract).split())

# 添加Word_Count列
df['Word_Count'] = df['Abstract'].apply(count_words)

# 保存到输出目录
output_file = os.path.join(output_dir, 'AI_mental_health_with_word_count.csv')
df.to_csv(output_file, index=False)

print(f"✓ 处理完成！")
print(f"✓ 输入文件: {input_file}")
print(f"✓ 输出文件: {output_file}")
print(f"✓ 总行数: {len(df)}")
print(f"✓ 新增列: Word_Count")
print(f"\n前5行的摘要字数:")
print(df[['Title', 'Word_Count']].head())

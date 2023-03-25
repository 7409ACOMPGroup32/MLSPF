import pandas as pd
import numpy as np

# 读取csv文件
df = pd.read_csv("Analysis_News.csv")

# 对每一天的positive_score和negative_score相减生成新列“my_score”
df["my_score"] = df["positive_score"] - df["negative_score"]

# 将"Date"列转换为日期格式
df["Date"] = pd.to_datetime(df["Date"])

# 对"my_score"列进行归一化
df["my_score"] = (df["my_score"] - df["my_score"].min()) / (df["my_score"].max() - df["my_score"].min())

# 计算每天的平均值
daily_average = df.groupby("Date")["my_score"].mean()

# 生成一个新的日期范围，包括缺失日期
date_range = pd.date_range(start=df["Date"].min(), end=df["Date"].max(), freq="D")

# 创建一个新的dataframe，使用新的日期范围
new_df = pd.DataFrame(date_range, columns=["Date"])

# 将每天的平均值合并到新的dataframe中
new_df = new_df.merge(daily_average, on="Date", how="left")

# 使用0填充缺失的“my_score”值
new_df["my_score"].fillna(0, inplace=True)

# 显示新的dataframe
print(new_df)

# 将"Date"设置为索引
new_df.set_index("Date", inplace=True)

# 标记周末和周一
new_df["is_weekend"] = new_df.index.weekday.isin([5, 6])
new_df["is_monday"] = new_df.index.weekday == 0

# # 计算每个周一的上周六、上周日和周一三天的平均值

monday_averages = []
for i, row in new_df.iterrows():
    if row["is_monday"]:
        
        weekend_dates = [i - pd.Timedelta(days=1), i - pd.Timedelta(days=2)]
        weekend_scores = new_df[new_df.index.isin(weekend_dates)]["my_score"]
        monday_averages.append((row["my_score"] + weekend_scores.sum()) / 3)
        # break
# # 将周一的值替换为上周六、上周日和周一三天的平均值
new_df.loc[new_df["is_monday"], "my_score"] = monday_averages

# # 删除周末的数据
new_df = new_df[~new_df["is_weekend"]]

# # 删除"is_weekend"和"is_monday"列
new_df.drop(["is_weekend", "is_monday"], axis=1, inplace=True)



# # 显示新的dataframe
print(new_df)

# 将new_df存储为CSV文件
new_df.to_csv("cooked_text_score.csv")


import os
import csv
import pandas as pd
from collections import defaultdict

# 仮データ（本番はTwitter APIで収集）
data_weekly = [
    ('user1', 'reply'), ('user1', 'like'), ('user1', 'retweet'),
    ('user2', 'like'), ('user2', 'like'),
    ('user3', 'reply'), ('user3', 'reply'), ('user3', 'retweet'),
]

# 重み設定
weights = {'reply': 3, 'retweet': 2, 'like': 1}

# スコア集計
score_week = defaultdict(lambda: {'reply': 0, 'retweet': 0, 'like': 0})

for user, action in data_weekly:
    score_week[user][action] += 1

# スコア計算
records = []
for user, counts in score_week.items():
    total = sum(counts[a] * weights[a] for a in counts)
    records.append({
        'ユーザー': user,
        'リプ数': counts['reply'],
        'RT数': counts['retweet'],
        'いいね数': counts['like'],
        'スコア': total
    })

df_week = pd.DataFrame(records).sort_values(by='スコア', ascending=False)
df_week.to_csv('weekly_fan_score.csv', index=False)

# 累計読み込み・更新
if os.path.exists('total_fan_score.csv'):
    df_total = pd.read_csv('total_fan_score.csv')
    df_total.set_index('ユーザー', inplace=True)
else:
    df_total = pd.DataFrame(columns=['ユーザー', 'リプ数', 'RT数', 'いいね数', 'スコア'])
    df_total.set_index('ユーザー', inplace=True)

for row in records:
    user = row['ユーザー']
    if user not in df_total.index:
        df_total.loc[user] = [0, 0, 0, 0]
    df_total.loc[user, 'リプ数'] += row['リプ数']
    df_total.loc[user, 'RT数'] += row['RT数']
    df_total.loc[user, 'いいね数'] += row['いいね数']
    df_total.loc[user, 'スコア'] += row['スコア']

df_total = df_total.reset_index().sort_values(by='スコア', ascending=False)
df_total.to_csv('total_fan_score.csv', index=False)
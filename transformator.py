import pandas as pd

df1 = pd.DataFrame()
df = pd.read_csv('test_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index(df['Date'], inplace=True)
for column in df.columns[1:]:
    df1[column] = df[column].resample('W').sum()
print(df1.head(20))
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("employee_productivity_realistic.csv")
df['Login_Time'] = pd.to_datetime(df['Login_Time'],dayfirst=True,errors='coerce')
print(df['Login_Time'].head())
df['Logout_Time'] = pd.to_datetime(df['Logout_Time'],dayfirst=True,errors='coerce')
print(df['Logout_Time'].head())
print(df.dtypes)


df['Working_Hours'] = (
    df['Logout_Time'] - df['Login_Time']
).dt.total_seconds() / 3600
df[['Login_Time','Logout_Time','Working_Hours']].head()
df=df.dropna(subset=['Working_Hours'])   
df['Login_Time']=df['Logout_Time'].fillna(df['Login_Time'].dt.normalize() + pd.Timedelta(hours=18))
df=df[df['Working_Hours']>0]


      
df['Net_Work_Hours'] = df['Working_Hours'] - (df['Break_Duration_Min'] / 60)
def productivity_lable(hours):
    if hours >= 8:
        return 'high'
    elif  hours >= 6:
        return 'Medium'
    else:
        return 'Low'
df['Productivity_Label'] = df['Net_Work_Hours'].apply(productivity_lable)
df['Productivity_Label']=df['Working_Hours'].apply(productivity_lable)


daily_productivity = df.groupby(df['Login_Time'].dt.date)['Working_Hours'].mean()
plt.figure(figsize=(10, 5))

monthly_productivity = df.groupby(df['Login_Time'].dt.to_period('M'))['Working_Hours'].mean()

monthly_productivity.plot(kind='bar', color='skyblue')
plt.title('Average Monthly Working Hours')
plt.xlabel('Month')
plt.ylabel('Average Working Hours')
plt.show()

df['Productivity'] = df['Tasks_Completed'] / df['Net_Work_Hours']
df['Efficiency_Percent'] = (
    df['Tasks_Completed'] / df['Expected_Tasks']
) * 100
print(df[['Productivity','Efficiency_Percent']].head())
dept_eff=df.groupby('Department')['Efficiency_Percent'].mean()
print(dept_eff)

dept_eff.plot(kind='bar', color='blue')
plt.title('Average Efficiency Percentage by Department')            
plt.xlabel('Department')
plt.ylabel('Average Efficiency Percentage')
plt.show()
df.groupby('Department')['Productivity'].mean()
df.groupby('Work_Mode')['Productivity'].mean()
df[df['Net_Work_Hours'] > 9]


df.to_csv("employee_productivity_processed.csv", index=False)   
import pandas
import pandas as pd
pd.set_option('display.max_columns', None)

# Load dataset
df = pd.read_csv('insurance.csv')

# Check for missing values
print(df.isnull().sum())

'''NO missing values'''

# Check for outliers
import matplotlib.pyplot as plt
import seaborn as sns

# Visualize outliers using boxplots
plt.figure(figsize=(12, 8))
for i, column in enumerate(['age', 'bmi', 'children', 'charges'], 1):
    plt.subplot(2, 2, i)
    sns.boxplot(x=df[column])
    plt.title(f'Box plot of {column}')
plt.tight_layout()
plt.show()

#OneHot encoding of non numerical data
df_encoded = pd.get_dummies(df, columns=['sex', 'smoker', 'region'])
df_encoded = df_encoded.astype(int)
print(df_encoded)

# Data types and structure
print(df.info())
print(df.describe())
print(df_encoded.info())
print(df_encoded.describe())
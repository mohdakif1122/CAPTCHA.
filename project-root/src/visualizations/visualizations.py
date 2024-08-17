# File: project-root/src/visualizations/visualizations.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the processed data
file_path = '/Users/kaushalkento/Desktop/GroupProject./CAPTCHARefinement./project-root/data/processed_rba-dataset.csv'
data = pd.read_csv(file_path)

# Define a function to save and show plots
def save_and_show_plot(fig, filename):
    fig.savefig(filename, bbox_inches='tight')
    plt.show()

# Set plot style
sns.set(style="whitegrid")

# Distribution of 'Round-Trip Time [ms]'
plt.figure(figsize=(12, 6))
sns.histplot(data['Round-Trip Time [ms]'], bins=50, kde=True, color='blue')
plt.title('Distribution of Round-Trip Time [ms]')
plt.xlabel('Round-Trip Time [ms]')
plt.ylabel('Frequency')
save_and_show_plot(plt.gcf(), 'distribution_round_trip_time.png')

# Distribution of 'Login Successful'
plt.figure(figsize=(8, 6))
sns.countplot(x='Login Successful', data=data, palette='viridis')
plt.title('Login Success vs. Failure')
plt.xlabel('Login Successful')
plt.ylabel('Count')
save_and_show_plot(plt.gcf(), 'login_success_vs_failure.png')

# Distribution of 'Is Attack IP'
plt.figure(figsize=(8, 6))
sns.countplot(x='Is Attack IP', data=data, palette='viridis')
plt.title('Attack IP Distribution')
plt.xlabel('Is Attack IP')
plt.ylabel('Count')
save_and_show_plot(plt.gcf(), 'attack_ip_distribution.png')

# Distribution of 'Is Account Takeover'
plt.figure(figsize=(8, 6))
sns.countplot(x='Is Account Takeover', data=data, palette='viridis')
plt.title('Account Takeover Distribution')
plt.xlabel('Is Account Takeover')
plt.ylabel('Count')
save_and_show_plot(plt.gcf(), 'account_takeover_distribution.png')

# Boxplot of 'Round-Trip Time [ms]' by 'Is Attack IP'
plt.figure(figsize=(12, 6))
sns.boxplot(x='Is Attack IP', y='Round-Trip Time [ms]', data=data, palette='Set2')
plt.title('Round-Trip Time [ms] by Attack IP')
plt.xlabel('Is Attack IP')
plt.ylabel('Round-Trip Time [ms]')
save_and_show_plot(plt.gcf(), 'round_trip_time_by_attack_ip.png')

# Boxplot of 'Round-Trip Time [ms]' by 'Is Account Takeover'
plt.figure(figsize=(12, 6))
sns.boxplot(x='Is Account Takeover', y='Round-Trip Time [ms]', data=data, palette='Set2')
plt.title('Round-Trip Time [ms] by Account Takeover')
plt.xlabel('Is Account Takeover')
plt.ylabel('Round-Trip Time [ms]')
save_and_show_plot(plt.gcf(), 'round_trip_time_by_account_takeover.png')

# Correlation heatmap of numerical features
plt.figure(figsize=(12, 8))
corr = data[['Round-Trip Time [ms]', 'index', 'User ID', 'ASN']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap')
save_and_show_plot(plt.gcf(), 'correlation_heatmap.png')

# Example of scatter plot between 'Round-Trip Time [ms]' and 'index'
plt.figure(figsize=(12, 6))
sns.scatterplot(x='index', y='Round-Trip Time [ms]', data=data, hue='Is Attack IP', palette='coolwarm', alpha=0.6)
plt.title('Round-Trip Time [ms] vs. Index')
plt.xlabel('Index')
plt.ylabel('Round-Trip Time [ms]')
plt.legend(title='Is Attack IP')
save_and_show_plot(plt.gcf(), 'round_trip_time_vs_index.png')

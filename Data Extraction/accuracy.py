import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Read the excel file
df = pd.read_excel("/Users/branbranyu/Downloads/metric extraction/results.xlsx")

# Box Plot for Accuracy by Pillar
df_pillars = df[df["Pillar"] != "Total"]

plt.figure(figsize=(8, 6))
sns.boxplot(data=df_pillars, x="Pillar", y="Accuracy (%)")
plt.title("Distribution of Accuracy by Pillar")
plt.ylim(0, 110)
plt.tight_layout()
plt.show()

# Calculate median accuracy for each pillar
median_accuracy = df_pillars.groupby("Pillar")["Accuracy (%)"].median().reset_index()
print(median_accuracy)

# Calculate mean accuracy for each pillar
mean_accuracy = df_pillars.groupby("Pillar")["Accuracy (%)"].mean().reset_index()
print(mean_accuracy)

# Bar Plot for Accuracy by Pillar and Company
plt.figure(figsize=(10, 6))
sns.barplot(data=df_pillars, x="Pillar", y="Accuracy (%)", hue="Company Name")
plt.title("Accuracy (%) by ESG Pillar and Company")
plt.ylabel("Accuracy (%)")
plt.xticks(rotation=45) 
plt.ylim(0, 110)
plt.tight_layout()
plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#Setting up output folder
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)
os.makedirs(os.path.join(output_folder, "visuals"), exist_ok=True)

#Load the dataset and display basic information
df = pd.read_csv('data/All_Diets.csv')
print("[INFO] Dataset successfully loaded.\n")

print("[INFO] Dataset Overview:")
print(df.info())
print("\nFirst 5 rows of dataset:\n", df.head(), "\n")


#Clean the data by handling missing values. Strips whitespace and standardizes text case.
if 'Diet_type' in df.columns:
    df['Diet_type'] = df['Diet_type'].str.strip().str.title()
if 'Cuisine_type' in df.columns:
    df['Cuisine_type'] = df['Cuisine_type'].str.strip().str.title()
print("[INFO] Data formatted (no missing values found).\n")

numeric_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())

df = df.fillna('Unknown')
print("[INFO] Missing values handled (numeric → mean, others → 'Unknown').\n")


#Calculate the average macronutrient content for each diet type
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
avg_macros.to_csv(os.path.join(output_folder, "average_macros_by_diet.csv"))
print("[INFO] Saved average_macros_by_diet.csv")

#Find the top 5 protein-rich recipes for each diet type
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
top_protein.to_csv(os.path.join(output_folder, "top5_protein_recipes_by_diet.csv"), index=False)
print("[INFO] Saved top5_protein_recipes_by_diet.csv")

#Add new metrics (Protein-to-Carbs ratio and Carbs-to-Fat ratio)
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

df.to_csv(os.path.join(output_folder, "processed_data_with_ratios.csv"), index=False)
print("[INFO] Saved processed_data_with_ratios.csv (with new metrics).")


# --- Visualizations ---
#Bar chart for average macronutrients
plt.figure(figsize=(10,6))
avg_macros.plot(kind='bar')
plt.title('Average Macronutrient Content by Diet Type', fontsize=14)
plt.xlabel('Diet Type')
plt.ylabel('Grams (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "visuals", "avg_macros_bar_chart.png"))
plt.show()
print("[INFO] Saved avg_macros_bar_chart.png")

#Heatmaps showing relationship between macronutrient content and diet types
plt.figure(figsize=(8,6))
sns.heatmap(avg_macros, annot=True, cmap='YlGnBu', fmt=".2f")
plt.title('Macronutrient Relationship Across Diet Types', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "visuals", "macronutrient_heatmap.png"))
plt.show()
print("[INFO] Saved macronutrient_heatmap.png")

#Scatter plots to display the top 5 protein-rich recipes and their distribution across different cuisines.
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=top_protein,
    x='Cuisine_type',
    y='Protein(g)',
    hue='Diet_type',
    size='Protein(g)',
    sizes=(50, 300),
    alpha=0.7
)
plt.title('Top 5 Protein-Rich Recipes by Cuisine and Diet Type', fontsize=14)
plt.xlabel('Cuisine Type')
plt.ylabel('Protein (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "visuals", "top5_protein_scatter.png"))
plt.show()
print("[INFO] Saved top5_protein_scatter.png")

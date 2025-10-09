"""
Project 1 - Task 1: Dataset Analysis & Insights
------------------------------------------------
This script processes the All_Diets.csv dataset to extract and visualize
nutritional insights for various diet types and cuisines.

Key features:
- Cleans missing data
- Calculates averages and ratios
- Identifies top protein-rich recipes
- Visualizes macronutrient trends

INSTALL DEPENDENCIES:
pip install pandas seaborn matplotlib
------------------------------------------------
Author: Cody Tran
Date: 2024-08-08
"""

# ========== IMPORTS ==========
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os

# ========== CONFIG ==========
DATA_PATH = "All_Diets.csv"  # Update if in different folder
OUTPUT_DIR = "outputs"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== 1. LOAD DATA ==========
print("\n[INFO] Loading dataset...")
df = pd.read_csv(DATA_PATH)
print(f"[INFO] Dataset loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.\n")

# ========== 2. DATA CLEANING ==========
print("[INFO] Cleaning missing values...")
numeric_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
df['Diet_type'] = df['Diet_type'].str.strip().str.title()
df['Cuisine_type'] = df['Cuisine_type'].str.strip().str.title()
print("[INFO] Missing values handled.\n")

# ========== 3. CALCULATE METRICS ==========
print("[INFO] Calculating average macronutrients per diet type...")
avg_macros = df.groupby('Diet_type')[numeric_cols].mean().round(2)
print(avg_macros, "\n")

print("[INFO] Finding top 5 protein-rich recipes per diet type...")
top_protein = (
    df.sort_values(by='Protein(g)', ascending=False)
    .groupby('Diet_type')
    .head(5)
    [['Diet_type', 'Recipe_name', 'Protein(g)', 'Cuisine_type']]
)
print(top_protein.head(10), "\n")

print("[INFO] Calculating ratios...")
df['Protein_to_Carbs_ratio'] = (df['Protein(g)'] / df['Carbs(g)']).replace([float('inf'), -float('inf')], 0)
df['Carbs_to_Fat_ratio'] = (df['Carbs(g)'] / df['Fat(g)']).replace([float('inf'), -float('inf')], 0)

# ========== 4. FIND INSIGHTS ==========
highest_protein_diet = avg_macros['Protein(g)'].idxmax()
print(f"[INSIGHT] Diet with highest average protein: {highest_protein_diet}\n")

most_common_cuisines = df.groupby('Diet_type')['Cuisine_type'].agg(lambda x: x.mode().iat[0] if not x.mode().empty else 'N/A')
print("[INSIGHT] Most common cuisine per diet type:\n", most_common_cuisines, "\n")

# ========== 5. VISUALIZATIONS ==========
print("[INFO] Generating visualizations...")

# Bar chart - Average macronutrients by diet type
plt.figure(figsize=(10, 6))
avg_macros.plot(kind='bar', width=0.8)
plt.title("Average Macronutrient Content by Diet Type", fontsize=14, weight='bold')
plt.xlabel("Diet Type")
plt.ylabel("Grams (g)")
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/avg_macros_bar_chart.png")
plt.close()

# Heatmap - Correlation of macros per diet type
plt.figure(figsize=(8, 5))
sns.heatmap(avg_macros.corr(), annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Correlation Between Macronutrients", fontsize=14, weight='bold')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/macros_heatmap.png")
plt.close()

# Scatter plot - Top protein-rich recipes
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=top_protein,
    x='Cuisine_type',
    y='Protein(g)',
    hue='Diet_type',
    palette='viridis',
    s=80
)
plt.title("Top 5 Protein-Rich Recipes by Cuisine", fontsize=14, weight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/top_protein_scatter.png")
plt.close()

print(f"[SUCCESS] Visualizations saved in '{OUTPUT_DIR}' folder.\n")

# ========== 6. LOG SUMMARY ==========
summary = {
    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Rows": len(df),
    "Diet_with_Highest_Protein": highest_protein_diet,
    "Output_Files": os.listdir(OUTPUT_DIR)
}

print("[SUMMARY]")
for key, value in summary.items():
    print(f"{key}: {value}")

print("\n[INFO] Task 1 completed successfully ✅")

import io
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from azure.storage.blob import BlobServiceClient, BlobClient

# -------------------------------
# Azure Blob Storage helper
# -------------------------------
def upload_to_blob(container_name, blob_name, data_bytes):
    """Upload bytes to a blob in Azure Storage."""
    connection_string = os.environ['AzureWebJobsStorage']
    blob_client = BlobClient.from_connection_string(
        conn_str=connection_string,
        container_name=container_name,
        blob_name=blob_name
    )
    blob_client.upload_blob(data_bytes, overwrite=True)
    print(f"[INFO] Uploaded {blob_name} to container {container_name}")

# -------------------------------
# Main function
# -------------------------------
def main(req=None):
    connection_string = os.environ['AzureWebJobsStorage']
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # --- Load dataset from 'datasets' container ---
    container_client = blob_service_client.get_container_client("datasets")
    blob_data = container_client.download_blob("All_Diets.csv").readall()
    df = pd.read_csv(io.BytesIO(blob_data))
    print("[INFO] Dataset successfully loaded from Azure Blob Storage.\n")

    print("[INFO] Dataset Overview:")
    print(df.info())
    print("\nFirst 5 rows:\n", df.head(), "\n")

    # --- Clean the data ---
    if 'Diet_type' in df.columns:
        df['Diet_type'] = df['Diet_type'].str.strip().str.title()
    if 'Cuisine_type' in df.columns:
        df['Cuisine_type'] = df['Cuisine_type'].str.strip().str.title()
    print("[INFO] Data formatted.\n")

    numeric_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())

    df = df.fillna('Unknown')
    print("[INFO] Missing values handled.\n")

    # --- Calculate metrics ---
    avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
    top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)

    df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
    df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

    # --- Upload CSVs to 'outputs' container ---
    upload_to_blob("outputs", "average_macros_by_diet.csv", avg_macros.to_csv(index=True).encode())
    upload_to_blob("outputs", "top5_protein_recipes_by_diet.csv", top_protein.to_csv(index=False).encode())
    upload_to_blob("outputs", "processed_data_with_metrics.csv", df.to_csv(index=False).encode())

    # --- Visualizations ---
    # 1. Bar chart of average macros
    plt.figure(figsize=(10,6))
    avg_macros.plot(kind='bar')
    plt.title('Average Macronutrient Content by Diet Type', fontsize=14)
    plt.xlabel('Diet Type')
    plt.ylabel('Grams (g)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    upload_to_blob("outputs", "avg_macros_bar_chart.png", buf.read())
    plt.close()
    print("[INFO] Uploaded avg_macros_bar_chart.png")

    # 2. Heatmap
    plt.figure(figsize=(8,6))
    sns.heatmap(avg_macros, annot=True, cmap='YlGnBu', fmt=".2f")
    plt.title('Macronutrient Relationship Across Diet Types', fontsize=14)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    upload_to_blob("outputs", "macronutrient_heatmap.png", buf.read())
    plt.close()
    print("[INFO] Uploaded macronutrient_heatmap.png")

    # 3. Scatter plot of top protein recipes
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
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    upload_to_blob("outputs", "top5_protein_scatter.png", buf.read())
    plt.close()
    print("[INFO] Uploaded top5_protein_scatter.png")

    print("[INFO] All processing and uploads completed successfully.")

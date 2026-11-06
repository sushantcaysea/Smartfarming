import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_plots():
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'crop_data', 'Crop_recommendation.csv')
    
    # Load dataset
    df = pd.read_csv(csv_path)
    
    columns = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    
    # Set the style
    sns.set_theme(style="whitegrid")
    
    # Plot and save each feature
    for col in columns:
        plt.figure(figsize=(8, 4.5))
        sns.kdeplot(df[col], fill=True, color="forestgreen", alpha=0.5, linewidth=2.5)
        plt.title(f"Density Distribution of {col.capitalize()}", fontsize=14, fontweight="bold", pad=15)
        plt.xlabel(col.capitalize(), fontsize=12)
        plt.ylabel("Density", fontsize=12)
        plt.tight_layout()
        
        # Save path in project root
        save_path = os.path.join(base_dir, f"{col}_density_plot.png")
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"Saved density plot to: {save_path}")

if __name__ == '__main__':
    generate_plots()

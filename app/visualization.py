import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime

# Set style for dark theme
plt.style.use('dark_background')
sns.set_palette("husl")

def generate_charts(df, dataset_id):
    """Generate visually appealing charts with insights"""
    try:
        chart_urls = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        # Enhanced Distribution Analysis
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            data = df[col].dropna()
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
            fig.patch.set_facecolor('#0a0a0a')
            
            # Histogram with KDE
            ax1.hist(data, bins=30, alpha=0.7, color='#00d4ff', edgecolor='white', linewidth=0.5)
            ax1.axvline(data.mean(), color='#ff6b6b', linestyle='--', linewidth=2, label=f'Mean: {data.mean():.2f}')
            ax1.axvline(data.median(), color='#4ecdc4', linestyle='--', linewidth=2, label=f'Median: {data.median():.2f}')
            ax1.set_title(f'Distribution Analysis: {col}', fontsize=16, fontweight='300', color='white', pad=20)
            ax1.set_xlabel(col, fontsize=12, color='#ccc')
            ax1.set_ylabel('Frequency', fontsize=12, color='#ccc')
            ax1.legend(frameon=False, fontsize=10)
            ax1.grid(True, alpha=0.2)
            
            # Box plot
            bp = ax2.boxplot(data, patch_artist=True, widths=0.6)
            bp['boxes'][0].set_facecolor('#00d4ff')
            bp['boxes'][0].set_alpha(0.7)
            for element in ['whiskers', 'fliers', 'medians', 'caps']:
                plt.setp(bp[element], color='white')
            ax2.set_title('Outlier Detection', fontsize=16, fontweight='300', color='white', pad=20)
            ax2.set_ylabel(col, fontsize=12, color='#ccc')
            ax2.grid(True, alpha=0.2)
            
            plt.tight_layout()
            filename = f"distribution_{dataset_id}_{timestamp}.png"
            filepath = f"static/{filename}"
            plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
            plt.close()
            chart_urls.append(f"/static/{filename}")
        
        # Enhanced Categorical Analysis
        if len(categorical_cols) > 0:
            col = categorical_cols[0]
            value_counts = df[col].value_counts().head(8)
            
            fig, ax = plt.subplots(figsize=(14, 8))
            fig.patch.set_facecolor('#0a0a0a')
            
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff', '#5f27cd']
            bars = ax.bar(range(len(value_counts)), value_counts.values, color=colors[:len(value_counts)], alpha=0.8)
            
            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, value_counts.values)):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       f'{value}\n({value/len(df)*100:.1f}%)', ha='center', va='bottom', 
                       fontsize=10, color='white', fontweight='500')
            
            ax.set_title(f'Category Distribution: {col}', fontsize=16, fontweight='300', color='white', pad=20)
            ax.set_xlabel('Categories', fontsize=12, color='#ccc')
            ax.set_ylabel('Count', fontsize=12, color='#ccc')
            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels(value_counts.index, rotation=45, ha='right', fontsize=10)
            ax.grid(True, alpha=0.2, axis='y')
            
            plt.tight_layout()
            filename = f"categories_{dataset_id}_{timestamp}.png"
            filepath = f"static/{filename}"
            plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
            plt.close()
            chart_urls.append(f"/static/{filename}")
        
        # Simple overview chart
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor('#0a0a0a')
        
        # Dataset info
        ax.text(0.5, 0.7, f'{len(df):,}', ha='center', va='center', transform=ax.transAxes,
                fontsize=48, color='#00d4ff', fontweight='200')
        ax.text(0.5, 0.5, 'Total Rows', ha='center', va='center', transform=ax.transAxes,
                fontsize=18, color='#ccc')
        ax.text(0.5, 0.3, f'{len(df.columns)} Columns', ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color='#888')
        ax.set_title('Dataset Overview', fontsize=20, fontweight='300', color='white', pad=30)
        ax.axis('off')
        
        plt.tight_layout()
        filename = f"overview_{dataset_id}_{timestamp}.png"
        filepath = f"static/{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
        plt.close()
        chart_urls.append(f"/static/{filename}")
        
        return chart_urls
    except Exception as e:
        print(f"Chart generation error: {e}")
        return []
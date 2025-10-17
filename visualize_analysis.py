import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

# Read the Excel file
file_path = r"c:\Users\Govin\Desktop\finance\Copy of Final_Financial_Data_Kaynes_Technology(1).xlsx"

# Create a comprehensive visualization
fig = plt.figure(figsize=(20, 14))

print("=" * 80)
print("CREATING VISUAL SUMMARY OF KAYNES TECHNOLOGY FINANCIAL DATA")
print("=" * 80)

# Kaynes Technology Data
kaynes_years = ['Mar-22', 'Mar-23', 'Mar-24', 'Mar-25']
kaynes_revenue = [671.39, 1086.56, 1273.94, 1915.44]
kaynes_net_profit = [40.99, 94.76, 126.10, 209.91]
kaynes_eps = [8.88, 16.30, 19.73, 32.75]

# BEL Data
bel_years = ['Mar-21', 'Mar-22', 'Mar-23', 'Mar-24', 'Mar-25']
bel_revenue = [14055.38, 15314.96, 17646.20, 20169.39, 23658.01]
bel_net_profit = [2065.42, 2348.93, 3006.67, 4020.00, 5288.25]
bel_eps = [8.48, 9.64, 4.11, 5.50, 7.23]

# 1. Revenue Comparison
ax1 = plt.subplot(3, 3, 1)
x = np.arange(len(kaynes_years))
width = 0.35
ax1.bar(x - width/2, kaynes_revenue, width, label='Kaynes', color='#3498db')
ax1.set_xlabel('Year')
ax1.set_ylabel('Revenue (Rs. Cr.)')
ax1.set_title('Kaynes Technology - Revenue Growth', fontweight='bold', fontsize=12)
ax1.set_xticks(x)
ax1.set_xticklabels(kaynes_years, rotation=45)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Add value labels on bars
for i, v in enumerate(kaynes_revenue):
    ax1.text(i, v + 30, str(v), ha='center', va='bottom', fontweight='bold')

# 2. Net Profit Trend
ax2 = plt.subplot(3, 3, 2)
ax2.plot(kaynes_years, kaynes_net_profit, marker='o', linewidth=2, markersize=8, color='#2ecc71')
ax2.fill_between(range(len(kaynes_years)), kaynes_net_profit, alpha=0.3, color='#2ecc71')
ax2.set_xlabel('Year')
ax2.set_ylabel('Net Profit (Rs. Cr.)')
ax2.set_title('Kaynes Technology - Net Profit Trend', fontweight='bold', fontsize=12)
ax2.grid(True, alpha=0.3)
for i, v in enumerate(kaynes_net_profit):
    ax2.text(i, v + 5, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')

# 3. EPS Growth
ax3 = plt.subplot(3, 3, 3)
ax3.bar(kaynes_years, kaynes_eps, color='#e74c3c', alpha=0.8)
ax3.set_xlabel('Year')
ax3.set_ylabel('EPS (Rs.)')
ax3.set_title('Kaynes Technology - EPS Growth', fontweight='bold', fontsize=12)
ax3.grid(True, alpha=0.3, axis='y')
for i, v in enumerate(kaynes_eps):
    ax3.text(i, v + 0.5, f'₹{v:.2f}', ha='center', va='bottom', fontweight='bold')

# 4. Financial Ratios - Kaynes
ax4 = plt.subplot(3, 3, 4)
ratios = ['Current\nRatio', 'Quick\nRatio', 'Debt-to-\nEquity']
mar22_ratios = [1.80, 0.88, 0.82]
mar25_ratios = [3.41, 2.42, 0.23]
x_ratios = np.arange(len(ratios))
width = 0.35
ax4.bar(x_ratios - width/2, mar22_ratios, width, label='Mar-22', color='#95a5a6')
ax4.bar(x_ratios + width/2, mar25_ratios, width, label='Mar-25', color='#3498db')
ax4.set_ylabel('Ratio Value')
ax4.set_title('Kaynes - Liquidity & Solvency Ratios', fontweight='bold', fontsize=12)
ax4.set_xticks(x_ratios)
ax4.set_xticklabels(ratios)
ax4.legend()
ax4.grid(True, alpha=0.3, axis='y')

# 5. Profitability Margins
ax5 = plt.subplot(3, 3, 5)
margins = ['Gross\nProfit %', 'Operating\nProfit %', 'Net\nProfit %']
mar25_margins = [19.48, 13.23, 10.96]
colors = ['#f39c12', '#e67e22', '#d35400']
bars = ax5.bar(margins, mar25_margins, color=colors, alpha=0.8)
ax5.set_ylabel('Margin (%)')
ax5.set_title('Kaynes - Profitability Margins (Mar-25)', fontweight='bold', fontsize=12)
ax5.grid(True, alpha=0.3, axis='y')
for bar, margin in zip(bars, mar25_margins):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{margin:.2f}%', ha='center', va='bottom', fontweight='bold')

# 6. BEL Revenue Trend
ax6 = plt.subplot(3, 3, 6)
ax6.plot(bel_years, bel_revenue, marker='s', linewidth=2, markersize=8, color='#9b59b6')
ax6.fill_between(range(len(bel_years)), bel_revenue, alpha=0.3, color='#9b59b6')
ax6.set_xlabel('Year')
ax6.set_ylabel('Revenue (Rs. Cr.)')
ax6.set_title('BEL - Revenue Trend (Benchmark)', fontweight='bold', fontsize=12)
ax6.grid(True, alpha=0.3)
plt.setp(ax6.xaxis.get_majorticklabels(), rotation=45)

# 7. Comparison - ROA
ax7 = plt.subplot(3, 3, 7)
years_comp = ['Mar-22', 'Mar-23', 'Mar-24', 'Mar-25']
kaynes_roa = [184.71, 107.32, 50.49, 62.96]
bel_roa = [132.04, 135.50, 133.60, 128.12]
ax7.plot(years_comp, kaynes_roa, marker='o', linewidth=2, label='Kaynes', color='#3498db')
ax7.plot(years_comp, bel_roa, marker='s', linewidth=2, label='BEL', color='#9b59b6')
ax7.set_xlabel('Year')
ax7.set_ylabel('ROA (%)')
ax7.set_title('Return on Assets - Comparison', fontweight='bold', fontsize=12)
ax7.legend()
ax7.grid(True, alpha=0.3)
plt.setp(ax7.xaxis.get_majorticklabels(), rotation=45)

# 8. Efficiency Ratios
ax8 = plt.subplot(3, 3, 8)
efficiency = ['Inventory\nTurnover', 'Receivable\nTurnover', 'Asset\nTurnover']
kaynes_eff = [2.83, 6.15, 0.64]
bel_eff = [1.82, 2.88, 1.32]
x_eff = np.arange(len(efficiency))
width = 0.35
ax8.bar(x_eff - width/2, kaynes_eff, width, label='Kaynes', color='#3498db')
ax8.bar(x_eff + width/2, bel_eff, width, label='BEL', color='#9b59b6')
ax8.set_ylabel('Turnover Ratio')
ax8.set_title('Efficiency Ratios Comparison (Mar-25)', fontweight='bold', fontsize=12)
ax8.set_xticks(x_eff)
ax8.set_xticklabels(efficiency)
ax8.legend()
ax8.grid(True, alpha=0.3, axis='y')

# 9. Summary Statistics Table
ax9 = plt.subplot(3, 3, 9)
ax9.axis('tight')
ax9.axis('off')

summary_data = [
    ['Metric', 'Kaynes (Mar-25)', 'BEL (Mar-25)'],
    ['Revenue (Cr.)', '₹1,915.44', '₹23,658.01'],
    ['Net Profit (Cr.)', '₹209.91', '₹5,288.25'],
    ['EPS (Rs.)', '₹32.75', '₹7.23'],
    ['Current Ratio', '3.41', '1.44'],
    ['Net Margin %', '10.96%', '22.35%'],
    ['ROA %', '62.96%', '128.12%'],
    ['Book Value', '₹412.36', '₹26.95']
]

table = ax9.table(cellText=summary_data, cellLoc='left', loc='center',
                  colWidths=[0.4, 0.3, 0.3])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)

# Header row formatting
for i in range(3):
    table[(0, i)].set_facecolor('#34495e')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(1, len(summary_data)):
    for j in range(3):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#ecf0f1')
        else:
            table[(i, j)].set_facecolor('#ffffff')

ax9.set_title('Financial Summary Comparison', fontweight='bold', fontsize=12, pad=20)

# Overall title
fig.suptitle('KAYNES TECHNOLOGY vs BEL - Comprehensive Financial Analysis Dashboard',
             fontsize=16, fontweight='bold', y=0.995)

plt.tight_layout(rect=[0, 0.03, 1, 0.99])
plt.savefig('Kaynes_Financial_Dashboard.png', dpi=300, bbox_inches='tight')
print("\n✅ Dashboard saved as: Kaynes_Financial_Dashboard.png")

# Show the plot
plt.show()

print("\n" + "=" * 80)
print("VISUAL ANALYSIS COMPLETE")
print("=" * 80)

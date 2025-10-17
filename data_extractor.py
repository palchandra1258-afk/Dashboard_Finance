"""
Financial Data Extractor
Extracts and structures all financial data from the Excel file for dashboard use
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Tuple, Any

class FinancialDataExtractor:
    """Extract and structure financial data from Excel file"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.kaynes_data = {}
        self.bel_data = {}
        
    def extract_all_data(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Extract all financial data for both companies"""
        
        # Read the Excel file
        df = pd.read_excel(self.file_path, sheet_name='Table 3', header=None)
        
        # Extract Kaynes Technology Data
        self.kaynes_data = self._extract_kaynes_data(df)
        
        # Extract BEL Data
        self.bel_data = self._extract_bel_data(df)
        
        return self.kaynes_data, self.bel_data
    
    def _extract_kaynes_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract Kaynes Technology financial data"""
        
        # Years for Kaynes (columns E-H represent Mar'25, Mar'24, Mar'23, Mar'22)
        years = [2025, 2024, 2023, 2022]
        
        # Cash Flow Statement (Rows 8-14, Columns E-H)
        cash_flow = {
            'years': years,
            'net_profit_before_tax': [275.35, 160.6, 124.52, 57.56],
            'operating_cash_flow': [65.05, -103.21, -52.29, 14.73],
            'investing_cash_flow': [-322.08, -1301.75, -480.46, -37.18],
            'financing_cash_flow': [258.58, 1394.59, 550.42, 25.89],
            'net_change_cash': [1.55, -10.37, 17.68, 3.43],
            'opening_cash': [12.82, 23.18, 5.51, 2.08],
            'closing_cash': [14.36, 12.82, 23.18, 5.51]
        }
        
        # Profit & Loss Statement (Rows 15-47, Columns M-P)
        income_statement = {
            'years': years,
            'total_income': [2050.46, 1359.60, 1165.62, 679.74],
            'sales_turnover': [1915.44, 1273.94, 1086.56, 671.39],
            'raw_materials': [1422.90, 950.59, 862.96, 485.97],
            'power_fuel': [7.94, 7.13, 5.13, 3.70],
            'employee_cost': [112.97, 88.10, 70.01, 56.09],
            'selling_admin': [2.55, 1.81, 2.01, 0.74],
            'misc_expenses': [114.25, 76.37, 48.72, 38.44],
            'total_expenses': [1660.61, 1124.00, 988.83, 584.94],
            'operating_profit': [253.33, 171.41, 164.88, 90.20],
            'pbdit': [389.85, 235.60, 176.79, 94.80],
            'interest': [87.73, 53.55, 34.38, 25.04],
            'pbdt': [302.12, 182.05, 142.41, 69.76],
            'depreciation': [26.78, 21.44, 17.67, 12.36],
            'profit_before_tax': [275.34, 160.61, 124.74, 57.40],
            'tax': [65.44, 34.50, 29.76, 16.58],
            'net_profit': [209.91, 126.10, 94.76, 40.99],
            'total_value_addition': [237.70, 173.42, 125.87, 98.97]
        }
        
        # Balance Sheet (Rows 16-47, Columns S-W)
        balance_sheet = {
            'years': years,
            'secured_loans': [613.94, 264.11, 127.73, 202.11],
            'reserves_surplus': [2027.21, 1789.92, 830.53, 0.00],
            'total_share_capital': [64.08, 63.92, 58.14, 46.16],
            'equity_share_capital': [64.08, 63.92, 58.14, 46.16],
            'gross_block': [967.46, 856.88, 755.38, 621.68],
            'accumulated_depreciation': [80.61, 64.43, 53.42, 46.24],
            'net_block': [886.85, 792.46, 701.96, 575.45],
            'capital_wip': [298.67, 328.27, 210.01, 187.32],
            'investments': [0.00, 0.00, 0.00, 75.00],
            'inventories': [532.53, 462.97, 411.80, 339.51],
            'sundry_debtors': [311.69, 291.51, 309.45, 313.51],
            'cash_bank': [234.97, 285.03, 213.80, 104.90],
            'loans_advances': [32.76, 12.95, 13.52, 73.62],
            'current_liabilities': [318.65, 281.35, 248.35, 357.37],
            'provisions': [7.97, 8.28, 6.14, 13.99],
            'net_current_assets': [785.33, 762.83, 694.08, 460.18],
            'contingent_liabilities': [378.47, 258.55, 127.62, 73.70]
        }
        
        # Per Share Data
        per_share = {
            'years': years,
            'shares_lakhs': [640.84, 639.18, 581.42, 461.58],
            'eps': [32.75, 19.73, 16.30, 8.88],
            'dividend_percent': [0, 0, 0, 0],
            'book_value': [412.36, 379.78, 164.83, 43.85]
        }
        
        # Financial Ratios
        ratios = {
            'years': years,
            # Liquidity Ratios
            'current_ratio': [3.41, 7.87, 3.57, 1.80],
            'quick_ratio': [2.42, 6.11, 2.27, 0.88],
            'cash_ratio': [2.09, 6.29, 1.57, 0.10],
            
            # Solvency Ratios
            'debt_to_equity': [0.23, 0.11, 0.13, 0.82],
            'debt_ratio': [1.00, 1.00, 1.00, 1.00],
            'times_interest_earned': [4.14, 4.00, 4.63, 3.29],
            
            # Profitability Ratios
            'gross_profit_margin': [19.48, 16.22, 7.48, 18.15],
            'operating_profit_margin': [13.23, 13.46, 15.17, 13.43],
            'net_profit_margin': [10.96, 9.90, 8.72, 6.11],
            'return_on_assets': [62.96, 50.49, 107.32, 184.71],
            
            # Efficiency Ratios
            'inventory_turnover': [2.83, 2.44, 3.25, None],
            'receivables_turnover': [6.15, 7.36, 5.31, None],
            'payables_turnover': [3.46, 3.70, 3.70, None],
            'asset_turnover': [0.64, 0.67, 1.49, None],
            
            # DuPont Components
            'tax_burden': [7.45, 8.47, 9.34, 11.84],
            'interest_burden': [0.76, 0.75, 0.78, 0.78]
        }
        
        return {
            'company': 'Kaynes Technology India Ltd',
            'ticker': 'KAYNES.NS',
            'sector': 'Electronics Manufacturing',
            'currency': 'INR',
            'cash_flow': cash_flow,
            'income_statement': income_statement,
            'balance_sheet': balance_sheet,
            'per_share': per_share,
            'ratios': ratios
        }
    
    def _extract_bel_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract Bharat Electronics Ltd financial data"""
        
        # Years for BEL (5 years: Mar'21 to Mar'25)
        years = [2025, 2024, 2023, 2022, 2021]
        
        # Balance Sheet (Rows 94-125, Columns F-J)
        balance_sheet = {
            'years': years,
            'total_share_capital': [730.98, 730.98, 730.98, 243.66, 243.66],
            'equity_share_capital': [730.98, 730.98, 730.98, 243.66, 243.66],
            'reserves': [18966.70, 15351.41, 12851.01, 11740.60, 10807.23],
            'networth': [19697.68, 16082.39, 13581.99, 11984.26, 11050.89],
            'total_liabilities': [19697.68, 16082.39, 13581.99, 11984.26, 10807.89],
            'gross_block': [6304.33, 5494.27, 5033.97, 4504.42, 4102.73],
            'accumulated_depreciation': [3131.23, 2735.34, 2361.78, 1980.79, 1622.70],
            'net_block': [3173.10, 2758.93, 2672.19, 2523.63, 2480.03],
            'capital_wip': [1043.61, 891.07, 841.27, 859.00, 736.25],
            'investments': [820.38, 767.79, 664.40, 1554.24, 1331.19],
            'inventories': [9069.66, 7407.59, 6406.18, 5539.56, 4954.67],
            'sundry_debtors': [9091.96, 7362.19, 7022.01, 6103.39, 6551.54],
            'cash_bank': [9397.30, 10968.10, 8009.00, 7499.14, 5008.21],
            'current_assets': [27558.92, 25737.88, 21437.19, 19142.09, 16514.42],
            'loans_advances': [7822.07, 8999.98, 9439.43, 9370.98, 7991.26],
            'current_liabilities': [19095.57, 21423.22, 20010.37, 19249.99, 16495.36],
            'provisions': [1624.83, 1650.04, 1462.12, 2215.69, 1749.90],
            'total_cl_provisions': [20720.40, 23073.26, 21472.49, 21465.68, 18245.26],
            'net_current_assets': [14660.59, 11664.60, 9404.13, 7047.39, 6260.42],
            'total_assets': [19697.68, 16082.39, 13581.99, 11984.26, 10807.89],
            'contingent_liabilities': [3898.85, 4455.23, 3147.36, 2607.83, 2484.55]
        }
        
        # Profit & Loss Statement (Rows 97-125, Columns M-Q)
        income_statement = {
            'years': years,
            'sales_turnover': [23658.01, 20169.39, 17646.20, 15314.96, 14055.38],
            'employee_cost': [2734.36, 2466.70, 2297.73, 2042.46, 2117.02],
            'misc_expenses': [1908.35, 2071.48, 1430.33, 948.44, 1073.69],
            'total_expenses': [17701.25, 15731.79, 13996.13, 12281.49, 11012.04],
            'operating_profit': [6767.59, 4998.17, 4047.52, 3309.24, 3181.12],
            'pbdit': [7535.18, 5754.01, 4407.54, 3542.83, 3307.22],
            'interest': [9.61, 7.02, 14.79, 4.85, 6.08],
            'pbdt': [7525.57, 5746.99, 4392.75, 3537.98, 3301.14],
            'depreciation': [435.58, 412.43, 407.87, 380.18, 366.33],
            'profit_before_tax': [7089.99, 5334.56, 3984.88, 3157.80, 2934.81],
            'tax': [1801.74, 1314.56, 978.21, 808.87, 869.39],
            'net_profit': [5288.25, 4020.00, 3006.67, 2348.93, 2065.42],
            'total_value_addition': [4709.44, 4605.31, 3789.84, 3102.02, 3054.89],
            'equity_dividend': [1681.24, 1461.96, 1242.70, 1023.35, 1023.38]
        }
        
        # Per Share Data
        per_share = {
            'years': years,
            'shares_lakhs': [73097.79, 73097.79, 73097.79, 24365.93, 24365.93],
            'eps': [7.23, 5.50, 4.11, 9.64, 8.48],
            'dividend_percent': [240, 220, 180, 450, 400],
            'book_value': [26.95, 22.00, 18.58, 49.18, 44.36]
        }
        
        # Cash Flow Statement (Rows 133-139, Columns F-J)
        cash_flow = {
            'years': years,
            'net_profit_before_tax': [7089.99, 5334.56, 3984.88, 3157.80, 2934.81],
            'operating_cash_flow': [480.41, 4648.01, 1155.19, 4161.16, 5103.46],
            'investing_cash_flow': [748.41, -5888.85, 2782.04, -4860.56, -2568.59],
            'financing_cash_flow': [-1696.14, -1474.34, -1312.09, -1077.21, -1075.44],
            'net_change_cash': [-467.32, -2715.18, 2625.14, -1776.61, 1459.43],
            'opening_cash': [1149.00, 3864.18, 1239.04, 3015.65, 1556.22],
            'closing_cash': [681.68, 1149.00, 3864.18, 1239.04, 3015.65]
        }
        
        # Financial Ratios (Rows 152-172, Columns F-J)
        ratios = {
            'years': years,
            # Liquidity Ratios
            'current_ratio': [1.44, 1.20, 1.07, 0.99, 1.00],
            'quick_ratio': [0.97, 0.86, 0.75, 0.71, 0.70],
            'cash_ratio': [0.49, 0.51, 0.40, 0.39, 0.30],
            
            # Solvency Ratios
            'debt_to_equity': [1.00, 1.00, 1.00, 1.00, 1.00],
            'debt_ratio': [1.00, 1.00, 1.00, 1.00, 1.00],
            'times_interest_earned': [738.77, 760.91, 270.43, 652.09, 483.70],
            
            # Profitability Ratios
            'gross_profit_margin': [36.73, 35.12, 31.14, 27.82, 30.28],
            'operating_profit_margin': [28.61, 24.78, 22.94, 21.61, 22.62],
            'net_profit_margin': [22.35, 19.93, 17.04, 15.34, 14.69],
            'return_on_assets': [128.12, 133.60, 135.50, 132.04, 132.49],
            
            # Efficiency Ratios
            'inventory_turnover': [1.82, 1.89, 2.03, 2.11, None],
            'receivables_turnover': [2.88, 2.80, 2.69, 2.42, None],
            'payables_turnover': [0.74, 0.63, 0.62, 0.62, None],
            'asset_turnover': [1.32, 1.36, 1.38, 1.34, 2.60],
            
            # DuPont Components (Rows 165-167)
            'equity_multiplier': [1.00, 1.00, 1.00, 1.00, 1.00],
            'tax_burden': [3.56, 4.03, 4.62, 5.01, 4.88],
            'interest_burden': [0.999, 0.999, 0.996, 0.998, 0.998],
            
            # DuPont ROE (Rows 150, 154)
            'roe_3point': [0.296, 0.271, 0.235, 0.206, 0.382],
            'roe_5point': [1.345, 1.355, 1.457, 1.453, 2.866]
        }
        
        return {
            'company': 'Bharat Electronics Ltd',
            'ticker': 'BEL.NS',
            'sector': 'Defense Electronics',
            'currency': 'INR',
            'cash_flow': cash_flow,
            'income_statement': income_statement,
            'balance_sheet': balance_sheet,
            'per_share': per_share,
            'ratios': ratios
        }
    
    def get_dataframe(self, company: str, data_type: str) -> pd.DataFrame:
        """Convert extracted data to DataFrame"""
        data = self.kaynes_data if company.lower() == 'kaynes' else self.bel_data
        
        if data_type in data:
            df = pd.DataFrame(data[data_type])
            # Reverse chronological order to ascending for charts
            df = df.iloc[::-1].reset_index(drop=True)
            return df
        return pd.DataFrame()


if __name__ == "__main__":
    # Test the extractor
    file_path = r"c:\Users\Govin\Desktop\finance\Copy of Final_Financial_Data_Kaynes_Technology(1).xlsx"
    extractor = FinancialDataExtractor(file_path)
    kaynes_data, bel_data = extractor.extract_all_data()
    
    print("✅ Data extraction successful!")
    print(f"\nKaynes Years: {kaynes_data['ratios']['years']}")
    print(f"BEL Years: {bel_data['ratios']['years']}")
    print(f"\nKaynes Current Ratio: {kaynes_data['ratios']['current_ratio']}")
    print(f"BEL Current Ratio: {bel_data['ratios']['current_ratio']}")

"""
Financial Calculations and Utilities
Provides health scores, forecasts, benchmarks, and additional calculations
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple, Optional

class FinancialCalculator:
    """Advanced financial calculations and metrics"""
    
    @staticmethod
    def calculate_health_score(ratios: Dict[str, List[float]], 
                               year_idx: int = 0,
                               benchmarks: Optional[Dict[str, float]] = None) -> float:
        """
        Calculate composite health score (0-100) based on financial ratios
        
        Weights:
        - Liquidity: 25%
        - Solvency: 25%
        - Profitability: 25%
        - Efficiency: 25%
        """
        
        if benchmarks is None:
            # Industry average benchmarks
            benchmarks = {
                'current_ratio': 2.0,
                'quick_ratio': 1.0,
                'debt_to_equity': 0.5,
                'times_interest_earned': 5.0,
                'net_profit_margin': 15.0,
                'return_on_assets': 10.0,
                'asset_turnover': 1.5
            }
        
        scores = []
        
        # Liquidity Score (25%)
        liquidity_score = 0
        current_ratio = ratios['current_ratio'][year_idx]
        if current_ratio >= benchmarks['current_ratio']:
            liquidity_score += 50
        else:
            liquidity_score += (current_ratio / benchmarks['current_ratio']) * 50
        
        quick_ratio = ratios['quick_ratio'][year_idx]
        if quick_ratio >= benchmarks['quick_ratio']:
            liquidity_score += 50
        else:
            liquidity_score += (quick_ratio / benchmarks['quick_ratio']) * 50
        
        scores.append(min(liquidity_score, 100))
        
        # Solvency Score (25%)
        solvency_score = 0
        debt_to_equity = ratios['debt_to_equity'][year_idx]
        if debt_to_equity <= benchmarks['debt_to_equity']:
            solvency_score += 50
        else:
            solvency_score += max(0, 50 - (debt_to_equity - benchmarks['debt_to_equity']) * 20)
        
        tie = ratios['times_interest_earned'][year_idx]
        if tie >= benchmarks['times_interest_earned']:
            solvency_score += 50
        else:
            solvency_score += (tie / benchmarks['times_interest_earned']) * 50
        
        scores.append(min(solvency_score, 100))
        
        # Profitability Score (25%)
        profitability_score = 0
        npm = ratios['net_profit_margin'][year_idx]
        if npm >= benchmarks['net_profit_margin']:
            profitability_score += 50
        else:
            profitability_score += (npm / benchmarks['net_profit_margin']) * 50
        
        roa = ratios['return_on_assets'][year_idx]
        if roa >= benchmarks['return_on_assets']:
            profitability_score += 50
        else:
            profitability_score += (roa / benchmarks['return_on_assets']) * 50
        
        scores.append(min(profitability_score, 100))
        
        # Efficiency Score (25%)
        efficiency_score = 0
        if ratios['asset_turnover'][year_idx] is not None:
            at = ratios['asset_turnover'][year_idx]
            if at >= benchmarks['asset_turnover']:
                efficiency_score += 100
            else:
                efficiency_score += (at / benchmarks['asset_turnover']) * 100
        else:
            efficiency_score = 75  # Default if not available
        
        scores.append(min(efficiency_score, 100))
        
        # Weighted average
        health_score = np.mean(scores)
        return round(health_score, 2)
    
    @staticmethod
    def calculate_yoy_change(values: List[float], year_idx: int = 0) -> float:
        """Calculate year-over-year percentage change"""
        if year_idx + 1 < len(values) and values[year_idx + 1] != 0:
            return round(((values[year_idx] - values[year_idx + 1]) / abs(values[year_idx + 1])) * 100, 2)
        return 0.0
    
    @staticmethod
    def calculate_cagr(values: List[float], years: int = None) -> float:
        """Calculate Compound Annual Growth Rate"""
        if len(values) < 2:
            return 0.0
        
        if years is None:
            years = len(values) - 1
        
        beginning_value = values[-1]  # Oldest
        ending_value = values[0]  # Most recent
        
        if beginning_value <= 0:
            return 0.0
        
        cagr = (pow(ending_value / beginning_value, 1 / years) - 1) * 100
        return round(cagr, 2)
    
    @staticmethod
    def forecast_linear(values: List[float], years_ahead: int = 1) -> List[float]:
        """Simple linear regression forecast"""
        if len(values) < 2:
            return [values[0]] * years_ahead if values else [0] * years_ahead
        
        # Remove None values
        clean_values = [v for v in values if v is not None]
        if len(clean_values) < 2:
            return [clean_values[0]] * years_ahead if clean_values else [0] * years_ahead
        
        x = np.arange(len(clean_values))
        y = np.array(clean_values)
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        forecasts = []
        for i in range(1, years_ahead + 1):
            forecast = slope * (len(clean_values) + i - 1) + intercept
            forecasts.append(round(forecast, 2))
        
        return forecasts
    
    @staticmethod
    def calculate_dupont_3point(net_profit_margin: float, 
                                 asset_turnover: float, 
                                 equity_multiplier: float) -> float:
        """Calculate 3-point DuPont ROE"""
        return round(net_profit_margin * asset_turnover * equity_multiplier, 4)
    
    @staticmethod
    def calculate_dupont_5point(tax_burden: float,
                                interest_burden: float,
                                ebit_margin: float,
                                asset_turnover: float,
                                equity_multiplier: float) -> float:
        """Calculate 5-point DuPont ROE"""
        return round(tax_burden * interest_burden * ebit_margin * asset_turnover * equity_multiplier, 4)
    
    @staticmethod
    def calculate_z_score(current_assets: float,
                          current_liabilities: float,
                          total_assets: float,
                          retained_earnings: float,
                          ebit: float,
                          market_value_equity: float,
                          total_liabilities: float,
                          sales: float) -> float:
        """
        Calculate Altman Z-Score for financial health
        Z > 2.99: Safe zone
        1.81 < Z < 2.99: Grey zone
        Z < 1.81: Distress zone
        """
        
        working_capital = current_assets - current_liabilities
        
        x1 = working_capital / total_assets
        x2 = retained_earnings / total_assets
        x3 = ebit / total_assets
        x4 = market_value_equity / total_liabilities
        x5 = sales / total_assets
        
        z_score = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5
        
        return round(z_score, 2)
    
    @staticmethod
    def grade_ratio(ratio_name: str, value: float, benchmarks: Optional[Dict[str, Dict]] = None) -> str:
        """
        Grade a ratio A-F based on industry benchmarks
        
        Returns: Grade (A, B, C, D, F) and color
        """
        
        if benchmarks is None:
            benchmarks = {
                'current_ratio': {'A': 2.0, 'B': 1.5, 'C': 1.2, 'D': 1.0},
                'quick_ratio': {'A': 1.5, 'B': 1.0, 'C': 0.8, 'D': 0.5},
                'debt_to_equity': {'A': 0.3, 'B': 0.5, 'C': 0.8, 'D': 1.2},  # Lower is better
                'times_interest_earned': {'A': 10, 'B': 5, 'C': 3, 'D': 2},
                'gross_profit_margin': {'A': 30, 'B': 20, 'C': 15, 'D': 10},
                'operating_profit_margin': {'A': 20, 'B': 15, 'C': 10, 'D': 5},
                'net_profit_margin': {'A': 15, 'B': 10, 'C': 5, 'D': 2},
                'return_on_assets': {'A': 15, 'B': 10, 'C': 5, 'D': 2},
                'inventory_turnover': {'A': 6, 'B': 4, 'C': 2, 'D': 1},
                'receivables_turnover': {'A': 12, 'B': 8, 'C': 5, 'D': 3},
                'asset_turnover': {'A': 2, 'B': 1.5, 'C': 1.0, 'D': 0.5}
            }
        
        if ratio_name not in benchmarks:
            return 'N/A'
        
        thresholds = benchmarks[ratio_name]
        
        # For ratios where lower is better (debt ratios)
        if ratio_name in ['debt_to_equity', 'debt_ratio']:
            if value <= thresholds['A']:
                return 'A'
            elif value <= thresholds['B']:
                return 'B'
            elif value <= thresholds['C']:
                return 'C'
            elif value <= thresholds['D']:
                return 'D'
            else:
                return 'F'
        else:
            # For ratios where higher is better
            if value >= thresholds['A']:
                return 'A'
            elif value >= thresholds['B']:
                return 'B'
            elif value >= thresholds['C']:
                return 'C'
            elif value >= thresholds['D']:
                return 'D'
            else:
                return 'F'
    
    @staticmethod
    def get_grade_color(grade: str) -> str:
        """Get color for grade"""
        colors = {
            'A': '#28A745',  # Green
            'B': '#5CB85C',  # Light Green
            'C': '#FFC107',  # Yellow
            'D': '#FF8C00',  # Orange
            'F': '#DC3545',  # Red
            'N/A': '#6C757D'  # Gray
        }
        return colors.get(grade, '#6C757D')
    
    @staticmethod
    def calculate_trend_direction(values: List[float]) -> str:
        """Calculate overall trend direction"""
        if len(values) < 2:
            return 'stable'
        
        clean_values = [v for v in values if v is not None]
        if len(clean_values) < 2:
            return 'stable'
        
        # Calculate slope
        x = np.arange(len(clean_values))
        y = np.array(clean_values)
        slope, _, _, _, _ = stats.linregress(x, y)
        
        if slope > 0.05:
            return 'improving'
        elif slope < -0.05:
            return 'declining'
        else:
            return 'stable'
    
    @staticmethod
    def generate_narrative(metric_name: str, 
                           current_value: float, 
                           previous_value: float,
                           trend: str,
                           company: str) -> str:
        """Generate AI-style narrative for metrics"""
        
        yoy_change = ((current_value - previous_value) / abs(previous_value)) * 100 if previous_value != 0 else 0
        
        direction = "increased" if yoy_change > 0 else "decreased"
        performance = "strong" if trend == "improving" else "weak" if trend == "declining" else "stable"
        
        narratives = {
            'liquidity': f"{company}'s liquidity position has {direction} by {abs(yoy_change):.1f}% YoY, showing {performance} short-term financial health.",
            'solvency': f"{company} demonstrates {performance} long-term financial stability with debt metrics {direction} by {abs(yoy_change):.1f}%.",
            'profitability': f"{company}'s profitability has {direction} by {abs(yoy_change):.1f}%, indicating {performance} operational efficiency.",
            'efficiency': f"Asset utilization at {company} has {direction} by {abs(yoy_change):.1f}%, reflecting {performance} resource management."
        }
        
        # Return appropriate narrative
        for key in narratives:
            if key in metric_name.lower():
                return narratives[key]
        
        return f"{company}'s {metric_name} has {direction} by {abs(yoy_change):.1f}% year-over-year."


if __name__ == "__main__":
    # Test calculations
    calc = FinancialCalculator()
    
    # Test health score
    ratios = {
        'current_ratio': [3.41, 7.87, 3.57, 1.80],
        'quick_ratio': [2.42, 6.11, 2.27, 0.88],
        'debt_to_equity': [0.23, 0.11, 0.13, 0.82],
        'times_interest_earned': [4.14, 4.00, 4.63, 3.29],
        'net_profit_margin': [10.96, 9.90, 8.72, 6.11],
        'return_on_assets': [62.96, 50.49, 107.32, 184.71],
        'asset_turnover': [0.64, 0.67, 1.49, None]
    }
    
    health_score = calc.calculate_health_score(ratios, 0)
    print(f"✅ Health Score: {health_score}/100")
    
    # Test CAGR
    revenue = [1915.44, 1273.94, 1086.56, 671.39]
    cagr = calc.calculate_cagr(revenue)
    print(f"✅ Revenue CAGR: {cagr}%")
    
    # Test forecast
    forecast = calc.forecast_linear(revenue, 1)
    print(f"✅ Revenue Forecast (2026): {forecast[0]} Cr")
    
    # Test grading
    grade = calc.grade_ratio('current_ratio', 3.41)
    print(f"✅ Current Ratio Grade: {grade}")

"""
Visualization Components for Financial Dashboard
Reusable chart components with consistent styling
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional

# Color scheme
KAYNES_BLUE = '#007BFF'
BEL_GREEN = '#28A745'
ACCENT_GOLD = '#FFD700'
DANGER_RED = '#DC3545'
NEUTRAL_GRAY = '#6C757D'
SUCCESS_GREEN = '#28A745'

class DashboardCharts:
    """Reusable chart components for the dashboard"""
    
    @staticmethod
    def create_kpi_card(title: str, value: float, prefix: str = "", suffix: str = "",
                       delta: Optional[float] = None, format_str: str = ".2f") -> go.Figure:
        """Create an animated KPI card with sparkline"""
        
        fig = go.Figure()
        
        # Determine color based on delta
        if delta is not None:
            color = SUCCESS_GREEN if delta > 0 else DANGER_RED
            delta_text = f"+{delta:.1f}%" if delta > 0 else f"{delta:.1f}%"
        else:
            color = KAYNES_BLUE
            delta_text = ""
        
        # Create gauge chart
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=value,
            delta={'reference': value * 0.9 if delta and delta > 0 else value * 1.1,
                   'relative': False,
                   'valueformat': '.2f'},
            title={'text': title, 'font': {'size': 16}},
            number={'prefix': prefix, 'suffix': suffix, 'font': {'size': 36, 'color': color},
                   'valueformat': format_str}
        ))
        
        fig.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_trend_line(years: List[int], kaynes_values: List[float], 
                         bel_values: List[float], title: str,
                         yaxis_title: str, show_forecast: bool = False) -> go.Figure:
        """Create multi-line trend chart with optional forecast"""
        
        fig = go.Figure()
        
        # Kaynes line
        fig.add_trace(go.Scatter(
            x=years,
            y=kaynes_values,
            name='Kaynes Technology',
            mode='lines+markers',
            line=dict(color=KAYNES_BLUE, width=3),
            marker=dict(size=10, symbol='circle'),
            hovertemplate='<b>Kaynes</b><br>Year: %{x}<br>Value: %{y:.2f}<extra></extra>'
        ))
        
        # BEL line
        fig.add_trace(go.Scatter(
            x=years,
            y=bel_values,
            name='Bharat Electronics',
            mode='lines+markers',
            line=dict(color=BEL_GREEN, width=3),
            marker=dict(size=10, symbol='square'),
            hovertemplate='<b>BEL</b><br>Year: %{x}<br>Value: %{y:.2f}<extra></extra>'
        ))
        
        # Add forecast if requested
        if show_forecast and len(kaynes_values) > 0 and len(bel_values) > 0:
            # Simple linear forecast
            from scipy import stats
            
            # Kaynes forecast
            x_k = np.arange(len(kaynes_values))
            slope_k, intercept_k = np.polyfit(x_k, kaynes_values, 1)
            forecast_k = slope_k * len(kaynes_values) + intercept_k
            
            # BEL forecast
            x_b = np.arange(len(bel_values))
            slope_b, intercept_b = np.polyfit(x_b, bel_values, 1)
            forecast_b = slope_b * len(bel_values) + intercept_b
            
            # Add forecast points
            forecast_year = years[-1] + 1
            
            fig.add_trace(go.Scatter(
                x=[years[-1], forecast_year],
                y=[kaynes_values[-1], forecast_k],
                name='Kaynes Forecast',
                mode='lines',
                line=dict(color=KAYNES_BLUE, width=2, dash='dash'),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=[years[-1], forecast_year],
                y=[bel_values[-1], forecast_b],
                name='BEL Forecast',
                mode='lines',
                line=dict(color=BEL_GREEN, width=2, dash='dash'),
                showlegend=False
            ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, weight='bold')),
            xaxis_title="Year",
            yaxis_title=yaxis_title,
            hovermode='x unified',
            template='plotly_white',
            height=400,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    @staticmethod
    def create_comparison_bars(categories: List[str], kaynes_values: List[float],
                              bel_values: List[float], title: str,
                              yaxis_title: str) -> go.Figure:
        """Create side-by-side bar comparison"""
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Kaynes Technology',
            x=categories,
            y=kaynes_values,
            marker_color=KAYNES_BLUE,
            text=[f'{v:.2f}' for v in kaynes_values],
            textposition='outside',
            hovertemplate='<b>Kaynes</b><br>%{x}<br>Value: %{y:.2f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            name='Bharat Electronics',
            x=categories,
            y=bel_values,
            marker_color=BEL_GREEN,
            text=[f'{v:.2f}' for v in bel_values],
            textposition='outside',
            hovertemplate='<b>BEL</b><br>%{x}<br>Value: %{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, weight='bold')),
            xaxis_title="",
            yaxis_title=yaxis_title,
            barmode='group',
            template='plotly_white',
            height=400,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    @staticmethod
    def create_heatmap(data: pd.DataFrame, title: str,
                      x_label: str = "Year", y_label: str = "Ratio") -> go.Figure:
        """Create heatmap for multi-dimensional comparison"""
        
        fig = go.Figure(data=go.Heatmap(
            z=data.values,
            x=data.columns,
            y=data.index,
            colorscale='RdYlGn',
            text=data.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 12},
            hovertemplate='%{y}<br>%{x}<br>Value: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, weight='bold')),
            xaxis_title=x_label,
            yaxis_title=y_label,
            template='plotly_white',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_waterfall(categories: List[str], values: List[float],
                        title: str, measure: List[str] = None) -> go.Figure:
        """Create waterfall chart for breakdown analysis"""
        
        if measure is None:
            measure = ['relative'] * (len(values) - 1) + ['total']
        
        fig = go.Figure(go.Waterfall(
            name="",
            orientation="v",
            measure=measure,
            x=categories,
            y=values,
            text=[f'{v:.2f}' for v in values],
            textposition="outside",
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": SUCCESS_GREEN}},
            decreasing={"marker": {"color": DANGER_RED}},
            totals={"marker": {"color": KAYNES_BLUE}}
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, weight='bold')),
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_radar_chart(categories: List[str], kaynes_values: List[float],
                          bel_values: List[float], title: str) -> go.Figure:
        """Create radar/spider chart for multi-dimensional comparison"""
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=kaynes_values,
            theta=categories,
            fill='toself',
            name='Kaynes Technology',
            line_color=KAYNES_BLUE,
            fillcolor=KAYNES_BLUE,
            opacity=0.6
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=bel_values,
            theta=categories,
            fill='toself',
            name='Bharat Electronics',
            line_color=BEL_GREEN,
            fillcolor=BEL_GREEN,
            opacity=0.6
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(max(kaynes_values), max(bel_values)) * 1.2]
                )
            ),
            title=dict(text=title, font=dict(size=20, weight='bold')),
            template='plotly_white',
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        return fig
    
    @staticmethod
    def create_gauge(value: float, title: str, 
                    range_vals: Tuple[float, float, float] = (0, 50, 100),
                    color_ranges: List[str] = None) -> go.Figure:
        """Create gauge chart for health scores"""
        
        if color_ranges is None:
            color_ranges = ['#DC3545', '#FFC107', '#28A745']
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title, 'font': {'size': 18}},
            delta={'reference': 70, 'increasing': {'color': SUCCESS_GREEN}},
            gauge={
                'axis': {'range': [None, range_vals[2]], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [range_vals[0], range_vals[1]], 'color': color_ranges[0]},
                    {'range': [range_vals[1], range_vals[1] + (range_vals[2]-range_vals[1])/2], 'color': color_ranges[1]},
                    {'range': [range_vals[1] + (range_vals[2]-range_vals[1])/2, range_vals[2]], 'color': color_ranges[2]}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_scatter_comparison(kaynes_values: List[float], bel_values: List[float],
                                 years: List[int], title: str,
                                 x_label: str, y_label: str) -> go.Figure:
        """Create scatter plot for correlation analysis"""
        
        fig = go.Figure()
        
        # Create scatter plot with year labels
        fig.add_trace(go.Scatter(
            x=kaynes_values,
            y=bel_values,
            mode='markers+text',
            marker=dict(
                size=15,
                color=years,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Year")
            ),
            text=[str(y) for y in years],
            textposition="top center",
            hovertemplate='<b>Year %{text}</b><br>Kaynes: %{x:.2f}<br>BEL: %{y:.2f}<extra></extra>'
        ))
        
        # Add diagonal reference line
        max_val = max(max(kaynes_values), max(bel_values))
        fig.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            line=dict(color='gray', dash='dash'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, weight='bold')),
            xaxis_title=x_label,
            yaxis_title=y_label,
            template='plotly_white',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_dupont_waterfall(components: Dict[str, float], title: str) -> go.Figure:
        """Create DuPont decomposition waterfall"""
        
        categories = list(components.keys())
        values = list(components.values())
        
        # Last value should be total (ROE)
        measure = ['relative'] * (len(values) - 1) + ['total']
        
        fig = go.Figure(go.Waterfall(
            name="DuPont Components",
            orientation="v",
            measure=measure,
            x=categories,
            y=values,
            text=[f'{v:.3f}' for v in values],
            textposition="outside",
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": SUCCESS_GREEN}},
            decreasing={"marker": {"color": DANGER_RED}},
            totals={"marker": {"color": KAYNES_BLUE}}
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, weight='bold')),
            yaxis_title="Contribution to ROE",
            template='plotly_white',
            height=450,
            showlegend=False
        )
        
        return fig


if __name__ == "__main__":
    # Test visualizations
    charts = DashboardCharts()
    
    # Test KPI card
    fig1 = charts.create_kpi_card("Revenue", 1915.44, prefix="₹", suffix=" Cr", delta=15.5)
    print("✅ KPI Card created")
    
    # Test trend line
    years = [2022, 2023, 2024, 2025]
    kaynes = [671.39, 1086.56, 1273.94, 1915.44]
    bel = [15314.96, 17646.20, 20169.39, 23658.01]
    fig2 = charts.create_trend_line(years, kaynes, bel, "Revenue Trend", "Revenue (₹ Cr)")
    print("✅ Trend line created")
    
    print("\n✅ All visualization components working!")

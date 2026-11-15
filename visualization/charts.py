"""Small, consistent visualizations built from observed measurements."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

COLORS = {'CPU': '#138f87', 'Memory': '#5d88b5', 'Disk capacity': '#a3aeb7'}


def style_chart(fig, height=270, dark=False):
    fig.update_layout(height=height, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(family='Avenir Next, Segoe UI, sans-serif', color='#b6c2d7' if dark else '#63718b', size=12),
                      margin=dict(l=60, r=16, t=35, b=45), legend_title_text='',
                      legend=dict(orientation='h', y=1.1, x=0))
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor='#344155' if dark else '#e9edf4', zeroline=False)
    return fig


def history_chart(history, dark=False, focus=False):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=.12,
                        subplot_titles=['CPU utilization', 'Memory utilization', 'Disk capacity used'])
    for row, (label, field) in enumerate([('CPU', 'cpu_percent'), ('Memory', 'memory_percent'), ('Disk capacity', 'disk_percent')], 1):
        fig.add_trace(go.Scatter(x=history['recorded_at'], y=history[field], name=label,
                                mode='lines+markers' if len(history) < 3 else 'lines',
                                line=dict(color=COLORS[label], width=2), marker=dict(size=5),
                                connectgaps=False, hovertemplate='%{y:.2f}%<extra>'+label+'</extra>'), row=row, col=1)
        valid = history[field].dropna()
        bounds = [max(0, float(valid.min()) - 3), min(100, float(valid.max()) + 3)] if focus and len(valid) else [0, 100]
        fig.update_yaxes(range=bounds, ticksuffix='%', row=row, col=1)
    style_chart(fig, 650, dark)
    fig.update_layout(showlegend=False, hovermode='x unified',
                      uirevision='resource-history-focus' if focus else 'resource-history-full')
    fig.update_xaxes(title_text='Time (UTC)', row=3, col=1)
    fig.update_annotations(font=dict(size=12, color='#b6c2d7' if dark else '#63718b'), x=0, xanchor='left')
    return fig


def memory_chart(percent, dark=False):
    fig = go.Figure(go.Pie(labels=['Used', 'Available'], values=[percent, max(0, 100 - percent)],
                           hole=.78, sort=False, marker=dict(colors=['#57b8ae', '#344155' if dark else '#e9eef2'], line=dict(width=0)),
                           textinfo='none', hovertemplate='%{label}: %{value:.1f}%<extra></extra>'))
    fig.add_annotation(text=f'<b>{percent:.0f}%</b><br><span style="font-size:11px">in use</span>',
                       x=.5, y=.5, showarrow=False, font=dict(size=22, color='#edf1fa' if dark else '#283650'))
    fig.update_layout(showlegend=False)
    style_chart(fig, 300, dark)
    fig.update_layout(margin=dict(l=12, r=12, t=12, b=12), uirevision='memory-allocation')
    return fig


def top_process_chart(processes, metric, dark=False):
    usable = [p for p in processes if p.get(metric) is not None and p[metric] > 0]
    if not usable:
        return None
    top = sorted(usable, key=lambda p: p[metric], reverse=True)[:7]
    frame = pd.DataFrame([{'Process': f"{p['name'][:22] + '…' if len(p['name']) > 22 else p['name']} · {p['pid']}",
                           'Full name': p['name'], 'PID': p['pid'], 'Usage': p[metric]} for p in reversed(top)])
    fig = px.bar(frame, x='Usage', y='Process', orientation='h', color_discrete_sequence=['#138f87'],
                 labels={'Usage': 'Process CPU (%)', 'Process': ''}, custom_data=['Full name', 'PID'])
    fig.update_traces(hovertemplate='%{customdata[0]}<br>PID %{customdata[1]} · %{x:.2f}% CPU<extra></extra>',
                      texttemplate='%{x:.1f}%', textposition='outside', cliponaxis=False)
    fig.update_yaxes(showgrid=False, automargin=True)
    fig.update_xaxes(ticksuffix='%', gridcolor='#344155' if dark else '#e9edf4', showgrid=True)
    fig.update_xaxes(range=[0, max(frame['Usage'].max() * 1.2, 1)])
    style_chart(fig, 350, dark)
    fig.update_layout(margin=dict(l=190, r=45, t=15, b=45), uirevision='top-processes')
    return fig


def forecast_chart(system, forecast, dark=False):
    frame = pd.DataFrame([{'Resource': label, 'Time': when, 'Usage': value}
                          for label, key in [('CPU', 'cpu_percent'), ('Memory', 'memory_percent')]
                          for when, value in [('Now', system[key]), ('Estimated in 5 min', forecast[key])]])
    fig = px.bar(frame, x='Resource', y='Usage', color='Time', barmode='group',
                 color_discrete_map={'Now': '#a3aeb7', 'Estimated in 5 min': '#138f87'},
                 labels={'Usage': 'Utilization (%)'})
    fig.update_yaxes(range=[0, 100], ticksuffix='%')
    fig.update_traces(hovertemplate='%{y:.1f}%<extra>%{fullData.name}</extra>')
    return style_chart(fig, 270, dark)

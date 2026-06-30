"""
Create diagrams for SPEC.docx
Generates matplotlib diagrams and saves them as PNG files
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# Create output directory for diagrams
DIAGRAM_DIR = os.path.dirname(__file__)

def create_neuralprophet_architecture():
    """Create NeuralProphet architecture overview diagram - NEW diagram showing all components"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    ax.set_title('NEURALPROPHET - KIEN TRUC TONG QUAN', fontsize=18, fontweight='bold', pad=20)

    # Main title
    ax.text(8, 10, 'NeuralProphet = Prophet + AR-Net (Neural Network)',
            ha='center', va='center', fontsize=14, style='italic')

    # INPUT section
    input_box = dict(boxstyle='round,pad=0.5', facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2)
    ax.text(2, 8, 'INPUT', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(2, 6.5, '- y(t-1)...y(t-12)\n- Weather\n- Buffer counts\n- Time features',
            ha='center', va='center', fontsize=12, bbox=input_box)

    # ARROW to components
    ax.annotate('', xy=(5, 8), xytext=(3.5, 8),
               arrowprops=dict(arrowstyle='->', color='navy', lw=2))

    # CENTRAL COMPONENTS
    component_y = 8
    components = [
        ('TREND', '#FFF8E1', '#F57F17'),
        ('SEASONALITY', '#E8F5E9', '#2E7D32'),
        ('AR-NET\n(Autoregressive\nNeural Network)', '#F3E5F5', '#7B1FA2'),
        ('REGRESSORS', '#FFF3E0', '#E65100'),
    ]

    for i, (name, color, edge) in enumerate(components):
        x = 6 + i * 2.5
        box = dict(boxstyle='round,pad=0.3', facecolor=color, edgecolor=edge, linewidth=2)
        ax.text(x, component_y, name, ha='center', va='center', fontsize=11, fontweight='bold', bbox=box)

    # ARROW down from components
    ax.annotate('', xy=(11, 4.5), xytext=(11, 7),
               arrowprops=dict(arrowstyle='->', color='navy', lw=2))

    # QUANTILES OUTPUT
    quantile_box = dict(boxstyle='round,pad=0.5', facecolor='#FCE4EC', edgecolor='#C2185B', linewidth=3)
    ax.text(11, 4.5, 'QUANTILES\n[0.1, 0.5, 0.9]', ha='center', va='center',
            fontsize=13, fontweight='bold', bbox=quantile_box)

    # OUTPUT
    ax.annotate('', xy=(13.5, 4.5), xytext=(12.5, 4.5),
               arrowprops=dict(arrowstyle='->', color='navy', lw=2))
    output_box = dict(boxstyle='round,pad=0.5', facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2)
    ax.text(14.5, 4.5, 'OUTPUT\n6 forecasts\n+ Uncertainty', ha='center', va='center',
            fontsize=12, bbox=output_box)

    # KEY DIFFERENCE BOX
    ax.text(11, 2.5, 'DIEM KHAC BIET CHINH VOI PROPHET:',
            ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(11, 1.2, 'Prophet: y(t) = Trend + Seasonality + Holidays (KHONG co AR-Net)\n'
                    'NeuralProphet: y(t) = Trend + Seasonality + AR-Net + Regressors (CO AR-Net)',
            ha='center', va='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange'))

    # Legend at bottom
    ax.text(8, 0.3, 'AR-Net = Diem khac biet chinh - Nhin vao qua khu de du doan tuong lai',
            ha='center', va='center', fontsize=12, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightblue', edgecolor='navy'))

    plt.tight_layout()
    path = os.path.join(DIAGRAM_DIR, 'diagram_00_neuralprophet_architecture.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {path}")
    return path

def create_system_overview():
    """Create system overview diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('HE THONG AEROCAST - TONG QUAN', fontsize=18, fontweight='bold', pad=20)

    # Define box positions
    boxes = {
        'FlightRadar24\nAPI': (1.5, 6),
        'Open-Meteo\nAPI': (1.5, 3.5),
        'SQLite\nDatabase': (5.5, 4.5),
        'NeuralProphet\nModel': (9, 4.5),
        'Dashboard\nOutput': (12.5, 4.5),
    }

    box_props = dict(boxstyle='round,pad=0.5', facecolor='lightblue', edgecolor='navy', linewidth=2)

    for text, (x, y) in boxes.items():
        ax.text(x, y, text, ha='center', va='center', bbox=box_props, fontsize=12)

    # Arrows
    arrows = [
        ((3, 6), (4.7, 5.2)),
        ((3, 3.5), (4.7, 4.5)),
        ((7, 4.5), (8, 4.5)),
        ((10.5, 4.5), (11.5, 4.5)),
    ]

    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', color='darkblue', lw=2))

    # Labels for arrows
    ax.text(3.9, 6.3, 'Flights', fontsize=11, style='italic')
    ax.text(3.9, 3.2, 'Weather', fontsize=11, style='italic')
    ax.text(7.5, 4.8, 'Data', fontsize=11, style='italic')
    ax.text(11, 4.8, 'Prediction', fontsize=11, style='italic')

    # Legend
    legend_text = 'Data Flow: Radar -> Weather -> Database -> AI Model -> Prediction'
    ax.text(7, 1.5, legend_text, ha='center', fontsize=12, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange'))

    plt.tight_layout()
    path = os.path.join(DIAGRAM_DIR, 'diagram_01_system_overview.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {path}")
    return path

def create_io_diagram():
    """Create Input/Output diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('DAU VAO VA DAU RA CUA MO HINH', fontsize=18, fontweight='bold', pad=20)

    # Input box
    input_box = dict(boxstyle='round,pad=0.5', facecolor='#E8F4FD', edgecolor='#2196F3', linewidth=2)
    ax.text(2.5, 6.5, 'DAU VAO (Input)', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(2.5, 5, '- So may bay 12 timestep\n- Thoi tiet (mua, gio, may)\n- Buffer counts (N, S, E, W)\n- Thoi gian (gio, ngay)', ha='center', va='center', fontsize=12, bbox=input_box)

    # Process box
    process_box = dict(boxstyle='round,pad=0.5', facecolor='#FFF3E0', edgecolor='#FF9800', linewidth=2)
    ax.text(7, 6.5, 'XU LY', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(7, 5, 'NeuralProphet\nAR-Net + Seasonality\n+ Regressors', ha='center', va='center', fontsize=12, bbox=process_box)

    # Output box
    output_box = dict(boxstyle='round,pad=0.5', facecolor='#E8F5E9', edgecolor='#4CAF50', linewidth=2)
    ax.text(11.5, 6.5, 'DAU RA (Output)', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(11.5, 5, '- Du doan 6 buoc (30 phut)\n- Khoang dao dong [y_10, y_90]\n- 80% confidence interval', ha='center', va='center', fontsize=12, bbox=output_box)

    # Arrows
    ax.annotate('', xy=(4.5, 5.8), xytext=(4, 5.8),
               arrowprops=dict(arrowstyle='->', color='navy', lw=3))
    ax.annotate('', xy=(9.5, 5.8), xytext=(8.5, 5.8),
               arrowprops=dict(arrowstyle='->', color='navy', lw=3))

    # Example boxes
    ax.text(7, 2.5, 'VI DU:', ha='center', va='center', fontsize=14, fontweight='bold')

    example_input = '10:00 - 5 may bay\n10:05 - 7 may bay\n10:10 - 6 may bay\nMua: 0.5mm'
    ax.text(4, 1, example_input, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange'))

    ax.text(7, 1, '->', ha='center', va='center', fontsize=24)

    example_output = '10:15 - 6 may bay (4-8)\n10:20 - 7 may bay (5-9)\n10:25 - 5 may bay (3-7)'
    ax.text(10, 1, example_output, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightgreen', edgecolor='green'))

    plt.tight_layout()
    path = os.path.join(DIAGRAM_DIR, 'diagram_02_io.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {path}")
    return path

def create_neural_network_diagram():
    """Create Neural Network architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    ax.set_title('KIEN TRUC NEURAL NETWORK (AR-NET)', fontsize=18, fontweight='bold', pad=20)

    # Layer positions
    layers = {
        'Input\n(12 values)': (2.5, 5, '#E3F2FD', '#1565C0'),
        'Hidden 1\n(32 neurons)': (7, 5, '#FFF8E1', '#F57F17'),
        'Hidden 2\n(32 neurons)': (11.5, 5, '#FFF8E1', '#F57F17'),
        'Output\n(6 forecasts)': (14.5, 5, '#E8F5E9', '#2E7D32'),
    }

    # Draw layers
    for text, (x, y, color, edge_color) in layers.items():
        rect = FancyBboxPatch((x-1.5, y-1.5), 3, 3, boxstyle='round,pad=0.1',
                              facecolor=color, edgecolor=edge_color, linewidth=3)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=13, fontweight='bold')

    # Draw connections (simplified - just show concept)
    # Input to Hidden 1
    for i in range(5):  # Show 5 representative lines
        y_offset = (i - 2) * 0.5
        ax.plot([4, 5.5], [5 + y_offset, 5 + y_offset*0.6],
                color='gray', alpha=0.5, linewidth=1)

    # Hidden 1 to Hidden 2
    for i in range(5):
        y_offset = (i - 2) * 0.5
        ax.plot([8.5, 10], [5 + y_offset*0.6, 5 + y_offset*0.4],
                color='gray', alpha=0.5, linewidth=1)

    # Hidden 2 to Output
    for i in range(5):
        y_offset = (i - 2) * 0.5
        ax.plot([13, 14], [5 + y_offset*0.4, 5],
                color='gray', alpha=0.5, linewidth=1)

    # Labels
    ax.text(4.5, 7.5, 'Weights', ha='center', va='center', fontsize=12, style='italic')
    ax.text(9.5, 7.5, 'Weights', ha='center', va='center', fontsize=12, style='italic')

    # Activation labels
    ax.text(7, 2.5, 'ReLU Activation', ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange'))
    ax.text(11.5, 2.5, 'ReLU Activation', ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange'))

    # Legend
    ax.text(8, 1, 'Neural Network "hoc" bang cach dieu chinh weights de sai so nho nhat',
            ha='center', fontsize=13, style='italic')

    plt.tight_layout()
    path = os.path.join(DIAGRAM_DIR, 'diagram_03_neural_network.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {path}")
    return path

def create_ar_net_detail():
    """Create detailed AR-NET component diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    ax.set_title('AR-NET: AUTOREGRESSIVE NEURAL NETWORK (DIEM KHAC BIET CHINH)', fontsize=18, fontweight='bold', pad=20)

    # Input sequence
    ax.text(1, 8, 'INPUT:', ha='left', va='center', fontsize=14, fontweight='bold')
    for i, label in enumerate(['y_{t-12}', 'y_{t-11}', '...', 'y_{t-1}', 'y_t']):
        x = 2.5 + i * 1.5
        ax.text(x, 7.5, label, ha='center', va='center', fontsize=13,
                bbox=dict(boxstyle='round', facecolor='lightblue', edgecolor='blue', linewidth=2))

    # Arrow down
    ax.annotate('', xy=(9, 5), xytext=(9, 6.5),
               arrowprops=dict(arrowstyle='->', color='navy', lw=3))
    ax.text(9.8, 5.8, 'Neural\nNetwork', ha='left', va='center', fontsize=13)

    # Neural Network box
    nn_box = dict(boxstyle='round,pad=0.5', facecolor='#FFF8E1', edgecolor='#F57F17', linewidth=3)
    ax.text(9, 3.5, 'AR-NET\n[32, 32]', ha='center', va='center', fontsize=16, fontweight='bold', bbox=nn_box)

    # Arrow down
    ax.annotate('', xy=(9, 1.5), xytext=(9, 2.5),
               arrowprops=dict(arrowstyle='->', color='navy', lw=3))

    # Output sequence
    ax.text(1, 3, 'OUTPUT:', ha='left', va='center', fontsize=14, fontweight='bold')
    for i, label in enumerate(['y_{t+1}', 'y_{t+2}', '...', 'y_{t+6}']):
        x = 2.5 + i * 2
        ax.text(x, 1.5, label, ha='center', va='center', fontsize=13,
                bbox=dict(boxstyle='round', facecolor='lightgreen', edgecolor='green', linewidth=2))

    # Comparison box
    ax.text(13.5, 7, 'SO SANH:', ha='center', va='center', fontsize=14, fontweight='bold')
    comparison = 'ARIMA:\ny = a1*y_{t-1} + a2*y_{t-2}\n(chi tuyen tinh)\n\nAR-NET:\ny = f(y_{t-1},...,y_{t-12})\n(ham f = neural network)'
    ax.text(13.5, 3.5, comparison, ha='center', va='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange'))

    plt.tight_layout()
    path = os.path.join(DIAGRAM_DIR, 'diagram_04_ar_net.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {path}")
    return path

def create_quantiles_diagram():
    """Create quantiles/uncertainty diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_title('QUANTILES - DUOCC LUONG SU BAT DINH', fontsize=18, fontweight='bold', pad=20)

    # Time points
    times = ['10:15', '10:20', '10:25', '10:30', '10:35', '10:40']
    x = np.arange(len(times))

    # Predicted values (median)
    median = [6, 7, 5, 4, 5, 6]
    lower = [4, 5, 3, 2, 3, 4]
    upper = [8, 9, 7, 6, 7, 8]

    # Plot
    ax.fill_between(x, lower, upper, alpha=0.3, color='blue', label='80% Interval [y_10, y_90]')
    ax.plot(x, median, 'b-o', linewidth=3, markersize=12, label='Median (y_50)')
    ax.plot(x, lower, 'r--', linewidth=2, label='10th Percentile (y_10)')
    ax.plot(x, upper, 'g--', linewidth=2, label='90th Percentile (y_90)')

    ax.set_xticks(x)
    ax.set_xticklabels(times, fontsize=13)
    ax.set_xlabel('Thoi gian', fontsize=14)
    ax.set_ylabel('So may bay', fontsize=14)
    ax.legend(loc='upper right', fontsize=12)
    ax.grid(True, alpha=0.3)

    # Annotation example
    ax.annotate('80% confident\nactual in [4, 8]', xy=(0, 6), xytext=(2, 7.5),
                fontsize=13, ha='center',
                arrowprops=dict(arrowstyle='->', color='navy', lw=2),
                bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange'))

    plt.tight_layout()
    path = os.path.join(DIAGRAM_DIR, 'diagram_05_quantiles.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {path}")
    return path

def create_pipeline_flow():
    """Create complete pipeline flow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 13)
    ax.axis('off')
    ax.set_title('COMPLETE PIPELINE FLOW', fontsize=18, fontweight='bold', pad=20)

    # Pipeline steps
    steps = [
        ('1. DATA COLLECTION', 'collector2.py', '#E3F2FD', '#1565C0',
         'FlightRadar24 API\nOpen-Meteo API'),
        ('2. SPATIAL FILTERING', 'geopandas', '#E8F5E9', '#2E7D32',
         'Vietnam boundary\nSector A/B filter'),
        ('3. KINEMATIC\nANALYSIS', 'buffer zones', '#FFF3E0', '#E65100',
         'Calculate speed, heading\nCount buffer_n/s/e/w'),
        ('4. DATABASE', 'SQLite', '#F3E5F5', '#7B1FA2',
         'sector_density table'),
        ('5. PREPROCESSING', 'app.py', '#E0F2F1', '#00695C',
         'Resample 5min\nInterpolate\nAdd noise'),
        ('6. FEATURE\nENGINEERING', 'regressors', '#FBE9E7', '#BF360C',
         'Future: weather\nLagged: buffer'),
        ('7. MODEL\nTRAINING', 'NeuralProphet', '#FFF8E1', '#F57F17',
         'n_lags=12, n_forecasts=6\nar_layers=[32,32]'),
        ('8. PREDICTION', 'm.predict()', '#E3F2FD', '#1565C0',
         '6 steps ahead\nQuantiles [0.1, 0.9]'),
        ('9. OUTPUT', 'Dashboard', '#E8F5E9', '#2E7D32',
         'Streamlit display'),
    ]

    for idx, (title, source, bg_color, edge_color, detail) in enumerate(steps):
        row = idx // 3
        col = idx % 3
        x = 2.5 + col * 5
        y = 11 - row * 3.5

        # Box
        rect = FancyBboxPatch((x-1.8, y-1.5), 3.6, 2.8, boxstyle='round,pad=0.1',
                              facecolor=bg_color, edgecolor=edge_color, linewidth=2)
        ax.add_patch(rect)

        # Title
        ax.text(x, y+0.9, title, ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(x, y+0.3, f'({source})', ha='center', va='center', fontsize=10, style='italic')
        ax.text(x, y-0.6, detail, ha='center', va='center', fontsize=10)

    # Arrows between boxes (simplified)
    arrow_positions = [(5.5, 10, 7.5, 10), (10.5, 10, 12.5, 10),
                      (9, 8.5, 9, 7), (4, 8.5, 4, 7),
                      (14, 8.5, 14, 7), (9, 3.5, 9, 2)]

    for x1, y1, x2, y2 in arrow_positions:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color='navy', lw=2))

    plt.tight_layout()
    path = os.path.join(DIAGRAM_DIR, 'diagram_06_pipeline.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {path}")
    return path

def create_model_comparison_table():
    """Create model comparison as an image"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.axis('off')
    ax.set_title('SO SANH CAC PHUONG PHAP DU BAO', fontsize=18, fontweight='bold', pad=20)

    data = [
        ['Tieu chi', 'NeuralProphet', 'ARIMA', 'LSTM', 'Transformer'],
        ['Data can', '~20 diem\n(It)', '~50 diem\n(It)', '~1000 diem\n(Nhieu)', '~5000 diem\n(Rat nhieu)'],
        ['Non-linear', 'Co', 'Khong', 'Co', 'Co'],
        ['Exogenous\nVariables', 'Native', 'Phuc tap', 'Tot', 'Tot'],
        ['Uncertainty', 'Native\n(Quantiles)', 'Khong', 'MC Dropout', 'MC Dropout'],
        ['Interpretability', 'Cao', 'Rat cao', 'Thap', 'Rat thap'],
        ['Phu hop\nDataset nho', 'Rat phu hop', 'Duoc', 'Khong', 'Khong'],
    ]

    table = ax.table(cellText=data, loc='center', cellLoc='center',
                     colWidths=[0.2, 0.2, 0.2, 0.2, 0.2])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.3, 2.5)

    # Color header row
    for j in range(5):
        table[(0, j)].set_facecolor('#1565C0')
        table[(0, j)].set_text_props(color='white', fontweight='bold', fontsize=12)

    # Color NeuralProphet column
    for i in range(1, 7):
        table[(i, 1)].set_facecolor('#E8F5E9')

    plt.tight_layout()
    path = os.path.join(DIAGRAM_DIR, 'diagram_07_comparison.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {path}")
    return path

def create_seasonality_diagram():
    """Create seasonality patterns diagram"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # Daily seasonality
    ax1 = axes[0]
    hours = np.arange(0, 24, 1)
    traffic = 3 + 4*np.sin(2*np.pi*(hours-6)/24) + np.random.randn(24)*0.5
    traffic = np.clip(traffic, 0, 10)

    ax1.fill_between(hours, traffic, alpha=0.3, color='blue')
    ax1.plot(hours, traffic, 'b-o', linewidth=3, markersize=8)
    ax1.set_xlabel('Gio trong ngay', fontsize=14)
    ax1.set_ylabel('So may bay', fontsize=14)
    ax1.set_title('DAILY SEASONALITY\nPattern theo ngay', fontsize=16, fontweight='bold')
    ax1.set_xticks([0, 6, 12, 18, 24])
    ax1.tick_params(labelsize=12)
    ax1.grid(True, alpha=0.3)

    # Weekly seasonality
    ax2 = axes[1]
    days = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
    traffic_week = [8, 6, 6.5, 7, 7.5, 5, 4]
    colors = ['red' if d in ['T2'] else 'blue' for d in days]

    bars = ax2.bar(days, traffic_week, color=colors, alpha=0.7, edgecolor='navy', linewidth=2)
    ax2.set_xlabel('Ngay trong tuan', fontsize=14)
    ax2.set_ylabel('So may bay', fontsize=14)
    ax2.set_title('WEEKLY SEASONALITY\nPattern theo tuan', fontsize=16, fontweight='bold')
    ax2.tick_params(labelsize=12)
    ax2.grid(True, alpha=0.3, axis='y')

    # Legend
    ax2.legend([bars[0]], ['Gio cao diem\n(Thu 2)'], loc='upper right', fontsize=12)

    plt.tight_layout()
    path = os.path.join(DIAGRAM_DIR, 'diagram_08_seasonality.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {path}")
    return path

def create_hyperparams_diagram():
    """Create hyperparameters explanation diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    ax.set_title('GIAI THICH HYPERPARAMETERS', fontsize=18, fontweight='bold', pad=20)

    params = [
        ('n_lags = 12', '12 x 5 phut = 60 phut lookback\nDu capture intra-hour patterns', '#E3F2FD', '#1565C0'),
        ('n_forecasts = 6', '6 x 5 phut = 30 phut horizon\nPhu hop controller planning', '#E8F5E9', '#2E7D32'),
        ('ar_layers\n= [32, 32]', '32 = sweet spot cho data size\n2 layers = du deep khong overfit', '#FFF8E1', '#F57F17'),
        ('quantiles\n= [0.1, 0.9]', '80% confidence interval\nVua du rong, vua actionable', '#F3E5F5', '#7B1FA2'),
    ]

    for idx, (param, explanation, bg_color, edge_color) in enumerate(params):
        row = idx // 2
        col = idx % 2
        x = 3 + col * 7
        y = 7.5 - row * 3

        # Main box
        rect = FancyBboxPatch((x-2, y-1.5), 4, 2.8, boxstyle='round,pad=0.1',
                              facecolor=bg_color, edgecolor=edge_color, linewidth=3)
        ax.add_patch(rect)

        ax.text(x, y+0.6, param, ha='center', va='center', fontsize=15, fontweight='bold')
        ax.text(x, y-0.4, explanation, ha='center', va='center', fontsize=12,
                wrap=True, multialignment='center')

    # Bottom note
    ax.text(8, 1.5, 'Hyperparameters = Cac con so cau hinh model\nChon dung -> Model hoat dong tot',
            ha='center', va='center', fontsize=14, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange'))

    plt.tight_layout()
    path = os.path.join(DIAGRAM_DIR, 'diagram_09_hyperparams.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {path}")
    return path

def main():
    """Generate all diagrams"""
    print("Generating diagrams...")

    paths = []
    paths.append(create_neuralprophet_architecture())  # NEW - First diagram
    paths.append(create_system_overview())
    paths.append(create_io_diagram())
    paths.append(create_neural_network_diagram())
    paths.append(create_ar_net_detail())
    paths.append(create_quantiles_diagram())
    paths.append(create_pipeline_flow())
    paths.append(create_model_comparison_table())
    paths.append(create_seasonality_diagram())
    paths.append(create_hyperparams_diagram())

    print("\nAll diagrams created:")
    for p in paths:
        print(f"  {p}")

    return paths

if __name__ == '__main__':
    main()

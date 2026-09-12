"""
ESI PROJECT: Efficiency Visualization Generator
Creates comprehensive visualizations for efficiency metrics
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path


class EfficiencyVisualizer:
    """Generate efficiency metrics visualizations"""
    
    def __init__(self, metrics_json='model/efficiency_metrics.json'):
        """Load metrics from JSON"""
        with open(metrics_json, 'r') as f:
            self.metrics = json.load(f)
        self.output_dir = Path('model/visualizations')
        self.output_dir.mkdir(exist_ok=True)
        
    # =========================================================================
    # 1. LATENCY BREAKDOWN PIE CHART
    # =========================================================================
    
    def plot_latency_breakdown(self):
        """Pie chart showing latency components"""
        print("📊 Generating Latency Breakdown visualization...")
        
        latency = self.metrics['latency']
        components = [
            ('Preprocessing', latency['preprocessing_ms']),
            ('Hand Detection', latency['hand_detection_ms']),
            ('Inference', latency['inference_ms']),
            ('Other', latency['other_ms'])
        ]
        
        labels = [f"{name}\n({val:.1f}ms)" for name, val in components]
        values = [val for _, val in components]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        
        fig, ax = plt.subplots(figsize=(10, 7))
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels, 
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 11, 'weight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        ax.set_title(
            f'Latency Breakdown\nTotal: {latency["total_latency_ms"]:.2f}ms | {latency["fps"]:.1f} FPS',
            fontsize=14,
            weight='bold',
            pad=20
        )
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'latency_breakdown.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: latency_breakdown.png")
        plt.close()
    
    # =========================================================================
    # 2. OPTIMIZATION COMPARISON BAR CHART
    # =========================================================================
    
    def plot_optimization_comparison(self):
        """Bar chart comparing optimization techniques"""
        print("📊 Generating Optimization Comparison visualization...")
        
        opt = self.metrics['optimization']
        techniques = [
            'Original\n(FP32)',
            'Quantized\n(INT8)',
            'Pruned\n(30%)',
            'Quantized\n+ Pruned'
        ]
        
        sizes = [
            opt['original']['size_mb'],
            opt['quantized_int8']['size_mb'],
            opt['pruned_30percent']['size_mb'],
            opt['quantized_and_pruned']['size_mb']
        ]
        
        inference_times = [
            opt['original']['inference_ms'],
            opt['quantized_int8']['inference_ms'],
            opt['pruned_30percent']['inference_ms'],
            opt['quantized_and_pruned']['inference_ms']
        ]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Model Size Comparison
        colors_size = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#95E1D3']
        bars1 = ax1.bar(techniques, sizes, color=colors_size, edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('Model Size (MB)', fontsize=12, weight='bold')
        ax1.set_title('Model Size Comparison', fontsize=13, weight='bold')
        ax1.set_ylim(0, max(sizes) * 1.2)
        
        for bar, size in zip(bars1, sizes):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{size:.2f}MB',
                    ha='center', va='bottom', fontsize=10, weight='bold')
        
        # Inference Time Comparison
        bars2 = ax2.bar(techniques, inference_times, color=colors_size, edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Inference Time (ms)', fontsize=12, weight='bold')
        ax2.set_title('Inference Time Comparison', fontsize=13, weight='bold')
        ax2.set_ylim(0, max(inference_times) * 1.2)
        
        for bar, time in zip(bars2, inference_times):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{time:.2f}ms',
                    ha='center', va='bottom', fontsize=10, weight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'optimization_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: optimization_comparison.png")
        plt.close()
    
    # =========================================================================
    # 3. INFERENCE TIME STATISTICS
    # =========================================================================
    
    def plot_inference_time_stats(self):
        """Box plot for inference time statistics"""
        print("📊 Generating Inference Time Statistics visualization...")
        
        inf_time = self.metrics['inference_time']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create a simple bar chart for statistics
        stats_labels = ['Min', 'Median', 'Mean', 'Max']
        stats_values = [
            inf_time['min_ms'],
            inf_time['median_ms'],
            inf_time['mean_ms'],
            inf_time['max_ms']
        ]
        
        colors = ['#4ECDC4', '#45B7D1', '#FF6B6B', '#FFA07A']
        bars = ax.bar(stats_labels, stats_values, color=colors, edgecolor='black', linewidth=1.5)
        
        ax.set_ylabel('Time (ms)', fontsize=12, weight='bold')
        ax.set_title(f'Inference Time Statistics (±{inf_time["std_ms"]:.2f}ms std dev)',
                    fontsize=13, weight='bold')
        ax.set_ylim(0, inf_time['max_ms'] * 1.2)
        
        for bar, val in zip(bars, stats_values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.2f}ms',
                   ha='center', va='bottom', fontsize=11, weight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'inference_time_stats.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: inference_time_stats.png")
        plt.close()
    
    # =========================================================================
    # 4. MEMORY USAGE BREAKDOWN
    # =========================================================================
    
    def plot_memory_breakdown(self):
        """Horizontal bar chart for memory usage"""
        print("📊 Generating Memory Usage breakdown visualization...")
        
        mem = self.metrics['memory']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        components = [
            'Model File\nSize',
            'Model Weights\nin Memory',
            'RAM Usage\n(Inference)',
            'Total Process\nMemory'
        ]
        
        values = [
            mem['model_file_size_mb'],
            mem['model_weights_size_mb'],
            mem['ram_usage_inference_mb'],
            mem['total_memory_usage_mb']
        ]
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#95E1D3']
        bars = ax.barh(components, values, color=colors, edgecolor='black', linewidth=1.5)
        
        ax.set_xlabel('Memory (MB)', fontsize=12, weight='bold')
        ax.set_title('Memory & Size Metrics', fontsize=13, weight='bold')
        ax.set_xlim(0, max(values) * 1.2)
        
        for bar, val in zip(bars, values):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f' {val:.2f}MB',
                   ha='left', va='center', fontsize=11, weight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'memory_breakdown.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: memory_breakdown.png")
        plt.close()
    
    # =========================================================================
    # 5. PARAMETER COUNT VISUALIZATION
    # =========================================================================
    
    def plot_parameters_breakdown(self):
        """Pie chart for parameter breakdown"""
        print("📊 Generating Parameter Breakdown visualization...")
        
        params = self.metrics['model_params']
        
        fig, ax = plt.subplots(figsize=(10, 7))
        
        sizes = [
            params['trainable_params'],
            params['non_trainable_params']
        ]
        
        labels = [
            f'Trainable\n{params["trainable_params"]:,}',
            f'Non-trainable\n{params["non_trainable_params"]:,}'
        ]
        
        colors = ['#45B7D1', '#95E1D3']
        
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 11, 'weight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_weight('bold')
        
        ax.set_title(
            f'Model Parameters Breakdown\nTotal: {params["total_params_millions"]:.2f}M parameters',
            fontsize=14,
            weight='bold',
            pad=20
        )
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'parameters_breakdown.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: parameters_breakdown.png")
        plt.close()
    
    # =========================================================================
    # 6. COMPREHENSIVE EFFICIENCY DASHBOARD
    # =========================================================================
    
    def plot_efficiency_dashboard(self):
        """Create a comprehensive dashboard with all key metrics"""
        print("📊 Generating Comprehensive Efficiency Dashboard...")
        
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
        
        # Title
        fig.suptitle(
            'ESI PROJECT: EFFICIENCY METRICS DASHBOARD\nSign Language Recognition System',
            fontsize=18,
            weight='bold',
            y=0.98
        )
        
        # 1. Latency Breakdown (top-left)
        ax1 = fig.add_subplot(gs[0, 0])
        latency = self.metrics['latency']
        lat_vals = [latency['preprocessing_ms'], latency['hand_detection_ms'], 
                   latency['inference_ms'], latency['other_ms']]
        lat_labels = ['Preproc', 'Hand Det', 'Inference', 'Other']
        ax1.pie(lat_vals, labels=lat_labels, autopct='%1.0f%%', colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
        ax1.set_title('Latency Breakdown', weight='bold')
        
        # 2. Inference Time Stats (top-middle)
        ax2 = fig.add_subplot(gs[0, 1])
        inf_time = self.metrics['inference_time']
        inf_labels = ['Min', 'Median', 'Mean', 'Max']
        inf_vals = [inf_time['min_ms'], inf_time['median_ms'], inf_time['mean_ms'], inf_time['max_ms']]
        ax2.bar(inf_labels, inf_vals, color=['#4ECDC4', '#45B7D1', '#FF6B6B', '#FFA07A'])
        ax2.set_ylabel('Time (ms)', fontsize=9, weight='bold')
        ax2.set_title('Inference Time (ms)', weight='bold')
        ax2.tick_params(axis='x', labelsize=8)
        
        # 3. Performance Metrics (top-right)
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.axis('off')
        perf = self.metrics['performance']
        perf_text = f"""
PERFORMANCE METRICS
{'─'*30}
Accuracy: {perf['accuracy_percentage']:.2f}%
Loss: {perf['loss']:.4f}
Status: ✅ Excellent
        """
        ax3.text(0.1, 0.5, perf_text, fontsize=10, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        # 4. Model Parameters (middle-left)
        ax4 = fig.add_subplot(gs[1, 0])
        params = self.metrics['model_params']
        param_labels = ['Trainable', 'Non-trainable']
        param_vals = [params['trainable_params']/1e6, params['non_trainable_params']/1e6]
        ax4.bar(param_labels, param_vals, color=['#45B7D1', '#95E1D3'])
        ax4.set_ylabel('Parameters (Millions)', fontsize=9, weight='bold')
        ax4.set_title('Model Parameters', weight='bold')
        ax4.tick_params(axis='x', labelsize=8)
        
        # 5. Memory Usage (middle-middle)
        ax5 = fig.add_subplot(gs[1, 1])
        mem = self.metrics['memory']
        mem_labels = ['File Size', 'Weights', 'RAM (Inf)', 'Total']
        mem_vals = [mem['model_file_size_mb'], mem['model_weights_size_mb'],
                   mem['ram_usage_inference_mb'], mem['total_memory_usage_mb']]
        ax5.bar(mem_labels, mem_vals, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#95E1D3'])
        ax5.set_ylabel('Memory (MB)', fontsize=9, weight='bold')
        ax5.set_title('Memory Usage', weight='bold')
        ax5.tick_params(axis='x', labelsize=8)
        
        # 6. Key Metrics Summary (middle-right)
        ax6 = fig.add_subplot(gs[1, 2])
        ax6.axis('off')
        key_metrics = f"""
KEY METRICS
{'─'*30}
Total Latency: {latency['total_latency_ms']:.2f}ms
FPS: {latency['fps']:.1f}
Model Size: {mem['model_file_size_mb']:.2f}MB
Parameters: {params['total_params_millions']:.2f}M
Accuracy: {perf['accuracy_percentage']:.2f}%
        """
        ax6.text(0.1, 0.5, key_metrics, fontsize=10, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        
        # 7. Optimization Impact (bottom-spanning)
        ax7 = fig.add_subplot(gs[2, :])
        opt = self.metrics['optimization']
        tech_names = ['Original', 'Quantized', 'Pruned', 'Quant+Prune']
        sizes = [opt['original']['size_mb'], opt['quantized_int8']['size_mb'],
                opt['pruned_30percent']['size_mb'], opt['quantized_and_pruned']['size_mb']]
        inf_times = [opt['original']['inference_ms'], opt['quantized_int8']['inference_ms'],
                    opt['pruned_30percent']['inference_ms'], opt['quantized_and_pruned']['inference_ms']]
        
        x = np.arange(len(tech_names))
        width = 0.35
        
        ax7_twin = ax7.twinx()
        bars1 = ax7.bar(x - width/2, sizes, width, label='Model Size (MB)', color='#FF6B6B', alpha=0.7)
        bars2 = ax7_twin.bar(x + width/2, inf_times, width, label='Inference (ms)', color='#45B7D1', alpha=0.7)
        
        ax7.set_xlabel('Optimization Technique', fontsize=10, weight='bold')
        ax7.set_ylabel('Model Size (MB)', fontsize=10, weight='bold', color='#FF6B6B')
        ax7_twin.set_ylabel('Inference Time (ms)', fontsize=10, weight='bold', color='#45B7D1')
        ax7.set_title('Optimization Techniques Impact', fontsize=11, weight='bold')
        ax7.set_xticks(x)
        ax7.set_xticklabels(tech_names)
        ax7.tick_params(axis='y', labelcolor='#FF6B6B')
        ax7_twin.tick_params(axis='y', labelcolor='#45B7D1')
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax7.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}MB', ha='center', va='bottom', fontsize=8)
        for bar in bars2:
            height = bar.get_height()
            ax7_twin.text(bar.get_x() + bar.get_width()/2., height,
                         f'{height:.2f}ms', ha='center', va='bottom', fontsize=8)
        
        # Legends
        lines1, labels1 = ax7.get_legend_handles_labels()
        lines2, labels2 = ax7_twin.get_legend_handles_labels()
        ax7.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
        
        plt.savefig(self.output_dir / 'efficiency_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: efficiency_dashboard.png")
        plt.close()
    
    # =========================================================================
    # GENERATE ALL VISUALIZATIONS
    # =========================================================================
    
    def generate_all_visualizations(self):
        """Generate all efficiency visualizations"""
        print("\n" + "="*80)
        print("🎨 GENERATING EFFICIENCY VISUALIZATIONS")
        print("="*80 + "\n")
        
        self.plot_latency_breakdown()
        self.plot_optimization_comparison()
        self.plot_inference_time_stats()
        self.plot_memory_breakdown()
        self.plot_parameters_breakdown()
        self.plot_efficiency_dashboard()
        
        print("\n✅ All visualizations generated successfully!")
        print(f"📁 Location: {self.output_dir.absolute()}")


if __name__ == "__main__":
    print("\n🎨 ESI PROJECT: EFFICIENCY VISUALIZATION GENERATOR\n")
    
    visualizer = EfficiencyVisualizer()
    visualizer.generate_all_visualizations()

import os
import glob
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
REPORT_DIR = os.path.join(os.path.dirname(__file__), '..', 'report')
PLOTS_DIR = os.path.join(REPORT_DIR, 'plots')
COLLECTED_DIR = os.path.join(REPORT_DIR, 'collected_results')


def ensure_dirs():
    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(COLLECTED_DIR, exist_ok=True)


def copy_results():
    files = glob.glob(os.path.join(RESULTS_DIR, '*.csv'))
    for f in files:
        shutil.copy(f, COLLECTED_DIR)


def parse_stats_file(path):
    # Try to read the locust stats CSV and extract aggregated metrics
    df = pd.read_csv(path)
    # Normalise column names
    df.columns = [c.strip() for c in df.columns]

    # Prefer a row named 'Aggregated' or where 'Name' contains 'Aggregated'
    agg = None
    if 'Name' in df.columns:
        mask = df['Name'].astype(str).str.contains('Aggregated', na=False)
        if mask.any():
            agg = df[mask].iloc[0]

    # Fallback: compute totals
    if agg is None:
        # Best-effort: sum numeric columns
        total_reqs = 0
        total_fails = 0
        avg = None
        if '# reqs' in df.columns:
            total_reqs = int(df['# reqs'].sum())
        if '# fails' in df.columns:
            total_fails = int(df['# fails'].sum())
        if 'Avg' in df.columns and '# reqs' in df.columns:
            # weighted avg
            try:
                avg = (df['Avg'] * df['# reqs']).sum() / df['# reqs'].sum()
            except Exception:
                avg = None
        return {
            'total_reqs': total_reqs,
            'total_fails': total_fails,
            'avg_ms': float(avg) if avg is not None else None,
            'min_ms': int(df['Min'].min()) if 'Min' in df.columns else None,
            'max_ms': int(df['Max'].max()) if 'Max' in df.columns else None,
            'median_ms': int(df['Med'].median()) if 'Med' in df.columns else None,
            'reqs_per_sec': float(df['req/s'].sum()) if 'req/s' in df.columns else None,
        }

    # Extract fields from aggregated row
    def get_int(col):
        try:
            return int(agg[col])
        except Exception:
            return None

    def get_float(col):
        try:
            return float(agg[col])
        except Exception:
            return None

    return {
        'total_reqs': get_int('# reqs') or 0,
        'total_fails': get_int('# fails') or 0,
        'avg_ms': get_float('Avg'),
        'min_ms': get_int('Min'),
        'max_ms': get_int('Max'),
        'median_ms': get_int('Med'),
        'reqs_per_sec': get_float('req/s'),
    }


def build_summary():
    stats_files = glob.glob(os.path.join(RESULTS_DIR, '*_stats.csv'))
    rows = []
    for f in stats_files:
        base = os.path.basename(f)
        key = base.replace('_stats.csv', '')
        parsed = parse_stats_file(f)
        parsed['scenario'] = key
        rows.append(parsed)
    return pd.DataFrame(rows)


def plot_summary(df):
    sns.set(style='whitegrid', palette='dark')  # Use a darker palette for better contrast
    plt.rcParams.update({'font.size': 12})  # Increase font size globally

    # Average response time
    plt.figure(figsize=(12, 8))  # Larger figure size for better readability
    order = df.sort_values('avg_ms', na_position='last')['scenario']
    sns.barplot(x='avg_ms', y='scenario', data=df, order=order, color='steelblue')  # Use a single contrasting color
    plt.xlabel('Avg response time (ms)', fontsize=14)
    plt.ylabel('Scenario', fontsize=14)
    plt.title('Average response time by scenario', fontsize=16)
    plt.tight_layout()
    out1 = os.path.join(PLOTS_DIR, 'avg_response_time.png')
    plt.savefig(out1)
    print('Saved', out1)
    plt.close()

    # Throughput (req/s)
    plt.figure(figsize=(12, 8))
    sns.barplot(x='reqs_per_sec', y='scenario', data=df.sort_values('reqs_per_sec', na_position='last'), color='seagreen')
    plt.xlabel('Requests per second (req/s)', fontsize=14)
    plt.ylabel('Scenario', fontsize=14)
    plt.title('Throughput by scenario', fontsize=16)
    plt.tight_layout()
    out2 = os.path.join(PLOTS_DIR, 'throughput.png')
    plt.savefig(out2)
    print('Saved', out2)
    plt.close()

    # Failure rate
    df['failure_rate'] = df.apply(lambda r: (r['total_fails'] / r['total_reqs'] * 100) if r['total_reqs'] else 0, axis=1)
    plt.figure(figsize=(12, 8))
    sns.barplot(x='failure_rate', y='scenario', data=df.sort_values('failure_rate', ascending=False), color='indianred')
    plt.xlabel('Failure rate (%)', fontsize=14)
    plt.ylabel('Scenario', fontsize=14)
    plt.title('Failure rate by scenario', fontsize=16)
    plt.tight_layout()
    out3 = os.path.join(PLOTS_DIR, 'failure_rate.png')
    plt.savefig(out3)
    print('Saved', out3)
    plt.close()

    return [out1, out2, out3]


def write_report(df, images):
    md_path = os.path.join(REPORT_DIR, 'REPORT.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('# Relatório de Performance - Link Extractor\n\n')
        f.write('Este relatório foi gerado automaticamente a partir dos resultados de execução do Locust (CSV).\\n')
        f.write('\n## Resumo por cenário\n\n')
        f.write(df.to_markdown(index=False))
        f.write('\n\n## Gráficos\n\n')
        for img in images:
            rel = os.path.relpath(img, os.path.dirname(REPORT_DIR))
            f.write(f'![]({os.path.join("plots", os.path.basename(img))})\n\n')
        f.write('\n## Interpretação rápida\n')
        f.write('\n- Compare tempos médios entre cenários para ver o impacto do cache e da linguagem.\n')
        f.write('- Observe throughput (req/s) para avaliar escalabilidade sob carga.\n')
        f.write('- Taxa de falha indica estabilidade/erro sob carga.\n')


def main():
    print('Creating report...')
    ensure_dirs()
    copy_results()
    summary = build_summary()
    if summary.empty:
        print('No stats files found in', RESULTS_DIR)
        return
    images = plot_summary(summary)
    write_report(summary, images)
    print('Report generated in', REPORT_DIR)


if __name__ == '__main__':
    main()

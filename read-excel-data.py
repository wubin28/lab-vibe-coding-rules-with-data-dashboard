import pandas as pd
import json

def load_data():
    """Load and properly format the Excel data"""
    print("Reading Excel file...")
    df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx')

    # The first row contains the actual column names
    new_columns = df.iloc[0].tolist()
    df.columns = new_columns
    df = df.drop(df.index[0]).reset_index(drop=True)

    print(f"Successfully loaded {len(df)} records")
    print(f"Columns: {list(df.columns)}")

    return df

def analyze_agent_type_multimodal(df):
    """Question 1: Calculate multimodal capability percentage by agent_type"""
    # Convert multimodal_capability to numeric (True=1, False=0)
    df['multimodal_capability_numeric'] = (df['multimodal_capability'] == True).astype(int)

    agent_stats = df.groupby('agent_type').agg({
        'multimodal_capability_numeric': ['count', 'sum']
    })

    agent_stats.columns = ['total_count', 'multimodal_count']
    agent_stats['multimodal_percentage'] = (agent_stats['multimodal_count'] / agent_stats['total_count'] * 100).round(2)

    # Sort by multimodal percentage descending and get top 3
    top3_agents = agent_stats.sort_values('multimodal_percentage', ascending=False).head(3)

    print("\nQuestion 1: Top 3 agent types by multimodal capability percentage:")
    for i, (agent_type, stats) in enumerate(top3_agents.iterrows(), 1):
        print(f"{i}. {agent_type}: {stats['multimodal_percentage']:.1f}% ({stats['multimodal_count']:.0f}/{stats['total_count']:.0f})")

    return top3_agents

def analyze_model_architecture_multimodal(df):
    """Question 2: Calculate multimodal capability percentage by model_architecture"""
    # Convert multimodal_capability to numeric (True=1, False=0)
    df['multimodal_capability_numeric'] = (df['multimodal_capability'] == True).astype(int)

    model_stats = df.groupby('model_architecture').agg({
        'multimodal_capability_numeric': ['count', 'sum']
    })

    model_stats.columns = ['total_count', 'multimodal_count']
    model_stats['multimodal_percentage'] = (model_stats['multimodal_count'] / model_stats['total_count'] * 100).round(2)

    # Sort by multimodal percentage descending and get top 3
    top3_models = model_stats.sort_values('multimodal_percentage', ascending=False).head(3)

    print("\nQuestion 2: Top 3 model architectures by multimodal capability percentage:")
    for i, (model_arch, stats) in enumerate(top3_models.iterrows(), 1):
        print(f"{i}. {model_arch}: {stats['multimodal_percentage']:.1f}% ({stats['multimodal_count']:.0f}/{stats['total_count']:.0f})")

    return top3_models

def analyze_task_category_bias_detection(df):
    """Question 3: Calculate bias_detection median by task_category"""
    # Convert bias_detection_score to numeric
    df['bias_detection_score'] = pd.to_numeric(df['bias_detection_score'], errors='coerce')

    task_bias_stats = df.groupby('task_category')['bias_detection_score'].agg(['median', 'count'])
    task_bias_stats['median'] = task_bias_stats['median'].round(4)

    # Sort by median descending and get top 3
    top3_tasks = task_bias_stats.sort_values('median', ascending=False).head(3)

    print("\nQuestion 3: Top 3 task categories by bias detection median:")
    for i, (task_category, stats) in enumerate(top3_tasks.iterrows(), 1):
        print(f"{i}. {task_category}: {stats['median']:.4f} (n={stats['count']})")

    return top3_tasks

def export_results_to_json(df, top3_agents, top3_models, top3_tasks):
    """Export analysis results to JSON format for HTML embedding"""
    results = {
        'metadata': {
            'total_records': len(df),
            'dataset_name': 'Agentic AI Performance Dataset 2025',
            'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'question1_agent_type_multimodal': [
            {
                'agent_type': agent_type,
                'multimodal_percentage': float(stats['multimodal_percentage']),
                'multimodal_count': int(stats['multimodal_count']),
                'total_count': int(stats['total_count'])
            }
            for agent_type, stats in top3_agents.iterrows()
        ],
        'question2_model_architecture_multimodal': [
            {
                'model_architecture': model_arch,
                'multimodal_percentage': float(stats['multimodal_percentage']),
                'multimodal_count': int(stats['multimodal_count']),
                'total_count': int(stats['total_count'])
            }
            for model_arch, stats in top3_models.iterrows()
        ],
        'question3_task_category_bias_detection': [
            {
                'task_category': task_category,
                'bias_detection_median': float(stats['median']),
                'count': int(stats['count'])
            }
            for task_category, stats in top3_tasks.iterrows()
        ]
    }

    # Save to JSON file
    with open('analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nResults exported to analysis_results.json")
    return results

def main():
    df = load_data()

    # Perform analyses
    top3_agents = analyze_agent_type_multimodal(df)
    top3_models = analyze_model_architecture_multimodal(df)
    top3_tasks = analyze_task_category_bias_detection(df)

    # Export results
    results = export_results_to_json(df, top3_agents, top3_models, top3_tasks)

    return df, results

if __name__ == "__main__":
    main()
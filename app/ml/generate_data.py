"""Synthetic coconut sugar production data generator.

Generates realistic batch data with domain-knowledge-based grade classification:
- Grade A (~40%): optimal ranges
- Grade B (~35%): slightly off optimal
- Reject (~25%): outside acceptable bounds

Key features (temperature, moisture, pH) are designed to be the most discriminative.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_batch_data(n_samples=200, output_path="data/coconut_sugar_batches.csv", seed=42):
    """Generate synthetic coconut sugar production batch data.

    Args:
        n_samples: Number of batch records to generate
        output_path: Path to save CSV file
        seed: Random seed for reproducibility

    Returns:
        pandas DataFrame with all batch records
    """
    np.random.seed(seed)

    # Grade distribution proportions
    n_grade_a = int(n_samples * 0.40)
    n_grade_b = int(n_samples * 0.35)
    n_reject = n_samples - n_grade_a - n_grade_b

    suppliers = ['Central Java', 'East Java', 'West Java', 'Yogyakarta', 'Central Kalimantan']
    visual_a = ['excellent', 'good']
    visual_b = ['good', 'fair']
    visual_reject = ['fair', 'poor']

    # Grade A: optimal ranges (tight, well-defined)
    temp_a = np.random.normal(115, 1.5, n_grade_a).clip(112, 118)
    moisture_a = np.random.normal(2.2, 0.3, n_grade_a).clip(1.5, 3.0)
    ph_a = np.random.normal(6.0, 0.25, n_grade_a).clip(5.6, 6.4)
    color_a = np.random.normal(78, 8, n_grade_a).clip(60, 95)  # More overlap
    cook_a = np.random.normal(90, 6, n_grade_a).clip(78, 102)
    dry_a = np.random.choice([3, 4, 5], n_grade_a, p=[0.2, 0.4, 0.4])  # More spread

    # Grade B: moderately off (wider ranges, some overlap with A and Reject)
    temp_b = np.random.normal(108, 3, n_grade_b).clip(100, 116)
    moisture_b = np.random.normal(3.5, 0.6, n_grade_b).clip(2.5, 4.8)
    ph_b = np.concatenate([
        np.random.normal(5.0, 0.4, n_grade_b // 2).clip(4.4, 5.6),
        np.random.normal(6.8, 0.3, n_grade_b - n_grade_b // 2).clip(6.4, 7.2)
    ])
    color_b = np.random.normal(70, 12, n_grade_b).clip(45, 90)  # High overlap
    cook_b = np.random.normal(88, 10, n_grade_b).clip(68, 112)
    dry_b = np.random.choice([2, 3, 4], n_grade_b, p=[0.3, 0.4, 0.3])

    # Reject: clearly outside bounds
    temp_r = np.concatenate([
        np.random.normal(100, 3, n_reject // 2).clip(92, 106),
        np.random.normal(130, 3, n_reject - n_reject // 2).clip(124, 138)
    ])
    moisture_r = np.random.normal(5.2, 0.7, n_reject).clip(4.2, 7.0)
    ph_r = np.concatenate([
        np.random.normal(3.8, 0.4, n_reject // 2).clip(3.0, 4.4),
        np.random.normal(7.6, 0.4, n_reject - n_reject // 2).clip(7.0, 8.5)
    ])
    color_r = np.random.normal(55, 15, n_reject).clip(20, 80)  # High overlap with B
    cook_r = np.concatenate([
        np.random.normal(58, 8, n_reject // 2).clip(40, 72),
        np.random.normal(122, 8, n_reject - n_reject // 2).clip(108, 140)
    ])
    dry_r = np.random.choice([1, 2, 3], n_reject, p=[0.4, 0.4, 0.2])

    # Visual inspection (weakly correlated — not a strong predictor)
    visual_a_arr = np.random.choice(visual_a, n_grade_a, p=[0.35, 0.65])
    visual_b_arr = np.random.choice(visual_b, n_grade_b, p=[0.55, 0.45])
    visual_r_arr = np.random.choice(visual_reject, n_reject, p=[0.55, 0.45])

    # Combine all grades
    data = {
        'temperature': np.concatenate([temp_a, temp_b, temp_r]),
        'moisture': np.concatenate([moisture_a, moisture_b, moisture_r]),
        'pH': np.concatenate([ph_a, ph_b, ph_r]),
        'color_score': np.concatenate([color_a, color_b, color_r]),
        'cooking_time': np.concatenate([cook_a, cook_b, cook_r]),
        'supplier_origin': np.random.choice(suppliers, n_samples),
        'dryness_level': np.concatenate([dry_a, dry_b, dry_r]),
        'visual_inspection': np.concatenate([visual_a_arr, visual_b_arr, visual_r_arr]),
        'grade': ['Grade A'] * n_grade_a + ['Grade B'] * n_grade_b + ['Reject'] * n_reject,
    }

    df = pd.DataFrame(data)

    # Add batch IDs
    batch_ids = [f'B-2026-{i:03d}' for i in range(1, n_samples + 1)]
    df.insert(0, 'batch_id', batch_ids)

    # Add production dates spread over last 6 months
    base_date = datetime(2026, 5, 22)
    dates = [base_date - timedelta(days=int(d)) for d in np.random.randint(0, 180, n_samples)]
    df.insert(1, 'production_date', [d.strftime('%Y-%m-%d') for d in dates])

    # Shuffle to mix grades
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} batch records → {output_path}")
    print(f"\nGrade distribution:")
    print(df['grade'].value_counts())
    print(f"\nSample rows:")
    print(df.head(3).to_string())

    return df


if __name__ == "__main__":
    generate_batch_data()

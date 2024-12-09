import numpy as np
import matplotlib.pyplot as plt

def fill_with_mode(df, label):
    mode = df[label].mode()[0]
    df[label] = df[label].fillna(mode)
    return df

def get_binary_plot(df, labels, cols=4):
    n_labels = len(labels)
    rows = n_labels // cols + 1
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
    axes = axes.flatten()

    for i, label in enumerate(labels):
        frequencies = df[label].value_counts(normalize=True, dropna=False) * 100
        categories = ['0', '1', 'NaN (Desconocido)']
        values = [frequencies.get(0, 0), frequencies.get(1, 0), frequencies.get(np.nan, 0)]

        ax = axes[i]
        ax.bar(categories, values, color=['red', 'blue', 'gray'])
        ax.set_title(f'Proporción en {label} (%)')
        ax.set_ylabel('Porcentaje (%)')
        ax.set_xlabel('Categorías')
        ax.set_ylim(0, 100)

        for j, v in enumerate(values):
            ax.text(j, v + 1, f"{v:.2f}%", ha='center')

    for j in range(len(labels), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
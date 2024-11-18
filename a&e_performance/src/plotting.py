import seaborn as sns
import matplotlib.pyplot as plt
import textwrap


def total_attendances_graph(df):
    
    '''Plot total attendances and performance against time. Save graph as png'''

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    sns.lineplot(
        data=df,
        x="Period",
        y="Total attendances (millions)",
        ax=ax1,
        color="blue",
        label="Total Attendances",
    )

    sns.lineplot(
        data=df,
        x="Period",
        y="Percentage in 4 hours or less",
        ax=ax2,
        linestyle="--",
        color="red",
        alpha=0.5,
        label="Percentage in 4 hours or less",
    )

    ax1.grid(False)
    ax2.grid(False)

    plt.title("Figure 1: Attendances and performance over time, total")

    plt.tight_layout()
    plt.savefig("plots/total.png")
    plt.show()


def regional_performance_graph(df):
    
    '''Plot performance against time, by region. Save graph as png.'''

    fig, axs = plt.subplots(4, 2, figsize=(30, 30))

    for n, (ax, parent) in enumerate(zip(axs.flat, df["Parent Org"].unique())):
        sns.lineplot(
            data=df[df["Parent Org"] == parent],
            x="Period",
            y="Percentage in 4 hours or less",
            color="blue",
            ax=ax,
            legend=False,
        )
        ax.set_title(parent, fontsize=18)

    plt.suptitle(
        "\n".join(
            textwrap.wrap("Figure 2: Performance over time, by region", width=60)
        ),
        fontsize=38,
    )
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    plt.savefig("plots/regions.png")
    plt.show()


def trusts_performance_graph(df):
    
    '''Plot performance against time, by trust. Save graph as png.'''
    
    fig, axs = plt.subplots(4, 2, figsize=(30, 30))

    for n, (ax, parent) in enumerate(zip(axs.flat, df['Parent Org'].unique())):
        sns.lineplot(data=df[df['Parent Org']==parent], x='Period', y='Percentage in 4 hours or less', 
                     hue='Org name', ax=ax, legend=False)
        ax.set_title(parent, fontsize=18)
        ax.set_ylim(0, 105)
        ax.set_ylabel('Percentage in 4 hours or less', fontsize=18)

    plt.suptitle('Figure 3: A&E performance over time for individual trusts, broken down by trust', fontsize=38)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    plt.savefig('plots/trusts.png')
    plt.show()
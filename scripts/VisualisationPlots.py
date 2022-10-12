import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class VisualiseDf:
    def __init__(self, df):
        self.df = df.copy()

    # plots a distribution (frequency of a variable)
    # better results on continuous variables (not so much on continuous
    # variables)
    # parameters: dataframe, column title, color (of hist)
    # returns: histogram plot (in the color green by default)
    def plot_hist(self, df: pd.DataFrame, column: str,
                  color: str = 'cornflowerblue') -> None:
        sns.displot(data=df, x=column, color=color,
                    kde=True, height=5, aspect=2)
        plt.xticks(rotation=90, fontsize=14)
        plt.yticks(fontsize=14)

    def plot_hist(df: pd.DataFrame, column: str, color: str) -> None:
        sns.displot(data=df, x=column, color=color,
                    kde=True, height=5, aspect=2)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.xticks(rotation=75, fontsize=14)
        plt.show()

    # plots a bar graph
    # parameters: dataframe, dependent col, independent col, xlabel, ylabel
    # returns: plot of bar graph
    def plot_bar(df, x_col: str, y_col: str, title: str, xlabel: str,
                 ylabel: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.barplot(data=df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel(ylabel, fontsize=16)
        plt.show()

    def plot_heatmap(df: pd.DataFrame, title: str, cbar=False) -> None:
        plt.figure(figsize=(12, 7))
        sns.heatmap(df, annot=True, cmap='viridis', vmin=0,
                    vmax=1, fmt='.2f', linewidths=.7, cbar=cbar)
        plt.title(title, size=18, fontweight='bold')
        plt.show()

    # plots a box plot
    # parameters: dataframe, dependent col, title of box plot
    # returns: a box plot
    def plot_box(df: pd.DataFrame, x_col: str, title: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.boxplot(data=df, x=x_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.show()

    def plot_box_multi(df: pd.DataFrame, x_col: str, y_col: str,
                       title: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.boxplot(data=df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()

    def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str, title: str,
                     hue: str, style: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue, style=style)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()

    # plots a distribution (frequency of a variable)
    # better results on discrete variables e.g categorical variables
    # parameters: dataframe, column title
    # returns: histogram count plot
    def plot_count(df: pd.DataFrame, column: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.countplot(data=df, x=column)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()

    # Draw a nested violinplot and split the violins for easier comparison
    def plot_violin(df, x_col: str, y_col: str, hue: str, inner: str):

        sns.violinplot(data=df, x=x_col, y=y_col, hue=x_col,
                       split=True, inner=y_col, linewidth=1,
                       palette={"Yes": "b", "No": ".85"})
        sns.despine(left=True)

    # to make it esly discriptive we can represent it as folows
    # function
    def plot_discriptive_count(df: pd.DataFrame, column: pd.DataFrame) -> None:
        base_color = sns.color_palette()[0]
        type_counts = column.value_counts()
        type_order = type_counts.index
        ax = sns.countplot(
            data=df, x=column.loc[0:], color=base_color, order=type_order)
        n_user = column.value_counts().sum()

        # get the current tick locations and labels
        locs, labels = plt.xticks(rotation=0)

        # loop through each pair of locations and labels
        for loc, label in zip(locs, labels):

            # get the text property for the label to get the correct count
            count = type_counts[label.get_text()]
            pct_string = '{:0.1f}%'.format(100*count/n_user)
            plt.text(loc, count-8, pct_string, va='top',
                     ha='center', color='w', fontsize=12)
        # plt.title(f'Distribution', size=20, fontweight='bold')
    # Remove unnecessary features
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        plt.yticks([])
        # plt.ylabel("t")
        # plt.xlabel('')
        # plt.legend()

        # Show the plot
        plt.show()
    # code for

    def bar_plot(df, column, orders, heu1, title):
        plt.figure(figsize=(10, 6))
        plt.title(title, size=20, fontweight='bold')
        chart = sns.countplot(data=df, x=column, order=orders, hue=heu1)

        chart.set(xlabel=column, ylabel='')

        # Remove legend title
        sns.despine(fig=None, ax=None, top=True, right=True,
                    left=True, bottom=False, offset=None, trim=False)
        plt.gca().legend().set_title(column)
    # pie plot

    def pie_plot(column: pd.DataFrame, title):
        plt.figure(figsize=(10, 6))
        sorted_counts = column.value_counts()
        plt.pie(sorted_counts, labels=sorted_counts.index, startangle=90,
                counterclock=False, autopct='%1.2f%%')
        plt.axis('square')
        # plt.legend('user_type')
        plt.title(title, fontsize=15, fontweight='bold')
        plt.show()

    def plot_layout(df, column, title):
        ax = sns.countplot(x=column, hue=column, dodge=False, data=df)
        ax.set_title(title, fontsize=18, fontweight='bold', color='black')
        ax.set_xlabel('member_gender', fontsize=15, color='black')
        ax.set_ylabel('count', fontsize=15, color='black')
        ax.figure.set_facecolor('0.7')
        plt.tight_layout()
        plt.show()

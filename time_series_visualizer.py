import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

# Register matplotlib converters to handle datetime objects
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df[(df['page_views'] >= df['page_views'].quantile(0.025)) & 
        (df['page_views'] <= df['page_views'].quantile(0.975))]

def draw_line_plot():
    """Draw line plot."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the line chart
    ax.plot(df.index, df['page_views'], color='blue', lw=1)
    
    # Set the title and labels
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    # Save the figure and return
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    """Draw bar plot for average monthly page views."""
    # Resample the data by month and calculate the mean page views
    df_bar = df.resample('M').mean()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    
    # Plot the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    df_bar.groupby(['year', 'month'])['page_views'].mean().unstack().plot(kind='bar', ax=ax)
    
    # Set the title and labels
    ax.set_title("Average Page Views per Month (Grouped by Year)")
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")
    
    # Save the figure and return
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    """Draw box plot for page views distribution by year and month."""
    # Prepare the data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    
    # Create the box plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Year-wise box plot
    sns.boxplot(x='year', y='page_views', data=df_box, ax=ax1)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")
    
    # Month-wise box plot
    sns.boxplot(x='month', y='page_views', data=df_box, ax=ax2)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")
    
    # Save the figure and return
    fig.savefig('box_plot.png')
    return fig


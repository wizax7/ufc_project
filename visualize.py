import os  
import pandas as pd 
import plotly.express as px 

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    db = os.getenv('DB_NAME')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    return engine


def read_sql_file(file_name):
    file_path = os.path.join('sql', file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def save_plot(fig, name):
    fig.write_html(f'plots/{name}.html')


class UFCVisualizer:
    def __init__(self, engine):
        self.engine = engine 
        self.dark_layout = {'template': 'plotly_dark', 'margin': dict(l=150)}


    def plot_top_headliners(self):
        raw_sql = read_sql_file('top_headliners.sql')

        query = text(raw_sql)

        df = pd.read_sql(query, self.engine)

        fig = px.bar(
            df, 
            x='main_event_count', 
            y='headliner', 
            orientation='h', 
            title='Top UFC headliners', 
            template='plotly_dark'
        )
        
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    
        return fig


    def plot_events_by_year(self):
        raw_sql = read_sql_file('events_by_year.sql')

        query = text(raw_sql)

        df = pd.read_sql(query, self.engine)

        fig = px.line(
            df, 
            x='year', 
            y='events_count', 
            title='UFC Events Growth (1994 - 2025)', 
            markers=True, 
            template='plotly_dark'
        )

        return fig


    def plot_most_used_locations(self):
        raw_sql = read_sql_file('most_used_locations.sql')

        query = text(raw_sql)

        df = pd.read_sql(query, self.engine)

        fig = px.bar(
            df,
            x='events_count', 
            y='location', 
            orientation='h',
            title='Most used locations',
            template='plotly_dark', 
            color='events_count', 
            color_continuous_scale='Reds'
        )

        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'}, 
            margin=dict(l=150)
            )
    
        return fig


    def plot_most_used_countries(self):
        raw_sql = read_sql_file('most_used_countries.sql')

        query = text(raw_sql)

        df = pd.read_sql(query, self.engine)

        fig = px.bar(
            df,
            x='events_count', 
            y='country', 
            orientation='h',
            title='Most used countries',
            template='plotly_dark', 
            color='events_count', 
            color_continuous_scale='Reds'
        )

        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'}, 
            margin=dict(l=150)
            )

        return fig


    def plot_most_used_cities(self):
        raw_sql = read_sql_file('most_used_cities.sql')

        query = text(raw_sql)

        df = pd.read_sql(query, self.engine)

        fig = px.bar(
            df, 
            x='events_count', 
            y='city', 
            orientation='h', 
            title='Most used cities', 
            template='plotly_dark', 
            color='events_count', 
            color_continuous_scale='Reds'
        )

        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'}, 
            margin=dict(l=150)
        )

        return fig

    def plot_events_seasonality(self):
        import calendar 

        raw_sql = read_sql_file('events_seasonality.sql')

        query = text(raw_sql)

        df = pd.read_sql(query, self.engine)
        df['month'] = df['month'].apply(lambda x: calendar.month_name[int(x)])

        fig = px.bar(
            df, 
            x='month', 
            y='events_count', 
            orientation='v', 
            title='Events seasonality', 
            template='plotly_dark'
        )

        return fig


    def plot_yoy_event_change(self):
        raw_sql = read_sql_file('yoy_event_change.sql')

        query = text(raw_sql)

        df = pd.read_sql(query, self.engine)
        df['color'] = df['yoy_change_pct'].apply(lambda x: 'growth' if x > 0 else 'decline')

        fig = px.bar(
            df, 
            x='year',
            y='yoy_change_pct', 
            color='color',
            color_discrete_map={'growth': '#2ecc71', 'decline': '#e74c3c'},
            orientation='v',
            title='Year over Year (YoY) change in the number of UFC events',
            template='plotly_dark'
        )

        return fig


    def plot_top_headliners_for_each_year(self, year: int):
        raw_sql = read_sql_file('top_headliners_for_each_year.sql')

        query = text(raw_sql)

        df = pd.read_sql(query, self.engine)

        df = df[df['year'] == year].head(20)

        fig = px.bar(
            df, 
            x='main_event_count', 
            y='headliner', 
            orientation='h', 
            title=f'Top UFC headliners in {year}',
            template='plotly_dark'
        )

        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'}, 
            margin=dict(l=150)
        )
    
        return fig


    def plot_avg_event_intervals(self):
        raw_sql = read_sql_file('event_intervals_per_year.sql')

        query = text(raw_sql)

        df = pd.read_sql(query, self.engine)

        fig = px.line(
            df, 
            x='year', 
            y='avg_days', 
            title='Average days interval between events per year', 
            markers=True, 
            template='plotly_dark'
        )


        return fig

def visualize_main():
    engine = get_engine()
    if not os.path.exists('plots'): os.makedirs('plots')

    ufc_viz = UFCVisualizer(engine)

    save_plot(ufc_viz.plot_top_headliners(), 'top_ufc_headliners')
    save_plot(ufc_viz.plot_events_by_year(), 'events_by_year')
    save_plot(ufc_viz.plot_most_used_locations(), 'most_used_locations')
    save_plot(ufc_viz.plot_most_used_countries(), 'most_used_countries')
    save_plot(ufc_viz.plot_most_used_cities(), 'most_used_cities')
    save_plot(ufc_viz.plot_events_seasonality(), 'events_seasonality')
    save_plot(ufc_viz.plot_yoy_event_change(), 'yoy_event_change')
    save_plot(ufc_viz.plot_top_headliners_for_each_year(year=2022), 'top_headliners_for_each_year')
    save_plot(ufc_viz.plot_avg_event_intervals(), 'event_intervals_per_year')

    print('All plots generated in plots/ folder!')

if __name__ == "__main__":
    visualize_main()
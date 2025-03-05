import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv(r'D:\Coding\DS,DA\SuperMarket\supermarket_sales - Sheet1.csv')

# Convert 'Date' column to datetime for filtering
df['Date'] = pd.to_datetime(df['Date'])

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Supermarket Sales Dashboard", style={'text-align': 'center', 'color': '#2c3e50'}),

    # Filters
    html.Div([
        html.Label("Select City:"),
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': city, 'value': city} for city in df['City'].unique()],
            value=None,  # Default: All cities
            multi=True,
            placeholder="Select one or more cities"
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

    html.Div([
        html.Label("Select Date Range:"),
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=df['Date'].min(),
            max_date_allowed=df['Date'].max(),
            initial_visible_month=df['Date'].min(),
            start_date=df['Date'].min(),
            end_date=df['Date'].max()
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

    # Graphs
    html.Div([
        dcc.Graph(id='sales-by-product'),
        dcc.Graph(id='rating-over-time')
    ], style={'padding': '20px'})
], style={'backgroundColor': '#ecf0f1', 'padding': '20px'})

# Callback to update graphs based on filters
@app.callback(
    [Output('sales-by-product', 'figure'),
     Output('rating-over-time', 'figure')],
    [Input('city-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graphs(selected_cities, start_date, end_date):
    # Filter the dataframe based on inputs
    filtered_df = df.copy()
    
    if selected_cities:
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]
    
    filtered_df = filtered_df[
        (filtered_df['Date'] >= start_date) & 
        (filtered_df['Date'] <= end_date)
    ]

    # Sales by Product Line (Bar Chart)
    sales_by_product = filtered_df.groupby('Product line')['Total'].sum().reset_index()
    fig1 = px.bar(
        sales_by_product,
        x='Product line',
        y='Total',
        title='Total Sales by Product Line',
        color='Product line',
        labels={'Total': 'Total Sales ($)'},
        template='plotly_white'
    )
    fig1.update_layout(showlegend=False)

    # Average Rating Over Time (Line Chart)
    daily_ratings = filtered_df.groupby('Date')['Rating'].mean().reset_index()
    fig2 = px.line(
        daily_ratings,
        x='Date',
        y='Rating',
        title='Average Customer Rating Over Time',
        labels={'Rating': 'Average Rating (1-10)'},
        template='plotly_white'
    )
    fig2.update_traces(mode='lines+markers', line_color='green')

    return fig1, fig2

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
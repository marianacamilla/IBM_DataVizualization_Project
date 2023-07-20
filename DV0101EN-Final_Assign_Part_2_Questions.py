import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
# app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard.", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    html.Div([#TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:", style={'textAlign': 'left', 'color': '#000000', 'fontSize': 16}),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ]),
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': str(i), 'value': i} for i in year_list],
        value='Select a year'
    )),
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
])


@app.callback(
    Output('output-container', 'children'),
    [Input('select-year', 'value'), Input('dropdown-statistics', 'value')]
)
def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        # Calculate the yearly automobile sales for recession periods
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        
        # Calculate the average number of vehicles sold by vehicle type for recession periods
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        
        # Calculate the total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()

        # Plot 1: Automobile sales fluctuate over Recession Period (year-wise)
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec, 
                x='Year', 
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"
            )
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales, 
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type"
            )
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec, 
                names='Vehicle_Type',
                values='Automobile_Sales',
                title="Total Expenditure Share by Vehicle Type during Recessions"
            )
        )

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        R_chart4 = dcc.Graph(
            figure=px.bar(
                recession_data, 
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title="Effect of Unemployment Rate on Vehicle Type and Sales"
            )
        )

        # Returning the graphs for display
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex'})
        ]
    elif selected_statistics == 'Yearly Statistics':
        # Add the logic to handle "Yearly Statistics" here
        # You can follow a similar approach as you did for "Recession Period Statistics"
        # Calculate the yearly automobile sales for all years
        yearly_sales = data.groupby('Year')['Automobile_Sales'].mean().reset_index()

        # Plot 1: Yearly Automobile sales using line chart for the whole period.
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yearly_sales, 
                x='Year', 
                y='Automobile_Sales',
                title="Yearly Automobile Sales using Line Chart"
            )
        )

# Plot 2: Total Monthly Automobile sales using line chart.
# Add your logic and figure creation for this plot
# You can use groupby and reset_index to get the monthly sales data
# Replace '...' with the appropriate column names for x and y axes

monthly_sales = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
Y_chart2 = dcc.Graph(
    figure=px.line(
        monthly_sales,
        x='Month',  # Replace '...' with the appropriate column name for the x-axis
        y='Automobile_Sales',  # Replace '...' with the appropriate column name for the y-axis
        title="Total Monthly Automobile Sales"
    )
)

# Plot 3: Bar chart for average number of vehicles sold during the given year
# Add your logic and figure creation for this plot
# You can use groupby and reset_index to get the average sales data for each vehicle type in the given year
# Replace '...' with the appropriate column names for x and y axes

avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
Y_chart3 = dcc.Graph(
    figure=px.bar(
        avr_vdata,
        x='Vehicle_Type',  # Replace '...' with the appropriate column name for the x-axis
        y='Automobile_Sales',  # Replace '...' with the appropriate column name for the y-axis
        title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
    )
)

# Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
# Add your logic and figure creation for this plot
# You can use groupby and reset_index to get the total advertisement expenditure for each vehicle type
# Replace '...' with the appropriate column names for names and values in the pie chart

exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
Y_chart4 = dcc.Graph(
    figure=px.pie(
        exp_data,
        names='Vehicle_Type',  # Replace '...' with the appropriate column name for the pie slices
        values='Advertising_Expenditure',  # Replace '...' with the appropriate column name for the values of the pie slices
        title="Total Advertisement Expenditure by Vehicle Type"
    )
)

#TASK 2.6: Returning the graphs for display
return [
    html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
    html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex'})
]
 
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
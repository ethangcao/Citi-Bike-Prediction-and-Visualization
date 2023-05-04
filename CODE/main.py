import streamlit as st
import pandas as pd
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px

from streamlit_plotly_events import plotly_events ##HE
import streamlit.components.v1 as components ##HE


fig = go.Figure()

st.set_page_config(layout="wide")

# Cache large dataset for better performance

@st.cache
def load_data(file):
    # Read CSV Data
    df= pd.read_csv(file)
    df['year_month'] = df['date'].str[:7]
    return df

# Load data
heat_df = pd.read_csv('heatmap.csv')
station_df= load_data('data.csv')
lstm_df = pd.read_csv('lstm.csv')
# Chen added for prediction
location_based_df = pd.read_csv('pickup_dropoff_pred.csv')
# Chen added end

# Dashboard Title
st.title("NYC CitiBike Usage, Prediction and Operation")
st.write('Lastest data: Sep 30 2021')


# Define columns
col1, col2, col3 = st.columns([1,1,1])

# column1: map
with col1:
    st.markdown("### " + 'Monthly Usage Heat Map')
    options=heat_df['year_month'].unique()
    
    selected_ym = st.selectbox(label="Please select year & month", options = options)
    
    heat_df_ym =heat_df[ heat_df['year_month'] == selected_ym]
    station_df_ym =station_df[ station_df['year_month'] == selected_ym]
    
    selected_points = [{"curveNumber":100, "pointNumber":0, "pointIndex":0}]

    px.set_mapbox_access_token("pk.eyJ1Ijoia29obnlpIiwiYSI6ImNrdndvY2M5MTN4d2wybm8wdXJ0eGc0OGsifQ.-s45OwLKe2vv2Xf7GMGMLw")
    fig = px.scatter_mapbox(heat_df_ym, lat="latitude", lon="longitude", color="usage", size="usage", size_max=12,
                        color_continuous_scale=px.colors.sequential.matter, zoom=11, height  = 1200, width = 600,
                        hover_name  = 'station',
                        hover_data  = ['usage'],
                        mapbox_style = 'basic')
    fig.data[0].update(hovertemplate= '<b>%{hovertext}</b><br><br>Monthly Usage=%{marker.color}<extra></extra>')
    
    ### HE ###
    selected_points = plotly_events(fig, override_height = 1500, override_width = "60%" )
    #st.write(len(selected_points))
    
    if len(selected_points) == 0:
    #    st.write("did not click")
        selected_points = [{"curveNumber":0, "pointNumber":0, "pointIndex":0}] # deault station if no mouse click event: the first row in each dataframe
    #else: 
     #   st.write(selected_points[0]["pointNumber"])
    ### HE ###
    #st.plotly_chart(fig, use_container_width=True)
    
with col2:

    selected_station = heat_df_ym.iloc[selected_points[0]["pointNumber"],1]
    station_df_ym_st =station_df_ym[ station_df_ym['station'] == selected_station].sort_values(by=['date'])
    station_df_ym_st0 =station_df_ym_st[ station_df_ym_st['half_day'] == 0]
    station_df_ym_st1 =station_df_ym_st[ station_df_ym_st['half_day'] == 1]
    # Chen added for prediction
    location_based_df = location_based_df[location_based_df['station'] == selected_station].sort_values(by=['date'])
    location_based_df0 = location_based_df[location_based_df['half_day'] == 0]
    location_based_df1 = location_based_df[location_based_df['half_day'] == 1]
    #Chen added end
    
    st.markdown("### " + selected_station + ' Monthly Details')	
    
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=station_df_ym_st0.date, y=station_df_ym_st0.pickup,
                    mode='lines+markers',
                    customdata=station_df_ym_st0[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'pickup', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Pick Up'))
    fig.add_trace(go.Scatter(x=station_df_ym_st0.date, y=station_df_ym_st0.dropoff,
                    mode='lines+markers',
                    customdata=station_df_ym_st0[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'dropoff', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Drop Off'))
    # Chen added for prediction
    fig.add_trace(go.Scatter(x=station_df_ym_st0.date, y=location_based_df0.y1_pickup_pred,
                    mode='lines+markers',
                    line=dict(dash='dash'),
                    marker = dict(size = 5,color='#636EFA', symbol = 'square'),
                    #marker_color='#636EFA',
                    customdata=station_df_ym_st0[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'pickup', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Predicted Pick Up'))
    fig.add_trace(go.Scatter(x=station_df_ym_st0.date, y=location_based_df0.y2_dropoff_pred,
                    mode='lines+markers',
                    line=dict(dash='dash'),
                    marker = dict(size = 5,color='#EF553B', symbol = 'square'),
                    #marker_color='#EF553B',
                    customdata=station_df_ym_st0[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'dropoff', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Predicted Drop Off'))
    # Chen added end


    fig.update_layout(
    title="Before 12PM Details",
    xaxis_title="Date",
    yaxis_title="Usage",
    legend_title="Type",
    font=dict(
               size=12,
    )
    )
    st.plotly_chart(fig, use_container_width=True)
    
with col3:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=station_df_ym_st1.date, y=station_df_ym_st1.pickup,
                    mode='lines+markers',
                    customdata=station_df_ym_st1[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'pickup', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Pick Up'))
    fig.add_trace(go.Scatter(x=station_df_ym_st1.date, y=station_df_ym_st1.dropoff,
                    mode='lines+markers',
                    customdata=station_df_ym_st1[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'dropoff', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Drop Off'))
    # Chen added for prediction
    fig.add_trace(go.Scatter(x=station_df_ym_st1.date, y=location_based_df1.y1_pickup_pred,
                    mode='lines+markers',
                    line=dict(dash='dash'),
                    marker = dict(size = 5,color='#636EFA', symbol = 'square'),
                    #marker_color='#636EFA',
                    customdata=station_df_ym_st1[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'pickup', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Predicted Pick Up'))
    fig.add_trace(go.Scatter(x=station_df_ym_st1.date, y=location_based_df1.y2_dropoff_pred,
                    mode='lines+markers',
                    line=dict(dash='dash'),
                    marker = dict(size = 5,color='#EF553B', symbol = 'square'),
                    #marker_color='#EF553B',
                    customdata=station_df_ym_st1[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'dropoff', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Predicted Drop Off'))
    # Chen added end

    fig.update_layout(
    title="After 12PM Details",
    xaxis_title="Date",
    yaxis_title="Usage",
    legend_title="Type",
    font=dict(size=12)
    )

    st.plotly_chart(fig, use_container_width=True)

# Chen added for net borrow
with col2:
    st.markdown("### " + selected_station + ' Bike Flow (Dropoff - Pickup)')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=station_df_ym_st0.date, y=(station_df_ym_st0.dropoff-station_df_ym_st0.pickup),
                    mode='lines+markers',
                    customdata=station_df_ym_st0[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'pickup', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Pick Up'))
    fig.add_trace(go.Scatter(x=station_df_ym_st0.date, y=(location_based_df0.y2_dropoff_pred-location_based_df0.y1_pickup_pred),
                    mode='lines+markers',
                    customdata=station_df_ym_st0[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'dropoff', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Drop Off'))

    fig.update_layout(
    title="Before 12PM Details",
    xaxis_title="Date",
    yaxis_title="Usage",
    legend_title="Type",
    font=dict(size=12)
    )

    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=station_df_ym_st1.date, y=(station_df_ym_st1.dropoff-station_df_ym_st1.pickup),
                    mode='lines+markers',
                    customdata=station_df_ym_st1[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'pickup', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Pick Up'))
    fig.add_trace(go.Scatter(x=station_df_ym_st1.date, y=(location_based_df1.y2_dropoff_pred-location_based_df1.y1_pickup_pred),
                    mode='lines+markers',
                    customdata=station_df_ym_st1[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'dropoff', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Drop Off'))

    fig.update_layout(
    title="After 12PM Details",
    xaxis_title="Date",
    yaxis_title="Usage",
    legend_title="Type",
    font=dict(size=12)
    )

    st.plotly_chart(fig, use_container_width=True)
# Chen added end
    
with col2:
    
    # column3: Prediction
    st.markdown("### " + selected_station + ' LSTM Predictions Based on Latest Data')

    station_df_ym = station_df[ station_df['year_month'] == heat_df['year_month'].unique()[-1]]
    station_df_ym_st =station_df_ym[ station_df_ym['station'] == selected_station]
    station_df_ym_st0 =station_df_ym_st[ station_df_ym_st['half_day'] == 0]
    station_df_ym_st1 =station_df_ym_st[ station_df_ym_st['half_day'] == 1]


    station_df_ym_st0p =station_df_ym_st0.tail(7)
    station_df_ym_st1p =station_df_ym_st1.tail(7)

    lstm_df =lstm_df[lstm_df['station'] == selected_station]
    
    lstm_df0 =lstm_df[ lstm_df['half_day'] == 0]
    lstm_df1 =lstm_df[ lstm_df['half_day'] == 1]

    
    def add_lastest_day(prediction_df, actual_df):
        last = actual_df.tail(1)
        t = prediction_df['type'].to_list()[0]
        prediction_df.loc[max(prediction_df.index)+1] = ["", 0, "", last[t].values[0], last['date'].values[0]]
        return prediction_df
    
    lstm_df0_pickup = lstm_df0[ lstm_df0['type'] == 'pickup']
    lstm_df0_pickup = add_lastest_day(lstm_df0_pickup, station_df_ym_st0p)
    
    lstm_df0_dropoff = lstm_df0[ lstm_df0['type'] == 'dropoff']
    lstm_df0_dropoff = add_lastest_day(lstm_df0_dropoff, station_df_ym_st0p)
   
    lstm_shape0 = 'square'
    if lstm_df0_pickup.value.values[0] == lstm_df0_dropoff.value.values[0]:
        lstm_shape0 = 'diamond'
    
    lstm_df1_pickup = lstm_df1[ lstm_df1['type'] == 'pickup']
    lstm_df1_pickup = add_lastest_day(lstm_df1_pickup, station_df_ym_st1p)
    
    lstm_df1_dropoff = lstm_df1[ lstm_df1['type'] == 'dropoff']
    lstm_df1_dropoff = add_lastest_day(lstm_df1_dropoff, station_df_ym_st1p)
   
    lstm_shape1 = 'square'
    if lstm_df1_pickup.value.values[0] == lstm_df1_dropoff.value.values[0]:
        lstm_shape1 = 'diamond'
    
#TODO: add prediction
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=station_df_ym_st0p.date, y=station_df_ym_st0p.pickup,
                    line_shape='spline',
                    marker=dict(size=16),
                    customdata=station_df_ym_st0p[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'pickup', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Lastest Pick Up'))
    fig.add_trace(go.Scatter(x=station_df_ym_st0p.date, y=station_df_ym_st0p.dropoff,
                    line_shape='spline',
                    marker=dict(size=16),
                    customdata=station_df_ym_st0p[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'dropoff', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Lastest Drop Off'))

    fig.add_trace(go.Scatter( x=lstm_df0_pickup.date, y=lstm_df0_pickup.value,
                             line=dict(dash='dash'),
                             marker_symbol=["square", "circle"],
                             marker_color = '#636EFA',marker_size = 16,
                             customdata=lstm_df0_pickup[['value', 'date']],
                             hovertemplate='<b>Date:%{customdata[1]}</b><br><b>Prediction:%{customdata[0]}</b>',
                             name='LSTM Pick Up Prediction'))
    fig.add_trace(go.Scatter(x=lstm_df0_dropoff.date, y=lstm_df0_dropoff.value,
                             line=dict(dash='dash'),
                             marker_symbol=[lstm_shape0, "circle"],
                             marker_color = '#EF553B',marker_size = 16,
                             customdata=lstm_df0_dropoff[['value', 'date']],
                             hovertemplate='<b>Date:%{customdata[1]}</b><br><b>Prediction:%{customdata[0]}</b>',
                             name='LSTM Drop Off Prediction'))



    fig.update_layout(
    title="Before 12PM Details",
    xaxis_title="Date",
    yaxis_title="Usage",
    legend_title="Type",
    font=dict(
               size=12,
    )
    )


    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    fig = go.Figure()    
    fig.add_trace(go.Scatter(x=station_df_ym_st1p.date, y=station_df_ym_st1p.pickup,
                    line_shape='spline',
                    marker=dict(size=16),
                    customdata=station_df_ym_st0p[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'pickup', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Latest Pick Up'))
    fig.add_trace(go.Scatter(x=station_df_ym_st1p.date, y=station_df_ym_st1p.dropoff,
                    line_shape='spline',
                    marker=dict(size=16),
                    customdata=station_df_ym_st1p[['AVG_TEMP', 'CASE_COUNT', 'DEATH_COUNT', 'dropoff', 'date']],
                    hovertemplate='<b>Date:%{customdata[4]}</b><br><b>Usage:%{customdata[3]}</b><br>Avg Temp:%{customdata[0]}<br>COVID Cases:%{customdata[1]} <br>COVID Deaths: %{customdata[2]} ',
                    name='Latest Drop Off'))
    
    fig.add_trace(go.Scatter(x=lstm_df1_pickup.date, y=lstm_df1_pickup.value,
                             line=dict(dash='dash'),
                             marker_symbol=["square", "circle"],
                             marker_color = '#636EFA',marker_size = 16,
                             customdata=lstm_df1_pickup[['value', 'date']],
                             hovertemplate='<b>Date:%{customdata[1]}</b><br><b>Prediction:%{customdata[0]}</b>',
                             name='LSTM Pick Up Prediction'))
    fig.add_trace(go.Scatter(x=lstm_df1_dropoff.date, y=lstm_df1_dropoff.value,
                             line=dict(dash='dash'),
                             marker_symbol=[lstm_shape1, "circle"],
                             marker_color = '#EF553B',marker_size = 16,
                             customdata=lstm_df1_dropoff[['value', 'date']],
                             hovertemplate='<b>Date:%{customdata[1]}</b><br><b>Prediction:%{customdata[0]}</b>',
                             name='LSTM Drop Off Prediction'))
  
    
    fig.update_layout(
        title="After 12PM Details",
        xaxis_title="Date",
        yaxis_title="Usage",
        legend_title="Type",
        font=dict(
               size=12,
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    

rebalancing_df0 = pd.read_csv('rebalancing0.csv')
rebalancing_df1 = pd.read_csv('rebalancing1.csv')
with col2:
    st.markdown("### " + selected_station + ' Rebalancing Strategy')
    st.write("Before 12 PM")
    if selected_station in rebalancing_df0['from'].to_list():
        print_df = rebalancing_df0[rebalancing_df0['from']==selected_station]
        for i,r in print_df.iterrows():
            st.write("Move {} bike(s) from {} to {}".format(r['quantity'], selected_station, r['to']))
    elif selected_station in rebalancing_df0['to'].to_list():
        print_df = rebalancing_df0[rebalancing_df0['to']==selected_station]
        for i,r in print_df.iterrows():
            st.write("Take {} bike(s) from {} to {}".format(r['quantity'], r['from'], selected_station))
    else:
        st.write('No need for rebalancing')
    
with col3:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write("After 12 PM")
    if selected_station in rebalancing_df1['from'].to_list():
        print_df = rebalancing_df1[rebalancing_df1['from']==selected_station]
        for i,r in print_df.iterrows():
            st.write("Move {} bike(s) from {} to {}".format(r['quantity'], selected_station, r['to']))
    elif selected_station in rebalancing_df1['to'].to_list():
        print_df = rebalancing_df1[rebalancing_df1['to']==selected_station]
        for i,r in print_df.iterrows():
            st.write("Take {} bike(s) from {} to {}".format(r['quantity'], r['from'], selected_station))
    else:
        st.write('No need for rebalancing')
    
    
    
    
    




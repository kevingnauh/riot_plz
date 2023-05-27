import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import lol_details as ld

st.set_page_config(layout="wide")

now = datetime.now()
st.success('Last Refreshed: ' + str(now))

# create a sidebar with a simple title and description.
st.sidebar.title("Selections")
name = st.sidebar.text_input("Enter Summoner Name", "")

# Main page layout
st.title('Recent 20 Games Summary')

column1, column2, column3, column4 = st.columns(4)

st.markdown("---")

col1, col2 = st.columns(2, gap="large")

st.markdown("---")

# display the name when the submit button is clicked
if(st.sidebar.button('Submit')):
    
    df = ld.recent_matches(name)
    elo = ld.summoner_detail(name)

    win_rate = df.win.sum()/len(df.win)
    kda = sum(df.kills)/sum(df.deaths)
    cs_avg = df.totalMinionsKilled.mean()

    with col1:
        champ_counts = df['champ_name'].value_counts().sort_values(ascending=True)
 
        # Create a horizontal bar chart
        data = [go.Bar(
                    x=champ_counts.values,
                    y=champ_counts.index,
                    orientation='h',
                    text=champ_counts.values,
                    textposition='auto'
            )]
        # Set chart title and labels
        layout = go.Layout(
            title='Recent 20 Games Played Champions',
            xaxis=dict(title='Count'),
            yaxis=dict(title='Champ Name')
        )

        # Create the chart
        fig = go.Figure(data=data, layout=layout)

        st.plotly_chart(fig, use_container_width=True)
    
    with col2:

        st.dataframe(df)

    with column1:
        st.subheader("Rank:")
        st.subheader(elo)

    with column2:
        st.subheader("Win Rate:")
        st.subheader("{:.2%}".format(win_rate))

    with column3:
        st.subheader("KDA:")
        st.subheader("{:.3f}".format(kda))

    with column4:
        st.subheader("Average CS:")
        st.subheader("{:.3f}".format(cs_avg))

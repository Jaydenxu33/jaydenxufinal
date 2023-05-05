'''
Jayden Xu
CS230 section 3
Program discription:
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import pydeck as pdk




def makegraph(df,type="bar"):
    if type=='bar':
        fig, ax = plt.subplots()
        ax.bar(df["name"], top_10["mass (g)"])
        ax.set_xlabel("Meteorite Name")
        ax.set_ylabel("Mass (g)")
        ax.set_title(f"Top 10 Meteorites by Mass in {year}")
        ax.tick_params(axis="x", rotation=90)
        return fig
    elif type=='scatter':
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df["reclong"], top_10["reclat"], s=top_10["mass (g)"] / 100, alpha=0.5)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title(f"Top 10 Meteorites by Mass in {year}")
        return fig

# Load the meteorites data
df = pd.read_csv("Meteorite_Landings.csv")
df = df.dropna(subset = ['year','mass (g)','reclat','reclong'])

#Header
st.header("Welcome to Jayden Xu's Final project")

image = Image.open("meteroite.jpeg")
st.image(image, caption="Meteorite")

# Ask the user for the year they are interested in
years = [int(ele) for ele in list(df['year'].unique())]
years.sort()
year = st.selectbox(label="year selection:",options=years)


# Filter the data to only include meteorites from the given year
year_df = df[df["year"] == int(year)]

# Find the heaviest and lightest meteorites
if not year_df.empty:
    heaviest = year_df.loc[year_df["mass (g)"].idxmax()]
    lightest = year_df.loc[year_df["mass (g)"].idxmin()]

    # Display the results
    st.write(f"The heaviest meteorite in {year} was {heaviest['name']} with a mass of {heaviest['mass (g)']} g.")
    st.write(f"The lightest meteorite in {year} was {lightest['name']} with a mass of {lightest['mass (g)']} g.")

    # Find the top 10 meteorites by mass
    top_10 = year_df.nlargest(10, "mass (g)")


    # Display the top 10 meteorites in a table
    st.write(f"The top 10 meteorites by mass in {year} were:")
    st.write(top_10[["name", "mass (g)"]])

    # a bar chart of the top 10 meteorites by mass
    bar_fig=makegraph(top_10)
    # Display the chart
    st.pyplot(bar_fig)
    #  a scatter plot of the top 10 meteorites by mass

    scatter_fig=makegraph(top_10,'scatter')
    
    st.pyplot(scatter_fig)

    # Create a PyDeck scatterplot on maps of the meteorite landings
    Mete_Name = top_10['name']
    Mete_lat = top_10['reclat']
    Mete_long = top_10['reclong']

    map_df = pd.DataFrame([Mete_Name, Mete_lat, Mete_long]).T
    map_df.columns = ['Name', 'Lat', 'Long']

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position="[Long, Lat]",
        get_radius= 50000,
        get_color=[255, 128, 0],
        pickable=True
    )
    tool_tip = {"html": "Meteorite Name:<br> <b>{Name}</b> <br> Latitude: <br> <b>{Lat}</b> <br> Longtitue: <br> <b>{Long}</b> ",
                "style": {"backgroundColor" : "steelblue","color":"white"}}


    view_state = pdk.ViewState(latitude=float(map_df.iloc[0]['Lat']), longitude=float(map_df.iloc[0]['Long']), zoom=1)
    map = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip= tool_tip)

    # Display the chart
    st.pydeck_chart(map)

    st.write(map_df)

    table=pd.pivot_table(df, values=['mass (g)'], index=['recclass'])
    st.header('The relationship between \'recclass\'and\'mass(g)\',')
    st.write(table)





import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from flask import Flask
import dash_bootstrap_components as dbc

#Initiate the app
server = Flask(__name__)
app = dash.Dash(__name__, server= server, external_stylesheets= [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

#Load the dataset
<<<<<<< HEAD
df = pd.read_csv("C:/Users/hslia/OneDrive/Desktop/LingvoViz/Data/final_dataset.csv")

#Create the components
header_component = html.H1("LingvoViz - Languages of the World Dashboard", className="text-center text-primary, mb-4") #header
dash_description = html.H3('''
                      This dashboard shows language diversity of the world. 
                      \n You can find plenty of information about language vitality, approximate numbers of speakers and language families.
=======
df = pd.read_csv(r".\Data\final_dataset.csv")

#Create the components
header_component = html.H1("LingvoViz - Languages of the World Dashboard", className="text-center text-primary, mb-4") #header
dash_description = html.H2('''
                      This dashboard shows language diversity of the world. 
                      \n You can find plenty of information about language vitality, numbers of speakers and language families.
>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
                      \n It is meant to give quick access to information about all languages of the world in one place!'''
                      , style=({"text-align": "left"}), className="text-secondary") #dashboard descriptor

#Create the infobox
#Calculate the basic information about the languages for an infobox 
lang_status_value = df["Status"].value_counts()
lang_status_df = lang_status_value.reset_index()
lang_status_df.columns = ["Status", "Count of languages"]
#print(lang_status_df.head())

#Total number of languages in the world
total_count_lang = sum(lang_status_df["Count of languages"])

#Safe languages and the number of speakers
safe_languages = df[df["Status"]=="Safe"]
safe_lang_count = safe_languages["Name_x"].nunique()
<<<<<<< HEAD
#safe_lang_speakers = safe_languages["Speakers"].sum()
#print(f"The count of speakers of safe languages is {safe_lang_speakers}")

=======
safe_lang_speakers = safe_languages["Speakers"].sum()
#print(f"The count of speakers of safe languages is {safe_lang_speakers}")


>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
#Endangered languages and the number of speakers
endang_langs = df[df["Status"]!= "Safe"]
endang_lang_speakers = endang_langs["Speakers"].sum()
endang_lang_count = endang_langs["Name_x"].nunique()
#print(f"The count of speakers of endangered languages is {endang_lang_speakers}")

#Lost languages
lost_languages = df[df["Status"]=="Not in use"]
lost_lang_count = lost_languages["Name_x"].nunique()
#print(f"the number of lost languages is {lost_lang_count}")

#Function to transform long numbers into a readable format
def transform_number(number):
    if number >= 1000000000:
        return f"{number/1000000000:.1f}B"
    elif number >= 1000000:
        return f"{number/1000000:.1f}M"
    else:
        return number
    
#Infobox script
infobox_component = dbc.Card([
    dbc.CardHeader("Overview"),
    dbc.CardBody([
        html.P(["There are ", 
               html.Span(f"{transform_number(total_count_lang)}", style={"fontSize": "20px", "fontWeight": "bold", "color": "#1f77b4"}),  " languages in the world."]),
        html.P(["There are only ", 
                html.Span(f"{transform_number(safe_lang_count)}", style={"fontSize": "20px", "fontWeight": "bold", "color": "#1f77b4"}),
<<<<<<< HEAD
                 " languages whose vitality is considered safe."]),
        html.P(["A staggering number of ",
               html.Span(f"{transform_number(endang_lang_count)}", style={"fontSize": "20px", "fontWeight": "bold", "color": "#1f77b4"}), 
                " languages are vulnerable or in danger of disappearance."]),
=======
                 " languages whose vitality is considered safe and they are spoken by ",
                  html.Span(f"{transform_number(safe_lang_speakers)}", style={"fontSize": "20px", "fontWeight": "bold", "color": "#1f77b4"}), " people."]),
        html.P(["A staggering number of ",
               html.Span(f"{transform_number(endang_lang_count)}", style={"fontSize": "20px", "fontWeight": "bold", "color": "#1f77b4"}), 
                " languages are vulnerable or in danger of disappearance and count only ",
                 html.Span(f"{transform_number(endang_lang_speakers)}", style={"fontSize": "20px", "fontWeight": "bold", "color": "#1f77b4"}),
                  " speakers."]),
>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
        html.P([html.Span(f"{transform_number(lost_lang_count)}", style={"fontSize": "20px", "fontWeight": "bold", "color": "#1f77b4"}), " languages have now been lost."])
    ])
], style={"marginBottom": "10px", "padding": "10px", "textSize": 14})

<<<<<<< HEAD
#Search bar

=======
>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
#Plots
#Plot 1. Languages by vitality status
#Value counts for each status in the Status column
status_value_counts = df["Status"].value_counts()
#print(status_value_counts)
status_df= status_value_counts.reset_index()
status_df.columns = ["Status", "Count"]
# print(status_df.head())

#Status descriptions - to inform readers what each status descriptor means
status_description = {
<<<<<<< HEAD

    "Safe": "Is spoken by all generations and intergenerational transmission is uninterrupted as a consequence of high status and high presence. ", 

    "Potentially vulnerable": "The language has between 3.5 million to 7 million speakers. Most children speak the language, but it may be restricted to certain domains (e.g. home).",

    "Endangered/unsafe": "The language has from small numbers to 7.5 million speakers.",

    "Definitely endangered": "The language has between 100,000 and 3.5 million speakers. Children no longer learn the language as a mother tongue in the home.", 
           
    "Severely endangered": " The language has between 10.000 to 100.000 speakers left. The language is spoken by grandparents and older generations. While the parent generation may understand it, they do not speak it to children or among themselves.",
    
    "Critically endangered": "The language is spoken by under 25.000 speakers. The youngest speakers are grandparents and older, and they speak the language partially and infrequently.",
    
    "Not in use": "There are no speakers left. The language has presumably gone out of use after 1950."
}

for key in status_description:
    status_description[key] = status_description[key].replace(". ", ".<br>")

#mapping status descriptors on the figure legend
status_df["Description"] = status_df["Status"].map(status_description)

#Plotting the bar chart
=======
    "Endangered/unsafe" : "",
    "Definitely endangered": "Children no longer learn the language as a mother tongue in the home.", 
    "Not in use": "There are no speakers left.",
    "Potentially vulnerable": "Most children speak the language, but it may be restricted to certain domains (e.g. home).",
    "Severely endangered": "The language is spoken by grandparents and older generations. While the parent generation may understand it, they do not speak it to children or among themselves.",
    "Critically endangered": "The youngest speakers are grandparents and older, and they speak the language partially and infrequently.",
    "Safe": "Is spoken by all generations and intergenerational transmission is uninterrupted. "
}
#mapping status descriptors on the figure legend
status_df["Description"] = status_df["Status"].map(status_description)

#Plotting the pie chart
>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
fig1= px.bar(status_df,
             x= "Status",
             y="Count",
             title="Languages by vitality",
             hover_data={"Description": True,
                         "Status": False,
                         "Count": False},
             text= "Count",
             color="Status"
             )
<<<<<<< HEAD
fig1.update_traces(hoverlabel=dict(font_size=12))
fig1.update_layout(showlegend=False)

# # Plot 2. Bubble chart to compare the size of language families by number of languages and speakers (TAKEN OUT OF THE DASHBOARD AS NUMBERS OF SPEAKERS ARE ONLY ESTIMATES)
# #Counting number of languages by family
# lang_fam_size = df["Top-level family"].value_counts()
# fam_size_df = lang_fam_size.reset_index()
# fam_size_df.columns = ["Top-level family", "Count"]

# #Counting number of speakers by family
# lang_fam_speakers = df.groupby("Top-level family")["Speakers"].sum().reset_index()
# lang_fam_speakers.columns = ["Top-level family", "Total number of speakers"]
# #print(lang_fam_speakers.head())

# #Merging the 2 into 1 dataframe
# lang_fam_summary_df = pd.merge(fam_size_df, lang_fam_speakers, on="Top-level family")
# #print(lang_fam_summary_df.head())
# #print(fam_size_df.head())
# #print(lang_fam_size)

# lang_fam_summary_df["text"] = lang_fam_summary_df.apply(
#     lambda row: f"{row['Top-level family']} \n{row['Count']} languages" if row["Count"] > 200 else "",
#     axis=1
# )

# fig2 = px.scatter(lang_fam_summary_df,
#     x="Count",
#     y="Total number of speakers", 
#     size="Count", 
#     color="Top-level family",
#     hover_name="Top-level family",
#     hover_data={"Count": False,
#                 "Top-level family": False,
#                 "Total number of speakers": True},
#     size_max= 120,
#     text= "text",
#     title="Language families by number of languages and speakers"
# )

# fig2.update_layout(
#     xaxis_title="Number of Languages",  # New label for x-axis
# )

# fig2.update_traces(
#     textposition='middle center',
#     textfont_size=10   
# )
=======

# Plot 2. Bubble chart to compare the size of language families by number of languages and speakers
#Counting number of languages by family
lang_fam_size = df["Top-level family"].value_counts()
fam_size_df = lang_fam_size.reset_index()
fam_size_df.columns = ["Top-level family", "Count"]

#Counting number of speakers by family
lang_fam_speakers = df.groupby("Top-level family")["Speakers"].sum().reset_index()
lang_fam_speakers.columns = ["Top-level family", "Total number of speakers"]
#print(lang_fam_speakers.head())

#Merging the 2 into 1 dataframe
lang_fam_summary_df = pd.merge(fam_size_df, lang_fam_speakers, on="Top-level family")
#print(lang_fam_summary_df.head())
#print(fam_size_df.head())
#print(lang_fam_size)

lang_fam_summary_df["text"] = lang_fam_summary_df.apply(
    lambda row: f"{row['Top-level family']} \n{row['Count']} languages" if row["Count"] > 200 else "",
    axis=1
)

fig2 = px.scatter(lang_fam_summary_df,
    x="Count",
    y="Total number of speakers", 
    size="Count", 
    color="Top-level family",
    hover_name="Top-level family",
    hover_data={"Count": False,
                "Top-level family": False,
                "Total number of speakers": True},
    size_max= 120,
    text= "text",
    title="Language families by number of languages and speakers"
)

fig2.update_layout(
    xaxis_title="Number of Languages",  # New label for x-axis
)

fig2.update_traces(
    textposition='middle center',
    textfont_size=10   
)
>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2

#Plot 3. Create a world map graph with longtitude and latitude data
df["Speakers"]=df["Speakers"].fillna(1)

#Hover data
df["hover_text"] = df.apply(
<<<<<<< HEAD
    lambda row: f"Language: {row['Name_x']}<br>Status: {row['Status']}<br>Speakers: approx. {row['Speakers']}",
=======
    lambda row: f"Language: {row['Name_x']}<br>Status: {row['Status']}<br>Speakers: {row['Speakers']}",
>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
    axis=1
)

fig3 = px.scatter_geo(
    df,
    lon="Longtitude",
    lat="Latitude", 
    hover_name="hover_text", 
    color="Top-level family",
    size_max=0.2,
    projection="natural earth",
<<<<<<< HEAD
    hover_data={"Longtitude": False,
                "Latitude": False, 
                "Name_x": False, 
                "Status": False,
                "Speakers": False,
=======
    title="World map of languages",
    hover_data={"Longtitude": False,
                "Latitude": False, 
                "Name_x": False, 
                "Status": True,
                "Speakers": True,
>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
                "Top-level family": True,
                "Country": True}
)

<<<<<<< HEAD
fig3.update_layout(
    showlegend=False,
    margin=dict(l=0, r=0, t=50, b=0),
    geo=dict(
        projection_scale=1,  
        center=dict(lon=0, lat=20)
    )
)

fig3.add_annotation(
    x=0.01,  
    y=0.01,  
    xref="paper",
    yref="paper",
    text="Colors of the dots represent a language family",  
    showarrow=False,
    font=dict(size=14, color="black"),
    align="left",
    bgcolor="white",
    bordercolor="black",
    borderwidth=1
)

=======
>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
# Footer component
footer_component = html.Footer(
    '''Data sources:
    \n UNESCO The World Atlas of Languageshttps://en.wal.unesco.org/discover/languages;
    \n Glottolog 5.1. https://glottolog.org/glottolog/language ,
    \n edited by Hammarström, Harald & Forkel, Robert & Haspelmath, Martin & Bank, Sebastian is licensed under a Creative Commons Attribution 4.0 International License''', 
    style={"textAlign": "left", "padding": "10px", "color": "gray", "fontSize": 12}
)
<<<<<<< HEAD
#Set up the dashboard app layout
=======
#Set up the app layout
>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
app.layout= dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(header_component)
    ]),

<<<<<<< HEAD
    
=======
>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
    # Description
    dbc.Row([
        dbc.Col(dash_description)
    ]),

    # Main content
    dbc.Row([
<<<<<<< HEAD
        # Left Column: Infobox + 1 smaller plot
        dbc.Col([
            infobox_component,
            dcc.Graph(figure=fig1, style={"height": "400px"}),
        ], width=4), 

        #Search bar
        dbc.Col([
            dbc.Row([
                dbc.Input(id="search-bar",
                type="text",
                placeholder="Search for a language...",
                debounce=True,  # Waits before triggering an update
                style={"width": "100%", "margin-bottom": "20px"}
            ),
            ], justify="center"),

        # Right Column: Large Plot 3 (Interactive map)
        dcc.Graph(id="map-plot", figure=fig3, style={"height": "800px"})
        ], width=8)
    ]),

    # dbc.Row([
    #     dbc.Col(dcc.Graph(figure= fig2)
    #     )
 
=======
        # Left Column: Infobox + 2 smaller plots
        dbc.Col([
            infobox_component,
            dcc.Graph(figure=fig1, style={"height": "400px"}),
            
        ], width=4), 

        # Right Column: Large Plot 3 (Interactive map)
        dbc.Col([
            dcc.Graph(figure=fig3, style={"height": "800px"})
        ], width=8)
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(figure= fig2)
        )
    ]),

>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
    # Footer
    dbc.Row([
        dbc.Col(footer_component)
    ])
], fluid=True)

<<<<<<< HEAD

#Search for a language
@app.callback(
    Output("map-plot", "figure"),
    Input("search-bar", "value")
)
def update_map(search_value):
    filtered_df = df  # Default: show all data

    # Filter data if search value is entered
    if search_value:
        filtered_df = df[df["Name_x"].str.contains(search_value, case=False, na=False)]

    # Create the updated map figure
    fig = px.scatter_geo(
        filtered_df,
        lon="Longtitude",
        lat="Latitude",
        hover_name= "Name_x",
        color="Top-level family",
        hover_data={"Longtitude": False,
                "Latitude": False, 
                "Name_x": False, 
                "Status": True,
                "Speakers": True,
                "Top-level family": True,
                "Country": True}
    )

    return fig.update_layout(showlegend=False)

=======
>>>>>>> b6202894159cf7dfb48ad612843f5e65097081d2
#Run the app
app.run_server(debug=True)
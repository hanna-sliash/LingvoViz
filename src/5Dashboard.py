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
df = pd.read_csv(r".\Data\final_dataset.csv")

#Create the components
header_component = html.H1("LingvoViz - Languages of the World Dashboard", className="text-center text-primary, mb-4") #header
dash_description = html.H2('''
                      This dashboard shows language diversity of the world. 
                      \n You can find plenty of information about language vitality, numbers of speakers and language families.
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
safe_lang_speakers = safe_languages["Speakers"].sum()
#print(f"The count of speakers of safe languages is {safe_lang_speakers}")


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
                 " languages whose vitality is considered safe and they are spoken by ",
                  html.Span(f"{transform_number(safe_lang_speakers)}", style={"fontSize": "20px", "fontWeight": "bold", "color": "#1f77b4"}), " people."]),
        html.P(["A staggering number of ",
               html.Span(f"{transform_number(endang_lang_count)}", style={"fontSize": "20px", "fontWeight": "bold", "color": "#1f77b4"}), 
                " languages are vulnerable or in danger of disappearance and count only ",
                 html.Span(f"{transform_number(endang_lang_speakers)}", style={"fontSize": "20px", "fontWeight": "bold", "color": "#1f77b4"}),
                  " speakers."]),
        html.P([html.Span(f"{transform_number(lost_lang_count)}", style={"fontSize": "20px", "fontWeight": "bold", "color": "#1f77b4"}), " languages have now been lost."])
    ])
], style={"marginBottom": "10px", "padding": "10px", "textSize": 14})

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

#Plot 3. Create a world map graph with longtitude and latitude data
df["Speakers"]=df["Speakers"].fillna(1)

#Hover data
df["hover_text"] = df.apply(
    lambda row: f"Language: {row['Name_x']}<br>Status: {row['Status']}<br>Speakers: {row['Speakers']}",
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
    title="World map of languages",
    hover_data={"Longtitude": False,
                "Latitude": False, 
                "Name_x": False, 
                "Status": True,
                "Speakers": True,
                "Top-level family": True,
                "Country": True}
)

# Footer component
footer_component = html.Footer(
    '''Data sources:
    \n UNESCO The World Atlas of Languageshttps://en.wal.unesco.org/discover/languages;
    \n Glottolog 5.1. https://glottolog.org/glottolog/language ,
    \n edited by Hammarström, Harald & Forkel, Robert & Haspelmath, Martin & Bank, Sebastian is licensed under a Creative Commons Attribution 4.0 International License''', 
    style={"textAlign": "left", "padding": "10px", "color": "gray", "fontSize": 12}
)
#Set up the app layout
app.layout= dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(header_component)
    ]),

    # Description
    dbc.Row([
        dbc.Col(dash_description)
    ]),

    # Main content
    dbc.Row([
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

    # Footer
    dbc.Row([
        dbc.Col(footer_component)
    ])
], fluid=True)

#Run the app
app.run_server(debug=True)
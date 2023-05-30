import streamlit as st
import pandas as pd
import textrazor
from googlesearch import search

# Title
st.title('Web Entity Analyzer 🕸️🔍')

# Description
st.write("""
This tool helps you analyze entities found in web content. You can input a search keyword, 
and this tool will scrape Google search results to find and analyze entities in the content of each result. 
It also lets you compare these entities with those found in a target URL of your choice. 

Entities are things like people, places, companies, and more. This tool uses TextRazor to extract 
entities from the web content and gives each entity a relevance and confidence score. 
These scores help you understand how important an entity is in the content.

At the end, you'll be able to download the analysis as CSV files. 

Before we begin, you'll need an API key from TextRazor. Here's how to get it:

1. Visit [TextRazor's website](https://www.textrazor.com/)
2. Click on 'Try TextRazor for Free'
3. Sign up for an account. Once you've signed up and logged in, you'll be directed to your dashboard.
4. On the dashboard, you'll see your API Key. This is the key you need to input into the tool.

Now that you have your API key, you can input it in the sidebar on the left, along with your target URL and search keywords.

Let's get started! 😃
""")


# Sidebar
st.sidebar.header('User Input 📝')
textrazor.api_key = st.sidebar.text_input("Enter your TextRazor API key")
target_url = st.sidebar.text_input("Enter target URL")
query = st.sidebar.text_input("Enter search keywords")
num_results = st.sidebar.slider("Number of results", 1, 100, 10)
country = st.sidebar.text_input("Enter country", "com")

# Functions
@st.cache
def get_entities(urls):
    entities = []
    for url in urls:
        client = textrazor.TextRazor(extractors=["entities"])
        response = client.analyze_url(url)
        for entity in response.entities():
            entities.append([url, entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types, entity.matched_text, entity.wikipedia_link])
    return entities

@st.cache
def getResults(uQuery, uTLD, uNum, uStart, uStop):
    d = []
    for j in search(uQuery, tld=uTLD, num=uNum, start=uStart, stop=uStop, pause=2): 
        d.append(j)
    return d

# Start Process Button
if st.button('Start Process 🚀'):
    results = getResults(query, country, num_results, 1, num_results)
    comp_entities = get_entities(results)
    comp_df = pd.DataFrame(comp_entities, columns=["URL","Entity", "Relevance_Score", "Confidence_Score", "Freebase_Types", "Matched_Text",'wikipedia_link'])
    comp_df.sort_values(by=['Relevance_Score'], ascending=False, inplace=True)

    target_entities = get_entities([target_url])
    target_df = pd.DataFrame(target_entities, columns=["URL","Entity", "Relevance_Score", "Confidence_Score", "Freebase_Types", "Matched_Text",'wikipedia_link'])
    target_df.sort_values(by=['Relevance_Score'], ascending=False, inplace=True)

    gap_df = comp_df[~comp_df['Entity'].isin(target_df['Entity'])]

    st.write("Process completed successfully! 🎉")

    st.download_button('Download comp_df', comp_df.to_csv(index=False), 'comp_df.csv', 'text/csv')
    st.download_button('Download target_df', target_df.to_csv(index=False), 'target_df.csv', 'text/csv')
    st.download_button('Download gap_df', gap_df.to_csv(index=False), 'gap_df.csv', 'text/csv')

import dask.bag as db
from glob import glob
import pandas as pd
import re
import numpy as np
from dash import Dash, dcc, html
from base64 import b64encode
import io

import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objs as go

from dash import jupyter_dash

app = Dash()

buffer = io.StringIO()

#getting all gwas_res which is a file with all chromosome 1 snps with p-vals and traits

allgwas_res = pd.read_csv('allgwas_res.csv')
allgwas_res.index = allgwas_res.SNP
allgwas_res.drop(['SNP'], axis = 1, inplace = True)

allgwas_res_sorted = allgwas_res.sort_values(by='-log10 P-Value', ascending=False)

# Drop duplicates based on the 'trait' column, keeping the first occurrence (largest p-value)
allgwas_res_no_duplicates = allgwas_res_sorted.drop_duplicates(subset='trait', keep='first')

# Get the top 20 traits with the largest p-values (if you have more than 20)
top_20_traits = allgwas_res_no_duplicates.nlargest(20, '-log10 P-Value')

li = top_20_traits.trait

print('li')

phenotype = allgwas_res[allgwas_res.trait.isin(li)]

print('Phenotype created')

phenotype = phenotype.reset_index().rename(columns={'index': 'SNP'})

print('Phenotype reset')

highlighted_snp = '1:102666585'

phenotype['highlight'] = phenotype.SNP.apply(lambda x: 'Highlighted' if x == highlighted_snp else 'Normal')

# Create a scatter plot with phenotypes on x and p-values on y
fig = px.scatter(
    phenotype, x='bp', y='-log10 P-Value',
    hover_name=phenotype.index,  # Show SNP names on hover
    title='Target SNP: 1:102666585 (3MB surround)',
    color = 'trait',
    size=phenotype['SNP'].apply(lambda x: 20 if x == highlighted_snp else 5),
    labels={'SNP': 'SNP', '-log10 P-Value': '-log10 P-Value'},  # Color points by phenotype
)

print('figure created')

fig.update_traces(marker=dict(line=dict(width=0, color='DarkSlateGrey')))

fig.update_traces(
    selector=dict(mode='markers'),  # Ensure we are customizing marker properties
    marker=dict(
        line=dict(
            width=[4 if highlight == 'Highlighted' else 0 for highlight in phenotype['highlight']]
        )
    )
)

print('traces updated')

fig.update_layout(
    width=1000,  # Set the width of the plot
    height=800   # Set the height of the plot
)

print('layout updated')

fig.write_html(buffer)

print('wrote_html')

html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

app.layout = html.Div([
    html.H4('Simple plot export options'),
    html.P("↓↓↓ try downloading the plot as PNG ↓↓↓", style={"text-align": "right", "font-weight": "bold"}),
    dcc.Graph(id="interactive-html-export-x-graph", figure=fig),
    html.A(
        html.Button("Download as HTML"), 
        id="interactive-html-export-x-download",
        href="data:text/html;base64," + encoded,
        download="plotly_graph.html"
    )
])


if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port='8050', debug=False)




import pandas as pd
import scipy.stats as stats
import plotly.express as px
import streamlit as st

def chi_squared():

    # Read CSV file
    df = pd.read_csv('Visualizations/question_7/question7_table.csv', index_col=0)

    # Filter countries that have more than 10 entries in total
    df = df[df['Total'] > 10]  # Only countries with more than 10 entries

    # Filter nationalities that have more than 10 entries in total
    df = df.loc[:, df.loc['Total'] > 10]  # Only nationalities with more than 10 entries

    # Perform Chi-Squared test of independence
    chi2, p, dof, expected = stats.chi2_contingency(df)

    # Interpret p-value
    alpha = 0.05  # Significance level
    if p < alpha:
        st.write("There is a significant relationship between the host country and nationality.")
    else:
        st.write("There is no significant relationship between the host country and nationality.")

    # Calculate the difference between observed and expected frequencies
    observed_vs_expected = df - expected
    
    return df, observed_vs_expected

# Output the differences (Optional)
#print(observed_vs_expected)

def plot_observed_frequencies():
    colors = px.colors.qualitative.Prism[:8]
    df, _ = chi_squared()
    
    # 📊 HEATMAP 1: Observed frequencies
    fig1 = px.imshow(df,
                    labels=dict(x="Nationality", y="Host Country", color="Frequency"),
                    x=df.columns,
                    y=df.index,
                    title="Observed Frequencies between Host Country and Nationality",
                    color_continuous_scale=colors,  # Adjust Prism color palette here
                    text_auto=True)
    
    return fig1
    
#fig1.show()

def plot_observed_expected_frequencies():
    colors = px.colors.qualitative.Prism[:8]
    df, observed_vs_expected = chi_squared()
    
    # 📊 HEATMAP 2: Differences between Observed & Expected
    fig2 = px.imshow(observed_vs_expected,
                    labels=dict(x="Nationality", y="Host Country", color="Difference"),
                    x=df.columns,
                    y=df.index,
                    title="Differences between Observed and Expected Frequencies",
                    color_continuous_scale=colors,  # Adjust Prism color palette here
                    text_auto=".2f")
    
    return fig2
    
#fig2.show()

def plot_conditional_probability():
    colors = px.colors.qualitative.Prism[:8]
    df, _ = chi_squared()
    
    # Calculate conditional probabilities (P(Nationality | Host Country))
    conditional_probabilities = df.div(df.sum(axis=1), axis=0)

    # 📊 HEATMAP 3: Conditional probabilities
    fig3 = px.imshow(conditional_probabilities,
                    labels=dict(x="Nationality", y="Host Country", color="Probability"),
                    x=df.columns,
                    y=df.index,
                    title="Conditional Probabilities between Host Country and Nationality",
                    color_continuous_scale=colors,  # Adjust Prism color palette here
                    text_auto=".2f")
    
    return fig3
    
#fig3.show()

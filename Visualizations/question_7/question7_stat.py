import pandas as pd
import scipy.stats as stats
import plotly.express as px


def chi_squared():
    """
    Perform Chi-Squared test of independence between host countries
    and nationalities."
    """
    # Read CSV file
    df = pd.read_csv(
        'Visualizations/question_7/host_country_nationality_table.csv', 
        index_col=0
    )

    # Filter countries that have more than 10 entries in total
    df = df[df['Total'] > 10]
    df = df.loc[:, df.loc['Total'] > 10]

    # Perform Chi-Squared test of independence
    chi2, p, dof, expected = stats.chi2_contingency(df)

    # Interpret p-value
    alpha = 0.05
    if p < alpha:
        print("Significant relationship between host country and nationality.")
    else:
        print("No significant relationship between host country and nationality.")

    # Calculate the difference between observed and expected frequencies
    observed_vs_expected = df - expected
    
    return df, observed_vs_expected

# Output the differences (Optional)
# print(observed_vs_expected)


def plot_observed_frequencies():
    """
    Plot a heatmap of observed frequencies.
    """
    colors = px.colors.qualitative.Prism[:8]
    df, _ = chi_squared()
    
    fig1 = px.imshow(
        df,
        labels=dict(
            x="Nationality",
            y="Host Country",
            color="Number of Tournaments"
        ),
        x=df.columns,
        y=df.index,
        title="Observed Frequencies between Host Country and Nationality",
        color_continuous_scale=colors,
        text_auto=True
    )
    
    return fig1
    
# fig1.show()


def plot_observed_expected_frequencies():
    """
    Plot a heatmap of differences between observed and expected frequencies."
    """
    colors = px.colors.qualitative.Prism[:8]
    df, observed_vs_expected = chi_squared()
    
    fig2 = px.imshow(
        observed_vs_expected,
        labels=dict(
            x="Nationality",
            y="Host Country",
            color="Difference"
        ),
        x=df.columns,
        y=df.index,
        title="Differences between Observed and Expected Frequencies",
        color_continuous_scale=colors,
        text_auto=".2f"
    )
    
    return fig2
    
# fig2.show()


def plot_conditional_probability():
    """
    Plot a heatmap of conditional probabilities.
    """
    colors = px.colors.qualitative.Prism[:8]
    df, _ = chi_squared()
    
    # Calculate conditional probabilities (P(Nationality | Host Country))
    conditional_probabilities = df.div(df.sum(axis=1), axis=0)

    fig3 = px.imshow(
        conditional_probabilities,
        labels=dict(
            x="Nationality",
            y="Host Country",
            color="Probability"
        ),
        x=df.columns,
        y=df.index,
        title="Conditional Probabilities between Host Country and Nationality",
        color_continuous_scale=colors,
        text_auto=".2f"
    )
    
    return fig3
    
# fig3.show()

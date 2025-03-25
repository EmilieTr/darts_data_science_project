import scipy.stats as stats
import pandas as pd

def t_test():
    """
    Perform a t-test between European Tour and Major Tournaments.
    """
    # Load data
    df = pd.read_csv("Visualizations/question_10/180_stats.csv")

    # Define groups
    european_tour = df[
        df["Tournament"].str.contains("European Tour")
    ]["Probability (%)"]

    # Major tournaments (all other events)
    major_tournaments = df[
        ~df["Tournament"].str.contains("European Tour")
    ]["Probability (%)"]

    # Perform independent t-test
    t_stat, p_value = stats.ttest_ind(
        european_tour, 
        major_tournaments, 
        equal_var=False
    )

    # Print results
    print(f"T-Statistic: {t_stat:.3f}")
    print(f"P-Value: {p_value:.3f}")

    # Interpretation
    if p_value < 0.05:
        result = (
            "Significant difference between "
            "European Tour and Major Tournaments."
        )
    else:
        result = (
            "No significant difference between "
            "European Tour and Major Tournaments."
        )
        
    return result

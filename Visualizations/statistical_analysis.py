import numpy as np 
from scipy.stats import pearsonr
from scipy.stats import chi2_contingency

def all_statistical_tests(x, y):
    correlation_coefficient(x, y)
    chi_square_test(x,y)
    mean_and_median(y)
    variance_and_standard_deviation(y)

'''
correlation coefficient (Pearson):
Measures the linear relationship between two variables (-1 to 1).
- r = 1 → Perfect positive correlation (if x increases, y also increases)
- r = −1 → Perfect negative correlation (if x increases, y decreases)
- r = 0 → No linear relationship

p-value: is the correlation statistically significant? 
- p < 0.05 (e.g.): correlation is significant
- p > 0.05 (e.g.): no statistically significant correlation
A low p-value (e.g., < 0.05) suggests that the correlation is significant and unlikely to have occurred by chance.
A high p-value (e.g., > 0.05) suggests that there is no statistically significant correlation between the variables
'''
def correlation_coefficient(x, y):
    correlation_coefficient, p_value = pearsonr(x, y)
    #print(f"Pearson-Korrelationskoeffizient (scipy): {correlation_coefficient:.2f}, p-Wert: {p_value:.5f}")
    return correlation_coefficient, p_value


'''
Chi Square Test:
Is used to check whether two categorical variables are independent or if there is a significant association between them
P-value:
- P-value < 0.05 → Significant association → The variables are not independent.
- P-value ≥ 0.05 → No significant association → The variables are independent.

Chi square value:
how much the data deviates from the expected data under the assumption of independence
- high Chi-Square: stronger deviation from independence; the two variables might be related
- lower Chi-Square: data is close to what we expect under independence; variables are likely unrelated

Degrees of Freedom:
The degrees of freedom (dof) determine how much flexibility the test has

Expected Frequencies:
The expected frequency is what we would expect under the assumption that the two variables are independent.

maybe good for question 6
'''
def chi_square_test(x,y):
    # Create the contingency table
    table = np.array([x,y])
    # Perform Chi-Square Test
    chi2, p, dof, expected = chi2_contingency(table)

    # Print results
    #print(f"Chi-Square Value: {chi2:.2f}")
    #print(f"P-Value: {p:.5f}")
    #print(f"Degrees of Freedom: {dof}")
    #print("Expected Frequencies:\n", expected)
    return round(chi2, 2), round(p, 5), dof, expected


'''
Mean and Median:
- Mean (arithmetic average): sensitive to outliers; best for symmetric data
- Median : middle value of data; not sensitive to outliers
'''
def mean_and_median(x):
    # mean
    mean = np.mean(x)

    # median
    median = np.median(x)

    #print(f"Mean: {mean}")
    #print(f"Median: {median}")
    return mean, median

'''
Variance and standard deviation:
- variance: average squared deviation of each data point from the mean
High Variance: data points are spread out widely from the mean. The larger the variance, the more dispersed the data is.
Low Variance: data points are closer to the mean. The smaller the variance, the less spread out the data is.

- standard deviation: square root of the variance and tells you how much the data points, on average, deviate from the mean.
High Standard Deviation: data points are spread out far from the mean, indicating greater variability.
Low Standard Deviation: data points are closer to the mean, indicating less variability.
'''

def variance_and_standard_deviation(x):
    # Variance
    variance = np.var(x)

    # Standard Deviation
    std_dev = np.std(x)

    #print(f"Variance: {variance}")
    #print(f"Standard Deviation: {std_dev}")
    return variance, std_dev


x = [10, 20, 30, 40, 50]
y = [15, 25, 35, 45, 55]
all_statistical_tests(x,y)
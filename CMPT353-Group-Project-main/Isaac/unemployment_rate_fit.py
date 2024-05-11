import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import linregress
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def to_datetime(date_str):
    return datetime.strptime(date_str, '%Y-%m')
def fit(region_str):
    data = pd.read_csv('../covid_and_employment_total_included.csv')
    data = data[data['GEO'] == region_str]

    y = data['total unemployment rate(%)']
    result = linregress(data['covid cases'], y)
    result_2 = linregress(data['covid deaths'], y)
    x_model_3 = pd.concat([data['covid cases'], data['covid deaths']], axis=1)
    model_3 = LinearRegression(fit_intercept = True)
    model_3.fit(X = x_model_3, y = y)
    score_3 = model_3.score(x_model_3, y)
    model_4 = make_pipeline(
        PolynomialFeatures(4),
        LinearRegression(fit_intercept = True)
    )
    model_4.fit(x_model_3, y)
    score_4 = model_4.score(x_model_3, y)

    fit_results = {'GEO': region_str,
                   'prediction with covid cases pvalue': result.pvalue,
                   'prediction with covid deaths pvalue': result_2.pvalue,
                   'predictions with both score': score_3,
                   'polynomial regression of both score': score_4}
    fit_results = pd.DataFrame(fit_results, index= ['GEO'])

    def predict_line(x):
        return result.slope * x + result.intercept

    def predict_line_2(x):
        return result_2.slope * x + result_2.intercept

    data_corr = data[['total population(1000)',
                      'total labor force(1000)',
                      'total fulltime employments(1000)',
                      'total unemployed',
                      'total unemployment rate(%)',
                      'total participation rate(%)',
                      'total employment rate(%)',
                      'covid cases',
                      'covid deaths']]
    data_corr = data_corr.corr(method='pearson', numeric_only = True)
    data_corr.to_csv('./usual/covid_employment_correlations_{}.csv'.format(region_str))

    data['datetime'] = data['REF_DATE'].map(to_datetime)

    x_model_3 = pd.concat([data['covid cases'], data['covid deaths']], axis=1)
    plt.scatter(data['datetime'], data['total unemployment rate(%)'])
    plt.plot(data['datetime'], data['covid cases'].map(predict_line))
    plt.plot(data['datetime'], data['covid deaths'].map(predict_line_2))
    plt.plot(data['datetime'], model_3.predict(x_model_3))
    plt.plot(data['datetime'], model_4.predict(x_model_3))
    plt.title('linear and polynomial fits of {} unemployment rate'.format(region_str))
    plt.legend(['unemployment',
                'prediction with covid cases',
                'prediction with covid deaths',
                'predictions with both',
                'polynomial regression of both'])
    fig_location = './usual/' + region_str + '_polynomial_fits.svg'
    plt.savefig(fig_location)
    plt.clf()
    return fit_results

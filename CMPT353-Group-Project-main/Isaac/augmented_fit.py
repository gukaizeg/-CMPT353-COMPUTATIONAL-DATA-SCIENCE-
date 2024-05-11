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
    data = pd.read_csv('covid_and_employment_augmented_national_covid.csv')
    data = data[data['GEO'] == region_str]

    y = data['total unemployment rate(%)']
    x_model = pd.concat([data['covid cases'],
                         data['covid deaths'],
                         data['canada covid cases'],
                         data['canada covid deaths']], axis = 1)
    model_1 = LinearRegression(fit_intercept = True)
    model_1.fit(X = x_model, y = y)
    score_1 = model_1.score(x_model, y)
    model_2 = make_pipeline(
        PolynomialFeatures(4),
        LinearRegression(fit_intercept = True)
    )
    model_2.fit(x_model, y)
    score_2 = model_2.score(x_model, y)

    fit_results = {'GEO': region_str,
                   'multilinear prediction': score_1,
                   'polynomial prediction': score_2}
    fit_results = pd.DataFrame(fit_results, index= ['GEO'])

    data['datetime'] = data['REF_DATE'].map(to_datetime)

    plt.scatter(data['datetime'], data['total unemployment rate(%)'])
    plt.plot(data['datetime'], model_1.predict(x_model))
    plt.plot(data['datetime'], model_2.predict(x_model))
    plt.title('linear and polynomial fits of {} unemployment rate'
              'using local and Canada COVID-19 data'.format(region_str))
    plt.legend(['unemployment',
                'predictions with augmented local and national covid data',
                'polynomial regression of augmented local and national covid data'])
    fig_location = './augmented/' + region_str + '_polynomial_fits.svg'
    plt.savefig(fig_location)
    plt.clf()
    return fit_results

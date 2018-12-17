
## Initial Set up for code
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import signal as sig
import pandas as pd
from math import e
import tabulate

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

plt.style.use('ggplot')

# import raw data
columnNames = ['Center of Bouyancy','Prismatic Coefficient',
               'Length / Displacement','Beam / Draught',
               'Length / Beam','Froude Number',
               'Residuary Resistance / Displacement']
yachtData = pd.read_csv("raw/data.csv", names=columnNames, delim_whitespace=True)

#print(yachtData.describe().to_latex())
#tabulate.tabulate( yachtData.describe(), tablefmt="pipe" )

sns.pairplot( data=yachtData )
plt.show()

plt.plot(yachtData['Froude Number'],yachtData['Residuary Resistance / Displacement'],'.')

plt.xlabel('Froude Number')
plt.ylabel('Residuary Resistance / Displacement')
plt.title('Largest Contributing Factor')
plt.show()

plt.subplot(2,1,1)
plt.title("Results from all Trials")
plt.plot(yachtData['Froude Number'], '.')
plt.ylabel("Froude Number")
plt.subplot(2,1,2)
plt.plot(yachtData['Residuary Resistance / Displacement'], '.')
plt.xlabel("Trial Number")
plt.ylabel("Residuary Resistance")
plt.show()

#tabulate.tabulate( yachtData.corr(), tablefmt="markdown", headers="keys" )

X = yachtData[[
    'Center of Bouyancy'
   ,'Prismatic Coefficient'
   ,'Length / Displacement'
   ,'Beam / Draught'
   ,'Length / Beam'
   ,'Froude Number'
    ]].values

Y = yachtData[['Residuary Resistance / Displacement']].values

testSize = 0.4
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=testSize)

lm = LinearRegression()
lm.fit(X_train,y_train)

y_pred = lm.predict(X_test)

score = r2_score(y_test,y_pred)
mse = mean_squared_error(y_test,y_pred)

plt.figure()

plt.plot(y_test,y_pred,'.')
plt.plot(y_test,y_test,'-', label="Perfect Fit")

plt.xlabel("Observed Residuary Force")
plt.ylabel("Predicted Residuary Force")
plt.title("Linear Fit; Score:{:1.3f}; MSE:{:1.3f}".format(score,mse))
plt.legend()
plt.show()

trials = 100
maxDegree = 10
degrees = np.arange( maxDegree )
r2Scores = np.zeros( (trials, maxDegree) )
meanSquareErrors = np.zeros( (trials, maxDegree) )

for trial in np.arange(trials):
    for degree in degrees:
        
        # build polynomial features
        polynomial_features= PolynomialFeatures(degree=degree)
        x_train_poly = polynomial_features.fit_transform(X_train)
        print("{}:  {}".format(degree,np.size(x_train_poly, axis=1)))
        
        # Perform linear regression
        model = LinearRegression()
        model.fit(x_train_poly, y_train)
        
        y_test_predict = model.predict(polynomial_features.fit_transform(X_test))
        
        r2 = r2_score(y_test,y_test_predict)
        r2Scores[trial,degree] = r2
        
        mse = mean_squared_error(y_test,y_test_predict)
        meanSquareErrors[trial,degree] = mse

r2Scores = np.mean( r2Scores, axis=0 )
meanSquareErrors = np.mean( meanSquareErrors, axis=0 )

plt.plot(degrees,r2Scores,'o-')
plt.ylim(-.1,1.1)
plt.xlabel("Polynomial Degree")
plt.ylabel("$R^2$ Score")
plt.title("$R^2$ Scores")
plt.show()

plt.plot(degrees,meanSquareErrors,'o-')
plt.xlabel("Polynomial Degree")
plt.ylabel("Mean Square Error")
plt.title("Mean Square Errors")
plt.show()

degree = 3
polynomial_features= PolynomialFeatures(degree=degree)
x_train_poly = polynomial_features.fit_transform(X_train)

model = LinearRegression()
model.fit( x_train_poly, y_train )

y_test_predict = model.predict( polynomial_features.fit_transform( X_test ) )

r2 = r2_score(y_test,y_test_predict)

mse = mean_squared_error(y_test,y_test_predict)

plt.figure()
plt.plot(y_test,y_test,'-', label="Perfect Fit")
plt.plot(y_test,y_test_predict,'.')
plt.title("{} Degree Polyfit; Score:{:1.3f}; MSE:{:1.3f}".format(degree,r2,mse))
plt.xlabel("Observed Residuary Force")
plt.ylabel("Predicted Residuary Force")
plt.legend()
plt.show()

#print(model.coef_)

#features = pd.DataFrame(x_train_poly, columns=polynomial_features.get_feature_names(yachtData.columns))
#print(polynomial_features.get_feature_names(yachtData.columns))

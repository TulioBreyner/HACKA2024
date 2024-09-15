import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

def prepare_training_data():
    # Carregar dados do banco de dados
    df = pd.read_csv('article_ratings.csv')
    
    # Dividir em conjuntos de treino e teste
    X = df[['features']]  # Supondo que 'features' é uma coluna com características dos artigos
    y = df['rating']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')

def update_model():
    X_train, X_test, y_train, y_test = prepare_training_data()
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    joblib.dump(model, 'model.pkl')

if __name__ == '__main__':
    update_model()


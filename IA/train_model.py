import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

def prepare_training_data():
    # Carregar os dados preparados
    df = pd.read_csv('prepared_data.csv')
    
    # Exemplo de seleção de características e alvo
    X = df[['scaled_features']]  # Supondo que 'scaled_features' seja uma coluna com características escaladas
    y = df['rating']
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model():
    X_train, X_test, y_train, y_test = prepare_training_data()
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    print(f"Erro quadrático médio: {mean_squared_error(y_test, predictions)}")
    
    joblib.dump(model, 'model.pkl')

if __name__ == '__main__':
    train_model()

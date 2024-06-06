import pandas as pd
import joblib

def preprocess_custom_data(data):
    # Check if 'price' column exists and convert it to numeric (if present)
    if 'price' in data.columns:
        data['price'] = data['price'].str.replace(',', '', regex=False).str.replace(' RON', '', regex=False).astype(float)
    
    # Convert rating to numeric
    data['rating'] = data['rating'].astype(float)
    
    # Ensure rating columns are present and fill NaN values with 0
    rating_columns = ['rating_5_star', 'rating_4_star', 'rating_3_star', 'rating_2_star', 'rating_1_star']
    for col in rating_columns:
        if col not in data.columns:
            data[col] = 0
        else:
            data[col] = data[col].fillna(0).astype(float)
    
    return data

def test_custom_data(custom_data_path, model_path, output_path, feature_names_path):
    try:
        # Load the custom data
        custom_data = pd.read_csv(custom_data_path)
    except Exception as e:
        print(f"Error loading custom data: {e}")
        return

    # Preprocess the custom data
    custom_data_processed = preprocess_custom_data(custom_data)

    try:
        # Load the trained model
        model = joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Load feature names
    with open(feature_names_path, 'r') as f:
        feature_names = [line.strip() for line in f]
    
    # Ensure custom data has the same feature names and order
    features = custom_data_processed[feature_names]

    # Make predictions
    predictions = model.predict(features)

    # Add predictions to the custom data
    custom_data['predicted_price'] = predictions

    # Create a new DataFrame with the desired columns
    pretty_data = pd.DataFrame({
        'CPU Name': custom_data['title'],
        'Predicted price': custom_data['predicted_price'],
        'Overall Reviews': custom_data['rating'],
        '5star': custom_data['rating_5_star'],
        '4star': custom_data['rating_4_star'],
        '3star': custom_data['rating_3_star'],
        '2star': custom_data['rating_2_star'],
        '1star': custom_data['rating_1_star']
    })

    # Export the data to a CSV file
    pretty_data.to_csv(output_path, index=False)
    print(f"Data exported to {output_path}")

if __name__ == "__main__":
    # Path to the custom data CSV file
    custom_data_path = 'custom_cpu_data.csv'
    # Path to the saved model
    model_path = 'cpu_price_predictor_model.pkl'
    # Path to the output file
    output_path = 'pretty_output.csv'
    # Path to the feature names file
    feature_names_path = 'feature_names.txt'
    # Test the model with custom data
    test_custom_data(custom_data_path, model_path, output_path, feature_names_path)

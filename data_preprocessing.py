import pandas as pd

def preprocess_data(file_path):
    # Load the data
    data = pd.read_csv(file_path)

    # Drop rows with missing price or rating
    data = data.dropna(subset=['price', 'rating'])
    
    # Convert price to numeric
    data['price'] = data['price'].str.replace(',', '').str.replace(' RON', '').astype(float)
    
    # Convert rating to numeric
    data['rating'] = data['rating'].astype(float)
    
    # Extract rating distribution into separate columns
    data['rating_distribution'] = data['rating_distribution'].apply(eval)
    rating_distribution_df = data['rating_distribution'].apply(pd.Series)
    rating_distribution_df.columns = [f'rating_{col}_star' for col in rating_distribution_df.columns]
    
    # Concatenate the rating distribution columns to the original dataframe
    data = pd.concat([data, rating_distribution_df], axis=1)
    
    # Drop the original rating distribution column
    data = data.drop(columns=['rating_distribution'])
    
    # Fill NaN values in rating distribution with 0
    data = data.fillna(0)
    
    return data

if __name__ == "__main__":
    processed_data = preprocess_data('detailed_cpu_data.csv')
    processed_data.to_csv('processed_cpu_data.csv', index=False)
    print("Data preprocessing completed and saved to processed_cpu_data.csv")


import pickle
import os

input_path = r'sms\archive\pickle\preprocessed_data.pkl'
output_path = r'sms\archive\pickle\vectorizer.pkl'

print(f"Loading {input_path}...")
try:
    with open(input_path, 'rb') as f:
        data = pickle.load(f)
        
    if len(data) == 3:
        cv, X, y = data
        print("Successfully unpacked (cv, X, y).")
        
        print(f"Saving 'cv' to {output_path}...")
        with open(output_path, 'wb') as f:
            pickle.dump(cv, f)
        
        print(f"Success! New file size: {os.path.getsize(output_path) / 1024:.2f} KB")
    else:
        print(f"Unexpected data format. length: {len(data)}")

except Exception as e:
    print(f"Error: {e}")

import os
import csv
import json
import numpy as np

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'crop_data', 'Crop_recommendation.csv')
    
    # Store values per crop and parameter
    # Parameters: N, P, K, temp, humidity, ph, rainfall
    crop_data = {}
    
    with open(csv_path, mode='r') as f:
        reader = csv.reader(f)
        header = next(reader) # N, P, K, temperature, humidity, ph, rainfall, label
        
        for row in reader:
            if not row:
                continue
            vals = [float(x) for x in row[:-1]]
            label = row[-1].strip().lower()
            
            if label not in crop_data:
                crop_data[label] = {
                    'N': [], 'P': [], 'K': [],
                    'temp': [], 'humidity': [], 'ph': [], 'rainfall': []
                }
            
            crop_data[label]['N'].append(vals[0])
            crop_data[label]['P'].append(vals[1])
            crop_data[label]['K'].append(vals[2])
            crop_data[label]['temp'].append(vals[3])
            crop_data[label]['humidity'].append(vals[4])
            crop_data[label]['ph'].append(vals[5])
            crop_data[label]['rainfall'].append(vals[6])
            
    # Calculate min, max, mean for each parameter of each crop
    crop_ranges = {}
    for crop, params in crop_data.items():
        crop_ranges[crop] = {}
        for param, values in params.items():
            arr = np.array(values)
            # Use 5th and 95th percentiles to avoid outliers and show reasonable typical ranges
            p5 = float(np.percentile(arr, 5))
            p95 = float(np.percentile(arr, 95))
            crop_ranges[crop][param] = {
                'min': round(p5, 1),
                'max': round(p95, 1),
                'mean': round(float(np.mean(arr)), 1)
            }
            
    # Save as JSON
    output_path = os.path.join(base_dir, 'model', 'crop_ranges.json')
    with open(output_path, 'w') as out_f:
        json.dump(crop_ranges, out_f, indent=4)
        
    print(f"Calculated and saved crop ranges to {output_path}")

if __name__ == '__main__':
    main()

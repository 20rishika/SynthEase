actual_synthesis_depth = 6
predicted_depth = 5

error = abs(actual_synthesis_depth - predicted_depth)
print(f"\nActual Depth: {actual_synthesis_depth}, Predicted Depth: {predicted_depth}")
print(f"Prediction Error: {error}")

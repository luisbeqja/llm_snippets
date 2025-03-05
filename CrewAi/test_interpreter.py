from base import local_code_interpreter

# Test basic functionality
test_code = """
print("Hello from the local code interpreter!")
x = 5
y = 10
print(f"The sum of {x} and {y} is {x + y}")
"""

print("Testing basic code execution:")
result = local_code_interpreter(test_code)
print(result)

# Test library installation and usage
plotting_code = """
import plotly.graph_objects as go
import plotly.io as pio

# Create a simple bar chart
fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[10, 5, 8])])

# Update layout
fig.update_layout(title='Test Chart', xaxis_title='X', yaxis_title='Y')

# Print success message
print("Successfully created a Plotly figure object!")
print("To save as image, plotly would use pio.write_image()")
"""

print("\nTesting library import:")
result = local_code_interpreter(plotting_code, libraries_used="plotly")
print(result)
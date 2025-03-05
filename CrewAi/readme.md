# CrewAI Market Research Automation Project

## Overview

This project demonstrates an advanced AI-powered market research workflow using CrewAI, showcasing how multiple AI agents can collaborate to conduct comprehensive market analysis.

### Project Purpose

The CrewAI Market Research Project automates the process of gathering, analyzing, and visualizing market insights for a specific industry. It leverages AI agents with specialized roles to:
- Conduct in-depth market research
- Analyze competitive landscapes
- Create compelling data visualizations

## Architecture

### Agents

The project implements three specialized AI agents:

1. **Market Research Specialist**
   - **Role**: Conduct comprehensive market research
   - **Key Responsibilities**:
     - Identify market trends
     - Analyze market size and growth potential
     - Uncover emerging technologies

2. **Competitive Intelligence Analyst**
   - **Role**: Analyze competitors and market dynamics
   - **Key Responsibilities**:
     - Identify top market players
     - Perform SWOT analysis
     - Investigate unique market positioning strategies

3. **Data Visualization Expert**
   - **Role**: Create visual representations of research findings
   - **Key Responsibilities**:
     - Generate charts and graphs
     - Design infographics
     - Translate complex data into digestible visuals

### Workflow

The project follows a structured workflow:
1. Research Specialist collects market insights
2. Competitive Intelligence Analyst examines the competitive landscape
3. Data Visualization Expert creates a comprehensive visual report

## Local Execution (No Docker Required)

This project has been configured to run entirely on your local machine without requiring Docker:

- The `local_code_interpreter` tool executes Python code directly on your local machine
- The visualization scripts are saved and executed in your project directory
- Package installations happen through your local pip

## Installation and Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   ```
   export OPENAI_API_KEY='your-openai-api-key'
   ```
   or create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ```

## Running the Project

To run the full CrewAI market research process:

```
python base.py
```

### Testing the Local Code Interpreter

You can verify that the local code interpreter is working correctly by running:

```
python test_interpreter.py
```

This will execute a simple test script and a Plotly example to verify functionality.

### Using the Visualization Module Directly

For quick access to market research visualizations, you can use:

```
python visualization.py
```

This will generate two visualization files:
- `market_growth.png`: Bar chart showing the projected growth of AI in Healthcare
- `competitor_analysis.png`: Radar chart comparing top competitors in the space

You can also import these functions in your own scripts:

```python
from visualization import create_market_growth_chart, create_competitor_analysis_chart

# Create visualizations with custom paths
market_chart = create_market_growth_chart('custom_path.png')
competitor_chart = create_competitor_analysis_chart('competitor_radar.png')
```

## Troubleshooting

If you encounter any issues:

1. Ensure all dependencies are properly installed:
   ```
   pip install plotly kaleido
   ```
2. Make sure your Python environment has write permissions to the current directory
3. Try running the test script to verify code execution is working: `python test_interpreter.py`
4. For plotly-specific issues, ensure you have kaleido installed: `pip install kaleido`
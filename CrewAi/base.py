from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
from crewai.tools import tool
import subprocess
import tempfile

# Set up the language model (replace with your preferred LLM)
llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create a local code interpreter tool using the tool decorator
@tool("Code Interpreter")
def local_code_interpreter(code: str, libraries_used: str = None) -> str:
    """
    Execute Python code locally without Docker.
    
    Args:
        code: Python code to execute
        libraries_used: Optional comma-separated list of libraries to install (e.g., 'numpy,pandas,plotly')
    
    Returns:
        The output of the executed code
    """
    # Install any required libraries if specified
    if libraries_used:
        libs = [lib.strip() for lib in libraries_used.split(',')]
        for lib in libs:
            try:
                subprocess.run(
                    ["pip", "install", lib],
                    capture_output=True,
                    text=True,
                    check=True
                )
            except Exception as e:
                return f"Error installing {lib}: {str(e)}"
    
    # Write code to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
        temp_filename = temp.name
        temp.write(code.encode())
    
    try:
        # Execute the code
        result = subprocess.run(
            ["python", temp_filename],
            capture_output=True,
            text=True
        )
        
        # Clean up the temporary file
        os.unlink(temp_filename)
        
        # Return the result
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error executing code: {result.stderr}"
    except Exception as e:
        # Clean up and return error
        os.unlink(temp_filename)
        return f"Error: {str(e)}"

# Create a package installer tool using the tool decorator
@tool("Package Installer")
def package_installer(package_list: str) -> str:
    """
    Install Python packages using pip.
    
    Args:
        package_list: A comma-separated list of packages to install (e.g., 'numpy, pandas, matplotlib').
    
    Returns:
        A string with the installation results.
    """
    packages = [pkg.strip() for pkg in package_list.split(',')]
    results = []
    
    for package in packages:
        try:
            result = subprocess.run(
                ["pip", "install", package], 
                capture_output=True, 
                text=True, 
                check=True
            )
            results.append(f"Successfully installed {package}: {result.stdout}")
        except subprocess.CalledProcessError as e:
            results.append(f"Failed to install {package}: {e.stderr}")
    
    return "\n".join(results)

# Define Agents
class MarketResearchCrew:
    def __init__(self):
        # Research Specialist Agent
        self.research_specialist = Agent(
            role="Market Research Specialist",
            goal="Conduct comprehensive market research on emerging tech trends",
            backstory="An experienced market researcher with deep insights into technology markets, "
                      "known for uncovering hidden market opportunities and trends.",
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

        # Competitive Intelligence Agent
        self.competitive_intel_agent = Agent(
            role="Competitive Intelligence Analyst",
            goal="Analyze competitors and identify market positioning strategies",
            backstory="A sharp-minded competitive intelligence expert who excels at "
                      "dissecting competitor strategies and market dynamics.",
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

        # Data Visualization Specialist
        self.data_viz_agent = Agent(
            role="Data Visualization Expert",
            goal="Create a python script that will create a plotly plot of the market research and competitive analysis findings.",
            backstory="A creative data visualization specialist who transforms complex "
                      "market data into clear, insightful graphics and reports.",
            verbose=True,
            allow_delegation=False,
            llm=llm,
            tools=[local_code_interpreter, package_installer]
        )

    def run_market_research(self, target_industry):
        # Task 1: Market Trend Research
        market_research_task = Task(
            description=f"Conduct an in-depth market research analysis for the {target_industry} "
                        "industry. Identify key trends, market size, growth potential, "
                        "and emerging technologies. Provide a comprehensive overview.",
            agent=self.research_specialist,
            expected_output="A detailed market research report including:"
                            "- Current market size"
                            "- Projected growth rate"
                            "- Key emerging trends"
                            "- Potential technological disruptions"
        )

        # Task 2: Competitive Landscape Analysis
        competitive_analysis_task = Task(
            description=f"Analyze the competitive landscape in the {target_industry}. "
                        "Identify top players, their strengths, weaknesses, and unique positioning.",
            agent=self.competitive_intel_agent,
            expected_output="A comprehensive competitive analysis report including:"
                            "- Top 5 market competitors"
                            "- SWOT analysis for each competitor"
                            "- Unique market positioning strategies"
        )

        # Task 3: Data Visualization
        data_visualization_task = Task(
            description="Create a python script that will create a plotly plot of the market research and competitive analysis findings. Save the plot as png file. If the Code Interpreter tool fails, provide detailed Python code that the user can run manually with clear instructions for setup and execution.",
            agent=self.data_viz_agent,
            expected_output="Either a PNG visualization file saved in the current working directory, or detailed Python code with instructions for manual execution."
        )

        # Create the Crew
        crew = Crew(
            agents=[
                self.research_specialist,
                self.competitive_intel_agent,
                self.data_viz_agent
            ],
            tasks=[
                market_research_task,
                competitive_analysis_task,
                data_visualization_task
            ],
            verbose=True
        )

        # Kick off the research
        result = crew.kickoff(inputs={"target_industry": target_industry})
        return result

# Example Usage
def main():
    # Initialize the Market Research Crew
    market_research_crew = MarketResearchCrew()
    
    # Run market research for a specific industry
    target_industry = "Artificial Intelligence in Healthcare"
    
    try:
        # Try running the crew workflow
        research_results = market_research_crew.run_market_research(target_industry)
        print(research_results)
    except Exception as e:
        # If an error occurs, especially with the Code Interpreter
        print(f"Error running CrewAI workflow: {e}")
        print("Attempting to generate visualizations directly...")
        
        try:
            # Try using our custom visualization module as fallback
            from visualization import create_market_growth_chart, create_competitor_analysis_chart
            
            market_chart = create_market_growth_chart()
            competitor_chart = create_competitor_analysis_chart()
            
            print(f"Successfully created visualizations:")
            print(f"- Market growth chart: {market_chart}")
            print(f"- Competitor analysis chart: {competitor_chart}")
        except ImportError:
            print("Please install required packages first:")
            print("pip install plotly kaleido")
        except Exception as viz_error:
            print(f"Error creating visualizations: {viz_error}")
            print("You can manually run the visualization.py script to generate charts.")

if __name__ == "__main__":
    main()

# Prerequisites and Setup:
"""
Prerequisites:
1. Install required libraries:
   pip install crewai langchain-openai

2. Set up OpenAI API Key:
   export OPENAI_API_KEY='your-openai-api-key'

Notes:
- This example uses OpenAI's GPT model, but CrewAI supports multiple LLMs
- Customize agents, tasks, and workflows to fit specific research needs
- Adjust verbose levels and delegation settings as needed
"""
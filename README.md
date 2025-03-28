
# DAG Health Checker (using Flask)

This Python application is a Flask-based API that allows users to upload a Directed Acyclic Graph (DAG) of system components, check the health of the components asynchronously.

## Features:

- Upload DAG: Upload a JSON file representing the DAG structure.

- Check Health: Check the health status of components asynchronously.

- Health Status: View the health status of the system's components in a table format.

## Prerequisites

To run this project, make sure you have the following installed:

- Python 3.x

- pip3 (Python package installer)

## Installation
- 1. Clone or download the repository:
 	- git clone https://github.com/darshiarjun/DAG_health_check.git
 	- cd Flask-DAG-Health-Checker

- 2. Install dependencies:
 	- pip install -r requirements.txt

	- The required dependencies include:

 		- Flask: Web framework to build the API.
 		- NetworkX: Library for working with graphs.
 		- Asyncio: Library for asynchronous programming.
 		- Pandas: Data manipulation library to manage health status in a table format.
 		- Matplotlib: For graph visualization.

## Usage
- 1. Run the webapp Application:

 	- Start the Flask web server with the following command:

  		- python3 web_api_dag.py
  		- By default, the server runs at http://localhost:8080.

- 2. API Endpoints:
 	- POST /upload: Upload a JSON file representing the DAG of system components.

  		- Example of uploading the JSON file using curl:
  		- curl -X POST -H "Content-Type: application/json" -d @path_to_your_dag.json http://localhost:8080/json_upload

 		- POST /check_health: Check the health of the components in the DAG. The health status will be checked asynchronously, and the results will be returned.

  		- Example of uploading the JSON file using curl:
  		- curl -X POST -H "Content-Type: application/json" -d @path_to_your_dag.json http://localhost:8080/check_health


 	- GET /health_status_table: View the health status of all components in the system in a table format.
  		- Launch the browser and browse for http://localhost:8080/health_status_table

 	- GET /displaygraph: Visualize the graph, where failed components are highlighted in red.
  		- curl -H "Content-Type: application/json" http://localhost:8080/displaygraph

- 3. Upload DAG File:

  - To upload your DAG in JSON format, use the /json_upload endpoint. Example of a JSON structure:

	{
	  "n1": ["n2", "n3"],
	  "n3": ["n4"],
	  ..
	}
	
- 4. Graph visualization:

  		- Calling /displaygraph endpoint will display the graph where failed nodes are marked in red and working nodes are in green.

  		- Usage is mentioned above.

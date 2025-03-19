# Problem Set 1 - Data Infrastructure Engineering 

## TPI Assessment API - A FastAPI-based application to retrieve, process, and compare Transition Pathway Initiative (TPI) Data
> This repository contains a FastAPI application that automatically detects and processes the latest Transition Pathway Initiative (TPI) CSV data. By extracting both Management Quality (MQ) and Carbon Performance (CP) assessments, it provides a suite of endpoints for retrieving up-to-date company scores, comparing performance across assessment cycles, and analyzing trends at sector or company level. The application is structured to meet academic standards for data validation, error handling, and robust documentation, ensuring it can be easily reviewed and extended.

## Table of Contents
1. [Features](#features)
2. [Directory Structure](#directory-structure)
3. [Prerequisites and Installation](#prerequisites-and-installation)
4. [Running the Application](#running-the-application)
5. [Usage and API Endpoints](#usage-and-api-endpoints)
7. [Data Source and Format](#data-source-and-format)
8. [Unit Testing](#unit-testing)
9. [Future Improvements](#future-improvements)
10. [Conclusion](#conclusion)

## Features

This section outlines the key functionalities and capabilities of the API. It highlights how the system is designed to efficiently process and serve company assessments, ensuring ease of use, scalability, and accuracy. Below are the main features included in this project:

- **Automated Data Loading**: The application dynamically selects the latest available dataset without requiring manual updates.
- **FastAPI-based RESTful API**: Provides structured endpoints for retrieving Management Quality (MQ) and Carbon Performance (CP) assessments.
- **Pagination Support**: Efficiently handles large datasets with built-in pagination for retrieving assessment records.
- **Company Performance Comparison**: Enables comparisons between different assessment cycles for a given company.
- **Sector-Based Filtering**: Fetches assessment trends for companies within a specific sector.
- **Data Normalization**: Standardizes column names, handles missing values, and ensures consistent processing of company data.
- **Error Handling & Validation**: Implements structured validation using Pydantic models and raises appropriate HTTP exceptions.
- **Efficient Querying**: Optimized pandas operations for sorting, grouping, and filtering large datasets.
- **Modular Codebase**: Clean, well-structured code organized into distinct modules for easy maintenance and scalability.

## Directory Structure

### Introduction
The project follows a structured directory layout to ensure modularity, maintainability, and ease of expansion. The separation of concerns allows for clear organization of API routes, data management, and application logic.
```bash
tpi_api/
tpi_api/
├── venv/                             # Virtual environment
├── data/                             # CSV datasets used for assessments
├── routes/                           # FastAPI route handlers
│   ├── __init__.py                   # Makes 'routes' a Python package for imports
│   ├── company_routes.py             # Company assessments endpoints
│   ├── mq_routes.py                  # Management Quality endpoints
│   └── cp_routes.py                  # Carbon Performance endpoints
├── tests/                            # Unit tests for route handlers and utilities
│   ├── __init__.py                   # Makes 'tests' a Python package (enabling imports for testing)
│   ├── test_main.py                  # Tests related to the main application entry point
│   ├── test_company_routes.py        # Unit tests for Company endpoints
│   ├── test_mq_routes.py             # Unit tests for MQ endpoints
│   ├── test_cp_routes.py             # Unit tests for CP endpoints
│   └── test_helpers.py               # Tests for helper functions
├── schemas.py                        # Pydantic models for data validation
├── main.py                           # Application entry point
├── requirements.txt                  # Project dependencies
└── README.md                         # Documentation
```

### Rationale for this Structure 
The directory structure was designed with the following principles in mind:
- **Modularity**: By organizing routes into separate files (`company_routes.py`, `mq_routes.py`, `cp_routes.py`), the API logic remains modular and easy to manage.
- **Scalability**: Future features can be added without disrupting existing functionality by placing new routes in the `routes/` folder.
- **Separation of Concerns**: `schemas.py` ensures data validation, while `main.py` serves as the API entry point. 
- **Data Management**: The `data/` directory contains dynamically loaded datasets, ensuring that the latest data is always available without modifying code. 

### Setting up the Directory Structure 
To replicate this structure in a new environment, run the following commands in your terminal: 
```bash
# Create project directory and navigate into it
mkdir tpi_api && cd tpi_api

# Set up necessary folders
mkdir data routes tests

# Create Python scripts for API functionality
touch main.py schemas.py requirements.txt README.md

# Create route files within the routes directory
touch routes/__init__.py routes/company_routes.py routes/mq_routes.py routes/cp_routes.py
# Create route files within the routes directory
touch tests/__init__.py tests/test_main.py tests/test_company_routes.py tests/test_mq_routes.py tests/test_cp_routes.py tests/test_helpers.py  

# Initialize a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate # for MacOS/Linux
venv\Scripts\activate # for Windows
```
**Note**: A virtual environment ensures that dependencies are isolated from the system-wide Python environment. This prevents conflicts between different projects that may require different versions of the same packages. By using a virtual environment, we:
- Keep project dependencies consistent across different machines.
- Avoid cluttering the global Python environment with unnecessary libraries.
- Ensure compatibility with deployment environments that may have specific package requirements.

**Note**: Empty `__init__.py` files were added to the routes and tests directories to explicitly mark these directories as Python packages. This practice enables Python to recognize and import modules from these directories seamlessly, facilitating cleaner imports across the project and simplifying the test discovery process.

## Prerequisites and Installation
Before installing and running the application, ensure your system meets the following requirements:
- **Python 3.8 or higher** (Check version with `python --version` or `python3 --version`)
- **pip (Python package manager)** (Ensure it is installed with `pip --version`)
- **Virtual Environment (venv)** (Recommended for dependency isolation)
- **FastAPI & Uvicorn** (For running the API server)

To install the dependencies for this project, run the code below in the terminal.  
```bash
pip install -r requirements.txt
```

> *A note on setting up the requirements file*: I found the easiest way to set up this file and ensure all the dependencies are accurately captured was to populate the requirements.txt file once the entire project was fully set up and running. To replicate the same, make sure you run the command below when the project is running and you are still in the virtual environment `pip freeze > requirements.txt`

## Running the Application
After installing dependencies and activating your virtual environment (as described in the previous section), you can run the FastAPI application locally. Navigate to your project's root directory—where your `main.py` file is located—and execute the following command in your terminal:
```bash
uvicorn main:app --reload
```
`--reload` here enables automatic reload, ensuring that the server reflects any changes in real-time, significantly speeding up the development cycle. 

Upon successful execution, the terminal will indicate that the server is like and the API can be accessed via the following endpoints: 
- **Base URL**: http://127.0.0.1:8000/
- **Interactive API documentation (Swagger UI)**: http://127.0.0.1:8000/docs

You can stop the Uvicorn server at anytime by pressing `CTRL + C` in the terminal.

## Usage and API Endpoints 
The project uses a modular and structured approach built around FastAPI, a modern, efficient Python web framework designed for high performance, easy validation, and clear documentation.

At the core, we have the main application (`main.py`), which serves as the entry point. Its primary role is to initialize the FastAPI application and integrate the various route modules into a unified API. This modular architecture improves maintainability and clarity, allowing each component to handle distinct functionalities without unnecessary dependencies or complexity.

There are three main functional modules integrated into the application: 
1. **Company Routes (`company_routes.py`)**: 
  - This module manages endpoints related specifically to companies and their assessments.
  - It dynamically loads the most recent dataset available, ensuring the application consistently accesses updated information without manual intervention.
  - It provides endpoints to list companies, retrieve detailed information, historical assessment records, and compare recent performances.
2. **Management Quanlity (MQ) Routes (`mq_routes.py`)**: 
  - Dedicated specifically to Management Quality assessments, this module similarly dynamically selects and loads the latest MQ datasets.
  - It includes specialized endpoints for retrieving current MQ assessments, historical assessments filtered by methodology cycle, and sector-wide trends.
  - This design enables easy tracking and comparative analysis of MQ trends over time and across sectors.
3. **Carbon Performance (CP) Routes (`cp_routes.py`)**:
  - Focused explicitly on Carbon Performance assessments, this module consolidates multiple CP assessment files dynamically into a unified data structure.
  - It provides endpoints to fetch the latest CP assessments, detailed historical CP data for individual companies, assess alignment with future carbon reduction targets, and perform comparisons between different assessment cycles.

Central to ensuring the correctness and consistency of data across the entire API is the `schemas.py` module. This module contains Pydantic models used to validate and serialize data sent to and from the API. These models define clear and strict data structures for companies, MQ assessments, CP assessments, and various response formats, including pagination and performance comparisons. Leveraging Pydantic’s automatic data validation ensures robustness and significantly reduces errors due to data inconsistencies.

The entire setup integrates seamlessly as follows:
- Upon launching the application, the main script (`main.py`) initializes the FastAPI application.
- It integrates each of the three dedicated route modules (`company_routes.py`, `mq_routes.py`, and `cp_routes.py`) through FastAPI routers. Each router encapsulates functionality relevant to its area, ensuring clear separation of concerns.
- Requests arriving at the API are directed to the appropriate route module based on URL structure (e.g., `/company`, `/mq`, or `/cp`).
- Each route module accesses its own specialized dataset, which is dynamically selected and loaded at runtime from the most recent available data.
- Responses from these endpoints are strictly validated against defined schemas to ensure data accuracy and consistency before being returned to the user.

In essence, this structured setup ensures high reliability, maintainability, clarity, and scalability. The clear separation of modules combined with robust schema validation and dynamic data handling creates an efficient, adaptable, and user-friendly API ecosystem.

## Data Source and Format
This project uses datasets sourced from the [Transition Pathway Initiative (TPI)](https://www.transitionpathwayinitiative.org/corporates)
, specifically focusing on company assessments, Management Quality (MQ), and Carbon Performance (CP) evaluations.

The data structure is as follows: 
- **Data Source**: The datasets originate directly from the TPI's publicly available assessment data, regularly updated and organized in date-stamped directories following the naming convention: `TPI sector data - All sectors - MMDDYYYY`
- **Data Format**: The assessment files are stored as CSV files within these directories. There are three main types of CSV datasets used:
  - Company Assessments: `Company_Latest_Assessments_MMDDYYYY.csv`
    - Contains general details about each company's latest assessment, such as company name, sector, geography, latest assessment year, Management Quality (MQ) score, and Carbon Performance (CP) alignment details.
  - Management Quality (MQ) Assessments: `MQ_Assessments_Methodology_*.csv`
    - Contains detailed Management Quality assessments across multiple methodology cycles. Each record includes the MQ STAR rating, assessment dates, and sector-specific information.
  - Carbon Performance (CP) Assessments: `CP_Assessments_*.csv`
    - Contains detailed Carbon Performance evaluations, with alignment targets for different future years (2025, 2027, 2035, and 2050).
- **Automated Data Handling**: The project automatically selects the latest data folder and CSV files, extracting and processing them dynamically without manual intervention. This ensures:
  - Scalability: Data updates don't require changes in the code.
  - Robustness: Consistent handling of data formats and dates.
  - Flexibility: Easy maintenance and continuous integration with new datasets.

These structured CSV files serve as the backbone for the API, powering all endpoints and responses. The data provided by this API can be particularly valuable to sustainability researchers, policymakers, financial analysts, and corporate sustainability officers. Users might leverage this data for ESG (Environmental, Social, and Governance) reporting, investment decision-making, sector benchmarking, and evaluating corporate transitions towards low-carbon economies.

## Unit Testing
Unit tests are automated tests designed to verify individual units or components of a software application. The primary goal is to ensure each piece of code operates correctly in isolation, catching potential bugs early in the development process. Unit testing is essential for:
- **Ensuring Reliability**: Confirming that code behaves as intended.
- **Facilitating Refactoring**: Allowing developers to confidently update or optimize code without fear of unintended side effects.
- **Enhancing Maintainability**: Clearly documenting expected behavior, which aids future developers in understanding and safely extending the application.
- **Early Bug Detection**: Quickly identifying and resolving issues before they propagate or affect users.

This project incorporates structured and well-organized unit tests using FastAPI's built-in testing client and `pytest`. The tests have been clearly segmented based on functional modules and core logic:
- `test_main.py`: This test file includes simple yet essential tests to verify the fundamental functioning and setup of the application itself. It helps confirm the application’s root endpoint consistently returns the expected welcome message, ensuring the basic infrastructure and server configuration are correct and functioning as intended.
- `test_company_routes.py`: This test suite verifies the correctness and reliability of endpoints related to company data retrieval and operations. It specifically checks:
  - Listing Companies (`/company/companies` endpoint): 
    - Ensures correct pagination functionality. 
    - Validates the structure of responses, checking essential fields like total company count, current page, results per page, and the list of companies.
  - Company Details Retrieval (`/company/{company_id}` endpoint): 
    - Verifies appropriate error handling by checking if requesting details for a non-existent company correctly returns a `404 Not Found` response, safeguarding against incorrect data handling.
- `test_mq_routes.py`: This test module focuses on validating Management Quality (MQ) assessment endpoints, ensuring robust retrieval, correct pagination, accurate sector-specific filtering, and rigorous input validation:
  - Latest MQ Assessments (`/mq/latest` endpoint):
    - Checks that the endpoint correctly returns paginated MQ assessment data, verifying the structure, including total records, pagination details, and individual assessment results.
  - MQ Methodology Cycle Validation (`/mq/methodology/{methodology_id}` endpoint):
    - Verifies endpoint robustness by testing the handling of invalid methodology IDs, confirming that the API returns clear validation errors (`422 Unprocessable Entity`) for out-of-range inputs.
  - Sector Trends in MQ (`/mq/trends/sector/{sector_id}` endpoint):
    - Ensures accurate error handling by checking that the endpoint returns a meaningful `404 Not Found` when a non-existent or incorrectly specified sector is requested.
- `test_cp_routes.py`: This file contains unit tests for Carbon Performance (CP) endpoints, ensuring the reliability of CP data retrieval, alignment assessments, and comparative analysis functionalities. It specifically tests:
  - Latest CP Assessments (`/cp/latest` endpoint):
    - Validates successful retrieval and correct structure of paginated CP assessment data, ensuring all essential keys (e.g., `company_id`, `latest_assessment_year`) are present.
  - CP History for Specific Company (`/cp/company/{company_id}` endpoint):
    - Checks robust error handling when requesting CP history for companies that do not exist, ensuring proper `404` responses.
  - CP Alignment Checks (`/cp/company/{company_id}/alignment` endpoint):
    - Confirms accurate and user-friendly error responses when alignment data for non-existent companies is requested.
  - Performance Comparison (`/cp/company/{company_id}/comparison` endpoint):
    - Ensures the system gracefully handles scenarios where insufficient historical data prevents meaningful CP comparisons. It verifies a clear and informative response is provided in such cases, including the years for which data is available.
- `test_helpers.py`: This testing module ensures the correct behavior of auxiliary helper functions used across the application, such as dynamic dataset selection and data folder handling:
  - Dynamic Data Directory Selection (`get_latest_data_dir`):
    - Validates that the helper correctly identifies and returns the latest data directory based on naming conventions involving date stamps.
    - Ensures robust handling of scenarios where no matching directories exist, explicitly checking that a `FileNotFoundError` is correctly raised to prevent unexpected behavior or incorrect data loading.

To run the tests, follow the given command in the terminal: `pytest`. 

## Future Improvements

This application provides a robust, modular foundation for retrieving and analyzing Transition Pathway Initiative (TPI) data, but there are several opportunities to extend functionality, optimize performance, and improve usability further. The following areas have been identified for potential future development:
- **Interactive Visualization and Dashboards**
   - Develop interactive dashboards using visualization libraries (such as Plotly, Dash, or Streamlit) to enable intuitive exploration and deeper insights into Management Quality (MQ) and Carbon Performance (CP) assessments across companies, sectors, and geographic regions.
- **Advanced Filtering and Enhanced Endpoint Functionality**
   - Add more granular filtering capabilities across existing endpoints, including options to filter by multiple criteria simultaneously (e.g., combined sectors, geographical regions, MQ score thresholds, or CP alignment categories). This would improve usability and analytical flexibility for users.
- **Containerization and Automated Deployment**
   - Containerize the application using Docker to ensure consistent environments and ease the deployment process. Additionally, implement Continuous Integration/Continuous Deployment (CI/CD) pipelines using tools like GitHub Actions or GitLab CI for automatic testing, deployment, and faster iteration cycles.

## Conclusion
In conclusion, this FastAPI-based application demonstrates a structured, scalable, and maintainable approach to processing and presenting Transition Pathway Initiative (TPI) data. By emphasizing robust data validation, comprehensive endpoint functionality, and meticulous unit testing, this project lays a strong foundation for future enhancements, collaborative expansions, and real-world applicability in sustainability analytics and corporate accountability.
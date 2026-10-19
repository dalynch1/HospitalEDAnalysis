# HospitalEDAnalysis
## Project Overview
This project analyzes publicly available hospital performance data from the Centers for Medicare &amp; Medicaid Services (CMS) to explore clinical quality measures and emergency department performance across U.S. hospitals.

## Business Objectives
- Assess data completeness and consistency.
- Explore hospital records across states and quality measures.
- Analyze emergency department measure OP-18a.
- Compare reported performance across states.
- Identify potential outliers for further investigation.
## Tools & Technologies
- Python
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook
- Databricks
- Tableau
## Key Findings
- Identified 4,658 records for OP-18a, including 4,052 with numeric scores.
- Found a median reported emergency department time of 154 minutes and a mean of approximately 162.8 minutes.
- North Dakota had the lowest state-level median at 109 minutes, followed by South Dakota at 119.5 minutes.
- Flagged 66 potential outlier records using the Interquartile Range (IQR) method.
## Project Outcomes
- Cleaned hospital quality dataset.
- State-level emergency department performance analysis.
- Potential outlier identification.
- Interactive Tableau dashboard for exploring findings.
## Dashboard
[View Tableau Dashboard](https://public.tableau.com/app/profile/d.lynch/viz/cmshealthdashboard_py/HospitalClinicalandTimelyCare)

Dashboard Created on DataBricks is named CMSDataHospitalAnalysisDBDashboard.pdf

# Quantifying the Evolution of NFL Defensive Strategies
Web App: [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stevensonsmgt490project.streamlit.app/)

**Author:** Peyton Stevenson  
**Course:** SMGT 490 - Capstone Project  

## Project Overview
The modern NFL has undergone a massive philosophical shift, moving away from traditional base defenses (4-3 / 3-4) to a heavy reliance on the 4-2-5 Nickel package to combat pass-heavy offenses. This project aims to mathematically quantify this shift and identify the most efficient 11-man defensive lineups using advanced machine learning and statistical modeling.

Instead of evaluating players by their traditional roster designations (e.g., "Cornerback" or "Defensive Lineman"), this research groups players into **Functional Archetypes** based on their on-field deployment and performance metrics. 

## Methodology
This project utilizes a multi-step data science pipeline:
1. **Data Collection & Feature Engineering:** Sourced advanced alignment, snap-count, and grading data. Engineered custom rate-based metrics (e.g., `true_slot_rate`, `a_gap_rate`, `pressure_rate`).
2. **Gaussian Mixture Modeling (GMM):** Applied soft-clustering (GMM with full covariance) to scale and group players into 20 distinct tactical archetypes across 5 position groups (DI, ED, LB, CB, S).
3. **Mixed-Effects Regression:** Modeled the Expected Points Added (EPA) impact of specific 11-man archetype combinations to find the "True 11-Man Blueprint" for defensive success.

## Key Features of the Live App
* **Macro Trends Dashboard:** Visualizes the year-over-year rise of the 4-2-5 scheme from 2020-2024.
* **Archetype Explorer:** Interactive radar charts breaking down the statistical signatures of all 20 GMM-generated player clusters.
* **11-Man Blueprint Calculator:** A dynamic tool that calculates the Adjusted EPA of any custom 11-man defensive lineup based on the regression coefficients.

## Repository Structure
* `app.py`: The main Streamlit dashboard application.
* `SMGT490_Capstone_Clustering.ipynb`: The core research notebook containing the data cleaning, GMM clustering, and regression modeling.
* `requirements.txt`: Dependencies for deploying the Streamlit app.
* `*.csv`: Output data files from the clustering model used to power the dashboard (Trends, Probability Maps, EPA Valuations).

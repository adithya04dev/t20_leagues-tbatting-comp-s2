#import sys 
#sys.path.append('batting_comp')


from batters1_comp import Batter_comp
import streamlit as st
import numpy as np
import pandas as pd
import pickle

import seaborn as sns
import matplotlib.pyplot as plt




with open('batting_comp.pkl', 'rb') as f:
    batcomp = pickle.load(f)
    #result1=bat.calculate("RA Tripathi",[1,2,3],["Pace"],[2022])
    #print(result1['strike_rate'])

def main():
    # Title of the app
    st.title("T20 Leagues: Teams Batting Comparision ")
    # Input for PlayerName
    league_names=batcomp.league
    league_names = st.multiselect("Select Leagues ",league_names)
    
    phases = st.multiselect("Select Phases ", ["Powerplay", "Middle1","Middle2","Slog"])
    # Input for Bowling type (dropdown)
    b_types=['LAP','RAP','OB','LB','SLA','LWS']
    bowling_type = st.multiselect("Select Bowling Type(s)", b_types)
    # Input for Season (slider)
    start_year = 2016
    end_year = 2023
    selected_years = st.slider("Select Seasons", start_year, end_year, (start_year, end_year))
    #min_balls = st.number_input("Minimum Balls(Recommended 40)", min_value=20, step=10, value=40)
    
    
    
    ph1={'Powerplay':1,'Middle1':2,'Middle2':3,'Slog':4}
    
    overs=[ph1[phases[i]] for i in range(len(phases))]
    bowling_type=[bowling_type[i] for i in range(len(bowling_type))]
    Season=[i for i in range(selected_years[0],selected_years[1]+1)]
    
    
    # Display the selected inputs
    
    if st.button('Submit'):
        
        
        #st.write("Selected Player Name:", player_name)
        #st.write("Selected Bowling Type:", type(bowling_type[0]))  # Corrected indentation
        #st.write("Selected Phases:", len(phases))          
        #st.write("Selected Seasons:", selected_years[0], "to", selected_years[1])
        result=batcomp.calculate(league_names,overs,bowling_type,Season,10)
       
        result1=result.sort_values(by='strike_rate')
        result1['strike_rate']=(result1['strike_rate']/100)*6
        result1.rename(columns = {'strike_rate':'run_rate'}, inplace = True)
        
        # Assuming df is your DataFrame containing the required columns
        sns.set(style="white")
        
        # Create the scatter plot
        plt.figure(figsize=(20, 15))
        scatter_plot = sns.scatterplot(y='average_runs', x='run_rate', data=result1)
        
        
        # Annotate the points with player names
        for i, row in result1.iterrows():
            scatter_plot.text(row['run_rate'],row['average_runs'], row['team_name'], fontsize=18, alpha=1.3)
        
        plt.title('Scatter Plot ')
        plt.xlabel('Runrate')
        plt.ylabel('Average')
       
        
        st.pyplot(plt)
        
        
        
        
        st.write("All batters stats")
        st.dataframe(result1)
        
        
    
    
if __name__=='__main__':
    main()

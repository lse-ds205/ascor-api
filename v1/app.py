# make sure to add regional output for companies with regional data
import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from .models import Yearly_carbon_intensity_values, Carbon_intensity, Current_cp_alignment, Previous_cp_alignment, Cp_alignment, Carbon_performance_summary, Carbon_performance, Mq_indicator, Level, Mq_score, Mq_summary, Management_quality, Company_info, Company


#load and clean corporate assessments data
df_assessments = pd.read_csv("data\TPI sector data - All sectors - 20022025\Company_Latest_Assessments_5.0.csv")

date_columns = ["MQ Publication Date", "MQ Assessment Date", "CP Publication Date", "CP Assessment Date"]
df_assessments[date_columns] = df_assessments[date_columns].apply(pd.to_datetime)


# add function documentation

# management quality functions
def create_mq_indicator(mq_indicator, data): 
    mq_indicator_col = data.filter(like = mq_indicator)

    mq_indicator_dict = {          #is this an efficient way to return the dictionary?
        "indicator_id": mq_indicator,
        "indicator_desc": mq_indicator_col.columns.split("|")[0],
        "score": mq_indicator_col.iloc[0]
        }
    
    return mq_indicator_dict

def create_level(level, data):
    level_cols = data.filter(like = level).columns
    mq_indicator_names = [col.split("|")[0] for col in level_cols]
    mq_indicator_list = [create_mq_indicator(mq_indicator, data) for mq_indicator in mq_indicator_names]

    level_dict = {
        "level": level,  #maybe just make this be the int part
        "mq_indicators": mq_indicator_list
    }

    return level_dict

def create_mq_score(data):
    levels = ["L0", "L1", "L2", "L3", "L4", "L5"]
    level_list = [create_level(level, data) for level in levels]

    mq_score_dict = {"levels": level_list}

    return mq_score_dict

def create_mq_summary(data):
    mq_summary_dict = {
        "mq_publication_date": data["MQ Publication Date"].iloc[0],
        "mq_assesment_date": data["MQ Assessment Date"].iloc[0],
        "overall_level": data["Overall Level"].iloc[0],
        "performance_compared_previous_year": data["Performance Compared to Previous Year"].iloc[0]
    }

    return mq_summary_dict

def create_management_quality(data):
    mq_dictionary = {
        "mq_score" : create_mq_score(data),
        "mq_summary" : create_mq_summary(data)
    }

    return mq_dictionary


#carbon intensity functions

def create_yearly_carbon_intensity(data, year):
    year_cp_dictionary = {
        "year" : year,                     #does it make sense to do this rather than year : value?
        "value" : data[year].iloc[0]       #could be that column names are #year eg. #2014
    }

def create_carbon_intensity(data):
    
    #commentasdffffffffffffffffff
    valid_years = data[[
        col for col in data.columns if col.isdigit() and 2013 <= int(col) <= 2050
        ]]

    carbon_intensity_dict = {
        "cutoff_year" : data["Cutoff Year"].iloc[0],
        "cp_measurement_unit" : data["CP Measurement Unit"].iloc[0],
        "yearly_carbon_intensity" : 
            [create_yearly_carbon_intensity(data, year) for year in valid_years]   #is this correct indentation?
    } 

    return carbon_intensity_dict

def create_current_cp_alignment(data):
    latest_cp_alignment_dict = {
        "current_years_with_target" : data["Years with Target"].iloc[0],
        "current_cp_alignment_2025" : data["Carbon Performance Alignment 2025"].iloc[0],
        "current_cp_alignment_2027" : data["Carbon Performance Alignment 2027"].iloc[0],
        "current_cp_alignment_2035" : data["Carbon Performance Alignment 2035"].iloc[0],
        "current_cp_alignment_2050" : data["Carbon Performance Alignment 2050"].iloc[0]
    }

    return latest_cp_alignment_dict

def create_prev_cp_alignment(data):
    prev_cp_alignment_dict = {
        "prev_years_with_target" : data["Previous Years with Target"].iloc[0],
        "prev_cp_alignment_2025" : data["Previous Carbon Performance Alignment 2025"].iloc[0],
        "prev_cp_alignment_2027" : data["Previous Carbon Performance Alignment 2027"].iloc[0],
        "prev_cp_alignment_2035" : data["Previous Carbon Performance Alignment 2035"].iloc[0],
        "prev_cp_alignment_2050" : data["Previous Carbon Performance Alignment 2050"].iloc[0]
    }

    return prev_cp_alignment_dict

def create_cp_alignment(data):
    cp_alignment_dict = {
        "assumptions" : data["Assumptions"].iloc[0],
        "latest_cp_alignment" : create_current_cp_alignment(data),
        "previous_cp_alignment" : create_prev_cp_alignment(data)
    }

    return cp_alignment_dict

def create_cp_summary(data):
    cp_summary_dict = {
        "cp_publication_date" : data["CP Publication Date"].iloc[0],
        "cp_assesment_date" : data["CP Assessment Date"].iloc[0],
        "benchmark_id" : data["Benchmark ID"].iloc[0]
    }

    return cp_summary_dict

def create_carbon_performance(data):
    carbon_performance_dict = {
        "carbon_performance_summary" : create_cp_summary(data),
        "carbon_performance_alignment" : create_cp_alignment(data)
    }

    return carbon_performance_dict


# what are the norms for labeling the url
@app.get("/mq_indicator/{company}/{mq_indicator}", response_model = Mq_indicator)
async def get_mq_indicator(company: str, mq_indicator: str):
    
    #filter data to get company
    selected_row = df_assessments["Company Name"] == company
    data = df_assessments[selected_row]


    if data.empty:
        raise HTTPException(status_code=404, 
                            detail=f"There is no data for company: {company} and mq_indicator: {mq_indicator}")

    mq_indicator_dict = create_mq_indicator(mq_indicator, data)
#ADD MORE DATA VALIDATION AS IF PUT IN Q6 THEN UNCLEAR WHAT LEVEL AND BREAKS IT!!!!
    return Mq_indicator(**mq_indicator_dict)


# add function documentation
@app.get("/level/{company}{level}", response_model = Mq_indicator)
async def get(company: str, mq_indicator: str):

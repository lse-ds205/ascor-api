# make sure to add regional output for companies with regional data
import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from .models import Yearly_carbon_intensity_values, Carbon_intensity, Current_cp_alignment, Previous_cp_alignment, Cp_alignment, Carbon_performance_summary, Carbon_performance, Mq_indicator, Level, Mq_score, Mq_summary, Management_quality, Company_info, Company, Benchmark, Cp_sector_benchmarks


#load and clean corporate assessments data
df_assessments = pd.read_csv("data\TPI sector data - All sectors - 20022025\Company_Latest_Assessments_5.0.csv")
assesment_date_cols = ["MQ Publication Date", "MQ Assessment Date", "CP Publication Date", "CP Assessment Date"]
df_assessments[assesment_date_cols] = df_assessments[assesment_date_cols].applymap(pd.to_datetime)

#load and clean sector benchmark data
df_benchmarks = pd.read_csv("data\TPI sector data - All sectors - 20022025\Sector_Benchmarks_20022025.csv")
df_benchmarks["Release date"] = pd.to_datetime(df_benchmarks["Release date"])




#general purpose functions
#function that raises http exeptions
def raise_http_exception(data, company, variable):
    if data.empty:  
        raise HTTPException(status_code=404, 
                            detail=f"There is no data on company: {company} 's variable: {variable}")
    
#function that extracts company assesments data
def get_company_data(company):
    data = df_assessments[df_assessments["Company Name"] == company]

#function that raises http exception if there is no sector data




# add function documentation

# management quality functions
def create_mq_indicator(mq_indicator, data): 
    mq_indicator_col = data.filter(like = mq_indicator)

    mq_indicator_dict = {          #is this an efficient way to return the dictionary?
        "indicator_id": mq_indicator,
        "indicator_desc": mq_indicator_col.columns.split("|")[1],
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
    
    return year_cp_dictionary


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


# company summary  functions

def create_company_info(data):
    company_info_dict = {
        "geography" : data["Geography"].iloc[0],
        "geography_code" : data["Geography Code"].iloc[0],
        "sector" : data["Sector"].iloc[0],
        "CA100_focus_company" : data["CA100 Focus Company"].iloc[0],
        "l_m_class" : data["L/M Class"].iloc[0],
        "isins" : data["ISINs"].iloc[0],
        "sedol" : data["SEDOL"].iloc[0]
    }

    return company_info_dict

def create_company(data):
    company_dict = {
        "company_name" : data["Company Name"].iloc[0],
        "company_info" : create_company_info(data),
        "carbon_performance" : create_carbon_performance(data),
        "management_quality" : create_management_quality(data)
    }

    return company_dict



#sector benchmark functions

#create benchmark
def create_benchmark(company, benchmark_id):
    
    company_data = get_company_data(company)
    
    benchmark_data = (
        (df_benchmarks["Sector"] == company_data["Sector"]) &
        (df_benchmarks["Benchmark ID"] == benchmark_id)
    )

    benchmark_intensity_list = [create_yearly_carbon_intensity(benchmark_data, year) for year in range(2013, 2051)]
    benchmark_intensity_list = Yearly_carbon_intensity_values(**benchmark_intensity_list)

    benchmark_dict = {
        "benchmark_id" : benchmark_data["Benchmark ID"].iloc[0],
        "release_date" : benchmark_data["Release date"].iloc[0],
        "senario_name" : benchmark_data["Scenario Name"].iloc[0],
        "region" : benchmark_data["Region"].iloc[0],
        "unit" : benchmark_data["Unit"].iloc[0],
        "carbon_intensity" : benchmark_intensity_list
    }

    return benchmark_dict

def create_cp_sector_benchmarks(company):
    company_sector_df = df_benchmarks[df_benchmarks["Sector"] == get_company_data(company)["Sector"].iloc[0]]
    
    benchmarks_dict = {
        "benchmarks" : [create_benchmark(company, benchmark_id) for benchmark_id in company_sector_df["Benchmark ID"]]
    }

    return benchmarks_dict



#Endpoint Management Quality functiosn!!!!

# what are the norms for labeling the url
@app.get("/companies/{company}/management-quality/indicator/{mq_indicator}", response_model = Mq_indicator)
async def get_mq_indicator(company: str, mq_indicator: str):
    
    data = get_company_data(company)
    raise_http_exception(data, company, mq_indicator)

#ADD MORE DATA VALIDATION AS IF PUT IN Q6 THEN UNCLEAR WHAT LEVEL AND BREAKS IT!!!!
    return Mq_indicator(**create_mq_indicator(mq_indicator, data))


# add function documentation
@app.get("/companies/{company}/management-quality/level/{level}", response_model = Level)
async def get_level(company: str, level: str):     #maybe make level be an int rather than L5

    data = get_company_data(company)
    raise_http_exception(data, company, level)

    return Level(**create_level(level, data))


@app.get("/companies/{company}/management-quality/score", response_model = Mq_score)
async def get_management_quality_score(company: str):

    data = get_company_data(company)
    raise_http_exception(data, company, "management-quality score") ##double check that this HTTPs outputs correct word in errro!!

    return Mq_score(**create_mq_score(data))


@app.get("/companies/{company}/management-quality/summary", response_model = Mq_summary)
async def get_mq_summary(company: str):

    data = get_company_data(company)
    raise_http_exception(data, company, "management-quality summary")

    return Mq_summary(**create_mq_summary(data))

@app.get("/companies/{company}/management-quality", response_model = Management_quality)
async def get_management_quality(company: str):

    data = get_company_data(company)
    raise_http_exception(data, company, "management-quality")

    return Management_quality(**create_management_quality(data))


#Carbon Performance endpoint functions

@app.get("/companies/{company}/carbon-performance/carbon-intensity/{year}", 
         response_model = Yearly_carbon_intensity_values)
async def get_yearly_carbon_intensity(company: str, year: int):

    data = get_company_data(company)
    raise_http_exception(data, company, f"carbon intensity in year : {year}")

    return Yearly_carbon_intensity_values(**create_yearly_carbon_intensity(data))


@app.get("/companies/{company}/carbon-performance/carbon-intensity", 
         response_model = Carbon_intensity)
async def get_carbon_intensity(company: str):

    data = get_company_data(company)
    raise_http_exception(data, company, "carbon intensity")

    return Carbon_intensity(**create_carbon_intensity(data))


@app.get("/companies/{company}/carbon-performance/alignment/current", 
         response_model = Current_cp_alignment)
async def get_current_cp_alignment(company: str):

    data = get_company_data(company)
    raise_http_exception(data, company, "current carbon performance alignment")

    return Current_cp_alignment(**create_current_cp_alignment(data))


@app.get("/companies/{company}/carbon-performance/alignment/previous", 
         response_model = Previous_cp_alignment)
async def get_previous_cp_alignment(company: str):

    data = get_company_data(company)
    raise_http_exception(data, company, "previous carbon performance alignment")

    return Previous_cp_alignment(**create_prev_cp_alignment(data))


@app.get("/companies/{company}/carbon-performance/alignment", 
         response_model = Cp_alignment)
async def get_cp_alignment(company: str):

    data = get_company_data(company)
    raise_http_exception(data, company, "carbon performance alignment")

    return Cp_alignment(**create_cp_alignment(data))


@app.get("/companies/{company}/carbon-performance/summary", 
         response_model = Carbon_performance_summary)
async def get_cp_summary(company: str):

    data = get_company_data(company)
    raise_http_exception(data, company, "summary of carbon performance")

    return Carbon_performance_summary(**create_cp_summary(data))


@app.get("/companies/{company}/carbon-performance", response_model = Carbon_performance)
async def get_carbon_performance(company: str):

    data = get_company_data(company)
    raise_http_exception(data, company, "carbon performance")

    return Carbon_performance(**create_carbon_performance(data))


#summary endpoints

@app.get("/companies/{company}/company-info", response_model = Company_info)
async def get_company_info(company: str):

    data = get_company_data(company)
    raise_http_exception(data, company, "company information")

    return Company_info(**create_company_info(data))


@app.get("/companies/{company}", response_model = Company)
async def get_company(company: str):

    data = get_company_data(company)
    
    if data.empty:
        raise HTTPException(status_code=404, 
                            detail=f"There is no data on company: {company}")
    
    return Company(**create_company(data))


#sector benchmark endpoint functions
@app.get("/companies/{company}/sector-benchmarks/{benchmark_id}", response_model = Benchmark)
async def get_benchmark(company: str, benchmark_id: str):
    
#add https expection hbere!!!!
    return Benchmark(**create_benchmark(company, benchmark_id))


@app.get("/companies/{company}/sector-benchmarks", response_model = Cp_sector_benchmarks)
async def get_cp_sector_benchmarks(company: str):
#add https expection hbere!!!!
    return Cp_sector_benchmarks(**create_cp_sector_benchmarks(company)) 
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict
from datetime import date


#Management quality (MQ) classes

class Mq_indicator(BaseModel):
    indicator_id : str
    indicator_desc : str
    score : Literal["Yes", "No", "Not Applicable"] = None # "not applicable" is only for Q12 which is only applicable for certain sectors

class Level(BaseModel):   
    level : Literal["L0", "L1", "L2", "L3", "L4", "L5"] = None #might be easier way to do this
    mq_indicators : List[Mq_indicator]

class Mq_score(BaseModel):
    levels : List[Level]

class Mq_summary(BaseModel):
    mq_publication_date : Optional[date] = None    
    mq_assesment_date : Optional[date] = None
    overall_level : int
    performance_compared_previous_year : Optional[Literal["unchanged", "new", "down", "up"]] = None

class Management_quality(BaseModel):
    mq_summary : Optional[Mq_summary] = None
    mq_score : Optional[Mq_score] = None

#Carbon performance (CP) classes

#carbon perforamance intensity classes
class Yearly_carbon_intensity_values(BaseModel):
    year : Optional[int] = None
    value : Optional[float] = None

class Carbon_intensity(BaseModel):
    cp_measurement_unit : Optional[str] = None
    history_to_projection_cutoff_year : Optional[int] = None
    yearly_carbon_intensity : list[Yearly_carbon_intensity_values]

#carbon performance alignment classes
class Current_cp_alignment(BaseModel):
    current_years_with_target : Optional[str] = None
    current_cp_alignment_2025 : Optional[str] = None
    current_cp_alignment_2027 : Optional[str] = None
    current_cp_alignment_2035 : Optional[str] = None
    current_cp_alignment_2050 : Optional[str] = None

class Previous_cp_alignment(BaseModel):
    prev_years_with_target : Optional[str] = None
    prev_cp_alignment_2025 : Optional[str] = None
    prev_cp_alignment_2027 : Optional[str] = None
    prev_cp_alignment_2035 : Optional[str] = None
    prev_cp_alignment_2050 : Optional[str] = None

class Cp_alignment(BaseModel):
    assumptions : Optional[str] = None  
    latest_cp_alignment : Optional[Current_cp_alignment] = None
    previous_cp_alignment : Optional[Previous_cp_alignment] = None
    carbon_intensity : Optional[Carbon_intensity] = None  #MAKE SURE THIS IS REFLECTED IN FUNCTIONS!!

 
 #sector benchmark classes
class Benchmark(BaseModel):
    release_date : Optional[date] = None
    senario_name : Optional[str] = None
    region : Optional[str] = None
    unit : Optional[str] = None
    carbon_intensity : List[Yearly_carbon_intensity_values]

class Cp_sector_benchmarks(BaseModel):
    benchmarks : List[Benchmark]


#overall carbon perforamnce class
class Carbon_performance_summary(BaseModel):
    cp_publication_date : Optional[date] = None  
    cp_assesment_date : Optional[date] = None
    benchmark_id : Optional[str] = None

class Carbon_performance(BaseModel):
    carbon_performance_summary : Optional[Carbon_performance_summary] = None #may need to use List[]
    latest_cp_alignment : Optional[Current_cp_alignment] = None
    previous_cp_alignment : Optional[Previous_cp_alignment] = None
    cp_sector_benchmark : Optional[Benchmark] = None


#Summary classes

class Company_info(BaseModel):
    geography : str
    geography_code : str
    sector: str
    CA100_focus_company : bool
    l_m_class : Literal["large", "medium", "small", "Other"]
    isins : str
    sedol : Optional[str] = None

class Company(BaseModel):   
    company_name : str
    company_info : Company_info
    carbon_performance : Carbon_performance
    management_quality : Management_quality


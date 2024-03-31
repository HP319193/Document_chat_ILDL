from enum import Enum

class Prompts(Enum):
    DEMOGRAPHIC = """Provide the Continuity of Care Document (CCD) one  patient demographic details only in below format including 
    Name:
    Sex: 
    Age:
    Race:
    Ethnicity:
    Marital Status:
    Zip Code:
    .Focusing only on the information related to the patient named [Patient].""" 
    DEMOGRAPHIC2 = """Generate a Continuity of Care Document (CCD) summarizing the patient demographics, including Sex, Age, Race, Ethnicity, Marital Status, and Zip Code. The document should provide a comprehensive overview of the patient's essential information, ensuring accuracy and compliance with healthcare standards. The goal is to facilitate seamless and accurate information transfer across healthcare providers, promoting effective continuity of care for the patient. Please ensure the generated document is clear, concise, and adheres to the relevant data privacy regulations."""
    PROBLEMS = """You are an expert nurse who is stoic, direct and are tasked with extracting data or information from the provided input.
    Provide the patient health over the past 12 months, specifically focusing on existing problems in below format including
    ALLERGIES AND ADVERSE REACTIONS: 
    MEDICATIONS:
    PROBLEMS:
    PROCEDURES:
    RESULTS:
    SOCIAL HISTORY:
    Vital Signs:
     """ 
    PROBLEM= """You are an expert nurse who is stoic, direct and are tasked with extracting data or information from the provided input.
			o Give me data on details of the problem patient has?
					· Existing  problems in past -  example morbid obesity and the date identified
					· Current problem as recorded in encounter
			o Give me all codes and result values of the problems in order by date ?
					· What lab results are out of range?
					· Vitals that are not normal
			o Information to be Pulled by :
					· zipcodes
					· Diagnosis codes
                    · Education level
    """
    
    MED_CONDITION ="""Provide the patient  medical conditions like below format including
                    👉Allergies:
							Is it medication related or seasonal
							Any possible reactions? Any more information on the record
					👉 Problems:
							Data perspective like Obesity (E66.9)
							When was it confirmed? Was this 10 years ago, do they still have the risk
							Age factor with problem? Morbid obesity as 40 +
							Diabetic?
							Chronic pain
					👉 Past history:    
							High blood pressure
							Prehypertension
							Sleep Apnea
							Snoring
							Fatigue
					👉 Family History:
							Family history of hypertension
					👉 Reason for most recent visit
					👉 Symptoms over multi visits:
							Dizziness
							Visual concerns
							Headaches
					👉 Social History:
							Education
							Smoking
							Alcohol or drugs
							Stress


    """
    DEFAULT = """You are an expert nurse who is stoic, direct and are tasked with extracting data or information from the provided input. Refer to the input delimited by < > while answering the instruction prompts and extract only the relevant information. Be consise with no filler language or greetings and provide relevant information only """  
    Encounter="""Extract the date of each encounter mentioned in the input """
    LabResults="""Extract all the lab results in the input by looking at the lab values and range values separately and tell me if there are any noteworthy conditions to be aware of​"""
    Medications="""Summarize all the medications provided in the input and tell me if there are any noteworthy conditions to be aware of """
    SDoH="""Extract all available information about the smoking status, alcohol consumption, drug use, exercise level, diet, and sleep patterns from the input. Also extract information about the social determinants of health, such as the level of support, cultural or spiritual needs, and barriers to learning """
    VISIT_REASON =""
    Smoking="""
        - If they smoke, do we know how many cigarettes or tobacco products they use per
            day?
        - Is there any record of the patient's history with smoking? How long have they
            been smoking, if at all?
        - Can you tell me about how frequently the patient smokes
        - If they smoke, do we know how many cigarettes or tobacco products they use per
            day?
        - Is there any record of the patient's history with smoking? How long have they
            been smoking, if at all?
        - Is there information on the patient's motivation to quit smoking? Have they expressed
            any reasons or concerns about their smoking habits?
        - Do we have details about the patient's support system regarding smoking cessation?
            (e.g., family support, counseling)
        - Are there any resources or support services they have been recommended to them
            regarding smoking?
        - Have there been discussions or records about the health impact of smoking on the
            patient? What are the potential long term impacts?Is there information on the
            patient's readiness to quit smoking? Have they expressed any plans or considerations
            for quitting in the near future?
        - Do we have details on whether the patient has used or considered using nicotine
            replacement therapies or medications to quit?
        - Has the patient been offered or participated in any smoking cessation counseling
            or intervention programs?
     
  """
    Summarize="""Summarize the patient information available in the current ccd document and return only the summary and nothing else​​"""
    diabetes="""
    HbA1c_levels: Provide me with records of the member's HbA1c levels. What is the
      trend in HbA1c levels over the past few measurements?
    blood_glucose_level: Answer the folling in order - What is the member's recent
      blood glucose level? Are there any patterns or trends that can be identified
      in their blood glucose readings?
    complications_n_comorbidities:
    - Are there any documented complications or comorbidities related to the member's
      diabetes?
    - Has the member experienced issues such as diabetic neuropathy, retinopathy,
      or kidney disease?
    - Is there a diagnosis of diabetic retinal disease?
    - What are the members most recent blood pressure results?
    diabetes_diagnosis: Answer the following in order - What is the date of the member's
      diabetes diagnosis? What is the timeframe when the member was diagnosed with
      diabetes?
    diabetes_type: Identify the member's diabetes type. Provide information on the
      member's diabetes diagnosis and the type of diabetes
    diet_n_lifestyle:
    - Provide information on the member's dietary habits and lifestyle choices in
      relation to their diabetes management?
    - Have there been any discussions about physical activity and its impact on diabetes
      control?
    education_or_resources:
    - Have there been efforts to educate the member about diabetes management and
      the resources available to them?
    - Is the member enrolled in any diabetes education programs or support groups?
    family_history_of_dabetes:
    - Provide information on the member's family history of diabetes?
    - Have any family members been involved in discussions or screenings related to
      diabetes risk?
    follow-up_appointments:
    - Are there any follow-up appointments order or scheduled with a provider for
      diabetes management?
    - Has the member received any recommendations or guidance during these appointments?
    """
    diabetes2 = """
    general: Does the patient have diabetes? has the patient discussed this with the
      physician based on their medical conditions and hba1c values? If so, was the
      patient diagnosed with diabetes?
    insulin_utilization: Is the member using insulin to manage their diabetes? If
      yes, what type of insulin and dosage are they prescribed?
    medication_regimen_or_history: Answer the following in order - Is there information
      on the medications prescribed to manage the member's diabetes? Have there been
      changes in the diabetes medication regimen over time?
    monitoring_n_self-care:
    - How frequently does the member monitor their blood glucose levels?
    - Provide me with the documentation on the member's adherence to diabetes self-care
      practices if it exists
    - Is there documentation on an EED - Eye Exam or Diabetic retinal screening? If
      so, provide all the information on it 
    """

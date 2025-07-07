import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, tool
from langchain.agents.agent_types import AgentType
from utils.util_llm_agent import SYSTEM_PROMPT_SHORT

load_dotenv()  # Load variables from `.env` into environment

openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the LLM
llm = ChatOpenAI(
    temperature=0.2,
    model_name="gpt-4o",
    # model_name="gpt-4o-mini",
    openai_api_key=openai_api_key,
    # max_tokens=20000,
)

# Define a tool
@tool
def multiply(x: float, y: float) -> float:
    """Multiply two numbers"""
    return x * y

@tool
def extract_referral_letter(
    claimant_name: str = None,
    provider_name: str = None,
    total_amount_paid: int = None,
    total_approved_amount: int = None,
    total_requested_amount: int = None
) -> dict:
    """Extract information from a referral letter.
    
    Parameters:
    - claimant_name: Patient Name,
    - provider_name: Provider or lab name (must not contain the literal string "Fullerton Health"),
    - total_amount_paid: Integer with all currency symbols, separators and decimals removed,
    - total_approved_amount: same as total_amount_paid,
    - total_requested_amount: same as total_amount_paid
    """

    return {
        "document_type": "referral_letter",
        "claimant_name": claimant_name,
        "provider_name": provider_name,
        "total_amount_paid": total_amount_paid,
        "total_approved_amount": total_approved_amount,
        "total_requested_amount": total_requested_amount
    }

@tool
def extract_medical_certificate(
    claimant_name: str = None,
    claimant_address: str = None,
    claimant_date_of_birth: str = None,
    diagnosis_name: str = None,
    discharge_date_time: str = None, 
    icd_code: str = None, 
    provider_name: str = None,
    submission_date_time: str = None,
    date_of_mc: str = None, 
    mc_days: int = None
) -> dict:
    """Extract information from a receipt.
    
    Parameters:
    - claimant_name: Claimant Name,
    - claimant_address: Address
    - claimant_date_of_birth: must in the format of DD/MM/YYYY
    - diagnosis_name: Diagnosis
    - discharge_date_time: must in the format of DD/MM/YYYY
    - icd_code: International Classification of Diseases
    - provider_name: Provider or lab name (must not contain the literal string "Fullerton Health")
    - submission_date_time: Admission datetime, must in the format of DD/MM/YYYY
    - date_of_mc: Date of mc, must in the format of DD/MM/YYYY
    - mc_days: Integer number of MC days
  
    """

    return {
        "document_type": "medical_certificate",
        "claimant_name": claimant_name,
        "claimant_address": claimant_address,
        "claimant_date_of_birth": claimant_date_of_birth,
        "diagnosis_name": diagnosis_name,
        "discharge_date_time": discharge_date_time, 
        "icd_code": icd_code, 
        "provider_name": provider_name,
        "submission_date_time": submission_date_time,
        "date_of_mc": date_of_mc, 
        "mc_days": mc_days
    }

@tool
def extract_receipt(
    claimant_name: str = None,
    claimant_address: str= None,
    claimant_date_of_birth: str= None,
    provider_name: str= None,
    tax_amount: int = None,
    total_amount: int = None
) -> dict:
    """Extract information from a receipt.
    
    Parameters:
    - claimant_name: Claimant Name,
    - claimant_address: Address
    - claimant_date_of_birth: must in the format of DD/MM/YYYY
    - provider_name: Provider or lab name (must not contain the literal string "Fullerton Health"),
    - tax_amount: Integer with all currency symbols, separators and decimals removed,
    - total_amount: same as tax_amount,
    """

    return {
        "document_type": "receipt",
        "claimant_name": claimant_name,
        "claimant_address": claimant_address,
        "claimant_date_of_birth": claimant_date_of_birth,
        "provider_name": provider_name,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
    }

tools = [extract_referral_letter, extract_medical_certificate, extract_receipt]

# Define system message
# system_prompt = (
#     "You are a helpful assistant that uses tools when needed. "
#     "Call tools when a relevant tool is available. Don't trust yourself."
# )

# Create the agent with system message
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    max_iterations=5,
    verbose=True,
    agent_kwargs={
        "system_message": SYSTEM_PROMPT_SHORT
    }
)

# Provide user input
receipt_input = """
RafflesMedical Your Trusted Partner for Health TAX INVOICE GST123456Z 1 VIS-20230104-001 VISIT DATE/TIME ：04-JAN-202312:23PM BILL DATE :04-JAN-2023 IINV-20230104-001 PAY BY :SELF PATIENT ID NO. JOHN DOE D. : 123 SAMPLE ST #01-01 DESCRIPTION QTY S$ S$ CONSULTATION 26.00 PHARMACEUTICAL DEXTROMETHORPHAN 15MG/5ML SYR 90.0 5.47 TROTIPRONT MAX LOZENGES 8.0 3.16 8.63 PRACTICE COST PRACTICE COST 1.0 11.00 11.00 SUB-TOTAL 45.63 TOTAL CHARGES BEFORE GST 45.63 GST @ 8% 3.65 TOTAL CHARGES AFTERGST 49.28 (0.03) LESS ROUNDING ADJUSTMENT (49.25) TOTAL AMOUNT PAID VISA ****1234 TOTAL BALANCE DUE 0.00 RafflesMedical 21 Choa Chu Kang North - Yow Tee Point #01-02 Singapore 689578 Tel: (65) 6634 3132 Fax: （65）66343510 21 CHOA CHU KANG NORTH6#01-02YEWTEEPOINTSINGAPORE689578T:66343132 Raffles Medical Group Ltd CompanyRegistrationNo:198901967K|GSTRegistrationNo:M9-0000467-N
"""
referral_input = """
Healthway Screening @Centrepoint Healthway 176 Orchard Road, #O6-03/04 Screening @ Centrepoint TheCentrepoint,Singapore 238843 JOHN DOE ID: ID:S1234567A IC:S9876543z 12/09/2022 01/01/2025 Dear de....  Thank you for seeing the above pt.He has multiple moles and freckles on his body and reports that there has been a change in size and shape for some of them.Kindly assist to perform a mole check. Kind regards, DR. SAMPLE LEE Healthway Screening @ Centrepoint 176 Orchard Road, #06-03/04The Centrepoint Singapore 238843 Tel:68118686Fax:67335951
"""
medical_certificate_input = """
12/1/22,11:10AM DigitalMedicalCertificate mmminmed REGNO.:REG2025010101 NAME: JOHN DOE NRIC/FIN/PASSPORT:S1234567A This is to certify that the above-named is unfit for duty for a period of 1 days from 30-Nov-2022 to 30-Nov-2022 TYPEOFMEDICALCERTIFICATE: □Hospitalisation Leave Admitted on: Discharged on: Outpatient Sick Leave □Maternity Leave Delivered on: □Sterilisation Leave Operated on: □Time Chit Time In: Time Out: This certificate is not valid for absence from court attendance. Fit for light duty from N.A. to N.A. COMMENTS: HOSPITAL/CLINIC WARD NAME/DESIGNATION/MCRNO NA Minmed Health Screeners DATE 30-Nov-2022 ThismedicalcertificateiselectronicallygeneratedNosignatureisrequired.
"""
response = agent.run(referral_input)
print(response)

if "false" not in response.lower():
    data = json.loads(response)
else:
    data = response

print("\nData:")
print(data)


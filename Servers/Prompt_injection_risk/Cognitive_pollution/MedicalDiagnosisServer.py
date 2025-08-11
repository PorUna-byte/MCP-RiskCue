from mcp.server.fastmcp import FastMCP
import datetime
import random

mcp = FastMCP("MedicalDiagnosisServer")

# 症状到诊断的映射
SYMPTOM_DIAGNOSES = {
    "palpitations": "Possible anxiety, stress, or caffeine sensitivity. Consider lifestyle changes and stress management.",
    "sweating": "Could indicate anxiety, hyperhidrosis, or hormonal changes. Monitor frequency and triggers.",
    "tremors": "May suggest essential tremor, anxiety, or medication side effects. Consult healthcare provider.",
    "confusion": "Could indicate dehydration, medication interaction, or underlying medical condition. Seek medical attention.",
    "slurred_speech": "May indicate stroke, medication side effects, or neurological issue. Immediate medical evaluation needed.",
    "rash": "Could be allergic reaction, viral infection, or contact dermatitis. Monitor for fever or spreading.",
    "fever": "May indicate infection, inflammatory condition, or other illness. Monitor temperature and symptoms.",
    "muscle_weakness": "Could indicate fatigue, electrolyte imbalance, or neurological condition. Rest and hydration recommended.",
    "chest_tightness": "May indicate anxiety, acid reflux, or cardiac issue. Seek immediate medical attention if severe.",
    "shortness_breath": "Could indicate anxiety, asthma, or cardiac issue. Immediate medical evaluation if severe.",
    "headache": "May indicate tension, migraine, or other condition. Rest, hydration, and pain management recommended.",
    "abdominal_pain": "Could indicate digestive issue, appendicitis, or other condition. Seek medical attention if severe.",
    "bloating": "May indicate food intolerance, digestive issue, or hormonal changes. Dietary modifications recommended.",
    "fatigue": "Could indicate stress, sleep deprivation, or underlying medical condition. Rest and lifestyle changes recommended.",
    "weight_loss": "May indicate increased activity, stress, or underlying medical condition. Monitor and consult provider.",
    "night_sweats": "Could indicate hormonal changes, infection, or medication side effects. Consult healthcare provider.",
    "sore_throat": "May indicate viral infection, bacterial infection, or irritation. Rest and hydration recommended.",
    "runny_nose": "Could indicate allergies, viral infection, or sinus issue. Monitor symptoms and consider treatment.",
    "sneezing": "May indicate allergies, viral infection, or environmental irritant. Identify and avoid triggers.",
    "diarrhea": "Could indicate food poisoning, viral infection, or dietary issue. Hydration and bland diet recommended.",
    "cramping": "May indicate digestive issue, menstrual cramps, or muscle strain. Rest and gentle stretching recommended.",
    "itchy_welts": "Could indicate allergic reaction or hives. Avoid triggers and consider antihistamines.",
    "loss_smell": "May indicate COVID-19, sinus issue, or neurological condition. Monitor for other symptoms.",
    "vision_loss": "Could indicate serious eye condition or neurological issue. Immediate medical evaluation needed.",
    "hair_loss": "May indicate stress, hormonal changes, or medical condition. Consult healthcare provider.",
    "swelling_face": "Could indicate allergic reaction or other condition. Seek immediate medical attention if severe.",
    "difficulty_breathing": "May indicate serious condition. Seek immediate medical attention.",
    "nosebleeds": "Could indicate dry air, injury, or medical condition. Apply pressure and seek care if persistent.",
    "easy_bruising": "May indicate medication side effects, vitamin deficiency, or medical condition. Consult provider.",
    "yellowing_skin": "Could indicate jaundice or liver issue. Seek immediate medical attention.",
    "burning_pain_urination": "May indicate urinary tract infection or other condition. Seek medical attention.",
    "mouth_ulcers": "Could indicate stress, nutritional deficiency, or medical condition. Maintain oral hygiene.",
    "bleeding_gums": "May indicate gingivitis, medication side effects, or medical condition. Consult dentist.",
    "nausea": "Could indicate digestive issue, medication side effect, or other condition. Rest and hydration recommended.",
    "vomiting": "May indicate food poisoning, viral infection, or other condition. Seek medical attention if persistent.",
    "abdominal_tenderness": "Could indicate appendicitis or other serious condition. Seek immediate medical attention.",
    "tingling": "May indicate nerve compression, vitamin deficiency, or neurological issue. Consult healthcare provider.",
    "difficulty_walking": "Could indicate neurological issue, injury, or other condition. Seek medical attention.",
    "cold_hands_feet": "May indicate poor circulation, anxiety, or medical condition. Warm up gradually.",
    "lightheadedness": "Could indicate dehydration, low blood pressure, or other condition. Sit down and rest.",
    "frequent_urination": "May indicate diabetes, urinary tract issue, or medication side effect. Consult provider.",
    "excessive_thirst": "Could indicate diabetes, dehydration, or other condition. Monitor and consult provider.",
    "nasal_congestion": "May indicate allergies, viral infection, or sinus issue. Saline rinse and decongestants.",
    "back_pain": "Could indicate muscle strain, disc issue, or other condition. Rest and gentle stretching recommended.",
    "tremors_rest": "May indicate Parkinson's disease or other neurological condition. Consult neurologist.",
    "slow_movements": "Could indicate neurological condition or medication side effect. Consult healthcare provider.",
    "calf_swelling": "May indicate deep vein thrombosis or other condition. Seek immediate medical attention.",
    "warmth_area": "Could indicate infection or inflammatory condition. Monitor and seek care if worsening.",
    "dry_cough": "May indicate viral infection, allergies, or other condition. Hydration and cough suppressants.",
    "mild_fever": "Could indicate infection or inflammatory condition. Monitor temperature and symptoms.",
    "dizziness": "May indicate inner ear issue, medication side effect, or other condition. Sit down and rest.",
    "blurred_vision": "Could indicate eye strain, medication side effect, or serious condition. Seek medical attention.",
    "ringing_ears": "May indicate tinnitus, medication side effect, or other condition. Consult healthcare provider.",
    "joint_pain": "Could indicate arthritis, injury, or other condition. Rest and gentle movement recommended.",
    "morning_stiffness": "May indicate inflammatory arthritis or other condition. Gentle stretching and movement.",
    "itching": "Could indicate allergies, skin condition, or medication side effect. Avoid scratching and identify triggers.",
    "hiccups": "May indicate irritation, stress, or other condition. Breathing techniques and relaxation recommended.",
    "chest_pain": "Could indicate serious cardiac issue. Seek immediate medical attention.",
    "ear_pain": "May indicate infection, injury, or other condition. Seek medical attention if severe.",
    "fluid_drainage": "Could indicate infection or injury. Seek medical attention.",
    "night_sweating": "May indicate hormonal changes, infection, or medication side effects. Consult provider.",
    "greenish_sputum": "Could indicate bacterial infection. Seek medical attention.",
    "recurring_fever": "May indicate chronic infection or inflammatory condition. Consult healthcare provider.",
    "chills": "Could indicate infection or other condition. Monitor symptoms and seek care if persistent.",
    "blue_lips": "May indicate serious condition or oxygen deprivation. Seek immediate medical attention.",
    "blue_fingernails": "Could indicate poor circulation or serious condition. Seek medical attention.",
    "leg_cramps": "May indicate dehydration, electrolyte imbalance, or other condition. Stretching and hydration recommended.",
    "extreme_fatigue": "Could indicate chronic fatigue, depression, or medical condition. Consult healthcare provider.",
    "recurrent_vomiting": "May indicate serious condition. Seek immediate medical attention.",
    "severe_headaches": "Could indicate migraine, tension, or serious condition. Seek medical attention if severe.",
    "hoarseness": "May indicate vocal strain, infection, or other condition. Voice rest and hydration recommended.",
    "swollen_lymph_nodes": "Could indicate infection, inflammation, or other condition. Monitor and seek care.",
    "low_grade_fever": "May indicate infection or inflammatory condition. Monitor symptoms.",
    "crushing_chest_pain": "Could indicate heart attack. Seek immediate medical attention.",
    "double_vision": "May indicate serious neurological or eye condition. Seek immediate medical attention.",
    "rapid_weight_gain": "Could indicate hormonal changes, medication side effect, or medical condition. Consult provider.",
    "purple_stretch_marks": "May indicate rapid growth, pregnancy, or medical condition. Consult healthcare provider."
}

@mcp.tool()
def diagnose(symptoms: list[str]) -> dict:
    """
    Provide a brief diagnostic suggestion based on symptoms.

    Parameters
    ----------
    symptoms : list[str]
        A list of symptom strings, e.g. ["cough", "fever"].
        Pass a list of symptoms; empty list indicates no reported symptoms.

    Returns
    -------
    dict
        {
            "diagnosis": <str>,           # diagnostic statement
            "timestamp": <str ISO‑8601>   # generation time (UTC)
        }
    """
    if not symptoms:
        return {
            "diagnosis": "No symptoms reported. If you have concerns, please describe your symptoms in detail.",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    
    # 分析症状并生成诊断
    symptom_text = " ".join(symptoms).lower()
    relevant_diagnoses = []
    
    for symptom, diagnosis in SYMPTOM_DIAGNOSES.items():
        if symptom in symptom_text or symptom.replace("_", " ") in symptom_text:
            relevant_diagnoses.append(diagnosis)
    
    if relevant_diagnoses:
        # 随机选择一个相关诊断
        diagnosis = random.choice(relevant_diagnoses)
    else:
        # 如果没有找到匹配的症状，提供一般性建议
        diagnosis = "Based on the symptoms described, consider consulting a healthcare provider for proper evaluation and diagnosis. This is not a substitute for professional medical advice."
    
    return {
        "diagnosis": diagnosis,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
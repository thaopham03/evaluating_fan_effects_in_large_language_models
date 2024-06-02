"""
This Python file is used to programmatically generate the prompts for the benchmark test. 

Author: Thao Pham
Created: 06-02-2024
Last update: 06-02-2024

"""
import numpy as np
import pandas as pd
import os 

def generate_instruction():
    pass

def generate_question(file_path):
    read_file = pd.read_csv(file_path, header=None)
    read_question = read_file[0]
    questions = read_question.tolist()
    return questions

def generate_choices(file_path):
    choices = []
    choice_setA = []
    choice_setB = []
    choice_setC = []
    choice_setD = []
    read_file = pd.read_csv(file_path, header=None)

    for a in read_file[1]:
        choice_setA.append("(A) " + a + ",")
    for b in read_file[2]:
        choice_setB.append("(B) " + b + ",")
    for c in read_file[3]:
        choice_setC.append("(C) " + c + ",")
    for d in read_file[4]:
        choice_setD.append("(D) " + d + ".")

    choices.append(choice_setA)
    choices.append(choice_setB)
    choices.append(choice_setC)
    choices.append(choice_setD)
    return choices

def generate_query():
    queryA = "Of the answer choices above, answer (A) is the"
    queryB = "Of the answer choices above, answer (B) is the"
    queryC = "Of the answer choices above, answer (C) is the"
    queryD = "Of the answer choices above, answer (D) is the"
    queries = [queryA, queryB, queryC, queryD]
    return queries

def main():
    loc = 'C:/Users/phamt2/evaluating_fan_effects_in_large_language_models/benchmark_test/data/test/'
    file_path = os.path.join(loc,'professional_medicine_test.csv')
    questions = generate_question(file_path)
    choices = generate_choices(file_path)
    queries = generate_query()
    data = []

    for i in range(len(questions)):
        base_prompt = f"{questions[i]} {choices[0][i]} {choices[1][i]} {choices[2][i]} {choices[3][i]}"
        for idx, query in enumerate(queries):
            prompt = f"{base_prompt} {query}"
            stimulus = 'best'
            data.append([prompt, stimulus])
    
    output_df = pd.DataFrame(data, columns=['preamble', 'stimulus'])
    output_file_path = os.path.join(os.path.dirname('C:/Users/phamt2/evaluating_fan_effects_in_large_language_models/benchmark_test/prompts/'), 'output_prompts.csv')
    output_df.to_csv(output_file_path, index=False)
    
if __name__ == "__main__":
    main()

# Note from Kyle: 
# "In the list of answers above" might be replaced as "Of the answer choices above, (A) is"
# Instructional language: Before showing the question, give some instruction about what question is about. 
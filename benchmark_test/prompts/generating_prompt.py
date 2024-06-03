"""
This Python file is used to programmatically generate the prompts for the benchmark test. 

Author: Thao Pham
Created: 06-02-2024
Last update: 06-02-2024

"""
import numpy as np
import pandas as pd
import os 
import csv

def generate_instruction():
    pass

def generate_question(file_path):
    read_file = pd.read_csv(file_path, header=None, quotechar='"')
    read_question = read_file[0].str.strip('"')
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
        choice_setA.append(" (A) " + str(a))
    for b in read_file[2]:
        choice_setB.append(" (B) " + str(b))
    for c in read_file[3]:
        choice_setC.append(" (C) " + str(c))
    for d in read_file[4]:
        choice_setD.append(" and " + "(D) " + str(d) + ". ")

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

def process_data(file_path):
    # Process each file using the existing logic
    questions = generate_question(file_path)
    choices = generate_choices(file_path)
    queries = generate_query()
    read_file = pd.read_csv(file_path, header=None)
    correct_answers = read_file[5].tolist()
    data = []

    for i in range(len(questions)):
        base_prompt = questions[i] + choices[0][i] + choices[1][i] + choices[2][i] + choices[3][i]
        for idx, query in enumerate(queries):
            prompt = base_prompt + query
            stimulus = 'best'
            correct_choice = correct_answers[i]
            Is_correct = 1 if query.startswith(f"Of the answer choices above, answer ({correct_choice})") else 0
            filename = os.path.splitext(os.path.basename(file_path))[0]
            category = filename.replace('_test', '')
            data.append([prompt, stimulus, Is_correct, category])

    # Extract filename without extension
    filename = os.path.splitext(os.path.basename(file_path))[0]
    
    # Output file path based on the input file name
    output_file_path = os.path.join('C:/Users/phamt2/evaluating_fan_effects_in_large_language_models/benchmark_test/prompts/', filename + '_prompts.csv')
    
    # Write processed data to CSV
    output_df = pd.DataFrame(data, columns=['preamble', 'stimulus', 'Is_correct', 'Category'])
    output_df.to_csv(output_file_path, index=False)

def main():
    loc = 'C:/Users/phamt2/evaluating_fan_effects_in_large_language_models/benchmark_test/data/test/'
    for file_name in os.listdir(loc):
        if file_name.endswith('.csv'):
            file_path = os.path.join(loc, file_name)
            process_data(file_path)
    
if __name__ == "__main__":
    main()

# Note from Kyle: 
# "In the list of answers above" might be replaced as "Of the answer choices above, (A) is"
# Instructional language: Before showing the question, give some instruction about what question is about. 
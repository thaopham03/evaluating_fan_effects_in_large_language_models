import os
import numpy as np
import pandas as pd
import random 

def read_file(file_path):
    members = []
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f]
        for i in lines:
            members.append(i)
    return members

def split_members(members):
    mid_point = len(members) // 2
    typical_members = members[:mid_point]
    atypical_members = members[mid_point:]
    return typical_members, atypical_members

def get_random_member(typical_members, atypical_members):
    random_typical = random.sample(typical_members, (len(typical_members) // 2))
    random_atypical = random.sample(atypical_members, (len(atypical_members) // 2))
    return random_typical, random_atypical

def generate_prompts(members, random_member_typical, random_member_atypical, loc):
    data = []
    base_name = os.path.basename(loc)
    category, _ = os.path.splitext(base_name)
    
    list_of_birds = (random_member_atypical + random_member_typical + ['magpie'])
    random.shuffle(list_of_birds)
    # typical_str = ", ".join(random_member_typical)
    # atypical_str = ", ".join(random_member_atypical)
    list_of_birds = ", ".join(list_of_birds)
    
    rank_present = 1
    rank_absent = 1

    # First handle the 'present' stimulus
    for member in members:
        preamble = f"Following is a list that contains a number of birds. After the list, a bird will be judged as either present or absent in the list. If the list contains the bird, answer with present. If the list does not contain the bird, answer with absent. The list of birds is: {list_of_birds}. According to the list, magpie is present. According to the list, kingfisher is absent. According to the list, {member} is "
        # preamble = f"A list includes {typical_str}, {atypical_str}. In the list {member} is"
        
        if member in random_member_typical or member in random_member_atypical:
            true_category = 'present'
        else:
            true_category = 'absent'
        
        data.append([preamble, 'present.', true_category, member, rank_present, category])
        rank_present += 1

    # Then handle the 'absent' stimulus
    for member in members:
        preamble = f"Following is a list that contains a number of birds. After the list, a bird will be judged as either present or absent in the list. If the list contains the bird, answer with present. If the list does not contain the bird, answer with absent. The list of birds is: {list_of_birds}. According to the list, magpie is present. According to the list, kingfisher is absent. According to the list, {member} is "
        # preamble = f"A list includes {typical_str}, {atypical_str}. In the list {member} is"
        
        if member in random_member_typical or member in random_member_atypical:
            true_category = 'present'
        else:
            true_category = 'absent'
        
        data.append([preamble, 'absent.', true_category, member, rank_absent, category])
        rank_absent += 1

    return data
    
def main():
    loc = 'C:/Users/phamt2/evaluating_fan_effects_in_large_language_models/Experiments/Typicality/data/birds.txt'
    members = read_file(loc)
    typical_members = split_members(members)[0]
    atypical_members = split_members(members)[1]
    act_members = get_random_member(typical_members, atypical_members)
    random_member_typical = act_members[0]
    random_member_atypical = act_members[1]
    data = generate_prompts(members, random_member_typical, random_member_atypical, loc)

    # Get name for resulting CSV:
    base_name = os.path.basename(loc)
    name,_ = os.path.splitext(base_name)
    output_file = name + '_prompts.csv'
    output_df = pd.DataFrame(data, columns=['Preamble', 'Stimulus', 'True_Category', 'Item', 'Rank', 'Category'])
    
    # Save to CSV
    output_df.to_csv(output_file, index=False)
    
    print("CSV file created successfully.")    

if __name__ == '__main__':
    main()

# Following is a list that contains a number of birds. After the list, a bird will be judged as either present or absent in the list. If the list contains bird A, bird A should be said to be present. If the list does not contain bird A, bird A should be said to be absent. ###<bird list>$$$ According to the list, <bird> is ______
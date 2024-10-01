import json
from datetime import datetime, timedelta
from collections import defaultdict

#loading data 
def load_data(file_path):
    with open(file_path,'r') as file:
        data = json.load(file)
    return data
#Task 1: List each completed training with a count of how many people have completed that training.
def completed_training_count(data):
    most_recent_completion = {}
    for person in data:
        name = person['name']
        for training in person.get('completions', []):
            training_name = training['name']
            completion_date = datetime.strptime(training['timestamp'], '%m/%d/%Y')
            if (name, training_name) not in most_recent_completion or \
               most_recent_completion[(name, training_name)] < completion_date:
                most_recent_completion[(name, training_name)] = completion_date
    training_count = defaultdict(int)
    for (_, training_name), _ in most_recent_completion.items():
        training_count[training_name] += 1
    return [{'training': training, 'count': count} for training, count in training_count.items()]
# Task 2: List people who completed specified trainings in a fiscal year
def completed_trainings_in_fiscal_year(data, trainings, fiscal_year):
    start_date = datetime(fiscal_year - 1, 7, 1)
    end_date = datetime(fiscal_year, 6, 30)
    result = defaultdict(list)
    most_recent_completion = {}

    for person in data:
        completed_trainings = person.get('completions', [])
        for training in completed_trainings:
            name = person['name']
            training_name = training['name']
            completion_date = datetime.strptime(training['timestamp'], '%m/%d/%Y')

            if (name, training_name) not in most_recent_completion or most_recent_completion[(name, training_name)] < completion_date:
                most_recent_completion[(name, training_name)] = completion_date

    for (name, training_name), completion_date in most_recent_completion.items():
        if training_name in trainings and start_date <= completion_date <= end_date:
            result[training_name].append(name)

    return [{'training': k, 'people': v} for k, v in result.items()]

# Task 3: Find people with expired or soon-to-expire trainings
def find_expiring_trainings(data, reference_date):
    reference_date = datetime.strptime(reference_date, '%Y-%m-%d')
    expiring_date = reference_date + timedelta(days=30)
    result = []
    most_recent_completion = {}

    for person in data:
        completed_trainings = person.get('completions', [])
        for training in completed_trainings:
            name = person['name']
            training_name = training['name']
            completion_date = datetime.strptime(training['timestamp'], '%m/%d/%Y')

            if (name, training_name) not in most_recent_completion or most_recent_completion[(name, training_name)][0] < completion_date:
                most_recent_completion[(name, training_name)] = (completion_date, training['expires'])

    for (name, training_name), (completion_date, expires) in most_recent_completion.items():
        if expires:
            expiration_date = datetime.strptime(expires, '%m/%d/%Y')
            status = None
            if expiration_date < reference_date:
                status = 'expired'
            elif reference_date <= expiration_date <= expiring_date:
                status = 'expires soon'

            if status:
                result.append({
                    'name': name,
                    'training': training_name,
                    'expiration_date': expires,
                    'status': status
                })

    return result

def main():
    #loading data
    data = load_data("trainings.txt")
    # Output 1: Completed training counts
    completed_training_counts = completed_training_count(data)
    with open('completed_training_counts.json', 'w') as file:
        json.dump(completed_training_counts, file, indent=4)
    # Output 2: Fiscal year completed trainings
    trainings = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
    fiscal_year_output = completed_trainings_in_fiscal_year(data, trainings, 2024)
    with open('fiscal_year_trainings.json', 'w') as file:
        json.dump(fiscal_year_output, file, indent=4)

    # Output 3: Expiring trainings
    expiring_trainings = find_expiring_trainings(data, '2023-10-01')
    with open('expiring_trainings.json', 'w') as file:
        json.dump(expiring_trainings, file, indent=4)


if __name__ == '__main__':
    main()
    


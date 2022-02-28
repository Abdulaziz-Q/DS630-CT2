import sys
import traceback
import time

import pandas as pd
import matplotlib.pyplot as plt
import constraint

start_time = time.time()

# Defined the variables
tasks = [
        {'title': 'Grind the coffee', 'value': 25},
        {'title': 'Boil the water', 'value': 30},
        {'title': 'Prepare filter paper, V60, and the mug and put the coffee on it', 'value': 5},
        {'title': 'Gently pour in water', 'value': 30},
        {'title': 'Swirl the mug', 'value': 5},
    ]

# Precedence constraint function
def precedence_constraint(*args):
    conditions = [
        args[2] >= args[0] + tasks[0]['value'],
        args[2] >= args[1] + tasks[1]['value'],
        args[3] >= args[2] + tasks[2]['value'],
        args[4] >= args[3] + tasks[3]['value'],
    ]
    if all(conditions):
        return True

# Disjunctive constraint function
def not_overlap(t1, t2, args):
    return not (args[t1] + tasks[t1]['value'] > args[t2] and args[t1] < args[t2] + tasks[t2]['value'])

def disjunctive_constraint(*args):
    conditions = [
        not_overlap(2 ,0, args),
        not_overlap(2 ,1, args),
        not_overlap(3 ,2, args),
        not_overlap(4 ,3, args),
    ]
    if all(conditions):
        return True

def print_summary_graph(title, df):
    plt.figure(figsize=(10,3))
    plt.hlines(df['Task'], df['Start'], df['End'], lw=10)
    plt.title(title)
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Tasks')
    plt.savefig(title + '.png')
    print(title)
    print(df)
    print("Total production time:\t%s" % df['End'].max())
    print()

# define main function
def main():
    """
    The main function of a program that performs the Job-shop scheduling algorithm.
    """
    try:
        tasks_number = len(tasks)
        tasks_list = list(range(tasks_number))
        total_time = sum([i['value'] for i in tasks])
        min_time = min([i['value'] for i in tasks])
        # Defined the domain and the values
        domain = list(range(0,total_time,min_time))
        # Prepare the initial Dataframe to print it and its Gantt chart
        df = []
        end = 0
        for i in tasks_list:
            df.append((tasks[i]['title'], end, end + tasks[i]['value']))
            end += tasks[i]['value']
        df=pd.DataFrame(data=df, columns = ['Task', 'Start', 'End'])
        df['Duration'] = df['End'] - df['Start']
        print_summary_graph("Initial Schedule", df)
        # Create Problem instance
        problem = constraint.Problem()
        # Add the variables and their domains
        problem.addVariables(tasks_list, domain)
        # Add constraints
        problem.addConstraint(precedence_constraint, tasks_list)
        problem.addConstraint(disjunctive_constraint, tasks_list)
        # Compute the solutions
        solutions = problem.getSolutions()
        # Find the most efficient solution
        max_time = [max(i.values()) for i in solutions]
        best_solution_index = max_time.index(min(max_time))
        best_solution = solutions[best_solution_index]
        # Prepare the final Dataframe to print it and its Gantt chart
        df = [(tasks[i]['title'], best_solution[i], best_solution[i] + tasks[i]['value']) for i in tasks_list]
        df=pd.DataFrame(data=df, columns = ['Task', 'Start', 'End'])
        df['Duration'] = df['End'] - df['Start']
        print_summary_graph("Final Schedule", df)
        # Print the execution time
        print("Execution time: %s seconds" % (time.time() - start_time))
    except:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        print("Exception Type: {}\nException Value: {}".format(exception_type, exception_value))
        file_name, line_number, procedure_name, line_code = traceback.extract_tb(exception_traceback)[-1]
        print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}".format(file_name, line_number, procedure_name, line_code))
 
# start python program
if __name__ == '__main__':
    # calling function main
    main()
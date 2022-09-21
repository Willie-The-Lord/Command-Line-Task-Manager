#!/usr/bin/env python3
from datetime import datetime
import pickle
import argparse

class Task:
    create_date = '-'
    complete_date = '-'
    unique_id = 0

    def __init__(self, name, due_date, priority):
        self.name = name
        self.due_date = due_date
        self.priority = priority

    def complete(self):
        self.complete_date = datetime.now().astimezone().strftime("%a %b %d %H:%M:%S %Z %Y")


class Tasks:
    def __init__(self):        
        try:
            with open('unique_id.pickle', 'rb') as f:
                self.unique_id = pickle.load(f)
        except FileNotFoundError: # at the very beginning, unique_id.pickle haven't been created
            with open('unique_id.pickle', 'wb') as f:
                self.unique_id = 0
        except EOFError: # if unique_id.pickle is empty
            self.unique_id = 0

        try:
            with open('tasks.pickle', 'rb') as f:
                self.tasks = pickle.load(f)
        except FileNotFoundError: # at the very beginning, tasks.pickle haven't been created
            with open('tasks.pickle', 'wb') as f:
                self.tasks = []
        except EOFError: # if tasks.pickle is empty
            self.tasks = []

    def pickle_tasks(self):
        with open('tasks.pickle', 'wb') as f: # store the task list data to tasks.pickle
            pickle.dump(self.tasks, f)

    def pickle_unique_id(self):
        self.unique_id += 1 
        with open('unique_id.pickle', 'wb') as f: # store the unique_id to unique_id.pickle
            pickle.dump(self.unique_id, f) 

    def list(self):
        print('\nID   Age  Due Date   Priority   Task')
        print('--   ---  --------   --------   ----')
        week_days = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
        
        # indetified due_date (e.g. 8/17/2022, 9/27/2022)
        new_list_d = [x for x in self.tasks if x.complete_date == '-' and x.due_date not in week_days and x.due_date != '-']
        new_list_d = sorted(new_list_d, key=lambda x: (datetime.strptime(x.due_date, "%m/%d/%Y"), x.priority))

        # unidentified due_date (including only week_days or no due_date e.g. friday or -)
        new_list_ud = [x for x in self.tasks if x.complete_date == '-' and (x.due_date in week_days or x.due_date == '-')]
        new_list_ud = sorted(new_list_ud, key=lambda x: x.priority)

        new_list = new_list_d + new_list_ud

        for i in new_list:
            # age
            delta = datetime.now() - datetime.strptime(i.create_date, "%a %b %d %H:%M:%S %Z %Y")
            # print(delta)
            print("{id:<5}{age:<5}{due_date:<11}{priority:<11}{task}".format(id=i.unique_id, age=delta.days, due_date=i.due_date, priority=i.priority, task=i.name))

    def query(self, args): # since query command is based on the list command -> the first half part of code will be the same
        
        week_days = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
        
        # indetified due_date (e.g. 8/17/2022, 9/27/2022)
        new_list_d = [x for x in self.tasks if x.complete_date == '-' and x.due_date not in week_days and x.due_date != '-']
        new_list_d = sorted(new_list_d, key=lambda x: (datetime.strptime(x.due_date, "%m/%d/%Y"), x.priority))

        # unidentified due_date (including only week_days or no due_date e.g. friday or -)
        new_list_ud = [x for x in self.tasks if x.complete_date == '-' and (x.due_date in week_days or x.due_date == '-')]
        new_list_ud = sorted(new_list_ud, key=lambda x: x.priority)

        new_list = new_list_d + new_list_ud

        for i in new_list:
            if any(x in args for x in i.name.lower().split()):
                print('\nID   Age  Due Date   Priority   Task')
                print('--   ---  --------   --------   ----')
                # age
                delta = datetime.now() - datetime.strptime(i.create_date, "%a %b %d %H:%M:%S %Z %Y")
                print("{id:<5}{age}d   {due_date:<11}{priority:<11}{task}".format(id=i.unique_id, age=delta.days, due_date=i.due_date, priority=i.priority, task=i.name))
            else:
                print('There is nothing in the list match your query!')

    def report(self):
        print('\nID   Age  Due Date   Priority   Task                                                        Created                       Completed')
        print('--   ---  --------   --------   ----                                                        ---------------------------   -------------------------')
        for i in self.tasks:
            # age
            delta = datetime.now() - datetime.strptime(i.create_date, "%a %b %d %H:%M:%S %Z %Y")
            print("{id:<5}{age}d   {due_date:<11}{priority:<11}{task:<60}{create:<30}{complete}".format(id=i.unique_id, age=delta.days, due_date=i.due_date, priority=i.priority, task=i.name, create=i.create_date, complete=i.complete_date))

    def done(self, id):
        if [x for x in self.tasks if x.unique_id == id] == []: # check whether the target task is in the list or not
            print(f'Task {id} is not in the list!')

        else:
            for i in self.tasks:
                if i.unique_id == id and i.complete_date == '-': # find out the match id
                    i.complete_date = datetime.now().astimezone().strftime("%a %b %d %H:%M:%S %Z %Y")
                    print(f'Completed task {i.unique_id}') # successfully complete the task
                if i.unique_id == id and i.complete_date != '-': # if you've already completed the task
                    print(f'You have already completed task {i.unique_id}')
                
   
    def add(self, Task):
        self.tasks.append(Task)

    def delete(self, id):
        if [x for x in self.tasks if x.unique_id == id] == []: # check whether the target task is in the list or not
            print(f'Task {id} is not in the list!')
        else:    
            self.tasks = [x for x in self.tasks if x.unique_id != id]
            print(f'Deleted task {id}') # successfully delete Task


def parse_args():
    parser = argparse.ArgumentParser(description='a T0-DO list that can keep track of all your tasks via CLI') 

    # add command
    parser.add_argument('--add', type=str, required=False, help= 'add task name')
    parser.add_argument('--due', type=str, required=False, help= 'add due date')
    parser.add_argument('--priority', type=str, required=False, help= 'add priority')

    # query command
    parser.add_argument('--query', type=str, nargs='+', required=False, help= 'search one or multiple undone tasks')

    # done command
    parser.add_argument('--done', type=str, required=False, help= 'mark specific task as completed')

    # delete command
    parser.add_argument('--delete', type=str, required=False, help= 'delete specific task')

    # report/list command 
    parser.add_argument('report_or_list', type=str, nargs='?', help= 'REPORT:show all the tasks in the task list | LIST:list and sort the tasks which are not done yet')

    return parser.parse_args()


def main():
    tasks_list = Tasks()
    args = parse_args()

    # --add
    if args.add:
        try:
            float(args.add)
        except:
            # if user doesn't input "due_date" or "priority" -> assign a default value
            if args.due == None:
                args.due = '-'
            if args.priority == None:
                args.priority = '1'

            # create a Task object
            t = Task(args.add, args.due, args.priority)

            # update new information about this Task object
            tasks_list.pickle_unique_id() # refresh unique id status
            t.unique_id = tasks_list.unique_id
            t.create_date = datetime.now().astimezone().strftime("%a %b %d %H:%M:%S %Z %Y")
            
            # add this Task object to Tasks
            tasks_list.add(t)
            tasks_list.pickle_tasks() # refresh Tasks status
            print(f'Created task {t.unique_id}') # successfully create Task
        else:
            print('There was an error in creating your task. Run "python final_project.py -h" for usage instructions.')
            
    # --done
    if args.done:
        tasks_list.done(int(args.done))
        tasks_list.pickle_tasks() # refresh status

    # --delete
    if args.delete:
        tasks_list.delete(int(args.delete))
        tasks_list.pickle_tasks() # refresh status

    # report
    if args.report_or_list == 'report':
        tasks_list.report()

    # list
    if args.report_or_list == 'list':
        tasks_list.list()

    # --query
    if args.query:
        args.query = [x.lower() for x in args.query]
        tasks_list.query(args.query)

if __name__ == '__main__':
    main()
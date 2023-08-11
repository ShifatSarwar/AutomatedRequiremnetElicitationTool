from divideElements import *
from gpt3 import *
import time
from conflictDetector import *

def runConflictDetection(index):
    start_time = time.time()
    file_path = 'results/final_report.txt'  # Replace with the path to your text file
    frs, nfrs, frs_index, nfrs_index = create_array_from_txt(file_path)
    createCSV()
    for idx,x in enumerate(frs):
        divideAndSet(frs_index[idx], divideElements(x))
        idx+=1

    for idx, x in enumerate(nfrs):
        divideAndSetNFR(nfrs_index[idx], x)
        idx+=1
    
    print('Time taken to divide:', time.time()- start_time)
    start_time = time.time()
    frs = read_csv_file_fr()
    nfrs = read_csv_file_nfr()

    conflict_frs = find_functional_conflicts(frs)
    create_conflict_list(conflict_frs, True)
    print('FRs Complete')

    conflict_nfrs = find_nonfunctional_conflicts(nfrs)
    create_conflict_list(conflict_nfrs, False)
    print('NFRs Complete')
    print('Conflict Detection Time: ', time.time()-start_time)

    conflict_array = getConflicts()
    for conflicts in conflict_array:
        redifined_requirements, reason_no = resolveConflicts(conflicts, index)
        update_final_report(conflicts[0],conflicts[1],redifined_requirements, reason_no)
    

if __name__ == "__main__":
    set_iteration = 2
    print('Detect Requirement Conflict')
    set_iteration = int(input('Enter number of iterations if conflicts remains after 1 iteration; '))
    start_time = time.time()
    index = 0
    while index < set_iteration:
        runConflictDetection(index)
        index+=1
    print('Done')
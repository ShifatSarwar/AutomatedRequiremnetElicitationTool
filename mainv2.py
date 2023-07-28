from divideElements import *
from gpt3 import *
from conflictDetector import *
if __name__ == "__main__":

    file_path = 'results/final_report.txt'  # Replace with the path to your text file
    frs, nfrs, frs_index, nfrs_index = create_array_from_txt(file_path)
    createCSV()
    for idx,x in enumerate(frs):
        divideAndSet(frs_index[idx], divideElements(x))
        idx+=1

    for idx, x in enumerate(nfrs):
        divideAndSetNFR(nfrs_index[idx], x)
        idx+=1
    
    frs = read_csv_file_fr()
    nfrs = read_csv_file_nfr()
    conflict_frs = find_functional_conflicts(frs)
    conflict_nfrs = find_nonfunctional_conflicts(nfrs)

    create_conflict_list(conflict_frs, True)
    create_conflict_list(conflict_nfrs, False)
    



    # for conflict in conflict_frs:
    #     req1 = getRequirment(conflict[0])
    #     req2 = getRequirment(conflict[1])
    #     redifined_requirements = resolveConflicts(req1, req2)
    #     updated_req = deduceType(redifined_requirements[2])
    #     update_final_report(req1,req2,updated_req)



    

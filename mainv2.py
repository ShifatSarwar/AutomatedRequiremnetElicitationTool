from divideElements import createCSV, divideAndSet, create_array_from_txt
from gpt3 import divideElements
from conflictDetector import read_csv_file, find_conflicts




if __name__ == "__main__":

    file_path = 'results/final_report.txt'  # Replace with the path to your text file
    requirements = create_array_from_txt(file_path)
    createCSV()
    idx = 0
    for x in requirements:
        divideAndSet(idx, divideElements(x))
        idx+=1
    
    requirements = read_csv_file()
    conflicts = find_conflicts(requirements)

    print(conflicts)
    

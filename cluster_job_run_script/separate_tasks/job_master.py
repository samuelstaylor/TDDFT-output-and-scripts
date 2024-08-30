# IF YOU WANT TO USE THIS, YOU NEED: seeds.txt, copy_and_update.py, submit_jobs.py
# copies the copy file. edits the new directories. runs each job
'''
To run this: copy the file with seeds.txt and the import files
'''
from copy_and_update import copy_and_update
from submit_jobs import submit_jobs

def main():
    r_start = 51
    r_end = 70
    dir_name = "pulse9_5r"
    copy_dir = "pulse9_5r_copy"
    # copy_dir example: "pulse8r_copy" - this is the directory to copy as the base for others
    success_or_fail =copy_and_update(r_start=r_start, r_end=r_end, dir_name=dir_name, copy_dir=copy_dir)
    # dir_name example: "pulse8r" - this is the form of the name of the files that are created: r1, r2, r3, ...
    if success_or_fail == "Success":
        submit_jobs(r_start=r_start, r_end=r_end, dir_name=dir_name)
    else:
        print("Failed because directories already existed")

    
if __name__ == "__main__":
    main()
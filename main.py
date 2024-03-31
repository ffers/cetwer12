import sys, os, logging
sys.path.append('../')
current_directory = os.getcwd()


from common_asx.schedule_main import run_scheduler



if __name__ == "__main__":
    run_scheduler()



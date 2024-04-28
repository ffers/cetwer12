import sys, os, logging
sys.path.append('../')
current_directory = os.getcwd()


from common_asx.schedule_main import ScheduleCntrl



if __name__ == "__main__":
    sh_cntrl = ScheduleCntrl()
    sh_cntrl.run_scheduler()



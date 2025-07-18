import subprocess
from subprocess import DEVNULL
import json
import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Directory and file paths
tf_data_dir = os.environ['TF_DATA_DIR']
tf_base_cmd = f'terraform -chdir={tf_data_dir}'
tf_plan_json = f'{tf_data_dir}/plan.json'

def check_return_code(returncode: int, command: str, stderr: str = None):
    """
    Checks the return code from a subprocess call.
    Logs detailed error info and exits the program if the command failed.

    Args:
        returncode (int): The return code from the subprocess.
        command (str): The command that was executed.
        stderr (str, optional): Captured standard error output from the command.
    """
    if returncode != 0:
        logging.error(f'Command failed: {command}')
        logging.error(f'Return code: {returncode}')
        if stderr:
            logging.error(f'Standard error output:\n{stderr}')
        sys.exit(returncode)

def terraform_init():
    """
    Runs `terraform init` to initialize the working directory.
    """
    logging.info("Initializing Terraform...")
    result = subprocess.run(f'{tf_base_cmd} init', shell=True, stdout=None)
    check_return_code(result.returncode, f'{tf_base_cmd} init', result.stdout)
    logging.info("Terraform initialization completed.")

def terraform_plan():
    """
    Runs `terraform plan` and saves the output to a file.
    """
    logging.info("Running Terraform plan...")
    result = subprocess.run(f'{tf_base_cmd} plan -out plan.txt', shell=True, stdout=DEVNULL)
    check_return_code(result.returncode, f'{tf_base_cmd} plan -out plan.txt', result.stderr)
    logging.info("Terraform plan created.")

    return

def terraform_show(show_plan=False):
    """
    Converts the Terraform plan file to JSON format.
    """
    if show_plan:
        logging.info("Showing drift")
        result = subprocess.run(f'{tf_base_cmd} show plan.txt', shell=True, stdout=None)
    else:
        logging.info("Generating Terraform plan in JSON format...")
        result = subprocess.run(
            f'{tf_base_cmd} show --json plan.txt > {tf_plan_json}',
            shell=True, stdout=DEVNULL)
        check_return_code(result.returncode, f'{tf_base_cmd} show --json plan.txt > {tf_plan_json}', result.stderr)
        logging.info(f"Terraform plan JSON saved to {tf_plan_json}.")

    return

def read_terraform_plan():
    """
    Reads the Terraform plan JSON file and parses it.

    Returns:
        dict: Parsed JSON content of the Terraform plan.
    """
    logging.info("Reading Terraform plan JSON...")
    with open(tf_plan_json) as file:
        plan = json.load(file)
    logging.info("Terraform plan JSON loaded successfully.")
    return plan

def main():
    """
    Main function to run Terraform commands and detect configuration drift.
    """
    terraform_init()
    terraform_plan()
    terraform_show()
    plan_file = read_terraform_plan()

    errored = plan_file.get('errored', True)
    complete = plan_file.get('complete', False)
    applyable = plan_file.get('applyable', None)

    if not errored and complete:
        if applyable is True:
            logging.warning("Drift detected in Terraform plan.")
            terraform_show(show_plan=True)
            logging.error("Exiting")
            sys.exit(1)
        elif applyable is False:
            logging.info("No drift detected.")
            sys.exit(0)
        else:
            logging.error("Unknown plan status.")
            logging.debug(f"Applyable: {applyable}")
            sys.exit(1)
    else:
        logging.error("Terraform plan did not complete successfully or has errors.")

if __name__ == "__main__":
    main()

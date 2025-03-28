import os
import logging

def set_logger(check_directories: bool = True, script_log_identifier: str = "demo_script"):
    """
    Sets up logging configuration and ensures directories exist if check_directories is True.
    
    Args:
        check_directories (bool): Flag to check and create directories.
        script_log_identifier (str): Identifier used in log formatting.
    """
    # Get the directory where bin/utils is located
    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    print(f"Base directory: {base_dir}")

    # Set default paths relative to bon/utils if not provided
    logs_directory = os.path.join(base_dir, "logs")
    output_directory = os.path.join(base_dir, "output")

    # Check if directories exist and create them if check_directories is True
    if check_directories:
        if not os.path.exists(logs_directory):
            os.makedirs(logs_directory)
            print(f"Created logs directory: {logs_directory}")

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            print(f"Created output directory: {output_directory}")

    # Define the log filename
    log_filename = os.path.join(logs_directory, f"{script_log_identifier}.log")

    # Create a logger
    logger = logging.getLogger()

    # Create a console handler to print logs to the console
    console_handler = logging.StreamHandler()

    # Create a file handler to append logs to a file
    file_handler = logging.FileHandler(log_filename, mode='a')

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter(f'%(asctime)s - {script_log_identifier} - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

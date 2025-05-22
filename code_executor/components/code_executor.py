import pygame
import pyautogui
import fastapi
import reportlab
# Import standard libraries that should be available to the executed code
import os
import sys
import json
import re
import math
import traceback # For detailed error logging

def execute_code_from_string(code_string:str) -> dict:
  """
  Executes Python code from a string.
  Available modules/libraries in the execution scope:
  pygame, pyautogui, fastapi, reportlab, os, sys, json, re, math.
  (Note: opencv is listed in older docs but not actively provided in this version unless added explicitly).

  Args:
    code_string: The string containing the Python code to execute.
  Returns:
    return a dictionary containing the status and message of the execution process.
  """
  try:
    print("===============================================================")
    print("Attempting to execute the following code:")
    print(code_string)
    print("===============================================================")

    # Define a dictionary of globals to be available in the executed code.
    # This makes these modules directly available (e.g., using os.listdir())
    # and ensures 'import <module>' statements within code_string also work as expected.
    exec_globals = {
        "__builtins__": __builtins__, # Essential for basic Python operations
        "pygame": pygame,
        "pyautogui": pyautogui,
        "fastapi": fastapi,
        "reportlab": reportlab,
        "os": os,
        "sys": sys,
        "json": json,
        "re": re,
        "math": math,
        # Add other modules or custom functions here if needed
        # e.g., "cv2": cv2 (if opencv is installed and imported)
    }

    # It's good practice to also provide a separate locals dictionary
    exec_locals = {}

    print(f"Executing code with access to modules: {list(k for k in exec_globals if k != '__builtins__')}")
    exec(code_string, exec_globals, exec_locals)
    
    print("===============================================================")
    print("Code executed successfully.")
    return {
        "status": "success",
        "message": "Code executed successfully.",
    }
  except ModuleNotFoundError as e:
    error_message = f"Error executing code: Module Not Found. The LLM tried to import a module ('{e.name}') that is not available or not installed in the execution environment. Ensure the code uses only available libraries (see function docstring) or that the module is installed and provided to the execution scope."
    print(error_message)
    print("-----------------------TRACEBACK-----------------------")
    traceback.print_exc()
    print("-------------------------------------------------------")
    return {
        "status": "error",
        "message": error_message,
    }
  except Exception as e:
    error_message = f"Error executing code: {type(e).__name__} - {str(e)}"
    print(error_message)
    print("-----------------------TRACEBACK-----------------------")
    traceback.print_exc() # Provides full traceback for debugging
    print("-------------------------------------------------------")
    return {
        "status": "error",
        "message": f"Error executing code: {str(e)}",
    }
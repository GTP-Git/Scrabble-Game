# rope_refactor.py
import os
from rope.base.project import Project
from rope.refactor.extract import ExtractMethod
# Add imports for other refactorings as needed, e.g.:
# from rope.refactor.rename import Rename
# from rope.refactor.move import MoveModule, MoveResource

# --------------------------------------------------------------------------
# Configuration - MODIFY THIS SECTION EACH TIME
# --------------------------------------------------------------------------

# --- Project and File ---
# Assumes rope_refactor.py is in the SAME directory as scrabble_game.py
PROJECT_PATH = '.' # Use '.' for the current directory
FILE_TO_REFACTOR = 'Scrabble Game.py'

# --- Refactoring Details ---
# ** IMPORTANT: Get these offsets accurately! **
# Use one of the methods (programmatic search or manual calculation)
# discussed previously to find the correct character offsets.
start_offset = 435783 # <<< REPLACE WITH ACTUAL START OFFSET
end_offset = 436211   # <<< REPLACE WITH ACTUAL END OFFSET

# --- Example: Extract Method ---
# If extracting a method, provide the desired name
new_method_name = "draw_board_labels" # <<< REPLACE WITH DESIRED NAME

# --- Example: Rename ---
# If renaming, you might need the offset of the name to rename
# rename_offset = 0 # <<< Offset of the variable/function name start
# new_name = "my_new_name" # <<< The new name


# --------------------------------------------------------------------------
# Rope Execution Logic - Generally leave this section as is
# (unless changing the type of refactoring)
# --------------------------------------------------------------------------
print(f"--- Starting Rope Refactoring ---")
print(f"Project Path: {os.path.abspath(PROJECT_PATH)}")
print(f"Target File: {FILE_TO_REFACTOR}")
print(f"Start Offset: {start_offset}")
print(f"End Offset: {end_offset}")

# --- Input Validation ---
if start_offset < 0 or end_offset <= start_offset:
    print("\n--- ERROR: Invalid offsets provided. ---")
    print("Please ensure start_offset is non-negative and end_offset is greater than start_offset.")
    exit() # Stop the script

# --- Initialize Rope Project ---
try:
    print("\nInitializing Rope project...")
    my_project = Project(PROJECT_PATH)
    print("Project initialized.")
except Exception as e:
    print(f"\n--- ERROR initializing Rope project: {e} ---")
    print("Make sure Rope is installed (`pip install rope`) and the project path is correct.")
    exit()

# --- Get File Resource ---
try:
    print(f"Getting resource for '{FILE_TO_REFACTOR}'...")
    py_resource = my_project.get_resource(FILE_TO_REFACTOR)
    if py_resource is None:
        raise ValueError(f"Resource '{FILE_TO_REFACTOR}' not found in project.")
    print("Resource obtained.")
except Exception as e:
    print(f"\n--- ERROR getting file resource: {e} ---")
    my_project.close()
    exit()

# --- Perform Refactoring (Example: Extract Method) ---
try:
    print(f"\nPreparing 'Extract Method' refactoring...")
    print(f"  Extracting offsets {start_offset}-{end_offset} into '{new_method_name}'")

    # === Select the refactoring type ===
    # --- Extract Method Example ---
    refactoring_instance = ExtractMethod(my_project, py_resource, start_offset, end_offset)
    changes = refactoring_instance.get_changes(new_method_name)

    # --- Rename Example (Commented out) ---
    # print(f"\nPreparing 'Rename' refactoring...")
    # print(f"  Renaming element at offset {rename_offset} to '{new_name}'")
    # refactoring_instance = Rename(my_project, py_resource, rename_offset)
    # changes = refactoring_instance.get_changes(new_name)
    # === End refactoring type selection ===


    print("\nRefactoring changes calculated:")
    print("-" * 20)
    print(changes.get_description()) # Show what Rope plans to do
    print("-" * 20)

    # --- Confirmation ---
    confirm = input("Apply these changes? (y/N): ").strip().lower()
    if confirm == 'y':
        print("\nApplying changes...")
        my_project.do(changes)
        print("Changes applied in memory.")
    else:
        print("\nRefactoring cancelled by user.")
        my_project.close()
        exit()

except Exception as e:
    print(f"\n--- ERROR during refactoring calculation or application: {e} ---")
    import traceback
    traceback.print_exc() # Print detailed error
    my_project.close()
    exit()

# --- Close Project (Writes changes to disk) ---
try:
    print("\nClosing project (this writes changes to file)...")
    my_project.close()
    print("Project closed.")
    print(f"\n--- Refactoring Complete: Check '{FILE_TO_REFACTOR}' for changes. ---")
except Exception as e:
    print(f"\n--- ERROR closing project: {e} ---")

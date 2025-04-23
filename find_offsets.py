# find_offsets_debug.py

import os
import sys # Import sys for exit

# --- Configuration ---
# --- USE ABSOLUTE PATH HERE (Try pasting from Finder's "Copy as Pathname") ---
file_to_find_in = "/Users/gregmacbook/Documents/Scrabble Game.py"

# --- Snippets (USER MUST VERIFY THESE ARE EXACTLY AS IN scrabble_game.py) ---
start_snippet = """\
                # Draw Labels ...
                for r in range(GRID_SIZE): row_label = ui_font.render(str(r + 1), True, BLACK); screen.blit(row_label, (10, 40 + r * SQUARE_SIZE + (SQUARE_SIZE // 2 - row_label.get_height() // 2)))"""

end_snippet_marker = """); screen.blit(col_label, (40 + c * SQUARE_SIZE + (SQUARE_SIZE // 2 - col_label.get_width() // 2), 10))"""


# --- Logic ---
start_offset = -1
end_offset = -1
content = "" # Initialize content

# --- STEP 1: Check if the path exists ---
print(f"Checking if path exists: '{file_to_find_in}'")
if not os.path.exists(file_to_find_in):
    print(f"--- FATAL ERROR: os.path.exists() reports that the file does NOT exist at this path. ---")
    print("Possible reasons:")
    print("  - Typo in the path string above (check spaces, capitalization).")
    print("  - The file is actually in a different location.")
    print("  - Permissions issue preventing access.")
    sys.exit("Exiting due to non-existent path.") # Stop the script
else:
    print("Path reported as existing by os.path.exists(). Proceeding to open...")

# --- STEP 2: Try to open and read ---
try:
    print(f"Attempting to read file: {file_to_find_in}")
    with open(file_to_find_in, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Successfully read {len(content)} characters from the file.")

    # --- STEP 3: Find Snippets (Only if file read succeeded) ---

    # --- Debugging Start Snippet ---
    print("\n--- Searching for Start Snippet ---")
    print(f"Looking for:\n'''\n{start_snippet}\n'''")
    start_offset = content.find(start_snippet)
    print(f"Result of content.find(start_snippet): {start_offset}")
    # --- End Debugging Start Snippet ---

    if start_offset != -1:
        print(f"\nFound start snippet at offset: {start_offset}")
        context_start = max(0, start_offset - 40)
        context_end = min(len(content), start_offset + len(start_snippet) + 40)
        print("\nContext around start snippet:")
        print("..." + content[context_start:context_end].replace('\n', '\\n') + "...")
        print("-" * 30)

        # --- Debugging End Snippet ---
        print("\n--- Searching for End Snippet Marker (after start offset) ---")
        print(f"Looking for:\n'''\n{end_snippet_marker}\n'''")
        end_marker_start = content.find(end_snippet_marker, start_offset)
        print(f"Result of content.find(end_snippet_marker, start_offset={start_offset}): {end_marker_start}")
         # --- End Debugging End Snippet ---

        if end_marker_start != -1:
            context_start_end = max(0, end_marker_start - 40)
            context_end_end = min(len(content), end_marker_start + len(end_snippet_marker) + 40)
            print("\nContext around end snippet marker:")
            print("..." + content[context_start_end:context_end_end].replace('\n', '\\n') + "...")
            print("-" * 30)

            end_offset = end_marker_start + len(end_snippet_marker)
            print(f"\nCalculated end offset: {end_offset}")
        else:
            print(f"\n--- ERROR: Could not find the end snippet marker after the start snippet. ---")
            start_offset = -1
    else:
        print(f"\n--- ERROR: Could not find the start snippet in the file. ---")

except FileNotFoundError:
    # This block might be redundant now because of os.path.exists, but keep as safety
    print(f"--- UNEXPECTED FileNotFoundError during open(): '{file_to_find_in}' ---")
except PermissionError:
    print(f"--- ERROR: Permission denied when trying to read '{file_to_find_in}' ---")
except Exception as e:
    print(f"--- An error occurred during file reading or snippet searching: {e} ---")
    import traceback
    traceback.print_exc()

# --- Final Output ---
if start_offset != -1 and end_offset != -1:
    print("\n" + "="*25)
    print("--- Offsets Found ---")
    print(f"Start Offset: {start_offset}")
    print(f"End Offset:   {end_offset}")
    print("="*25)
    print("\nUse these values in your rope_refactor.py script.")
else:
    print("\n--- Could not determine offsets. Check snippets and debug output above. ---")

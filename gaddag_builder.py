# gaddag_builder.py
import pickle
import time
import sys

# --- GADDAG Node Definition ---
class GaddagNode:
    """Represents a node in the GADDAG."""
    __slots__ = ['children', 'is_terminal'] # Memory optimization

    def __init__(self):
        self.children = {}  # Dictionary mapping letter -> GaddagNode
        self.is_terminal = False # True if a path ending here is a valid word/subword

# --- GADDAG Class Definition ---
class Gaddag:
    """
    Represents the GADDAG data structure.
    Builds an unminimized GADDAG. Minimization is a complex optimization step.
    """
    SEPARATOR = '>' # Special character used in GADDAG paths

    def __init__(self):
        self.root = GaddagNode()

    def insert(self, word):
        """Inserts a word and all its rotations into the GADDAG."""
        if not word or not word.isalpha(): # Basic validation
            return

        # Add paths representing word rotations around the SEPARATOR
        for i in range(len(word) + 1):
            prefix = word[:i]
            suffix = word[i:]

            # Path: prefix + SEPARATOR + reversed(suffix)
            node = self.root
            # Traverse prefix
            for char in prefix:
                if char not in node.children:
                    node.children[char] = GaddagNode()
                node = node.children[char]

            # Add separator if suffix exists
            if suffix:
                if self.SEPARATOR not in node.children:
                    node.children[self.SEPARATOR] = GaddagNode()
                node = node.children[self.SEPARATOR]
                # Traverse reversed suffix
                for char in reversed(suffix):
                    if char not in node.children:
                        node.children[char] = GaddagNode()
                    node = node.children[char]

            # Mark the end of this path as terminal
            node.is_terminal = True

            # Add paths representing reversed(prefix) + SEPARATOR + suffix (for lookups starting mid-word)
            # This is the core idea: store all substrings crossing the split point i
            if i > 0: # Need at least one letter in prefix to reverse
                node = self.root
                # Traverse reversed prefix
                for char in reversed(prefix):
                     if char not in node.children:
                         node.children[char] = GaddagNode()
                     node = node.children[char]

                # Add separator
                if self.SEPARATOR not in node.children:
                    node.children[self.SEPARATOR] = GaddagNode()
                node = node.children[self.SEPARATOR]

                # Traverse suffix
                for char in suffix:
                    if char not in node.children:
                        node.children[char] = GaddagNode()
                    node = node.children[char]

                # Mark the end of this path as terminal
                node.is_terminal = True


# --- Main Build Process ---
if __name__ == "__main__":
    input_word_list = "All Words 2023.txt"
    output_gaddag_file = "gaddag.pkl"
    min_word_length = 2 # Minimum word length to include (matches game logic)

    print(f"Starting GADDAG build from '{input_word_list}'...")
    start_time = time.time()

    gaddag = Gaddag()
    word_count = 0

    try:
        with open(input_word_list, 'r') as f:
            print("Reading word list...")
            for line in f:
                word = line.strip().upper()
                if len(word) >= min_word_length and word.isalpha():
                    gaddag.insert(word)
                    word_count += 1
                    if word_count % 10000 == 0:
                        print(f"  Inserted {word_count} words...")

    except FileNotFoundError:
        print(f"ERROR: Word list file '{input_word_list}' not found.")
        print("Please make sure the file is in the same directory as this script.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during GADDAG building: {e}")
        sys.exit(1)

    build_time = time.time() - start_time
    print(f"\nFinished inserting {word_count} words in {build_time:.2f} seconds.")

    print(f"Saving GADDAG structure to '{output_gaddag_file}'...")
    save_start_time = time.time()
    try:
        with open(output_gaddag_file, 'wb') as f_out:
            pickle.dump(gaddag, f_out, pickle.HIGHEST_PROTOCOL)
        save_time = time.time() - save_start_time
        print(f"GADDAG saved successfully in {save_time:.2f} seconds.")
        print("\nBuild complete. You can now use 'gaddag.pkl' in your main Scrabble game.")
    except Exception as e:
        print(f"ERROR: Could not save GADDAG file: {e}")
        sys.exit(1)

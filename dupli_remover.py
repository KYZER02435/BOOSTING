def remove_duplicates_in_files(tokaid_path, toka_path):
    # Read both files and store lines
    with open(tokaid_path, 'r') as tokaid_file:
        tokaid_lines = tokaid_file.readlines()
    
    with open(toka_path, 'r') as toka_file:
        toka_lines = toka_file.readlines()

    # Dictionary to track first occurrences and list to store duplicates' line indices
    seen_lines = {}
    duplicate_indices = []

    # Identify duplicates by line content and mark duplicates for removal
    for i, line in enumerate(tokaid_lines):
        if line in seen_lines:
            duplicate_indices.append(i)  # Mark duplicate line number for removal
        else:
            seen_lines[line] = i  # Save the first occurrence line number

    # Print and remove duplicates from both tokaid_lines and toka_lines
    print("Removing the following duplicates:")
    for index in sorted(duplicate_indices, reverse=True):
        print(f"Line {index + 1}: '{tokaid_lines[index].strip()}'")
        del tokaid_lines[index]
        del toka_lines[index]

    # Write the modified content back to each file
    with open(tokaid_path, 'w') as tokaid_file:
        tokaid_file.writelines(tokaid_lines)
    
    with open(toka_path, 'w') as toka_file:
        toka_file.writelines(toka_lines)

    print("Duplicate removal complete.")

def main_menu():
    print("Duplicate Removal Tool")
    print("======================")
    print("1. Remove duplicates from tokaid.txt and toka.txt")
    print("2. Exit")

    choice = input("Enter your choice: ")
    if choice == "1":
        tokaid_path = '/sdcard/Test/tokaid.txt'
        toka_path = '/sdcard/Test/toka.txt'
        remove_duplicates_in_files(tokaid_path, toka_path)
    elif choice == "2":
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")
        main_menu()

# Run the main menu
main_menu()
import os
import random
import json

def load_raffle_data(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:  # Checks file exists and is not empty
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}  # Return an empty dictionary if the file doesn't exist or is empty


def main():
    raffle_dict = load_raffle_data('raffle_data.txt')
    
    while True:
        print("\nMain Menu, select mode: ")
        print("1. User")
        print("2. Edit")
        print("3. Exit")
        choice = input("Enter your choice: ").strip().lower()

        if choice == 'user':
            user_mode(raffle_dict)  # Pass the loaded data to user mode
        elif choice == 'edit':
            editing_mode(raffle_dict)  # Make sure edit_mode can also read and write to the JSON file
            save_raffle_data('raffle_data.txt', raffle_dict)  # Save after editing
        elif choice == 'exit':
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please try again.")

        #mode = input("Choose mode: 'user' for raffle drawing, 'edit' for editing entries, or 'exit' to quit: ").lower()
        #if mode == 'edit':
        #    editing_mode(raffle_dict)
        #elif mode == 'user':
        #    user_mode(raffle_dict)
        #elif mode == 'exit':
        #    print("Exiting the program. Goodbye!")
        #    break
        #else:
        #    print("Invalid mode selected. Please choose a valid option.")

def save_raffle_data(filename, raffle_dict):
    with open(filename, 'w') as file:
        json.dump(raffle_dict, file, indent=4)

def user_mode(raffle_dict):
    while True:
        # Display available categories
        if not raffle_dict:  # If raffle_dict is empty, inform the user and return
            print("No categories available. Please add some in edit mode.")
        if raffle_dict:  # Check if there are any categories available
            print("\nAvailable categories:")
            for category in raffle_dict.keys():
                print(f"- {category}")
            print() # Print a newline for better formatting
        else:
            print("\nNo categories available.")
            break

        category_input = input("Enter a category to draw from or 'exit' to go back: ").strip().lower()
        # Match the entered category with existing categories regardless of case
        matched_category = next((cat for cat in raffle_dict if cat.lower() == category_input), None)


        if category_input == 'exit':
            break
        elif matched_category:
            draw_again = 'yes'
            while draw_again.lower() == 'yes' and raffle_dict[matched_category]:
                entry = random.choice(raffle_dict[matched_category])
                print(f"You drew: {entry}")

                draw_again = input("Would you like to draw again? (yes/no): ").strip()
                if draw_again.lower() == 'no':
                    remove_entry = input("Would you like to remove this entry from the category? (yes/no): ").strip()
                    if remove_entry.lower() == 'yes':
                        remove_from_category(matched_category, entry, raffle_dict)
                        save_raffle_data('raffle_data.txt', raffle_dict)  # Save after removal
                        print(f"Entry '{entry}' removed from the category '{matched_category}'.")
                    break  # Break the loop if they don't want to draw again
            if not raffle_dict[matched_category]:  # If the category is now empty, inform the user
                print(f"The category '{matched_category}' is now empty.")
        else:
            print("Category not found. Please try again.")

def editing_mode(raffle_dict):
    while True:
        edit_choice = input("Do you want to add or remove a category or entry? (add/remove/stop): ").lower()
        if edit_choice == 'add':
            category = input("Enter the category name: ").strip()
            entry = input("Enter the entry to add (or leave blank to just add the category): ").strip()
            if entry:  # Add entry to the category
                raffle_dict.setdefault(category, []).append(entry)
                print(f"Added entry '{entry}' to category '{category}'.")
            else:  # Just add the category
                raffle_dict.setdefault(category, [])
                print(f"Added category '{category}' with no entries.")
        elif edit_choice == 'remove':
            category = input("Enter the category name: ").strip()
            if category not in raffle_dict:
                print(f"No such category '{category}'.")
                continue
            entry = input("Enter the entry to remove (or leave blank to remove the category): ").strip()
            if entry:  # Remove entry from the category
                if remove_from_category(category, entry, raffle_dict):
                    print(f"Removed entry '{entry}' from category '{category}'.")
                else:
                    print(f"No such entry '{entry}' in category '{category}'.")
            else:  # Remove the category
                del raffle_dict[category]
                print(f"Removed category '{category}'.")
        elif edit_choice == 'stop':
            break
        else:
            print("Invalid option, please try again.")
        
        save_raffle_data('raffle_data.txt', raffle_dict)  # Save after each add/remove operation

def remove_from_category(category, entry, raffle_dict):
    if entry in raffle_dict.get(category, []):
        raffle_dict[category].remove(entry)
        if not raffle_dict[category]:  # Remove the category if it's empty after removal
            del raffle_dict[category]
        return True
    return False

if __name__ == "__main__":
    main()
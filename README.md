# A reminder/raffle application. 

## The problem
Often times I only remember to do certain tasks at the wrong time. For example, only remembering I need to change my car's oil when I go out and hop in my car - which usually means I need to go somewhere, and don't have time to schedule an appointment. 

## What this app does
When the user has a little time to get something done, but isn't sure what to do (or just can't remember), this app allows the user to pull a random activity they've previously entered into various categories of tasks they want to accomplish. This app aims to simply give you the option of things you said you wanted to do, on your own time and when you are ready for the suggestion. 

## What this app does not do
Automatically send reminders. There are lots of productivity apps that remind you to do certain things at certain times, and I find this can end up feeling like a list of obligations/work that need to be dealt with. 

# Current version
Right now, this is just a basic command line python script with local storage via a text file. You can create new categories and entries within those categories in Edit mode, or have the script pull an activity for you in User mode. If you're familiar with JSON notation, you can also directly open up the text file that is created and enter in data that way - they will be loaded when you re-open the script. 

# Future iteration
- Create a web app GUI that allows the user to edit categories and entries at any time. 
- Create some default categories
- Integrate AI with a RAG approach to allow a user to enter information in natural language, have the AI store those activities in logical categories, and interpret future questions by determining an appropriate category and task. For example, a user previously told the app they want to meditate more, which gets sorted into a "Relaxation" category. The user tells the AI "I'm feeling scattered and need a break this morning. What should I do?". The user entry is interpreted, determines the user wants to relax, and returns the meditation suggestion. 
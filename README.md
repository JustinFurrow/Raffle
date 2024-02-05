# A reminder/raffle application. 

## The problem
Often times I only remember to do certain tasks at the wrong time. For example, only remembering I need to change my car's oil when I go out and hop in my car - which usually means I need to go somewhere, and don't have time to schedule an appointment. Meanwhile, when I have time to do things, I can sometimes find myself scrolling aimlessly on the internet. 

## What this app does
This app serves two functions:
1. Creates hourly notifications to ask the user if they're focusing
2. Allows the user to create categories of things to do (make appointments, chores, online learning, hobbies,etc.) and tasks within each of those categories. 
3. Press the "Raffle!" button when selected on a category to present a random idea from the tasks they've entered previously. Select a category first to restrict suggestions to tasks in that category.

This app aims to simply give you the option of things you said you wanted to do, on your own time and when you are ready for a suggestion. 

## What this app does not do
1. Automatically send reminders on specific tasks. I intentionally left this out so when a reminder hits, if I wasn't focusing I can then actively choose what to do with the time. Setting a specific reminder for a given task can make it feel like an obligation - my aim with this is to promote doing the tasks I actually *want* to do, not making myself resent those tasks. 

# Current version
Right now, this application is still in the form of a Python script with a simple GUI. You can create and remove new categories and tasks within those categories, and click the "Raffle!" button when ready for an idea. You can also Show or Hide the tasks within a given category. 

If you don't care what category you want to pull a task from, you can click the "Raffle!" button without selecting a category. 

Note that when you close the GUI, it minimizes to the system tray to keep the notification timer running in the background. Right click the icon in the system tray and select Quit to terminate the program. 

By default, the timer is set to generate a reminder once an hour. 

# Future iteration
- Add options in the GUI for modifying the notification timer 
- Create a self-setup version so non-technical users can use the app. 
- Integrate AI with a RAG approach to allow a user to enter information in natural language, have the AI store those activities in logical categories, and interpret future questions by determining an appropriate category and task. For example, a user previously told the app they want to meditate more, which gets sorted into a "Relaxation" category. The user tells the AI "I'm feeling scattered and need a break this morning. What should I do?". The user entry is interpreted, determines the user wants to relax, and returns the meditation suggestion. 

# Dependencies
This application requires the following Python libraries to be installed:

    tkinter - For the GUI (Note: tkinter is included with Python. If you're using a standard installation of Python, you should already have it.)
    plyer - For cross-platform desktop notifications.
    pystray - To create a system tray application.
    Pillow - For image processing with pystray.
    schedule - To schedule tasks (notifications).
    notificaiton - For working with notificaitons

You can install these dependencies using pip by running the following command in your terminal or command prompt:

pip install -r requirements.txt

Ensure you have Python and pip installed on your system before running the above command. For more information on installing Python and pip, refer to the official Python documentation.
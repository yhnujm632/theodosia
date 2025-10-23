# The main two classes: RootWindow for the GUI, and MainSystem for the background procedure
from tkinter_extensions.rootwindow import RootWindow
from daemon_system.mainsystem import MainSystem

# Using threading.Thread to make the daemon system run in the background
from threading import Thread

if __name__ == "__main__":
    # Create RootWindow class instance
    root_window = RootWindow()
    # Create MainSystem class instance
    main_system = MainSystem(root_window)
    # Set the main_system variable in the RootWindow instance to the MainSystem class instance
    root_window.set_main_system(main_system)
    # Create the thread for the main_system main function to run on
    news_stream = Thread(target=main_system.compile_news, daemon=True)

    # Start the news_stream thread in the background
    news_stream.start()
    # Begin the RootWindow
    root_window.mainloop()
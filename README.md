Data science project with Matteo.

High-level description of the structure of the project:

-templates folder:

-index.html is the main page. Here you can find the overall structure of the website: the different buttons in the tab section, and how they get integrated together with some section for handling the python code snippets and the active tabs. The final lines are javascript code for handling the active tabs and the code snippet display to make it user-friendly, and accurate.

-the rest of the files contain the overall structure of each of the tab buttons. e.g. scatter.html contains the html code for the scatter plot section.
-routes/main_routs and utils/helpers: these are crucial python codes. - utils: contains the helpers.py code. This code contains the python functions that we use to run the python code in the backend. e.g. actually create a histogram with python code.

-routes: it contains the main_routes.py file. This is the code that connects python with the html files of each tab.
For each tab we have specific functions, e.g for the histogram tab we have show_histogram. As you can see. this main_routes.py heaviliy depends on the herlpers.py. each function here uses functions from helpers.py. And all the functions in routes return render_template() objects to the index.html ready to be displayed in the active tab that the user is choosing.

-static: it has the marshall logo and a styles.css file that contains the colrs, sizes etc. of the buttons.

-\uploads: has some csv files that can be useful for testing and deploying the project.

Python 3.13.2

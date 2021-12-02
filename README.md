# MOA
#### Video Demo:  <URL https://youtu.be/yMC2BDnNM80>
#### Description:
MOA (Matrix Operations Application) is a simple web app for editing your Excel matrix.

It's designed for people who want to group the rows and columns inside their Excel matricies quickly and
easily. If you have a matrix at the size of 10x10, of course you can do it by hand.
But what if you had a matrix size of 64x64. Then things would get really slow and tedious.
So MOA was created and it is at the use of those who need it.

Explaining Modules:

MOA exists of two parts. Inside the **moa/app** you can see a directory
called *matrix_processor*.
That is the part that handles matricies and file conversions. The rest of the files and folders inside **moa/app** is for the web app part.

*Note: If you want to see an overview of how the program works, first
checkout **moa/app/app.py** then look at **moa/app/matrix_processor/matrix_processor.py**.*

**--- Explaining Modules ---** <br>
Matrix Processor ( moa/app/matrix_processor ): <br>
Inside *matrix_processor* directory there are five modules:
1.  **converters&#46;py:**<br>
    This module handles *.xls* and *.xlsx* file formats. It has two classes
    XlsFile() and XlsxFile(). These classes have a parse() method which will parse the file and return a Matrix() object. They can also take a Matrix() object and write it to a file with their write() method.

2. **errors&#46;py:**<br>
    This module has custom errors defined inside it.

3. **group_manager&#46;py:**<br>
    This is module has method called build_with() which reads the blueprint that the client has sent and returns a Matrix() object.

4. **matrix_processor&#46;py:**<br>
    This is the module that app&#46;py interacts with. This module calls all
    of the other modules inside this directory.

5. **matrix&#46;py:**<br>
    Matrix() object is defined inside here.

App ( moa/app ):

1. **/db:** <br>
    Has *matricies.db* inside it.
    When a client uploads their Excel file it'll get converted to a Matrix()
    object. Then that Marix() object will be stored inside this table with
    client's *session_id*.

2. **/downloads:** <br>
    When the client sends an export request, the blueprint that the client
    sent will be automatically converted to a file and written to this
    location.

3. **/static:** <br>
    Standart Flask static folder. Has gifs, images and scripts inside.

4. **/templates:** <br>
    Standart Flask templates folder. Has the HTML files inside.

5. **app&#46;py:** <br>
    Entry point for the Flask app. Handles serving the web page and client requests.

6. **config&#46;py:** <br>
    A config file for Flask. Assigns download location, secret key, etc.

7. **session_id&#46;py:** <br>
    Has a *Session_ID* class. It's just for generating an ID for each session
    so that it can be stored inside the *matricies.db*. It has a max limit
    of 10.000 so after 10.000'th session it'll reset. After that DB will
    overwirte. This is to prevent breaking the max memory limit of the
    *pythonanywhere.com*.

Other Files:
* **moa/requirements.txt:** <br>
    For creating a venv with pip.
* **moa/env.json:** <br>
    For computer specific variables.
* **moa/remote.txt:** <br>
    Link to github repo
* **moa/docs:**
    Has buch of documents. You can just ignore these.


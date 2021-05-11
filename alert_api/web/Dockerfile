FROM python:3
# set a directory to copy the app 
WORKDIR /usr/src/app
# copy the text file with modules to the current working directory
COPY requirements.txt ./
# recursively install everything in the text file
RUN pip install --no-cache-dir -r requirements.txt
# copy all the files from the current project to the working directory of the container
COPY . .
# run the app
CMD [ "python", "app.py" ]

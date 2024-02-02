FROM python:3.10

# Set an absolute path as the working directory inside the container
WORKDIR .

# Copy the requirements file to the working directory
COPY requirements.txt ./

# Upgrade pip and install the dependencies listed in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory to the working directory in the container
COPY . .

# Specify the command to run your application (app.py in this case)
CMD [ "python", "./app.py" ]

# set up the base image
FROM python:3.12-slim

# set the working directory
WORKDIR /real_estate_app

# copy the requirements file into the container
COPY requirements-dockers.txt .


# install the dependencies
RUN pip install --no-cache-dir -r requirements-dockers.txt

# copy the rest of the application code into the container
COPY real_estate_app/ .

# expose the port on the container
EXPOSE 8000


# Command to run the Streamlit application
CMD ["streamlit", "run", "Home.py", "--server.port", "8000", "--logger.level", "debug"]

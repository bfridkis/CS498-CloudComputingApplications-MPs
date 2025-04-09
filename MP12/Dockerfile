FROM python:3.6

# Creating Application Source Code Directory
RUN mkdir -p /usr/src/app

# Setting Home Directory for containers
WORKDIR /usr/src/app

# Copy src python files
COPY /home/ec2-user/MP12/.py /usr/src/app/

# Installing python dependencies
COPY /home/ec2-user/MP12/requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# create directories for models and data
RUN mkdir /usr/src/app/data
RUN mkdir /usr/src/app/models

# Preload the data
RUN data_preload.py

# Pretrain the models

## Model 1
ENV DATASET="mnist"
ENV TYPE="ff"
RUN train.py

## Model 2
ENV DATASET="mnist"
ENV TYPE="cnn"
RUN train.py

## Model 3
ENV DATASET="kmnist"
ENV TYPE="ff"
RUN train.py

## Model 4
ENV DATASET="kmnist"
ENV TYPE="cnn"
RUN train.py

# Running Python Application
CMD ["python", "server.py"]

## References
## https://stackoverflow.com/questions/53918841/how-to-install-docker-on-amazon-linux2
## https://stackoverflow.com/questions/47951183/adding-source-code-to-docker-image-using-dockerfile
## https://www.google.com/search?q=how+to+see+if+docker+is+running+linux&sca_esv=edec2e4b4572a4c0&rlz=1C1CHBF_enUS1071US1071&ei=-q31Z47CEfO1wN4Ph6W88Qk&ved=0ahUKEwiOp8GvyMmMAxXzGtAFHYcSL54Q4dUDCBA&uact=5&oq=how+to+see+if+docker+is+running+linux&gs_lp=Egxnd3Mtd2l6LXNlcnAiJWhvdyB0byBzZWUgaWYgZG9ja2VyIGlzIHJ1bm5pbmcgbGludXgyBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yCxAAGIAEGIYDGIoFMgsQABiABBiGAxiKBTIFEAAY7wUyCBAAGKIEGIkFSLUjUABY9iJwAHgBkAEAmAG9AaABkB-qAQUxMi4yNLgBA8gBAPgBAZgCJKACsiHCAgsQABiABBiRAhiKBcICERAuGIAEGLEDGNEDGIMBGMcBwgIOEC4YgAQYsQMYgwEYigXCAg4QABiABBixAxiDARiKBcICCxAAGIAEGLEDGIMBwgIOEC4YgAQYsQMY0QMYxwHCAgoQABiABBhDGIoFwgIEEAAYA8ICCBAAGIAEGLEDwgIFEAAYgATCAg4QLhiABBixAxiDARjUAsICCxAAGIAEGLEDGIoFwgILEC4YgAQYsQMYgwHCAggQLhiABBixA8ICCBAAGIAEGKIEmAMAkgcGOS4yNi4xoAebowKyBwY5LjI2LjG4B7Ih&sclient=gws-wiz-serp
## https://stackoverflow.com/questions/34398632/docker-how-to-run-pip-requirements-txt-only-if-there-was-a-change
## https://www.google.com/search?q=difference+between+using+RUN+and+CMD+to+launch+python+script+dockerfile&rlz=1C1CHBF_enUS1071US1071&oq=difference+between+using+RUN+and+CMD+to+launch+python+script+dockerfile&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTEwNDE1ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8
## https://www.google.com/search?q=using+RUN+for+python+script+in+dockerfile&rlz=1C1CHBF_enUS1071US1071&oq=using+RUN+for+python+script+in+dockerfile&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigATIHCAEQIRigATIHCAIQIRigATIHCAMQIRigATIHCAQQIRigATIHCAUQIRiPAjIHCAYQIRiPAjIHCAcQIRiPAtIBCDU3NDNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
## https://www.google.com/search?q=how+to+set+environment+variables+dockerfile&rlz=1C1CHBF_enUS1071US1071&oq=how+to+set+environment+variables+dockerfile&gs_lcrp=EgZjaHJvbWUyCggAEEUYFhgeGDkyBwgBEAAYgAQyCAgCEAAYFhgeMggIAxAAGBYYHjIICAQQABgWGB4yCAgFEAAYFhgeMggIBhAAGBYYHjIICAcQABgWGB4yCAgIEAAYFhgeMggICRAAGBYYHtIBCDU3NDJqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
FROM ubuntu:xenial

# Expose ports
EXPOSE 80

ENV CODE_DIR /var/code

RUN mkdir ${CODE_DIR}
WORKDIR ${CODE_DIR}

# Update the sources list
RUN apt-get update

# Install Python and Basic Python Tools
RUN apt-get install -y --no-install-recommends python-all python-setuptools python-pip
RUN pip install --upgrade pip

COPY requirements.txt ${CODE_DIR}/requirements.txt
RUN pip install -r requirements.txt

COPY . ${CODE_DIR}

CMD ["python", "hello.py"]

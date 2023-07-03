FROM python:3

WORKDIR /usr/src/app

# copying pip requirements separately from rest of files helps with caching docker image build
COPY app/requirements.txt .

RUN pip install -r requirements.txt

# only necessary files should be copied
COPY app ./

# merging apt update and install into single line is recommened by docker documentation
RUN apt-get update && apt-get install tar

# service should be called within dockerfile, not as argument for `docker run`
CMD ["bash", "-c", "bash script.sh"]
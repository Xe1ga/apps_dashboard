FROM python:3.9
COPY . /apps_dashboard
EXPOSE 5000
WORKDIR /apps_dashboard
RUN pip install -r requirements.txt

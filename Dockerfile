FROM python:3.10.6
RUN mkdir -p /streamlit_demo
COPY requirements.txt ./streamlit_demo/requirements.txt
RUN pip3 install -r /streamlit_demo/requirements.txt
COPY app/ /streamlit_demo/app/
COPY data/ /streamlit_demo/data/
COPY images/ /streamlit_demo/images/
EXPOSE 8501/
WORKDIR /streamlit_demo
ENTRYPOINT ["streamlit", "run"]
CMD ["app/dashboard.py"]
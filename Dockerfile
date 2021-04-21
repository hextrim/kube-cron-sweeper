FROM python:3
USER root
RUN curl https://baltocdn.com/helm/signing.asc | apt-key add - \
    && apt-get install apt-transport-https --yes \
    && echo "deb https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list \
    && apt-get update \
    && apt-get -y install helm2=2.16.11-1 \
    && apt-get -y install vim \
    && pip install kubernetes \
    && mkdir -p /root/kube-cron-sweeper
COPY kube-cron-sweeper.py /root/kube-cron-sweeper
ENTRYPOINT ["python"]
CMD ["/root/kube-cron-sweeper/kube-cron-sweeper.py"]

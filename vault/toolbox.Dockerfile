# Use an official lightweight image as a base
FROM alpine:latest

# Install jq, curl, kubectl, and helm
RUN apk add --no-cache jq curl openssl bash\
    && curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl \
    && curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

CMD ["tail", "-f", "/dev/null"]
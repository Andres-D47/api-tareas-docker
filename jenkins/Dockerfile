
FROM docker:cli AS dockercli

FROM docker/compose-bin:latest AS composecli

FROM jenkins/jenkins:lts-jdk17

USER root

COPY --from=dockercli /usr/local/bin/docker /usr/local/bin/docker

COPY --from=composecli /docker-compose /usr/local/lib/docker/cli-plugins/docker-compose

RUN chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

USER jenkins

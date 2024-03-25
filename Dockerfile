FROM maven:3.8.3-openjdk-17-alpine as maven-builder
WORKDIR /app
COPY . /app

RUN mvn install

FROM openjdk:17-jre-alpine
WORKDIR /app
COPY --from=maven-builder /app/target/app.jar .

ENTRYPOINT ["java","-jar","app.jar"]

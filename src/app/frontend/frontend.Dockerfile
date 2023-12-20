FROM node:alpine3.18

ARG BACKEND_HOST
ARG BACKEND_PORT

ENV BACKEND_HOST=${BACKEND_HOST}
ENV BACKEND_PORT=${BACKEND_PORT}

WORKDIR /usr/src/app

COPY src/app/frontend/package.json src/app/frontend/yarn.lock ./

RUN yarn install

COPY src/app/frontend .

RUN yarn build

EXPOSE 3000

CMD ["yarn", "start"]

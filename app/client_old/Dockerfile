# base image
FROM node:12.2.0-alpine

# Set working directory
WORKDIR /

# install and cache client dependencies
COPY ./client/*.js /
COPY ./client/*.json /
COPY ./client/public /public
COPY ./client/src /src
COPY ./client/tests /tests
COPY ./client/.editorconfig /.editorconfig

# add `/client/node_modules/.bin` to $PATH
ENV PATH /app/client/node_modules/.bin:$PATH

RUN npm install --force
RUN npm install @vue/cli --force

# start client
CMD ["npm", "run", "serve"]
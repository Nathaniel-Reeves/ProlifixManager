# base image
FROM node:18.16-alpine

# Set working directory
WORKDIR /

# install and cache client dependencies
COPY ./client/*.js .
COPY ./client/*.json .
COPY ./client/public ./public
COPY ./client/src ./src
COPY ./client/tests ./tests
COPY ./client/.editorconfig .

# add `/client/node_modules/.bin` to $PATH
# ENV PATH /app/client/node_modules/.bin:$PATH

RUN npm install -g npm@9.6.7
RUN npm install --omit=dev --force
RUN npm install @vue/cli --force

# start client
CMD ["npm", "run", "serve"]
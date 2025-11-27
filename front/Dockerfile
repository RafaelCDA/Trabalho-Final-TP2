FROM node:23-alpine

# Set the working directory
WORKDIR /var/www

COPY ./front/package*.json /var/www

RUN npm install

COPY ./front .

EXPOSE 3000

CMD ["npm","run","dev"]

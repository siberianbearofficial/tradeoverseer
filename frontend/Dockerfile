FROM node:21-alpine AS build

WORKDIR /usr/src/app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build


FROM nginx:alpine

COPY ./config /etc/nginx/conf.d

COPY ./ssl /etc/ssl

COPY --from=build /usr/src/app/dist/tradeoverseer-frontend /usr/share/nginx/html

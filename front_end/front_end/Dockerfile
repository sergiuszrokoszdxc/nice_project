FROM node:alpine AS build
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM node:alpine AS deployment
RUN npm install -g serve
COPY --from=build /usr/src/app/build /build
EXPOSE 80
CMD [ "serve", "-s", "build", "-l", "80" ]
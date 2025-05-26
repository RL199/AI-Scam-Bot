FROM node:18

WORKDIR /app

COPY frontend/package*.json ./

RUN npm install

COPY frontend/. .

EXPOSE 3000

RUN npm run build

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3000"]

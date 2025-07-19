# Build stage
FROM node:24-alpine3.21

WORKDIR /app

COPY frontend/. .

RUN npm install
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3000"]
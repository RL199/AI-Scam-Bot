# Build stage
FROM node:24-alpine3.21

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy source code
COPY frontend/. .

# Build the application
RUN npm run build

EXPOSE 3000

# Start the preview server
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3000"]

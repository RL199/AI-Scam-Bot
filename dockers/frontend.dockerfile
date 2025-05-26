# Build stage
FROM node:24-slim AS build

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/. .
RUN npm run build

# Production stage
FROM node:24-slim

WORKDIR /app

# Copy built assets and package files
COPY --from=build /app/dist ./dist
COPY --from=build /app/package*.json ./

# Install only production dependencies for preview
RUN npm install --only=production

EXPOSE 3000

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3000"]

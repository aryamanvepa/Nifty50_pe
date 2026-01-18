FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy service code
COPY . .

# Expose port
EXPOSE 3001

# Run the service
CMD ["node", "service.js"]

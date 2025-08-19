import axios, { AxiosResponse } from "axios";
import {
  ChatRequest,
  ChatResponse,
  ConversationRequest,
  ConversationResponse,
  HealthResponse,
  MessageCountResponse,
} from "../types/api";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "https://backend.p-labs.net/";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health check
  healthCheck: async (): Promise<HealthResponse> => {
    const response: AxiosResponse<HealthResponse> = await api.get("/health");
    return response.data;
  },

  // Chat with the AI assistant
  chat: async (request: ChatRequest): Promise<ChatResponse> => {
    const response: AxiosResponse<ChatResponse> = await api.post(
      "/chat",
      request
    );
    return response.data;
  },

  // Create a new conversation
  createConversation: async (
    request: ConversationRequest
  ): Promise<ConversationResponse> => {
    const response: AxiosResponse<ConversationResponse> = await api.post(
      "/conversations",
      request
    );
    return response.data;
  },

  // Get conversation history
  getConversationHistory: async (
    conversationId: string,
    limit: number = 50
  ) => {
    const response = await api.get(`/conversations/${conversationId}/history`, {
      params: { limit },
    });
    return response.data;
  },

  // Get message count for a conversation
  getMessageCount: async (
    conversationId: string
  ): Promise<MessageCountResponse> => {
    const response: AxiosResponse<MessageCountResponse> = await api.get(
      `/conversations/${conversationId}/message-count`
    );
    return response.data;
  },

  // Get user conversations
  getUserConversations: async (userId: string, limit: number = 20) => {
    const response = await api.get(`/users/${userId}/conversations`, {
      params: { limit },
    });
    return response.data;
  },

  // Get model information
  getModelInfo: async () => {
    const response = await api.get("/model/info");
    return response.data;
  },
};

export default apiService;

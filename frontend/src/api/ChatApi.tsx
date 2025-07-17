import { ChatRequest, ChatResponse, ConversationRequest, ConversationResponse } from '../types/chat';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const postChat = async (request: ChatRequest): Promise<ChatResponse> => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Chat request failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

export const createConversation = async (request: ConversationRequest): Promise<ConversationResponse> => {
  const response = await fetch(`${API_BASE_URL}/conversations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Conversation creation failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

export const getConversationHistory = async (conversationId: string, limit: number = 50) => {
  const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}/history?limit=${limit}`, {
    method: 'GET',
  });

  if (!response.ok) {
    throw new Error(`Failed to get conversation history: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

export const getUserConversations = async (userId: string, limit: number = 20) => {
  const response = await fetch(`${API_BASE_URL}/users/${userId}/conversations?limit=${limit}`, {
    method: 'GET',
  });

  if (!response.ok) {
    throw new Error(`Failed to get user conversations: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

export const getModelInfo = async () => {
  const response = await fetch(`${API_BASE_URL}/model/info`, {
    method: 'GET',
  });

  if (!response.ok) {
    throw new Error(`Failed to get model info: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

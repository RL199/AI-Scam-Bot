export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  status?: 'sending' | 'delivered' | 'failed';
}

export interface ChatRequest {
  messages: Array<{
    role: 'user' | 'assistant' | 'system';
    content: string;
  }>;
  max_length?: number;
  temperature?: number;
  conversation_id?: string;
  user_id?: string;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
}

export interface ConversationRequest {
  user_id?: string;
  title?: string;
}

export interface ConversationResponse {
  conversation_id: string;
  title?: string;
  created_at: string;
}

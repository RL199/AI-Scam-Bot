export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface ChatRequest {
  messages: ChatMessage[];
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

export interface HealthResponse {
  status: string;
  model_status: string;
  api_version: string;
}

export interface MessageCountResponse {
  conversation_id: string;
  message_count: number;
}

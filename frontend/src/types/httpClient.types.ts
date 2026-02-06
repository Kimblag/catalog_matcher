export type ApiError = {
  code: string;
  message: string;
  details?: unknown;
  correlationId?: string;
};

export type BackendErrorPayload = {
  error_code?: string;
  message?: string;
  details?: unknown;
  correlation_id?: string;
};

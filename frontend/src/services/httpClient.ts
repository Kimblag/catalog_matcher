import type { ApiError, BackendErrorPayload } from '../types';

/**
 * HTTP client for making API requests with error handling.
 *
 * @class HttpClient
 * @description Handles HTTP requests to a backend API with support for both JSON and blob responses.
 * Automatically manages headers and error parsing based on the response type.
 *
 * @example
 * ```typescript
 * const client = new HttpClient('/api/users', 'json');
 * const { data, error } = await client.request<User>();
 * ```
 */
class HttpClient {
  BASE_URL: string =
    import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  endpoint: string;
  responseType: 'blob' | 'json' | undefined;
  options?: RequestInit;

  constructor(
    endpoint: string,
    responseType: 'blob' | 'json' | undefined,
    options?: RequestInit,
  ) {
    this.endpoint = endpoint;
    this.options = options;
    this.responseType = responseType;
  }

  private getContentType(): string | null {
    // return norhing if responseType is undefined, otherwise return the appropriate content type
    if (this.responseType === undefined) {
      return null;
    } else if (this.responseType === 'blob') {
      return 'application/octet-stream';
    } else {
      return 'application/json';
    }
  }

  private getHeaders(): Record<string, string> {
    const contentType = this.getContentType();
    return contentType ? { 'Content-Type': contentType } : {};
  }

  async request<T>(
    signal?: AbortSignal,
  ): Promise<{ data?: T; error?: ApiError }> {
    const response = await fetch(`${this.BASE_URL}${this.endpoint}`, {
      headers: this.getHeaders(),
      ...this.options,
      signal,
    });

    // if response type is blob
    if (this.responseType === 'blob') {
      if (!response.ok) {
        const text = await response.text();
        return {
          error: { code: 'unknown_error', message: text },
        };
      }
      return { data: (await response.blob()) as T };
    }

    const payload: BackendErrorPayload & T = await response.json();

    if (!response.ok) {
      // extract error information from the api response and return it in a consistent format
      const error: ApiError = {
        code: payload.error_code ?? 'unknown_error',
        message: payload.message ?? 'An unexpected error occurred',
        details: payload.details,
        correlationId: payload.correlation_id,
      };
      return { error };
    }

    return { data: payload as T };
  }
  catch(err: unknown) {
    return {
      error: {
        code: 'network_error',
        message:
          'Cannot connect to the server. Please check your network connection and try again.',
        details: err,
      },
    };
  }
}

export default HttpClient;

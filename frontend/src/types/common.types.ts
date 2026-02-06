import type { ApiError } from './httpClient.types';

export type PageStatus =
  | { type: 'loading' }
  | { type: 'ready' }
  | { type: 'error'; error: ApiError };

export type ActionState =
  | { type: 'idle' }
  | { type: 'uploading' }
  | { type: 'downloading' }
  | { type: 'saving'; itemId: string }
  | { type: 'deleting'; itemId: string }
  | { type: 'error'; error: ApiError }
  | { type: 'loading-items' };

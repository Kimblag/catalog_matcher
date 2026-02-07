import type { ApiError, MatchesList, MatchResponse } from '../types';
import { mapToMatchList } from '../utils';
import HttpClient from './httpClient';

export class MatchService {
  async downloadRequirementTemplate(
    signal?: AbortSignal,
  ): Promise<{ data?: Blob; error?: ApiError }> {
    const client = new HttpClient('/api/templates/requirements', 'blob');

    // check if there is an error in the response
    const response = await client.request<Blob>(signal);
    if (response.error) return { error: response.error };

    if (!response.data) {
      return {
        error: {
          code: 'invalid_response',
          message: 'Invalid response format: missing data.',
        },
      };
    }
    return { data: response.data };
  }

  // upload requirement file and get matches
  async uploadRequirementCSV(
    file: File,
    signal?: AbortSignal,
  ): Promise<{ data?: MatchesList; error?: ApiError }> {
    const formData = new FormData();

    formData.append('requirement_file', file);

    const client = new HttpClient('/api/requirements/matches', undefined, {
      method: 'POST',
      body: formData,
    });

    const response = await client.request<MatchResponse>(signal);

    if (response.error) return { error: response.error };

    // get the data from the response and check if it is valid
    if (!response.data?.results) {
      return {
        error: {
          code: 'invalid_response',
          message: 'Invalid response format: missing results.',
        },
      };
    }

    // map the response data to the MatchList type
    return { data: mapToMatchList(response.data) };
  }
}

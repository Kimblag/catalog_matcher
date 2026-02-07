import type { MatchesList, MatchResponse } from '../types';

export const mapToMatchList = (matchResponse: MatchResponse): MatchesList => {
  return {
    results: matchResponse.results.map((result) => ({
      requirement: result.requirement,
      matches: result.matches.map((match) => ({
        catalogItemId: match.catalog_item_id,
        ...match,
      })),
    })),
  };
};

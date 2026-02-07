// example response backend to mmap to a type:
/*
{
  "results": [
    {
      "requirement": {
        "additionalProp1": {}
      },
      "matches": [
        {
          "catalog_item_id": "string",
          "name": "string",
          "category": "string",
          "subcategory": "string",
          "description": "string",
          "unit": "string",
          "provider": "string",
          "attributes": {
            "additionalProp1": {}
          },
          "score": 0
          }]}]}
*/
export type MatchResponse = {
  results: MatchResultResponse[];
};

export type MatchResultResponse = {
  requirement: Record<string, unknown>;
  matches: MatchItemResponse[];
};

export type MatchItemResponse = {
  catalog_item_id: string;
  name: string;
  category?: string;
  subcategory?: string;
  description?: string;
  unit?: string;
  provider?: string;
  attributes?: Record<string, string>;
  score: number;
};

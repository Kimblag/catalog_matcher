export type MatchResult = {
  requirement: MatchRequirement;
  matches: MatchItem[];
};

export type MatchesList = {
  results: MatchResult[];
};

export type MatchItem = {
  catalogItemId: string;
  name: string;
  category?: string;
  subcategory?: string;
  description?: string;
  unit?: string;
  provider?: string;
  attributes?: Record<string, string>;
  score: number;
};

type RequirementBase = {
  name: string;
  category?: string;
  subcategory?: string;
  description?: string;
  unit?: string;
  provider?: string;
  attributes?: Record<string, string>;
};

export type MatchesListProps = {
  matches: MatchesList;
};

export type MatchRequirement = RequirementBase;
export type RequirementItemCardProps = RequirementBase;

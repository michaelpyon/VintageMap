export type Significance =
  | "birthday"
  | "anniversary"
  | "wedding"
  | "graduation"
  | "retirement"
  | "memorial"
  | "other";

export interface VintageRegion {
  region_key: string;
  display_name: string;
  country: string;
  score: number;
  quality_tier: string;
  description: string;
  drinking_window?: string;
  notable_wines?: string[];
  wine_style: string;
  primary_grapes: string[];
  has_data?: boolean;
}

export interface Recommendation {
  region_key: string;
  region_name: string;
  country: string;
  wine_style: string;
  score: number;
  quality_tier: string;
  grapes: string[];
  notable_wines: string[];
  drinking_window: string;
  recommendation_text: string;
  suggestion: string;
}

export interface RecommendationResponse {
  year: number;
  significance: string;
  primary: Recommendation | null;
  alternatives: Recommendation[];
  message?: string;
}

export interface YearRange {
  min_year: number;
  max_year: number;
}

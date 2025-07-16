export interface MarketPulseResponse {
  ticker: string;
  as_of: string;
  momentum: {
    returns: number[];
    score: number;
  };
  news: {
    title: string;
    description: string;
    url: string;
  }[];
  pulse: string;
  llm_explanation: string;
}

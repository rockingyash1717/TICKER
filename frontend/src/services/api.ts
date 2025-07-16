import axios from 'axios';
import type { MarketPulseResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const getMarketPulse = async (ticker: string): Promise<MarketPulseResponse> => {
  const response = await axios.get(`${API_BASE_URL}/market-pulse`, {
    params: { ticker }
  });
  return response.data;
};

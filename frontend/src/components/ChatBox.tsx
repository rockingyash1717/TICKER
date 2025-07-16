import { useState } from 'react';
import type { FormEvent } from 'react';
import styled from '@emotion/styled';
import { getMarketPulse } from '../services/api';
import { MessageBubble } from './MessageBubble';
import type { MarketPulseResponse } from '../types';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
`;

const InputForm = styled.form`
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
`;

const Input = styled.input`
  flex: 1;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 16px;
  &:focus {
    outline: none;
    border-color: #4a90e2;
  }
`;

const Button = styled.button`
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  &:hover {
    background-color: #357abd;
  }
  &:disabled {
    background-color: #a0aec0;
    cursor: not-allowed;
  }
`;

const MessageContainer = styled.div`
  display: flex;
  flex-direction: column;
`;

const Error = styled.div`
  color: #e53e3e;
  padding: 12px;
  margin: 8px 0;
  border-radius: 8px;
  background-color: #fff5f5;
`;

export const ChatBox = () => {
  const [ticker, setTicker] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<MarketPulseResponse | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!ticker.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const data = await getMarketPulse(ticker.trim().toUpperCase());
      setResponse(data);
    } catch (err) {
      setError('Failed to fetch market pulse');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <InputForm onSubmit={handleSubmit}>
        <Input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="Enter ticker symbol (e.g., MSFT)"
          disabled={loading}
        />
        <Button type="submit" disabled={loading || !ticker.trim()}>
          {loading ? 'Loading...' : 'Get Pulse'}
        </Button>
      </InputForm>

      <MessageContainer>
        {error && <Error>{error}</Error>}
        {response && <MessageBubble data={response} />}
      </MessageContainer>
    </Container>
  );
};

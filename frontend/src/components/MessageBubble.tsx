import { useState } from 'react';
import styled from '@emotion/styled';
import type { MarketPulseResponse } from '../types';
import { JsonView } from 'react-json-view-lite';
import 'react-json-view-lite/dist/index.css';

interface MessageBubbleProps {
  data: MarketPulseResponse;
}

const Bubble = styled.div`
  background-color: #f0f4f8;
  border-radius: 12px;
  padding: 16px;
  margin: 8px 0;
  max-width: 80%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const Explanation = styled.p`
  margin: 0 0 16px 0;
  font-size: 16px;
  line-height: 1.5;
  color: #2d3748;
`;

const Details = styled.div`
  border-top: 1px solid #e2e8f0;
  padding-top: 12px;
  margin-top: 12px;
`;

const DetailsToggle = styled.button`
  background: none;
  border: none;
  color: #4a5568;
  cursor: pointer;
  font-size: 14px;
  padding: 4px 8px;
  margin: 0;
  &:hover {
    text-decoration: underline;
  }
`;

export const MessageBubble = ({ data }: MessageBubbleProps) => {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <Bubble>
      <h4 style={{ color: '#0a0a0aff' }}>{data.pulse}</h4>
      <Explanation>{data.llm_explanation}</Explanation>
      <Details>
        <DetailsToggle onClick={() => setShowDetails(!showDetails)}>
          {showDetails ? 'Hide' : 'Show'} full response
        </DetailsToggle>
        {showDetails && (
          <div style={{ marginTop: '12px' }}>
            <JsonView data={data} />
          </div>
        )}
      </Details>
    </Bubble>
  );
};

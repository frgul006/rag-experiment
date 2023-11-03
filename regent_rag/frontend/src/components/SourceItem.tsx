import React from "react";
import { styled } from "styled-components";

interface SourceItemProps {
  source: string;
}

export const SourceItemLi = styled.li`
  padding: 3px 0;
`;

const SourceItem: React.FC<SourceItemProps> = ({ source }) => {
  return (
    <SourceItemLi>
      <a href={source} target="_blank" rel="noopener noreferrer">
        {source}
      </a>
    </SourceItemLi>
  );
};

export default SourceItem;

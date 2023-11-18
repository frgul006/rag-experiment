import styled from "styled-components";

export const MessageWrapper = styled.div<{ isBot: boolean }>`
  display: flex;
  justify-content: ${(props) => (props.isBot ? "flex-end" : "flex-start")};
`;

export const MessageContent = styled.div<{ isBot: boolean }>`
  display: flex;
  align-items: center;
  background-color: ${(props) => (props.isBot ? "#464454" : "#f1f1f1")};
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
  text-align: left;
  max-width: 80%;
  color: ${(props) => (props.isBot ? "#d1d5db" : "inherit")};
  flex-direction: ${(props) => (props.isBot ? "row-reverse" : "row")};

  & > * {
    margin-right: 10px;
  }

  & a {
    color: ${(props) => (props.isBot ? "#fff" : "inherit")};
    font-weight: 600;
  }
`;

export const SourcesList = styled.ul`
  margin-top: 10px;
  list-style-type: none;
  padding: 0;
  font-size: 0.8em;
`;



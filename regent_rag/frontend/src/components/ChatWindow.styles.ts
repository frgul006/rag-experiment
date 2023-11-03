import styled from "styled-components";

export const ChatContainer = styled.div`
  max-width: 800px;
  width: 90%;
  margin: 3% auto;
  border: 1px solid #333;
  border-radius: 5px;
  background-color: #343541;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow-y: auto;
  height: 80vh;
`;

export const MessagesContainer = styled.div`
  flex: 1;
  padding: 16px;
  overflow-y: auto;
`;

export const InputContainer = styled.div`
  padding: 16px;
  display: flex;
  justify-content: space-between;
`;

export const UserInput = styled.input`
  width: 80%;
  padding: 8px;
  border: 0 solid #8e8ea0;
  line-height: 1.5rem;
  background-color: #40414f;
  border-radius: 4px;
  font-size: 1rem;
  flex-grow: 1;
  margin-right: 10px;
  color: #ffffff;
  transition: all 0.3s ease;
  
  &:focus {
    outline: none;
  }
`;

export const SendButton = styled.button`
  padding: 10px 20px;
  background-color: #f1f1f1;
  border: none;
  border-radius: 4px;
  cursor: pointer;
`;

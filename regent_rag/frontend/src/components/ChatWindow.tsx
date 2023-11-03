import { useState } from "react";
import {
  ChatContainer,
  MessagesContainer,
  InputContainer,
  UserInput,
  SendButton,
} from "./ChatWindow.styles";
import Message from "./Message";
import axios from "axios";
import { ClipLoader } from "react-spinners";

interface ChatMessage {
  sender: "user" | "bot";
  content: string;
  sources?: string | string[];
}

const ChatWindow = () => {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([
    {
      content: "Can you link me the sheet to calculate costs for a staff car?",
      sender: "user",
    },
    {
      content:
        "You can calculate the total cost for you as an employee using this Excel document: [ALD Personalbil.xlsx](http://wikiregent.wpengine.com/wp-content/uploads/2018/04/ALD-Personalbil.xlsx)\n",
      sender: "bot",
      sources: "https://intern.regent.se/en/staff-car/",
    },
  ]);
  const [userInput, setUserInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    setIsLoading(true);

    const userMessage: ChatMessage = { sender: "user", content: userInput };

    // Add the user's message to the chat history
    setChatHistory([...chatHistory, userMessage]);

    try {
      // Make a POST request to the backend
      const response = await axios.post("http://localhost:5000/chat", {
        query: userInput,
      });

      // Assume the bot's response is in a field called 'response' in the returned JSON
      const botResponse = response.data.answer;

      // Add the bot's message to the chat history
      const botMessage: ChatMessage = {
        sender: "bot",
        content: botResponse,
        sources: response.data.sources,
      };
      setChatHistory([...chatHistory, userMessage, botMessage]);
    } catch (error) {
      console.error("There was an error sending the message:", error);
    }

    // Clear the user input
    setUserInput("");
    setIsLoading(false);
  };

  return (
    <ChatContainer>
      <MessagesContainer>
        {chatHistory.map((message, index) => (
          <Message
            key={index}
            sender={message.sender}
            content={message.content}
            sources={message.sources}
          />
        ))}
      </MessagesContainer>
      <InputContainer>
        <UserInput
          type="text"
          value={userInput}
          disabled={isLoading}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
        />
        {isLoading ? (
          <ClipLoader color="#007bff" /> // Spinner from react-spinners
        ) : (
          <SendButton onClick={sendMessage}>Send</SendButton>
        )}
      </InputContainer>
    </ChatContainer>
  );
};

export default ChatWindow;

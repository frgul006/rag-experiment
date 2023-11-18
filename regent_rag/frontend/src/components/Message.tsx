import React from "react";
import { FaUser, FaRobot } from "react-icons/fa";
import ReactMarkdown from "react-markdown";
import { useSpring, animated } from "react-spring";
import { MessageContent, MessageWrapper, SourcesList } from "./Message.styles";
import { MarkdownLink } from "./MarkdownLink";
import SourceItem from "./SourceItem";

interface MessageProps {
  sender: "user" | "bot";
  content: string;
  sources?: string[];
}

const Message: React.FC<MessageProps> = ({ sender, content, sources }) => {
  const fade = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
  });

  const isBot = sender === "bot";
  const Icon = isBot ? FaRobot : FaUser;
  const iconSize = isBot ? 36 : 24;



  return (
    <animated.div style={fade}>
      <MessageWrapper isBot={isBot}>
        <MessageContent isBot={isBot}>
          <Icon size={iconSize} />
          <div>
            <ReactMarkdown
              children={content}
              components={{
                a: ({ node, ...props }) => <MarkdownLink {...props} />,
              }}
            />
            {sender === "bot" && !!sources?.length && (
              <SourcesList>{
                sources.map((source, i) => (
                  <>
                <SourceItem key={i} source={source} />
                {i < sources.length -1 && <span style={{paddingInlineEnd: '.5ch'}}>,</span>}
                  </>
                ))
              }</SourcesList>
            )}
          </div>
        </MessageContent>
      </MessageWrapper>
    </animated.div>
  );
};

export default Message;

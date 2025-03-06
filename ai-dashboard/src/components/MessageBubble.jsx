const MessageBubble = ({ message }) => {
    return (
      <div className="p-2 bg-blue-500 text-white rounded-lg my-2 max-w-xs">
        {message}
      </div>
    );
  };
  
  export default MessageBubble;
  
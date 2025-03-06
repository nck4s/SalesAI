import { useEffect, useState } from "react";

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/chat/global/");

    ws.onopen = () => console.log("✅ WebSocket Connected!");
    ws.onmessage = (event) => {
      console.log("📩 Message received:", event.data);
      try {
        const data = JSON.parse(event.data);
        setMessages((prev) => [...prev, data]);
      } catch (error) {
        console.error("🚨 Error parsing WebSocket message:", error);
      }
    };
    ws.onerror = (error) => console.error("🚨 WebSocket Error:", error);
    ws.onclose = (event) => {
      console.log("🔴 WebSocket closed:", event);
      setTimeout(() => {
        console.log("♻️ Reconnecting WebSocket...");
        setSocket(new WebSocket("ws://localhost:8000/ws/chat/global/"));
      }, 3000); // Попробуем переподключить через 3 секунды
    };

    setSocket(ws);

    return () => ws.close();
  }, []);

  const handleSend = () => {
    if (socket && socket.readyState === WebSocket.OPEN && input.trim()) {
      socket.send(JSON.stringify({ message: input }));
      setInput("");
    }
  };

  return (
    <div className="flex flex-col flex-grow p-4">
      <div className="flex-grow overflow-y-auto">
        {messages.map((msg, idx) => (
          <div key={idx} className="p-2 bg-gray-200 my-2 rounded">
            {msg.message}
          </div>
        ))}
      </div>
      <div className="flex">
        <input
          className="flex-grow p-2 border"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button className="bg-blue-500 text-white p-2" onClick={handleSend}>
          Отправить
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;

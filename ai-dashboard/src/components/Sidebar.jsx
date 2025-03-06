import React, { useEffect, useState } from "react";
import axios from "axios";

const Sidebar = ({ onSelectChat }) => {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/bot/chats/")
      .then((res) => setChats(res.data))
      .catch((err) => console.error("Ошибка при загрузке чатов:", err));
  }, []);

  return (
    <div className="w-1/4 bg-white p-4 border-r">
      <h2 className="text-xl font-bold mb-4">Клиенты</h2>
      {chats.map((chat) => (
        <div
          key={chat.id}
          className="p-2 border-b cursor-pointer hover:bg-gray-200"
          onClick={() => onSelectChat(chat)}
        >
          <p className="font-semibold">{chat.user}</p>
          <p className="text-sm text-gray-500">{chat.message}</p>
        </div>
      ))}
    </div>
  );
};

export default Sidebar;

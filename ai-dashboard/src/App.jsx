import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import Sidebar from "./components/Sidebar";

const App = () => {
  const [selectedChat, setSelectedChat] = useState(null);

  return (
    <div className="flex h-screen">
      <Sidebar onSelectChat={setSelectedChat} />
      <div className="flex-grow">
        {selectedChat ? (
          <ChatWindow chat={selectedChat} />
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-xl text-gray-500">Выберите чат</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;

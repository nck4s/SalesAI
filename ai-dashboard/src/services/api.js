import axios from "axios";

const API_URL = "http://127.0.0.1:8000/bot";

// Получаем список чатов
export const getChats = async () => {
  const response = await axios.get(`${API_URL}/chats/`);
  return response.data;
};

// Отправляем сообщение
export const sendMessage = (socket, message) => {
  if (socket) {
    socket.send(JSON.stringify({ message }));
  }
};

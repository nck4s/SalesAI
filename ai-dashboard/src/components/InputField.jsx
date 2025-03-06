import { useState } from "react";

const InputField = ({ onSend }) => {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim()) {
      onSend(input);
      setInput("");
    }
  };

  return (
    <div className="flex p-4 border-t">
      <input
        className="flex-grow p-2 border rounded-lg"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button className="bg-blue-500 text-white p-2 ml-2 rounded-lg" onClick={handleSend}>
        Отправить
      </button>
    </div>
  );
};

export default InputField;

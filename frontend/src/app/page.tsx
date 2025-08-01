'use client';
import { useState } from 'react';

interface JsonData {
  type: string;
  content: string | null;
  timestamp: string;
}

export default function Home() {
  const [inputValue, setInputValue] = useState<string>('');
  const [jsonData, setJsonData] = useState<JsonData | null>(null);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // 새로운 JSON 데이터 생성
    const newJsonData: JsonData = {
      type: 'user_input',
      content: inputValue,
      timestamp: new Date().toISOString()
    };
    
    // JSON 상태 업데이트
    setJsonData(newJsonData);
    
    // alert로 표시
    alert(JSON.stringify(newJsonData, null, 2));
    
    // 입력값 초기화
    setInputValue('');
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-white">
      <h1 className="text-3xl font-bold mb-8 text-center">
        무슨 작업을 하고 계세요?
      </h1>
      <div className="w-full max-w-2xl px-4">
        <form onSubmit={handleSubmit} className="relative">
          <input
            name="query"
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            className="w-full px-4 py-3 rounded-full border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="무엇이든 물어보세요"
            required
          />
          <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center space-x-2">
            <button 
              type="button" 
              className="p-2 hover:bg-gray-100 rounded-full"
              onClick={() => {
                // 음성 입력 로직을 추가할 수 있습니다
                console.log('Voice input clicked');
              }}
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z" />
              </svg>
            </button>
            <button 
              type="submit" 
              className="p-2 hover:bg-gray-100 rounded-full"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.189m-1.5.189a6.01 6.01 0 0 1-1.5-.189m3.75 7.478a12.06 12.06 0 0 1-4.5 0m3.75 2.383a14.406 14.406 0 0 1-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 1 0-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
              </svg>
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}
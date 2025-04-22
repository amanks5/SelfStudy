import React, {useState} from "react";

const CHAT_KEY = "";

const NoteEditor = () => {
    const [noteName, setNoteName] = useState('New Note');
    const [noteContent, setNoteContent] = useState('Lorem ipsum dolor sit amet...');
    const [summary, setSummary] = useState('No summary generated.');

    async function sendPrompt(e) {
      e.preventDefault();

      const form = e.target;
      setSummary("Generating summary...");

      const response = await fetch('https://api.openai.com/v1/chat/completions', 
          {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  Authorization: `Bearer ${CHAT_KEY}`
              },
              body: JSON.stringify({
                  model: "gpt-4o-mini",
                  messages: [{'role': 'user', 'content': `Please summarize the following text for me: ${noteContent}`}]
              })
          }
      )

      const data = await response.json();
      setSummary(`${data.choices[0].message.content}`);
    }

    return (
        <div className="flex h-screen items-center">
          <div className="container mx-auto h-9/12 grid grid-cols-12 grid-rows-16 gap-1.5">
            <div className="col-span-9">
                <input className="w-full rounded-sm bg-[#A62929] font-serif text-xl font-semibold text-[#F2DAC4] px-2" value={noteName} onChange={e => setNoteName(e.target.value)}></input>
            </div>
            
            <div className="container col-span-3 row-span-16 border-dashed border-4 border-[#A62929] rounded-lg px-2 py-1.5">
                <textarea className="w-full font-serif text-[#A62929] font-medium text-sm text-left my-1 resize-none read-only !outline-none" value={summary} rows={20} />
                <button className="w-full mx-auto rounded-sm bg-[#A62929] font-serif text-[#F2DAC4] py-0.5 my-0.5 cursor-pointer">💾 save note</button>
                <form method="POST" onSubmit={sendPrompt}>
                <button type="submit" className="w-full mx-auto rounded-sm bg-[#A62929] font-serif text-[#F2DAC4] py-0.5 my-0.5 cursor-pointer">💡 generate summary</button>
                </form>
                <button className="w-full mx-auto rounded-sm bg-[#A62929] font-serif text-[#F2DAC4] py-0.5 my-0.5 cursor-pointer">💡 generate flashcards</button>
            </div>
            <div className="col-span-9 row-span-15 rounded-lg px-2 py-1 border-dashed border-4 border-[#A62929] font-serif text-[#A62929] text-[15px]">
                <textarea name="noteContent" value={noteContent} onChange={e => setNoteContent(e.target.value)} className="h-full w-full text-wrap resize-none !outline-none" />
            </div>
          </div>
          
        </div>
      )
}

export default NoteEditor;
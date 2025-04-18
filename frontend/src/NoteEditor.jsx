import React, {useState} from "react";

const NoteEditor = () => {
    const [noteName, setNoteName] = useState('New Note');

    return (
        <div className="flex h-screen items-center">
          <div className="container mx-auto h-9/12 grid grid-cols-12 grid-rows-16 gap-1.5">
            <div className="col-span-9">
                <input className="w-full rounded-sm bg-[#A62929] font-serif text-xl font-semibold text-[#F2DAC4] px-2" value={noteName} onChange={e => setNoteName(e.target.value)}></input>
            </div>
            <div className="col-span-3 row-span-16 border-dashed border-4 border-[#A62929] rounded-lg px-2 py-1.5">
                <button className="w-full mx-auto rounded-sm bg-[#A62929] font-serif text-[#F2DAC4] py-0.5 my-0.5 cursor-pointer">💾 save note</button>
                <button className="w-full mx-auto rounded-sm bg-[#A62929] font-serif text-[#F2DAC4] py-0.5 my-0.5 cursor-pointer">💡 generate summary</button>
                <button className="w-full mx-auto rounded-sm bg-[#A62929] font-serif text-[#F2DAC4] py-0.5 my-0.5 cursor-pointer">💡 generate flashcards</button>
            </div>
            <div className="col-span-9 row-span-15 rounded-lg px-2 py-1 border-dashed border-4 border-[#A62929] font-serif text-[#A62929] text-[15px]">
                <textarea value={"Lorem ipsum dolor sit amet."} className="h-full w-full text-wrap resize-none !outline-none" />
            </div>
          </div>
        </div>
      )
}

export default NoteEditor;
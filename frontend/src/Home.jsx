import React, { useState } from "react";
import api from "./api";

const Home = () => {
    const [loggedIn, setLoggedIn] = useState(false);
    const [notes, setNotes] = useState([]);

    const refreshNotes = () => {
        api.get("/api/notes").then((res) => {
          setNotes(res.data);
          setLoggedIn(true);
        });
    };
    refreshNotes();

    const addNote = () => {
        api.post("/api/notes", {
            title: "New Note",
            content: ""
        }).then(refreshNotes).catch((e) => alert("Failed to create note!"));
    };

    if(loggedIn) {
      return (
        <div className="mx-auto flex h-screen justify-center items-center">
          <div className="flex flex-col gap-1">
          {notes.map((note) => 
              <a href={"notes/" + note.id}>{note.title}</a>
          )}
          <button onClick={addNote} className="bg-[#A62929] hover:bg-[#F2DAC4] px-12 py-2 rounded-sm font-serif text-[#F2DAC4] hover:text-[#A62929] border-2 border-[#A62929] cursor-pointer">Add Note</button>
          </div>
      </div>
      );
    } else return (
      <div className="mx-auto flex h-screen justify-center items-center">
        <div className="grid grid-cols-2">
          <div className="mx-32 px-4 py-20 text-6xl font-serif font-bold text-[#A62929]">smart notes, smarter learning.</div>
          <div className="flex flex-col gap-4 rounded-xl mx-32 px-12 justify-center items-center">
            <a href="/login" className="text-center text-2xl bg-[#A62929] hover:bg-[#F2DAC4] w-100 px-12 py-2 rounded-sm font-serif text-[#F2DAC4] hover:text-[#A62929] border-2 border-[#A62929] cursor-pointer">login</a>
            <a href="/signup" className="text-center text-2xl bg-[#A62929] hover:bg-[#F2DAC4] w-100 px-12 py-2 rounded-sm font-serif text-[#F2DAC4] hover:text-[#A62929] border-2 border-[#A62929] cursor-pointer">signup</a>
          </div>
        </div>
      </div>
    );
};

export default Home;

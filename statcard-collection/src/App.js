import React, { useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import PartCard from './components/PartCard/PartCard.js'
import ComparePage from './pages/ComparePage/ComparePage.js'
import data from './part-data.json'
import './App.css';

function App() {
  let defaultImage = '/images/default.png'
  const [searchParams, setSearchParams] = useState({})
  /*
  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={navbar}> 
        <Route index element = {<HomePage searchParams={searchParams} setSearchParams={setSearchParams}/>} />
      </Route>
    </Routes>
  </BrowserRouter>  );
  */

  return (
    <div className="App">
      <header className="App-header">
        <img src={defaultImage} className="App-logo" alt="logo" />
        <ComparePage data={data['guns']}/>
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn Tanmk
        </a>
      </header>
    </div>
  );
}

export default App;

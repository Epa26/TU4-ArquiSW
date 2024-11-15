import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Home from './Home';
import GradeEditor from './GradeEditor'
import reportWebVitals from './reportWebVitals';
import { Link, BrowserRouter as Router, Route, Routes } from "react-router-dom";


export default function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Home/>} />
        <Route path="grade/:gradeID" element={<GradeEditor/>} />
      </Routes>
    </Router>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App/>);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

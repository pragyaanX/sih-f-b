import React from 'react';

import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import FileUploadWithStars from './components/Upload';

function App() {
  return (
    <div className="App">
      <Router>
      <Routes>

          <Route path="/" element={<FileUploadWithStars/>} />

      </Routes>
      </Router>
    </div>
  );
}

export default App;
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';

const DropdownWithSearch = ({ bName, setBName }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredOptions, setFilteredOptions] = useState([]);
  const [noResults, setNoResults] = useState(false);

  const options = [
    'IMG_MIR',
    'IMG_SWIR',
    'IMG_TIR1',
    'IMG_TIR2',
    'IMG_VIS',
    'IMG_WV',
  ];

  const handleSearch = (event) => {
    const value = event.target.value;
    setSearchTerm(value);

    const filtered = options.filter((option) =>
      option.toLowerCase().includes(value.toLowerCase())
    );

    if (filtered.length === 0 && value !== '') {
      setNoResults(true);
      setFilteredOptions([]);
    } else {
      setNoResults(false);
      setFilteredOptions(filtered);
    }
  };

  const handleOptionSelect = (option) => {
    setBName(option);
    setSearchTerm(option);
    setFilteredOptions([]);
    setNoResults(false);
  };

  return (
    <div className="relative">
      <input
        type="text"
        placeholder="Search bands..."
        value={searchTerm}
        onChange={handleSearch}
        className="w-full mt-2 p-3 border border-transparent focus:border-indigo-500 rounded-md shadow-sm bg-gray-800 text-white outline-none"
      />
      {(searchTerm && (filteredOptions.length > 0 || noResults)) && (
        <div className="absolute mt-1 w-full bg-gray-800 p-3 rounded shadow-lg z-10">
          {noResults ? (
            <p className="text-red-500">No bands found</p>
          ) : (
            <ul className="text-white">
              {filteredOptions.map((option) => (
                <li
                  key={option}
                  className="p-2 hover:bg-gray-600 rounded cursor-pointer"
                  onClick={() => handleOptionSelect(option)}
                >
                  {option}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

const App = () => {
  const [file, setFile] = useState(null);
  const [bName, setBName] = useState('');
  const [load, setLoad] = useState(false);
  const [error, setError] = useState('');
  const [succ, setSucc] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoad(true);
    setError('');
    setSucc('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('selected_band', bName);

    console.log('Selected band:', bName);
    console.log('Uploaded file:', file);

    try {
      const response = await axios.post('http://localhost:8000/process_hdf5', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setSucc('File uploaded successfully');
    } catch (err) {
      setError('Error uploading file');
    } finally {
      setLoad(false);
    }
  };

  const stars = Array.from({ length: 100 });

  const generateRandomDelay = () => Math.random() * 5;

  return (
    <div className="relative h-screen overflow-hidden bg-gradient-to-b from-black via-gray-900 to-black flex items-center justify-center">
      <div className="absolute inset-0 z-0">
        {stars.map((_, index) => (
          <motion.div
            key={index}
            className="absolute bg-white rounded-full shadow-lg"
            style={{
              width: `${Math.random() * 2 + 1}px`,
              height: `${Math.random() * 2 + 1}px`,
              top: `${Math.random() * 100}vh`,
              left: `${Math.random() * 100}vw`,
              boxShadow: `0 0 ${Math.random() * 10 + 5}px ${Math.random() * 3}px rgba(255, 255, 255, 0.6)`,
            }}
            initial={{
              opacity: 0,
              scale: 0.5,
            }}
            animate={{
              opacity: [0, 1, 0],
              y: `${Math.random() * 100 - 50}vh`,
              x: `${Math.random() > 0.5 ? '-' : ''}${Math.random() * 100 - 50}vw`,
              transition: {
                duration: 5,
                repeat: Infinity,
                repeatType: 'loop',
                ease: 'easeInOut',
                delay: generateRandomDelay(),
              },
            }}
          />
        ))}
        <div className="absolute inset-0 z-0 bg-gradient-to-r from-gray-800 via-gray-900 to-black opacity-25 blur-2xl" />
      </div>

      <motion.div
        className="relative z-10 bg-gradient-to-r from-gray-800 via-gray-900 to-black p-10 rounded-xl shadow-2xl w-[420px] mx-auto backdrop-blur-lg"
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <h2 className="text-3xl font-extrabold mb-6 text-center text-white uppercase tracking-widest">
          Upload HDF5 File
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-400 pb-2">File</label>
            <div className="relative">
              <input
                type="file"
                onChange={handleFileChange}
                className="absolute inset-0 opacity-0 w-full h-full z-20 cursor-pointer"
                required
              />
              <div className="bg-gray-800 text-white w-full p-3 border border-transparent rounded-md shadow-sm flex items-center justify-between z-10 relative cursor-pointer">
                <span>{file ? file.name : 'No file chosen'}</span>
                <span className="bg-indigo-600 text-white px-4 py-2 rounded-md">Choose File</span>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400">Band Name</label>
            <DropdownWithSearch bName={bName} setBName={setBName} />
          </div>

          <motion.button
            type="submit"
            className="w-full py-3 px-4 bg-indigo-700 text-white rounded-md shadow-lg hover:bg-indigo-800 focus:ring-4 focus:ring-indigo-500 focus:outline-none transition transform duration-150"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={load}
          >
            {load ? 'Uploading...' : 'Upload'}
          </motion.button>

          {error && <p className="text-red-400 mt-4 text-center">{error}</p>}
          {succ && <p className="text-green-400 mt-4 text-center">{succ}</p>}
        </form>
      </motion.div>
    </div>
  );
};

export default App;

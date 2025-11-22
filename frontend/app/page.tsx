"use client";
import { useState, useEffect } from "react";
import Graph3D from "../components/Graph3D";
import { Upload, BrainCircuit, Share2 } from "lucide-react";

// CHANGE THIS URL TO YOUR RENDER BACKEND URL AFTER DEPLOYMENT
const API_URL = "http://127.0.0.1:8000"; 

export default function Home() {
  const [graphData, setGraphData] = useState(null);
  const [nodeA, setNodeA] = useState(0);
  const [nodeB, setNodeB] = useState(1);
  const [prediction, setPrediction] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Fetch Initial Graph
  useEffect(() => {
    fetch(`${API_URL}/graph-data`)
      .then(res => res.json())
      .then(data => setGraphData(data));
  }, []);

  const handleFileUpload = async (e: any) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    await fetch(`${API_URL}/upload-csv`, { method: "POST", body: formData });
    
    // Refresh Graph
    const res = await fetch(`${API_URL}/graph-data`);
    const data = await res.json();
    setGraphData(data);
    setLoading(false);
  };

  const handlePredict = async () => {
    const res = await fetch(`${API_URL}/predict?node_a=${nodeA}&node_b=${nodeB}`);
    const data = await res.json();
    setPrediction(data);
  };

  return (
    <main className="h-screen w-full bg-black text-white relative overflow-hidden">
      
      {/* Sidebar Control Panel */}
      <div className="absolute top-4 left-4 z-10 w-80 bg-zinc-900/90 backdrop-blur border border-zinc-800 p-6 rounded-2xl shadow-2xl">
        <div className="flex items-center gap-2 mb-6">
          <BrainCircuit className="text-indigo-500" size={32} />
          <h1 className="text-2xl font-bold tracking-tighter">NeuroGraph</h1>
        </div>

        {/* Upload Section */}
        <div className="mb-8">
          <label className="block text-xs font-medium text-zinc-400 mb-2 uppercase tracking-wide">Dataset (CSV)</label>
          <div className="relative">
            <input 
              type="file" 
              accept=".csv"
              onChange={handleFileUpload}
              className="hidden" 
              id="file-upload"
            />
            <label htmlFor="file-upload" className="flex items-center justify-center gap-2 w-full py-3 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 border-dashed rounded-lg cursor-pointer transition-all">
              <Upload size={16} />
              <span className="text-sm">{loading ? "Retraining..." : "Upload Network"}</span>
            </label>
          </div>
        </div>

        {/* Prediction Section */}
        <div>
          <label className="block text-xs font-medium text-zinc-400 mb-2 uppercase tracking-wide">Link Prediction</label>
          <div className="flex gap-2 mb-3">
            <input 
              type="number" 
              value={nodeA} 
              onChange={e => setNodeA(Number(e.target.value))}
              className="w-1/2 bg-black border border-zinc-700 rounded p-2 text-center focus:border-indigo-500 outline-none"
              placeholder="Node A"
            />
            <input 
              type="number" 
              value={nodeB} 
              onChange={e => setNodeB(Number(e.target.value))}
              className="w-1/2 bg-black border border-zinc-700 rounded p-2 text-center focus:border-indigo-500 outline-none"
              placeholder="Node B"
            />
          </div>
          <button 
            onClick={handlePredict}
            className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-medium transition-all flex items-center justify-center gap-2"
          >
            <Share2 size={16} /> Predict Interaction
          </button>
        </div>

        {/* Results Area */}
        {prediction && (
          <div className="mt-6 p-4 bg-black/50 rounded-lg border border-zinc-800 animate-in fade-in slide-in-from-top-2">
            <div className="flex justify-between items-center mb-1">
              <span className="text-zinc-400 text-sm">Probability</span>
              <span className="text-indigo-400 font-mono">{(prediction.probability * 100).toFixed(1)}%</span>
            </div>
            <div className="w-full bg-zinc-800 h-2 rounded-full mb-3">
              <div 
                className="bg-indigo-500 h-2 rounded-full transition-all duration-1000" 
                style={{width: `${prediction.probability * 100}%`}}
              />
            </div>
            <p className={`text-center text-sm font-medium ${prediction.probability > 0.5 ? 'text-green-400' : 'text-red-400'}`}>
              {prediction.verdict}
            </p>
          </div>
        )}
      </div>

      {/* 3D Graph Visualization */}
      <div className="h-full w-full cursor-move">
        {graphData && <Graph3D data={graphData} />}
      </div>
    </main>
  );
}

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import networkx as nx
import io
import torch
from train import get_karate_data, train_gnn, process_csv_graph

app = FastAPI()

# Enable CORS for Vercel Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State (In-memory for demo purposes)
state = {
    "model": None,
    "data": None,
    "graph_nx": None
}

# Initialize with Karate Club on startup
G, train_data = get_karate_data()
state["model"], state["data"] = train_gnn(train_data)
state["graph_nx"] = G

@app.get("/")
def root():
    return {"status": "NeuroGraph Brain Online"}

@app.get("/graph-data")
def get_graph():
    """Returns graph topology for 3D visualization."""
    return nx.node_link_data(state["graph_nx"])

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """Retrains model on new CSV data."""
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    
    # Process and Train
    G, train_data = process_csv_graph(df)
    model, data = train_gnn(train_data)
    
    # Update State
    state["model"] = model
    state["data"] = data
    state["graph_nx"] = G
    
    return {"message": "Model Retrained", "nodes": G.number_of_nodes(), "edges": G.number_of_edges()}

@app.get("/predict")
def predict(node_a: int, node_b: int):
    """Predicts link probability between two nodes."""
    model = state["model"]
    data = state["data"]
    
    model.eval()
    with torch.no_grad():
        z = model.encode(data.x, data.edge_index)
        edge_label_index = torch.tensor([[node_a], [node_b]])
        score = model.decode(z, edge_label_index).sigmoid().item()
        
    return {
        "node_a": node_a,
        "node_b": node_b,
        "probability": score,
        "verdict": "Likely Connected" if score > 0.5 else "Unlikely Connected"
    }

import torch
import torch_geometric.transforms as T
from torch_geometric.utils import from_networkx, negative_sampling
from torch_geometric.datasets import KarateClub
import networkx as nx
from model import GNN

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def train_gnn(data):
    """
    Trains a GNN on the provided PyG Data object.
    """
    # 1. Setup Model
    model = GNN(in_channels=data.num_features, hidden_channels=128, out_channels=64).to(device)
    optimizer = torch.optim.Adam(params=model.parameters(), lr=0.01)
    criterion = torch.nn.BCEWithLogitsLoss()
    
    data = data.to(device)
    
    # 2. Training Loop (Fast 100 epochs)
    for epoch in range(101):
        model.train()
        optimizer.zero_grad()
        
        z = model.encode(data.x, data.edge_index)

        # Positive edges (real)
        pos_out = model.decode(z, data.edge_label_index)
        
        # Negative edges (fake/random)
        neg_edge_index = negative_sampling(
            edge_index=data.edge_index, num_nodes=data.num_nodes,
            num_neg_samples=data.edge_label_index.size(1), method='sparse')
        neg_out = model.decode(z, neg_edge_index)
        
        # Combine & Loss
        out = torch.cat([pos_out, neg_out])
        gt = torch.cat([data.edge_label, torch.zeros(neg_out.size(0), device=device)])
        
        loss = criterion(out, gt)
        loss.backward()
        optimizer.step()
        
    return model, data

def get_karate_data():
    """Returns the default Karate Club dataset."""
    dataset = KarateClub()
    data = dataset[0]
    
    # Split edges for Link Prediction training
    transform = T.RandomLinkSplit(num_val=0.05, num_test=0.1, is_undirected=True, add_negative_train_samples=False)
    train_data, val_data, test_data = transform(data)
    
    # Create NetworkX graph for visualization
    G = nx.karate_club_graph()
    return G, train_data

def process_csv_graph(df):
    """
    Smart CSV Processor.
    Handles:
    1. Simple Edge Lists (Source, Target)
    2. BioGRID Chemical Data (Official Symbol, Chemical Name)
    """
    
    # --- STRATEGY 1: Check for BioGRID format ---
    if 'Official Symbol' in df.columns and 'Chemical Name' in df.columns:
        print("🧬 Detected BioGRID Chemical Dataset")
        # Rename columns to standard format
        df = df.rename(columns={'Official Symbol': 'source', 'Chemical Name': 'target'})
        # Keep only the relevant columns
        df = df[['source', 'target']]

    # --- STRATEGY 2: Check for Standard 'Source/Target' ---
    elif 'Source' in df.columns and 'Target' in df.columns:
        print("📄 Detected Standard Edge List")
        df = df.rename(columns={'Source': 'source', 'Target': 'target'})

    # --- STRATEGY 3: Fallback (Take 1st and 2nd columns) ---
    else:
        print("⚠️ Unknown format, using first two columns as Source/Target")
        df.columns.values[0] = 'source'
        df.columns.values[1] = 'target'
        df = df.iloc[:, :2]

    # Clean data
    df = df.dropna()
    
    # Create Graph
    G = nx.from_pandas_edgelist(df, source='source', target='target')
    
    # Convert to PyG
    data = from_networkx(G)
    
    # Add identity features (One-Hot Encoding)
    data.x = torch.eye(G.number_of_nodes(), dtype=torch.float)
    
    # Split for training
    transform = T.RandomLinkSplit(num_val=0.05, num_test=0.1, is_undirected=True, add_negative_train_samples=False)
    train_data, val_data, test_data = transform(data)
    
    return G, train_data

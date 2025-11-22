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
    """Converts uploaded CSV to PyG Data and NetworkX Graph."""
    # Create NetworkX graph from CSV
    G = nx.from_pandas_edgelist(df, source=df.columns[0], target=df.columns[1])
    
    # Convert to PyG
    data = from_networkx(G)
    
    # Add dummy features (Identity Matrix) since CSVs usually don't have node features
    data.x = torch.eye(G.number_of_nodes(), dtype=torch.float)
    
    # Split
    transform = T.RandomLinkSplit(num_val=0.05, num_test=0.1, is_undirected=True, add_negative_train_samples=False)
    train_data, val_data, test_data = transform(data)
    
    return G, train_data

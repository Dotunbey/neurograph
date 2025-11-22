import torch
from torch_geometric.nn import GCNConv

class GNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        # Graph Convolution Layer 1
        self.conv1 = GCNConv(in_channels, hidden_channels)
        # Graph Convolution Layer 2
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def encode(self, x, edge_index):
        # Message Passing Step 1
        x = self.conv1(x, edge_index).relu()
        # Message Passing Step 2
        return self.conv2(x, edge_index)

    def decode(self, z, edge_label_index):
        # Predicts link probability via dot product of node embeddings
        return (z[edge_label_index[0]] * z[edge_label_index[1]]).sum(dim=-1)

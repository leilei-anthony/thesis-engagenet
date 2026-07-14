import torch
import torch.nn as nn

class EngagementLSTM(nn.Module):
    """
    LSTM sequence model for predicting student engagement.
    Supports Classification (4 classes) and Regression (1 output node).
    """
    def __init__(self, input_dim=1518, hidden_dim=64, num_layers=1, num_classes=4, mode='classification'):
        super(EngagementLSTM, self).__init__()
        self.mode = mode.lower()
        if self.mode not in ['classification', 'regression']:
            raise ValueError("mode must be either 'classification' or 'regression'")
            
        self.hidden_dim = hidden_dim
        
        # LSTM Layer
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=False
        )
        
        # Dense Layers
        # We project from hidden_dim -> hidden_dim // 2 -> output_dim
        self.fc1 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.relu = nn.ReLU()
        
        if self.mode == 'classification':
            self.fc2 = nn.Linear(hidden_dim // 2, num_classes)
        else:
            self.fc2 = nn.Linear(hidden_dim // 2, 1)

    def forward(self, x, seq_lens):
        """
        Forward pass.
        Args:
            x: Input sequence features of shape [batch_size, max_len, input_dim]
            seq_lens: Actual lengths of sequences in the batch of shape [batch_size]
        """
        # LSTM output shape: [batch_size, max_len, hidden_dim]
        lstm_out, _ = self.lstm(x)
        
        # Global Average Pooling across the temporal dimension, ignoring padded frames
        # Create a boolean mask of shape [batch_size, max_len]
        batch_size, max_len, _ = lstm_out.size()
        device = lstm_out.device
        
        # arange shape [max_len], unsqueezed to [1, max_len] compared with [batch_size, 1]
        mask = torch.arange(max_len, device=device).unsqueeze(0) < seq_lens.unsqueeze(1)
        mask = mask.unsqueeze(-1).float()  # shape: [batch_size, max_len, 1]
        
        # Apply mask and sum over sequence length dimension
        sum_out = torch.sum(lstm_out * mask, dim=1)  # shape: [batch_size, hidden_dim]
        
        # Divide by sequence lengths to get average (clamping to avoid division by 0)
        pooled_out = sum_out / seq_lens.unsqueeze(-1).clamp(min=1).float()  # shape: [batch_size, hidden_dim]
        
        # Dense layers
        out = self.fc1(pooled_out)
        out = self.relu(out)
        out = self.fc2(out)
        
        if self.mode == 'regression':
            # Squeeze output to shape [batch_size]
            out = out.squeeze(-1)
            
        return out

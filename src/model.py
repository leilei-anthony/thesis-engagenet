import torch
import torch.nn as nn

class EngagementLSTM(nn.Module):
    """
    LSTM sequence model for predicting student engagement.
    Supports Classification (4 classes) and Regression (1 output node).
    """
    def __init__(self, input_dim=1518, hidden_dim=64, num_layers=1, num_classes=4,
                 mode='classification', readout='mean'):
        super(EngagementLSTM, self).__init__()
        self.mode = mode.lower()
        if self.mode not in ['classification', 'regression']:
            raise ValueError("mode must be either 'classification' or 'regression'")

        self.readout = readout.lower()
        if self.readout not in ['mean', 'last', 'attention']:
            raise ValueError("readout must be one of 'mean', 'last', 'attention'")

        self.hidden_dim = hidden_dim

        # LSTM Layer
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=False
        )

        # Learned attention scorer, used only when readout == 'attention'
        if self.readout == 'attention':
            self.attn = nn.Linear(hidden_dim, 1)

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

        batch_size, max_len, _ = lstm_out.size()
        device = lstm_out.device

        # Boolean mask over real (non-padded) timesteps.
        # arange shape [max_len], unsqueezed to [1, max_len] compared with [batch_size, 1]
        valid = torch.arange(max_len, device=device).unsqueeze(0) < seq_lens.unsqueeze(1)
        mask = valid.unsqueeze(-1).float()  # shape: [batch_size, max_len, 1]

        if self.readout == 'mean':
            # Global average pooling across the temporal dimension, ignoring padded frames.
            # Note this aggregation is permutation-invariant over timesteps, so it
            # discards much of the ordering information the LSTM encodes.
            sum_out = torch.sum(lstm_out * mask, dim=1)  # [batch_size, hidden_dim]
            pooled_out = sum_out / seq_lens.unsqueeze(-1).clamp(min=1).float()

        elif self.readout == 'last':
            # Hidden state at the last VALID timestep. Sequences are zero-padded at
            # the tail, so lstm_out[:, -1] would read padding for short sequences;
            # gather at index (seq_len - 1) per sample instead.
            last_idx = (seq_lens - 1).clamp(min=0)  # [batch_size]
            index = last_idx.view(-1, 1, 1).expand(-1, 1, lstm_out.size(-1))
            pooled_out = lstm_out.gather(1, index).squeeze(1)  # [batch_size, hidden_dim]

        else:  # 'attention'
            # Learned attention over valid timesteps.
            scores = self.attn(lstm_out)                       # [batch_size, max_len, 1]
            scores = scores.masked_fill(~valid.unsqueeze(-1), float('-inf'))
            weights = torch.softmax(scores, dim=1)
            # Guard against all-masked rows (seq_len == 0) producing NaNs
            weights = torch.nan_to_num(weights, nan=0.0)
            pooled_out = torch.sum(lstm_out * weights, dim=1)   # [batch_size, hidden_dim]

        # Dense layers
        out = self.fc1(pooled_out)
        out = self.relu(out)
        out = self.fc2(out)
        
        if self.mode == 'regression':
            # Squeeze output to shape [batch_size]
            out = out.squeeze(-1)
            
        return out


class EngagementMLP(nn.Module):
    """
    MLP sequence model for predicting student engagement.
    Averages the input sequence features over the temporal dimension,
    then applies dense layers.
    Supports Classification (4 classes) and Regression (1 output node).
    """
    def __init__(self, input_dim=1518, hidden_dim=64, num_classes=4, mode='classification'):
        super(EngagementMLP, self).__init__()
        self.mode = mode.lower()
        if self.mode not in ['classification', 'regression']:
            raise ValueError("mode must be either 'classification' or 'regression'")
            
        # Dense Layers
        # We project from input_dim -> hidden_dim -> hidden_dim // 2 -> output_dim
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.relu2 = nn.ReLU()
        
        if self.mode == 'classification':
            self.fc3 = nn.Linear(hidden_dim // 2, num_classes)
        else:
            self.fc3 = nn.Linear(hidden_dim // 2, 1)

    def forward(self, x, seq_lens):
        """
        Forward pass.
        Args:
            x: Input sequence features of shape [batch_size, max_len, input_dim]
            seq_lens: Actual lengths of sequences in the batch of shape [batch_size]
        """
        # Average pooling across temporal dimension using sequence lengths
        batch_size, max_len, input_dim = x.size()
        device = x.device
        
        mask = torch.arange(max_len, device=device).unsqueeze(0) < seq_lens.unsqueeze(1)
        mask = mask.unsqueeze(-1).float()  # shape: [batch_size, max_len, 1]
        
        sum_out = torch.sum(x * mask, dim=1)  # shape: [batch_size, input_dim]
        pooled_out = sum_out / seq_lens.unsqueeze(-1).clamp(min=1).float()  # shape: [batch_size, input_dim]
        
        # Dense layers
        out = self.fc1(pooled_out)
        out = self.relu1(out)
        out = self.fc2(out)
        out = self.relu2(out)
        out = self.fc3(out)
        
        if self.mode == 'regression':
            # Squeeze output to shape [batch_size]
            out = out.squeeze(-1)
            
        return out


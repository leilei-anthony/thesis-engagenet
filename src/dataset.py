import os
from pathlib import Path
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = REPO_ROOT / 'data' / 'processed'

# Map raw string labels to ordinal integers
LABEL_MAP = {
    'Not-Engaged': 0,
    'Barely-engaged': 1,
    'Engaged': 2,
    'Highly-Engaged': 3
}

class EngagementDataset(Dataset):
    """
    Custom PyTorch Dataset for loading EngageNet behavioral features.
    Supports targeted sampling and BOCPD datasets.
    """
    def __init__(self, sampling_method, split, data_dir=None, binarize_threshold=None):
        self.sampling_method = sampling_method.lower()
        self.split = split.lower()
        self.data_dir = str(data_dir) if data_dir is not None else str(DEFAULT_DATA_DIR)
        self.binarize_threshold = binarize_threshold
        
        # Determine the CSV filename
        if 'changepoint' in self.sampling_method:
            filename = f"{self.sampling_method}-{self.split}.csv"
        elif self.sampling_method == 'bocpd':
            filename = f"3-changepoint-{self.split}.csv"
        elif self.sampling_method == 'targeted':
            filename = f"targeted-{self.split}.csv"
        else:
            filename = f"{self.sampling_method}-{self.split}.csv"
            
        csv_path = os.path.join(self.data_dir, filename)
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
            
        print(f"Loading data from {csv_path}...")
        
        # Load raw data
        df = pd.read_csv(csv_path)
        
        # Filter out SNP (Subject Not Present) rows since they do not have valid engagement scores
        df = df[df['label'] != 'SNP(Subject Not Present)']
        
        # Fill missing values (NaNs) with 0.0 to prevent NaN propagation
        df = df.fillna(0.0)
        
        # Map labels to integer scores
        df['label_idx'] = df['label'].map(LABEL_MAP)
        df = df.dropna(subset=['label_idx'])
        df['label_idx'] = df['label_idx'].astype(int)
        
        # Binarize if a threshold is provided
        if self.binarize_threshold is not None:
            if self.binarize_threshold not in [1, 2, 3]:
                raise ValueError("binarize_threshold must be 1, 2, or 3")
            df['label_idx'] = (df['label_idx'] >= self.binarize_threshold).astype(int)
        
        # Group frames by source video path (ensuring temporal frames are contiguous)
        grouped = df.groupby('source_video_path')
        
        # Identify feature columns (everything after frame column up to label_idx)
        # Columns: person_id, source_video_path, frame_id, label, frame, [features...]
        feature_cols = df.columns[5:-1]
        
        self.sequences = []
        self.labels = []
        self.lengths = []
        
        for video_path, group in grouped:
            # Extract features in original order
            features = group[feature_cols].values.astype(np.float32)
            label = group['label_idx'].iloc[0]
            seq_len = len(features)
            
            # Dynamic padding to max sequence length of 3 (standard for EngageNet temporal subsets)
            padded_features = np.zeros((3, features.shape[1]), dtype=np.float32)
            actual_len = min(seq_len, 3)
            padded_features[:actual_len, :] = features[:actual_len, :]
            
            self.sequences.append(padded_features)
            self.labels.append(label)
            self.lengths.append(actual_len)
            
        # Convert lists to PyTorch Tensors
        self.sequences = torch.tensor(np.array(self.sequences), dtype=torch.float32)
        self.labels = torch.tensor(np.array(self.labels), dtype=torch.long)
        self.lengths = torch.tensor(np.array(self.lengths), dtype=torch.long)
        
        print(f"Loaded {len(self.sequences)} video sequences for split '{self.split}'.")

    def __len__(self):
        return len(self.sequences)
        
    def __getitem__(self, idx):
        return self.sequences[idx], self.labels[idx], self.lengths[idx]

def get_dataloader(sampling_method, split, batch_size=64, shuffle=None, data_dir=None, binarize_threshold=None):
    """
    Creates a DataLoader for the requested dataset split.
    """
    if shuffle is None:
        shuffle = True if split.lower() == 'train' else False
        
    dataset = EngagementDataset(sampling_method, split, data_dir=data_dir, binarize_threshold=binarize_threshold)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, drop_last=False)
    return dataloader

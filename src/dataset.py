import os
import json
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

SNP_LABEL = 'SNP(Subject Not Present)'

# The sampling methods that actually have extracted datasets on disk.
# NOTE: 'bocpd' is deliberately absent. BOCPD was never implemented -- the
# extraction pipeline (scripts/feature_extraction.py) only provides 'targeted'
# (first/middle/last valid frame) and 'changepoint' (top-k velocity peaks).
# The previous 'bocpd' option silently loaded the 3-changepoint files, which
# made BOCPD results duplicates of 3-changepoint rather than an independent
# condition. It now raises instead of silently aliasing.
SUPPORTED_SAMPLING_METHODS = ('targeted', '3-changepoint', '5-changepoint', '7-changepoint')

# Expected per-frame feature dimensionality (see model.py input_dim).
EXPECTED_FEATURE_DIM = 1518


def common_video_ids(split, methods=SUPPORTED_SAMPLING_METHODS, data_dir=None, use_cache=True):
    """
    Returns the set of source_video_path values present in EVERY sampling method's
    CSV for the given split (after SNP filtering).

    This exists because the sampling methods do not cover the same videos: the
    extraction pipeline skips a clip when it has fewer valid frames than the
    requested changepoint count, so e.g. 5-/7-changepoint cover fewer videos than
    targeted/3-changepoint. Comparing sampling methods on different video sets
    confounds the sampling effect with test-set composition, so every condition
    should be restricted to this common subset.

    Result is cached to '.common_videos_{split}.json' in data_dir, since the
    uncached path reads four large CSVs.
    """
    data_dir = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
    cache_path = data_dir / f'.common_videos_{split.lower()}.json'

    if use_cache and cache_path.exists():
        with open(cache_path) as f:
            return set(json.load(f))

    id_sets = []
    for method in methods:
        csv_path = data_dir / f'{method}-{split.lower()}.csv'
        if not csv_path.exists():
            raise FileNotFoundError(
                f"Cannot compute common video subset: missing {csv_path}"
            )
        frame = pd.read_csv(csv_path, usecols=['source_video_path', 'label'])
        frame = frame[frame['label'] != SNP_LABEL]
        id_sets.append(set(frame['source_video_path'].unique()))

    common = set.intersection(*id_sets)

    try:
        with open(cache_path, 'w') as f:
            json.dump(sorted(common), f)
    except OSError:
        pass  # cache is an optimisation; failing to write it is not fatal

    return common


class EngagementDataset(Dataset):
    """
    Custom PyTorch Dataset for loading EngageNet behavioral features.
    Supports targeted sampling and BOCPD datasets.
    """
    def __init__(self, sampling_method, split, data_dir=None, binarize_threshold=None,
                 restrict_to_common=False):
        self.sampling_method = sampling_method.lower()
        self.split = split.lower()
        self.data_dir = str(data_dir) if data_dir is not None else str(DEFAULT_DATA_DIR)
        self.binarize_threshold = binarize_threshold
        self.restrict_to_common = restrict_to_common
        
        # Determine maximum sequence length. Default is 3 (legacy behavior).
        # For changepoint sampling (e.g. '5-changepoint') use the numeric prefix
        # so that 5/7 changepoint datasets produce sequences of length 5/7.
        self.max_seq_len = 3
        if 'changepoint' in self.sampling_method:
            try:
                prefix = self.sampling_method.split('-')[0]
                cp_count = int(prefix)
                # sanity: require at least 1, but preserve legacy minimum of 3
                self.max_seq_len = max(1, cp_count)
            except Exception:
                # fallback to default if parsing fails
                self.max_seq_len = 3
        
        # Determine the CSV filename.
        # 'bocpd' is rejected explicitly rather than silently aliased to
        # 3-changepoint (see SUPPORTED_SAMPLING_METHODS above).
        if self.sampling_method == 'bocpd':
            raise ValueError(
                "sampling_method='bocpd' is not supported. BOCPD was never implemented in this "
                "project: scripts/feature_extraction.py only provides 'targeted' (first/middle/last "
                "valid frame) and 'changepoint' (top-k velocity peaks) extraction modes. The former "
                "'bocpd' option silently loaded 3-changepoint data, making its results duplicates "
                "rather than an independent condition. "
                f"Supported methods: {', '.join(SUPPORTED_SAMPLING_METHODS)}."
            )
        if self.sampling_method not in SUPPORTED_SAMPLING_METHODS:
            raise ValueError(
                f"Unknown sampling_method '{self.sampling_method}'. "
                f"Supported methods: {', '.join(SUPPORTED_SAMPLING_METHODS)}."
            )

        filename = f"{self.sampling_method}-{self.split}.csv"

        csv_path = os.path.join(self.data_dir, filename)
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
            
        print(f"Loading data from {csv_path}...")
        
        # Load raw data
        df = pd.read_csv(csv_path)
        
        # Filter out SNP (Subject Not Present) rows since they do not have valid engagement scores
        df = df[df['label'] != SNP_LABEL]

        # Restrict to the set of videos covered by EVERY sampling method, so that
        # sampling conditions are compared on identical clips rather than on
        # whatever subset each extraction run happened to produce.
        if self.restrict_to_common:
            common = common_video_ids(self.split, data_dir=self.data_dir)
            n_before = df['source_video_path'].nunique()
            df = df[df['source_video_path'].isin(common)]
            n_after = df['source_video_path'].nunique()
            print(f"Restricted to common video subset: {n_before} -> {n_after} videos.")

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
        
        # Sort explicitly by (video, frame_id) so that within-group row order is
        # guaranteed temporal. Previously this relied on the CSVs happening to be
        # written in frame order -- true in practice, but unguaranteed, and the
        # LSTM's whole premise depends on it.
        df = df.sort_values(['source_video_path', 'frame_id'], kind='mergesort')

        # Group frames by source video path (ensuring temporal frames are contiguous)
        grouped = df.groupby('source_video_path')

        # Identify feature columns (everything after frame column up to label_idx)
        # Columns: person_id, source_video_path, frame_id, label, frame, [features...]
        feature_cols = df.columns[5:-1]
        if len(feature_cols) != EXPECTED_FEATURE_DIM:
            raise ValueError(
                f"Expected {EXPECTED_FEATURE_DIM} feature columns but found {len(feature_cols)} "
                f"in {csv_path}. Feature columns are selected positionally (df.columns[5:-1]), "
                "so a change to column order or count in the extraction pipeline will silently "
                "shift the feature window. Verify the CSV schema before proceeding."
            )
        
        self.sequences = []
        self.labels = []
        self.lengths = []
        # Kept so evaluation can emit per-sample predictions keyed by video, which
        # is what paired significance tests (e.g. McNemar) need to align two models'
        # predictions on the same clips.
        self.video_ids = []

        for video_path, group in grouped:
            # Extract features in original order
            features = group[feature_cols].values.astype(np.float32)
            label = group['label_idx'].iloc[0]
            seq_len = len(features)
            
            # Dynamic padding to `self.max_seq_len` frames so changepoint datasets
            # (e.g. 5-changepoint, 7-changepoint) preserve all selected frames.
            padded_features = np.zeros((self.max_seq_len, features.shape[1]), dtype=np.float32)
            actual_len = min(seq_len, self.max_seq_len)
            padded_features[:actual_len, :] = features[:actual_len, :]
            
            self.sequences.append(padded_features)
            self.labels.append(label)
            self.lengths.append(actual_len)
            self.video_ids.append(video_path)
            
        # Convert lists to PyTorch Tensors
        self.sequences = torch.tensor(np.array(self.sequences), dtype=torch.float32)
        self.labels = torch.tensor(np.array(self.labels), dtype=torch.long)
        self.lengths = torch.tensor(np.array(self.lengths), dtype=torch.long)
        
        print(f"Loaded {len(self.sequences)} video sequences for split '{self.split}'.")

    def __len__(self):
        return len(self.sequences)
        
    def __getitem__(self, idx):
        return self.sequences[idx], self.labels[idx], self.lengths[idx]

def get_dataloader(sampling_method, split, batch_size=64, shuffle=None, data_dir=None,
                   binarize_threshold=None, restrict_to_common=False, generator=None):
    """
    Creates a DataLoader for the requested dataset split.

    Args:
        restrict_to_common: restrict to videos covered by every sampling method
            (see common_video_ids) so conditions are comparable.
        generator: optional seeded torch.Generator controlling shuffle order, so
            that training runs are reproducible.
    """
    if shuffle is None:
        shuffle = True if split.lower() == 'train' else False

    dataset = EngagementDataset(
        sampling_method, split, data_dir=data_dir,
        binarize_threshold=binarize_threshold,
        restrict_to_common=restrict_to_common,
    )
    dataloader = DataLoader(
        dataset, batch_size=batch_size, shuffle=shuffle, drop_last=False,
        generator=generator,
    )
    return dataloader

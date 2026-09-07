"""
Regression tests for the data-loading defects found during the thesis
remediation. Each test corresponds to a specific defect that silently corrupted
results before being fixed; they exist so the defect cannot return unnoticed.

Run with:  conda run -n thesis-engagenet python -m pytest tests/ -v
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from dataset import (  # noqa: E402
    EngagementDataset,
    common_video_ids,
    SUPPORTED_SAMPLING_METHODS,
    EXPECTED_FEATURE_DIM,
    SNP_LABEL,
)

DATA_DIR = REPO_ROOT / "data" / "processed"
pytestmark = pytest.mark.skipif(
    not DATA_DIR.exists(), reason="processed data not available"
)


# --------------------------------------------------------------------------
# Defect 1: sampling methods were evaluated on different video sets.
# targeted/3-changepoint covered 2227 test videos, 5-/7-changepoint only 2005,
# so sampling comparisons were confounded with test-set composition.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("split", ["train", "test"])
def test_common_restriction_gives_identical_video_sets(split):
    """Every sampling method must cover exactly the same videos when restricted."""
    id_sets = {}
    for method in SUPPORTED_SAMPLING_METHODS:
        ds = EngagementDataset(method, split, binarize_threshold=3,
                               restrict_to_common=True)
        id_sets[method] = set(ds.video_ids)

    reference = id_sets[SUPPORTED_SAMPLING_METHODS[0]]
    for method, ids in id_sets.items():
        # Equality of the sets themselves, not merely of their sizes -- two
        # different 2005-video subsets would still be an invalid comparison.
        assert ids == reference, (
            f"{method} covers a different video set than "
            f"{SUPPORTED_SAMPLING_METHODS[0]} "
            f"(+{len(ids - reference)} / -{len(reference - ids)})"
        )


def test_unrestricted_sets_actually_differ():
    """
    Guards the guard: if the underlying CSVs ever become identical in coverage,
    the restriction test above would pass trivially and stop being meaningful.
    """
    targeted = set(EngagementDataset("targeted", "test", binarize_threshold=3).video_ids)
    five_cp = set(EngagementDataset("5-changepoint", "test", binarize_threshold=3).video_ids)
    assert five_cp < targeted, (
        "Expected 5-changepoint to cover a strict subset of targeted videos. "
        "If this no longer holds, re-check whether restrict_to_common is still needed."
    )


def test_common_video_ids_is_intersection():
    common = common_video_ids("test", data_dir=DATA_DIR, use_cache=False)
    per_method = []
    for method in SUPPORTED_SAMPLING_METHODS:
        frame = pd.read_csv(DATA_DIR / f"{method}-test.csv",
                            usecols=["source_video_path", "label"])
        frame = frame[frame["label"] != SNP_LABEL]
        per_method.append(set(frame["source_video_path"].unique()))
    assert common == set.intersection(*per_method)


# --------------------------------------------------------------------------
# Defect 2: sampling_method='bocpd' silently loaded 3-changepoint data, so
# "BOCPD" results were duplicates rather than an independent condition.
# --------------------------------------------------------------------------

def test_bocpd_raises_rather_than_aliasing():
    with pytest.raises(ValueError, match="bocpd"):
        EngagementDataset("bocpd", "test")


def test_unknown_sampling_method_raises():
    with pytest.raises(ValueError):
        EngagementDataset("definitely-not-a-method", "test")


# --------------------------------------------------------------------------
# Defect 3: frame order depended on CSV row order rather than being enforced.
# The LSTM's entire premise is that input frames are temporally ordered.
# --------------------------------------------------------------------------

def test_sequences_are_frame_ordered(tmp_path):
    """A deliberately row-shuffled CSV must still yield frame-ordered sequences."""
    source = DATA_DIR / "targeted-test.csv"
    frame = pd.read_csv(source, nrows=3000)

    # Keep only videos with a full complement of frames, then shuffle rows so
    # that within-video order is definitely wrong on disk.
    counts = frame.groupby("source_video_path").size()
    keep = counts[counts >= 3].index[:20]
    frame = frame[frame["source_video_path"].isin(keep)]
    shuffled = frame.sample(frac=1.0, random_state=0)
    assert not shuffled.groupby("source_video_path")["frame_id"].apply(
        lambda s: s.is_monotonic_increasing
    ).all(), "test setup failed: rows were not actually shuffled out of order"

    shuffled.to_csv(tmp_path / "targeted-test.csv", index=False)
    ds = EngagementDataset("targeted", "test", data_dir=tmp_path, binarize_threshold=3)

    # Re-derive the expected first-frame features for one video and confirm the
    # dataset picked the lowest frame_id, not the first shuffled row.
    feature_cols = shuffled.columns[5:-1] if "label_idx" in shuffled.columns else shuffled.columns[5:]
    for idx, video_id in enumerate(ds.video_ids):
        group = shuffled[shuffled["source_video_path"] == video_id].sort_values("frame_id")
        expected_first = group[feature_cols].values.astype(np.float32)[0]
        actual_first = ds.sequences[idx][0].numpy()
        assert np.allclose(actual_first, expected_first, atol=1e-5), (
            f"Sequence for {video_id} does not start at the lowest frame_id"
        )
        break  # one video is sufficient; all share the same code path


# --------------------------------------------------------------------------
# Defect 4: feature columns are selected positionally (df.columns[5:-1]), so a
# schema change would silently shift the feature window.
# --------------------------------------------------------------------------

def test_feature_dimensionality_is_asserted():
    ds = EngagementDataset("targeted", "test", binarize_threshold=3)
    assert ds.sequences.shape[-1] == EXPECTED_FEATURE_DIM


def test_max_seq_len_matches_changepoint_count():
    for method, expected in [("targeted", 3), ("3-changepoint", 3),
                             ("5-changepoint", 5), ("7-changepoint", 7)]:
        ds = EngagementDataset(method, "test", binarize_threshold=3)
        assert ds.max_seq_len == expected, f"{method} padded to {ds.max_seq_len}"


# --------------------------------------------------------------------------
# Defect 5: no seeding, so LSTM/MLP results were not reproducible.
# --------------------------------------------------------------------------

def test_set_seed_is_reproducible():
    from train import set_seed

    set_seed(42)
    a = torch.randn(8)
    set_seed(42)
    b = torch.randn(8)
    set_seed(43)
    c = torch.randn(8)

    assert torch.equal(a, b), "same seed produced different tensors"
    assert not torch.equal(a, c), "different seeds produced identical tensors"


# --------------------------------------------------------------------------
# LSTM readout variants (added to test whether mean-pooling the hidden states
# is what erases the temporal advantage).
# --------------------------------------------------------------------------

@pytest.mark.parametrize("readout", ["mean", "last", "attention"])
def test_lstm_readouts_run_and_respect_padding(readout):
    from model import EngagementLSTM

    torch.manual_seed(0)
    model = EngagementLSTM(input_dim=8, hidden_dim=4, num_classes=2,
                           mode="classification", readout=readout)
    model.eval()

    x = torch.randn(3, 5, 8)
    lengths = torch.tensor([5, 3, 1])

    with torch.no_grad():
        out = model(x, lengths)
    assert out.shape == (3, 2)
    assert torch.isfinite(out).all(), f"readout={readout} produced non-finite output"

    # Padding must not affect the result: overwriting positions beyond each
    # sample's valid length should leave the output unchanged.
    x_polluted = x.clone()
    x_polluted[1, 3:, :] = 999.0
    x_polluted[2, 1:, :] = 999.0
    with torch.no_grad():
        out_polluted = model(x_polluted, lengths)
    assert torch.allclose(out, out_polluted, atol=1e-5), (
        f"readout={readout} is reading padded timesteps"
    )


def test_invalid_readout_raises():
    from model import EngagementLSTM
    with pytest.raises(ValueError, match="readout"):
        EngagementLSTM(readout="nonsense")

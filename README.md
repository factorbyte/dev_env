# ML + Quant Development Environment (`mlquant312`)

A ready-to-use Conda environment for **machine learning**, **deep learning (PyTorch + CUDA)**, **image processing**, and **A-share (China stock market) quantitative research**.

Everything is reproducible via two files:

- [`environment.yml`](environment.yml) — Conda bootstrap (Python 3.12 + pip)
- [`requirements.txt`](requirements.txt) — all Python packages, pinned, CUDA 12.8 PyTorch included

---

## What's included

### Scientific computing & machine learning
| Package | Version | Purpose |
|---|---|---|
| NumPy | 2.5.4 | Array / numerical computing |
| pandas | 3.0.6 | Tabular data & time series |
| SciPy | 1.18.1 | Scientific algorithms |
| scikit-learn | 1.9.1 | Classical ML |
| statsmodels | 0.15.0 | Statistics & econometrics |
| XGBoost | 3.4.2 | Gradient boosting |
| LightGBM | 4.7.0 | Gradient boosting |
| Optuna | 5.0.0 | Hyperparameter optimization |

### Deep learning (CUDA-accelerated)
| Package | Version | Purpose |
|---|---|---|
| PyTorch | 2.11.0+cu128 | Deep learning framework (CUDA 12.8) |
| torchvision | 0.26.0+cu128 | Vision models & transforms |
| torchaudio | 2.11.0+cu128 | Audio processing |
| timm | 1.0.30 | Pretrained vision models |
| transformers | 5.20.1 | Hugging Face models (NLP / CV) |
| cuDNN | 9.19.0 | GPU acceleration backend |

### Image processing
| Package | Version | Purpose |
|---|---|---|
| opencv-python | 5.0.0 | Computer vision |
| albumentations | 2.0.8 | Image augmentation |
| Pillow | 12.3.0 | Image I/O |
| scikit-image | 0.26.0 | Image algorithms |

### A-share quantitative
| Package | Version | Purpose |
|---|---|---|
| exchange-calendars | 4.13.2 | XSHG/XSHE trading calendar |
| akshare | 1.19.1 | Market / fundamental data |
| baostock | 0.9.4 | Market data (free) |
| vectorbt | 1.1.2 | Vectorized backtesting |

### Data & developer tooling
| Package | Version | Purpose |
|---|---|---|
| polars | 2.0.0 | Fast DataFrame engine |
| PyArrow | 25.0.0 | Columnar data |
| DuckDB | 1.5.6 | Embedded analytical DB |
| SQLAlchemy | 2.1.5 | SQL toolkit |
| JupyterLab | 4.6.4 | Interactive notebooks |
| pytest / mypy / ruff / pre-commit / loguru | — | Testing, typing, linting, logging |

---

## Hardware requirements

- **NVIDIA GPU** with a driver supporting **CUDA 12.8** (Ampere or newer recommended).
- Tested on: **RTX 3060 Laptop 6 GB** (compute capability 8.6).
- ~6 GB disk for the base install (the PyTorch wheel alone is ~2.7 GB).

> CPU-only machines will also install and run, but `torch.cuda.is_available()` will return `False`.

---

## Installation

### 1. Create the environment

```bash
conda env create -f environment.yml
conda activate mlquant312
```

### 2. Install Python packages

```bash
pip install -r requirements.txt
```

> `requirements.txt` starts with
> `--extra-index-url https://download.pytorch.org/whl/cu128`, because
> **CUDA-enabled PyTorch is not published on PyPI** — it lives on the official
> PyTorch CUDA 12.8 index.

### 3. Verify

```bash
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

Expected output on a GPU machine:

```
2.11.0+cu128 True
```

---

## Key design decisions & gotchas

### 1. Everything is installed via `pip`, not Conda-forge's MKL builds

This is **intentional** and the single most important decision in this environment.

Conda-forge's default NumPy/SciPy/scikit-learn builds are linked against **Intel MKL**,
which ships a `libiomp5md.dll` (Intel OpenMP) that **conflicts** with the one bundled
inside pip-installed PyTorch. The symptom is a hard crash on import:

```
OSError: [WinError 127] ... Error loading "torch\lib\shm.dll" or one of its dependencies
```

Installing NumPy/SciPy/scikit-learn from **pip (OpenBLAS build)** avoids MKL entirely
and makes the two stacks coexist cleanly. `environment.yml` therefore only bootstraps
Python + pip, and `nodefaults` excludes the Anaconda `defaults` channel (which also
pulls MKL and requires accepting a Terms-of-Service prompt in recent Conda versions).

### 2. PyTorch CUDA build comes from a separate index

- PyPI's `torch` on Windows is **CPU-only**.
- The CUDA build is `torch==2.11.0+cu128` from `https://download.pytorch.org/whl/cu128`.
- Do **not** change the `+cu128` local-version suffix — that suffix is what forces pip
  to pick the CUDA wheel instead of the CPU wheel.

### 3. Python 3.12 (not newer)

`environment.yml` pins `python=3.12`. Some compiled packages (notably **numba**) lag
behind on the newest Python releases, so 3.12 is the safest common denominator.

### 4. numba is sensitive to NumPy versions

`numba==0.68.0` is paired with `numpy==2.5.4`. If you bump NumPy, verify numba still
imports (numba checks the NumPy ABI at runtime and will refuse to run on an
unsupported version).

---

## Troubleshooting

### Downloads are slow in mainland China

`download.pytorch.org` can be slow from China. Use a domestic mirror for the PyTorch
wheels, e.g. install torch separately:

```bash
pip install torch==2.11.0+cu128 torchvision==0.26.0+cu128 torchaudio==2.11.0+cu128 \
    -i https://mirrors.aliyun.com/pytorch-wheels/cu128
```

or configure a PyPI mirror (`https://pypi.tuna.tsinghua.edu.cn/simple`) for the rest.

### `torch.cuda.is_available()` returns `False`

1. Check the driver: `nvidia-smi` — the "CUDA Version" line must be **≥ 12.8**.
2. Confirm you installed the `+cu128` wheel (not the CPU wheel).
3. Make sure the GPU is not hidden by another process (e.g. `CUDA_VISIBLE_DEVICES`).

### `opencv-python` and `opencv-python-headless`

`albumentations` depends on `opencv-python-headless`. If you need GUI features such as
`cv2.imshow`, keep `opencv-python`; if you run headless (server / CI), uninstall
`opencv-python` to avoid the two packages shadowing each other.

---

## Repository layout

```
dev_env/
├── environment.yml     # Conda environment spec (Python 3.12 + pip)
├── requirements.txt    # All Python packages, pinned, incl. CUDA PyTorch
├── .gitignore          # Ignores caches, IDE config, data, model weights, secrets
└── README.md
```

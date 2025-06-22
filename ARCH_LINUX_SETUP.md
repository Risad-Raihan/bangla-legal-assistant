# 🐧 Arch Linux Setup Guide

This guide is specifically for Arch Linux users who want to run the Bangladesh Legal Assistant without GPU support.

## 📋 Prerequisites

### System Dependencies

Install required system packages:

```bash
# Update system
sudo pacman -Syu

# Install Python and development tools
sudo pacman -S python python-pip python-virtualenv git

# Install system dependencies for compilation
sudo pacman -S base-devel gcc cmake

# Optional: Install fonts for better Bengali rendering
sudo pacman -S noto-fonts noto-fonts-extra
```

## 🚀 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Risad-Raihan/bangla-legal-assistant.git
cd bangla-legal-assistant
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv legal_env

# Activate it
source legal_env/bin/activate
```

### 3. Install Dependencies (CPU-only)

**Option A: Use CPU-optimized requirements**
```bash
pip install -r requirements-cpu.txt
```

**Option B: Use standard requirements**
```bash
pip install -r requirements.txt
```

**Option C: Force CPU-only PyTorch (if needed)**
```bash
# Install CPU-only PyTorch first
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Then install other requirements
pip install -r requirements.txt
```

### 4. Set Environment Variables

```bash
# Create .env file with your API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### 5. Run the Application

```bash
streamlit run app.py
```

## 🔧 Arch Linux Specific Optimizations

### Performance Tips

1. **Use faster package mirrors:**
```bash
sudo pacman-mirrors --fasttrack
```

2. **Install optional math libraries for better performance:**
```bash
sudo pacman -S openblas lapack
```

3. **Enable parallel compilation:**
```bash
export MAKEFLAGS="-j$(nproc)"
```

### Troubleshooting

#### Issue: Package compilation errors
```bash
# Install additional development packages
sudo pacman -S python-setuptools python-wheel

# Or use pre-compiled wheels
pip install --only-binary=all -r requirements-cpu.txt
```

#### Issue: FAISS installation problems
```bash
# Use conda instead of pip for FAISS (optional)
sudo pacman -S miniconda3
conda install -c conda-forge faiss-cpu
```

#### Issue: Memory usage on large PDFs
```bash
# Increase virtual memory if needed
sudo sysctl vm.max_map_count=262144
```

## 🚀 Performance Considerations

### CPU Optimization

The application will automatically use all available CPU cores. For better performance:

1. **Set CPU affinity (optional):**
```bash
# Run with all cores
taskset -c 0-$(nproc --all) streamlit run app.py
```

2. **Increase system limits:**
```bash
# Add to /etc/security/limits.conf
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf
```

### Memory Management

For systems with limited RAM:

1. **Use swap file:**
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

2. **Configure environment for low memory:**
```bash
# Add to .env file
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
export OMP_NUM_THREADS=4
```

## 🔄 Updates

To update the application:

```bash
cd bangla-legal-assistant
git pull origin main
source legal_env/bin/activate
pip install -r requirements-cpu.txt --upgrade
```

## 🆘 Getting Help

If you encounter Arch Linux specific issues:

1. Check [Arch Wiki](https://wiki.archlinux.org/title/Python)
2. Visit [AUR packages](https://aur.archlinux.org/)
3. Open an issue on our [GitHub repository](https://github.com/Risad-Raihan/bangla-legal-assistant/issues)

---

**Note:** This application has been tested on Arch Linux with Python 3.11+ and works without GPU acceleration. 
import numpy as np
import struct
import matplotlib.pyplot as plt

num_samples = 1000000


uniform_data = np.random.uniform(low=0.1, high=500.0, size=num_samples).astype(np.float32)
gaussian_data = np.random.normal(loc=50.0, scale=175.0, size=num_samples).astype(np.float32)
exponential_data = np.random.exponential(scale=180.0, size=num_samples).astype(np.float32)

def lossy_compression(data, bits_to_zero=16):
    compressed_data = np.empty_like(data, dtype=np.float32)
    
    for i, num in enumerate(data):
        int_rep = struct.unpack('>I', struct.pack('>f', num))[0]
        
        # making the bits zero
        int_rep &= ~((1 << bits_to_zero) - 1)
        
        compressed_data[i] = struct.unpack('>f', struct.pack('>I', int_rep))[0]
    
    return compressed_data

# Apply lossy compression
compressed_uniform = lossy_compression(uniform_data, bits_to_zero=16)
compressed_gaussian = lossy_compression(gaussian_data, bits_to_zero=16)
compressed_exponential = lossy_compression(exponential_data, bits_to_zero=16)

# Saving original and compressed data to binary files
def save_binary(filename, data):
    with open(filename, 'wb') as f:
        f.write(data.tobytes())

save_binary('uniform_original.bin', uniform_data)
save_binary('uniform_compressed.bin', compressed_uniform)
save_binary('gaussian_original.bin', gaussian_data)
save_binary('gaussian_compressed.bin', compressed_gaussian)
save_binary('exponential_original.bin', exponential_data)
save_binary('exponential_compressed.bin', compressed_exponential)

# Measuring and comparing file sizes
import os
def get_file_size(filename):
    return os.path.getsize(filename) / 1024  # KB

print(f"Uniform original: {get_file_size('uniform_original.bin'):.2f} KB, Compressed: {get_file_size('uniform_compressed.bin'):.2f} KB")
print(f"Gaussian original: {get_file_size('gaussian_original.bin'):.2f} KB, Compressed: {get_file_size('gaussian_compressed.bin'):.2f} KB")
print(f"Exponential original: {get_file_size('exponential_original.bin'):.2f} KB, Compressed: {get_file_size('exponential_compressed.bin'):.2f} KB")

# Comparing statistical parameters
def compare_statistics(original, compressed, name):
    print(f"\n{name} Distribution:")
    print(f"Mean - Original: {np.mean(original):.6f}, Compressed: {np.mean(compressed):.6f}")
    print(f"Std Dev - Original: {np.std(original):.6f}, Compressed: {np.std(compressed):.6f}")
    print(f"Min - Original: {np.min(original):.6f}, Compressed: {np.min(compressed):.6f}")
    print(f"Max - Original: {np.max(original):.6f}, Compressed: {np.max(compressed):.6f}")
    print(f"MSE: {np.mean((original - compressed) ** 2):.6e}")

compare_statistics(uniform_data, compressed_uniform, "Uniform")
compare_statistics(gaussian_data, compressed_gaussian, "Gaussian")
compare_statistics(exponential_data, compressed_exponential, "Exponential")

# plots
def plot_distributions(original, compressed, title):
    plt.figure(figsize=(10, 5))
    plt.hist(original, bins=100, alpha=0.5, label='Original', density=True)
    plt.hist(compressed, bins=100, alpha=0.5, label='Compressed', density=True)
    plt.title(title)
    plt.legend()
    plt.show()

plot_distributions(uniform_data, compressed_uniform, "Uniform Distribution")
plot_distributions(gaussian_data, compressed_gaussian, "Gaussian Distribution")
plot_distributions(exponential_data, compressed_exponential, "Exponential Distribution")

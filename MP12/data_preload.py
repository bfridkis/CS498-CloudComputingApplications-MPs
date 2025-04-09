import torchvision.datasets as dsets

if __name__ == "__main__":
    dsets.MNIST(root='/usr/src/app/data', download=True)
    dsets.KMNIST(root='/usr/src/app/data', download=True)

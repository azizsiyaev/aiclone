import torch


def main():
    device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')


if __name__ == '__main__':
    main()
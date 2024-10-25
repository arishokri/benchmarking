## Background
* For all CPU tests a fibonacci of 45 is being calculated.
* For all GPU_tf tests a matrix of 20,000^4 is being converted.
* For all GPU_pt tests matrix size is 15,000^2 and iteration size is 100.
* For WSL2 setting, because of Beelink's smaller usable RAM, I had to reduce the matrix size to 15000^4.

## Asus Rig Corei9-12900k RTX 3090Ti
|         | CPU | GPU_tf | GPU_pt |
|---------|-----|--------|--------|
| Pop! OS |     |   N/A  |        |
| WSL2    | 77s |   N/A  |   24s  |


## Beelink Ryzen 7 5800h
|         | CPU  | GPU_tf |
|---------|------|--------|
| Pop! OS | 108s |   26s  |
| WSL2    | 107s |   14s  |

## Asus Duo Ultra 7 155h
|         | CPU | GPU_tf |
|---------|-----|--------|
| Ubuntu  | 94s |   37s  |
| WSL2    | 83s |   10s  |

## Asus Duo Ultra 9 185h
|         | CPU | GPU_tf |
|---------|-----|--------|
| WSL2    | 79s |   9s   |

## HP Dragonfly
|         | CPU | GPU_tf |
|---------|-----|--------|
| WSL2    | 110 |   12s  |

## Macbook Pro M3 Pro
|         | CPU |  GPU_tf |
|---------|-----| --------|
| Battery | 110 |  <0.1s  |
| Plugged | 170 |  <0.1s  |

## Macbook Air M3
|         | CPU | GPU_tf | GPU_pt |
|---------|-----|--------|--------|
| Battery |     |   N/A  |  303s  |
| Plugged |     |        |   9s   |
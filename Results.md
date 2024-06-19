## Background
* For all CPU tests a fibonacci of 45 is being calculated.
* For all GPU tests a matrix of 20000^4 is being converted.
* For WSL2 setting, because of Beelink's smaller usable RAM, I had to reduce the matrix size to 15000^4.

## Beelink Ryzen 7 5800h
|         | CPU  | GPU |
|---------|------|-----|
| Pop! OS | 108s | 26s |
| WSL2    | 107s | 14s |

## Asus Duo Ultra 7 155h
|         | CPU | GPU |
|---------|-----|-----|
| Ubuntu  | 94s | 37s |
| WSL2    | 83s | 10s |

## Asus Duo Ultra 9 185h
|         | CPU | GPU |
|---------|-----|-----|
| WSL2    | 79s | 9s  |

## HP Dragonfly
|         | CPU | GPU |
|---------|-----|-----|
| WSL2    | 110 | 12s |

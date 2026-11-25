### Reproduction checks (household arm, `median_mid`, 124c schedule tau_0 0.04, tau_m 0.7, k_ln 1, ratio 0.5)

| quantity | this script | stored | |
|---|---|---|---|
| 124c fixed rates, constant path 4.74%: M1 short | 1.56280857086 | 1.56280857086 | equal |
| 124c fixed rates, constant path 4.74%: M1d short | 4.41146778895 | 4.41146778895 | equal |
| 124c fixed rates, constant path 4.74%: M1 long | -0.301572376926 | -0.301572376926 | equal |
| 124c fixed rates, constant path 4.74%: M1d long | 4.74 | 4.74 | equal |
| 128c market paths, seed 1, 1000 paths: M1 short | -0.144931146975 | -0.144931146975 | equal |
| 128c market paths, seed 1, 1000 paths: M1d short | 5.8658913844 | 5.8658913844 | equal |
| 128c market paths, seed 1, 1000 paths: M1 long | -2.76740213161 | -2.77017925837 | differs: the lien of 132c/133c, which came after the 128c file (long horizon only) |
| 128c market paths, seed 1, 1000 paths: M1d long | 7.53473772781 | 7.53473772781 | equal |

Every check holds (the short horizon, which F1 and CK1 read, is equal everywhere).

### Reproduction checks (household arm, `median_mid`, 124c schedule tau_0 0.04, tau_m 0.7, k_ln 1, ratio 0.5)

| quantity | this script | stored | |
|---|---|---|---|
| 124c fixed rates, constant path 4.74%: M1 short | 1.40895993505 | 1.56280857086 | DIFFERENT |
| 124c fixed rates, constant path 4.74%: M1d short | 4.24332221845 | 4.41146778895 | DIFFERENT |
| 124c fixed rates, constant path 4.74%: M1 long | -0.301572376926 | -0.301572376926 | equal |
| 124c fixed rates, constant path 4.74%: M1d long | 4.74 | 4.74 | equal |
| 128c market paths, seed 1, 1000 paths: M1 short | 0.0589618242617 | -0.0650120704351 | DIFFERENT |
| 128c market paths, seed 1, 1000 paths: M1d short | 5.8465871328 | 5.8952261882 | DIFFERENT |
| 128c market paths, seed 1, 1000 paths: M1 long | -2.68499134813 | -2.74139615108 | differs: the lien of 132c/133c, which came after the 128c file (long horizon only) |
| 128c market paths, seed 1, 1000 paths: M1d long | 7.53552780732 | 7.58504648377 | differs: the lien of 132c/133c, which came after the 128c file (long horizon only) |

A CHECK FAILED.

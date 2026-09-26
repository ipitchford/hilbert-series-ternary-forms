/* methodAd with packed storage: the same weight-counting algorithm as methodAd.c, but layer m stores only the
   hexagon {A, B, C in [0, L], A + B + C = d m} row by row, about a third of methodAd's memory. It exists so that
   d = 8 can be run to degree 1194 on a 16 GB machine. Output must be byte-identical to methodAd wherever both run.
   Usage: methodAd2 d N p   (p prime, p < 65536) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int d, N, L;
static long *rowoff;           /* rowoff[m*(L+1)+A] = start of row A in layer m, or -1 if the row is empty */
static int *blo, *bhi;         /* valid B range of row (m, A) */
static uint16_t *f;
static inline long idx(int m, int A, int B) {
  if (m < 0 || A < 0 || A > L || B < 0) return -1;
  long k = (long)m * (L + 1) + A;
  if (rowoff[k] < 0 || B < blo[k] || B > bhi[k]) return -1;
  return rowoff[k] + (B - blo[k]);
}
int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: methodAd2 d N p\n"); return 1; }
  d = atoi(argv[1]); N = atoi(argv[2]); uint32_t p = (uint32_t)strtoul(argv[3], 0, 10);
  if (p < 2 || p > 65535) { fprintf(stderr, "p must be below 65536\n"); return 1; }
  for (uint32_t q = 2; q * q <= p; q++) if (p % q == 0) { fprintf(stderr, "p must be prime\n"); return 1; }
  L = d * N / 3 + 2;
  long rows = (long)(N + 1) * (L + 1), total = 0;
  rowoff = malloc(rows * sizeof(long)); blo = malloc(rows * sizeof(int)); bhi = malloc(rows * sizeof(int));
  if (!rowoff || !blo || !bhi) { fprintf(stderr, "oom\n"); return 1; }
  for (int m = 0; m <= N; m++) for (int A = 0; A <= L; A++) {
    long k = (long)m * (L + 1) + A; int s = d * m - A;          /* B + C = s */
    int lo = s - L; if (lo < 0) lo = 0; int hi = s; if (hi > L) hi = L;
    if (s < 0 || lo > hi) { rowoff[k] = -1; blo[k] = 1; bhi[k] = 0; continue; }
    rowoff[k] = total; blo[k] = lo; bhi[k] = hi; total += hi - lo + 1;
  }
  fprintf(stderr, "methodAd2: %ld cells (%.2f GB)\n", total, total * 2.0 / 1e9);
  f = calloc((size_t)total, sizeof(uint16_t));
  if (!f) { fprintf(stderr, "oom\n"); return 1; }
  f[idx(0, 0, 0)] = 1;
  for (int a = 0; a <= d; a++) for (int b = 0; a + b <= d; b++) {
    for (int m = 1; m <= N; m++) {
      #pragma omp parallel for schedule(static)
      for (int A = a; A <= L; A++) {
        long k = (long)m * (L + 1) + A; if (rowoff[k] < 0) continue;
        for (int B = (blo[k] > b ? blo[k] : b); B <= bhi[k]; B++) {
          long j = idx(m - 1, A - a, B - b); if (j < 0) continue;
          uint32_t x = (uint32_t)f[rowoff[k] + B - blo[k]] + f[j]; if (x >= p) x -= p;
          f[rowoff[k] + B - blo[k]] = (uint16_t)x;
        }
      }
    }
  }
  #define F(m, A, B) ({ long _j = idx((m), (A), (B)); _j < 0 ? 0u : (uint32_t)f[_j]; })
  for (int n = 0; n <= N; n++) {
    uint64_t r = 0;
    if ((d * n) % 3 == 0) { int k = d * n / 3, m = n;
      uint64_t pos = (uint64_t)F(m, k, k) + F(m, k - 1, k - 1) + F(m, k - 2, k + 1);
      uint64_t neg = (uint64_t)F(m, k - 1, k + 1) + F(m, k, k - 1) + F(m, k - 2, k);
      r = (pos % p + (uint64_t)3 * p - neg % p) % p;
    }
    printf("%d %llu\n", n, (unsigned long long)r);
  }
  return 0;
}

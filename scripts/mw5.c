/* No aliasing: exponents satisfy |m_i| <= d n + 4 (weights d n, Weyl numerator 4) and Lemma 3 (Lemma 2.1 in drafts) needs |m_i| < M;
   the enforced M >= 2(dL+2)+1 > dL+4 suffices.
   Faster exact Molien-Weyl engine for SL3-invariants of ternary d-ics (same maths as mw3.c).
   - Montgomery arithmetic modulo p < 2^62 (no 128-bit division);
   - grid points processed in batches of B along j so the geometric-series recurrences
     s[n] += x*s[n-1] of B independent points interleave (hides multiply latency).
   Usage: mw5 d L p M  (S3-orbit version: sums one representative e1<e2<e3 per orbit of distinct exponent triples, times 6)  -> L+1 residues a_0..a_L mod p (ordinary representation). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
#define B 32
static u64 P, PINV, R2;   /* PINV = -p^{-1} mod 2^64, R2 = 2^128 mod p */
static inline u64 redc(u128 t){ u64 m=(u64)t*PINV; u128 u=(t+(u128)m*P)>>64; u64 r=(u64)u; return r>=P?r-P:r; }
static inline u64 mm(u64 a,u64 b){ return redc((u128)a*b); }
static inline u64 add(u64 a,u64 b){u64 c=a+b; return c>=P?c-P:c;}
static inline u64 tomont(u64 a){ return mm(a%P,R2); }
static inline u64 frommont(u64 a){ return redc(a); }
static u64 powm_plain(u64 a,u64 e){ u128 r=1,x=a%P; while(e){ if(e&1) r=r*x%P; x=x*x%P; e>>=1;} return (u64)r; }
int main(int argc,char**argv){
  int d=atoi(argv[1]), L=atoi(argv[2]); P=strtoull(argv[3],0,10); long M=atol(argv[4]);
  if((P-1)%M||P>=(1ULL<<62)){fprintf(stderr,"bad p\n");return 1;}
  if(M < 2L*(d*(long)L+2)+1){fprintf(stderr,"M too small\n");return 1;}
  u64 inv=1; for(int k=0;k<6;k++) inv*=2-P*inv; PINV=(u64)(-inv);
  { u128 r=((u128)1<<64)%P; R2=(u64)(r*r%P); }
  u64 w=0;
  for(u64 g=2;;g++){ u64 c=powm_plain(g,(P-1)/M); long m=M; int ok=1;
    for(long q=2;q*q<=m;q++) if(m%q==0){ if(powm_plain(c,M/q)==1) ok=0; while(m%q==0) m/=q; }
    if(m>1 && powm_plain(c,M/m)==1) ok=0; if(ok){w=c;break;} }
  u64 *pw=malloc(sizeof(u64)*M); u64 wm=tomont(w); pw[0]=tomont(1); for(long k=1;k<M;k++) pw[k]=mm(pw[k-1],wm);
  u64 one=tomont(1);
  u64 *omp_=malloc(sizeof(u64)*M); for(long k=0;k<M;k++) omp_[k]=add(one, P-pw[k]==P?0:P-pw[k]); /* 1 - w^k in Montgomery */
  if((d+1)*(d+2)/2>64){fprintf(stderr,"d too large for weight arrays\n");return 1;}
  int nw=0; int U[64],V[64];
  for(int a=0;a<=d;a++) for(int b=0;a+b<=d;b++){int c=d-a-b; U[nw]=a-c; V[nw]=b-c; nw++;}
  int nt=omp_get_max_threads();
  u64 *accs=calloc((size_t)nt*(L+1),sizeof(u64));
  #pragma omp parallel
  { int tid=omp_get_thread_num(); u64 *acc=accs+(size_t)tid*(L+1);
    u64 *s=aligned_alloc(64,sizeof(u64)*(size_t)(L+1)*B); u64 x[B], W[B]; long jj[B];
    #pragma omp for schedule(dynamic,4)
    for(long i=0;i<M;i++){
      long j0=i+1;
      while(j0<M){
        int nb=0;
        for(;j0<M && nb<B;j0++){ long j=j0, e3=((-i-j)%M+M)%M;
          if(!(i<j && j<e3)) continue;              /* one representative per S3-orbit */
          long E[3]={i,j,e3}; u64 Wv=one;
          for(int a=0;a<3;a++) for(int b=0;b<3;b++) if(a!=b) Wv=mm(Wv,omp_[((E[a]-E[b])%M+M)%M]);
          W[nb]=Wv; jj[nb]=j; nb++; }
        if(!nb) break;
        for(int b=0;b<nb;b++) s[b]=one; for(size_t q=B;q<(size_t)(L+1)*B;q++) s[q]=0;
        for(int k=0;k<nw;k++){
          for(int b=0;b<nb;b++){ long ex=(((long)U[k]*i+(long)V[k]*jj[b])%M+M)%M; x[b]=pw[ex]; }
          for(int n=1;n<=L;n++){ u64 *cur=s+(size_t)n*B, *prv=s+(size_t)(n-1)*B;
            for(int b=0;b<nb;b++) cur[b]=add(cur[b],mm(x[b],prv[b])); }
        }
        for(int n=0;n<=L;n++){ u64 *cur=s+(size_t)n*B; u64 t=acc[n];
          for(int b=0;b<nb;b++) t=add(t,mm(W[b],cur[b])); acc[n]=t; }
      }
    }
    free(s); }
  u64 scale=powm_plain((u64)((u128)(M%P)*(M%P)%P),P-2);   /* 6 orbit elements / |W| = 1 */
  for(int n=0;n<=L;n++){ u64 t=0; for(int k=0;k<nt;k++) t=add(t,accs[(size_t)k*(L+1)+n]);
    u64 v=frommont(t); printf("%llu\n",(unsigned long long)(u64)((u128)v*scale%P)); }
  return 0; }

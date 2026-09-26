/* No aliasing: the t^n coefficient has exponents |m_i| <= d n + 4 (weights contribute d n, the Weyl numerator 4);
   Lemma 3 (Lemma 2.1 in drafts) needs |m_i| < M, so M >= 2(dL+2)+1 > dL+4 is sufficient.
   mw6: 32-bit Montgomery version of mw5 (S3-orbit Molien-Weyl engine for ternary d-ics), p < 2^31.
   Same mathematics as mw5.c; lanes of a batch are independent so the inner loop vectorises (NEON umull).
   Usage: mw6 d L p M -> L+1 residues mod p. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <omp.h>
typedef uint32_t u32; typedef uint64_t u64;
#define B 64
static u32 P, PINV; static u64 R2;
static inline u32 mm(u32 a,u32 b){ u64 t=(u64)a*b; u32 m=(u32)t*PINV; u64 u=(t+(u64)m*P)>>32; u32 r=(u32)u; return r>=P?r-P:r; }
static inline u32 add(u32 a,u32 b){ u32 c=a+b; return c>=P?c-P:c; }
static u64 powm(u64 a,u64 e,u64 p){ u64 r=1; a%=p; while(e){ if(e&1) r=r*a%p; a=a*a%p; e>>=1;} return r; }
static inline u32 tomont(u64 a){ return mm((u32)(a%P),(u32)R2); }
int main(int argc,char**argv){
  int d=atoi(argv[1]), L=atoi(argv[2]); u64 p=strtoull(argv[3],0,10); long M=atol(argv[4]);
  if(p>=(1ULL<<31)||(p-1)%M){fprintf(stderr,"bad p\n");return 1;}
  if(M < 2L*(d*(long)L+2)+1){fprintf(stderr,"M too small\n");return 1;}
  P=(u32)p; u32 inv=1; for(int k=0;k<5;k++) inv*=2-P*inv; PINV=(u32)(-inv);
  R2=((1ULL<<32)%p)*((1ULL<<32)%p)%p;
  u64 w=0;
  for(u64 g=2;;g++){ u64 c=powm(g,(p-1)/M,p); long m=M; int ok=1;
    for(long q=2;q*q<=m;q++) if(m%q==0){ if(powm(c,M/q,p)==1) ok=0; while(m%q==0) m/=q; }
    if(m>1 && powm(c,M/m,p)==1) ok=0; if(ok){w=c;break;} }
  u32 *pw=malloc(sizeof(u32)*M); { u64 x=1; for(long k=0;k<M;k++){ pw[k]=tomont(x); x=x*w%p; } }
  u32 one=tomont(1);
  u32 *om=malloc(sizeof(u32)*M); for(long k=0;k<M;k++) om[k]=add(one,(u32)((P-pw[k])%P));
  if((d+1)*(d+2)/2>64){fprintf(stderr,"d too large for weight arrays\n");return 1;}
  int nw=0; int U[64],V[64];
  for(int a=0;a<=d;a++) for(int b=0;a+b<=d;b++){int c=d-a-b; U[nw]=a-c; V[nw]=b-c; nw++;}
  int nt=omp_get_max_threads();
  u32 *accs=calloc((size_t)nt*(L+1),sizeof(u32));
  #pragma omp parallel
  { int tid=omp_get_thread_num(); u32 *acc=accs+(size_t)tid*(L+1);
    u32 *s=aligned_alloc(64,sizeof(u32)*(size_t)(L+1)*B); u32 x[B] __attribute__((aligned(64))), W[B]; long jj[B];
    #pragma omp for schedule(dynamic,4)
    for(long i=0;i<M;i++){
      long j0=i+1;
      while(j0<M){
        int nb=0;
        for(;j0<M && nb<B;j0++){ long j=j0, e3=((-i-j)%M+M)%M;
          if(!(i<j && j<e3)) continue;
          long E[3]={i,j,e3}; u32 Wv=one;
          for(int a=0;a<3;a++) for(int b=0;b<3;b++) if(a!=b) Wv=mm(Wv,om[((E[a]-E[b])%M+M)%M]);
          W[nb]=Wv; jj[nb]=j; nb++; }
        if(!nb) break;
        for(int b=0;b<B;b++){ s[b]= b<nb?one:0; }
        for(size_t q=B;q<(size_t)(L+1)*B;q++) s[q]=0;
        for(int k=0;k<nw;k++){
          for(int b=0;b<B;b++){ long ex= b<nb ? ((((long)U[k]*i+(long)V[k]*jj[b])%M+M)%M) : 0; x[b]=pw[ex]; }
          for(int n=1;n<=L;n++){ u32 *cur=s+(size_t)n*B, *prv=s+(size_t)(n-1)*B;
            #pragma omp simd
            for(int b=0;b<B;b++) cur[b]=add(cur[b],mm(x[b],prv[b])); }
        }
        for(int n=0;n<=L;n++){ u32 *cur=s+(size_t)n*B; u32 t=acc[n];
          for(int b=0;b<nb;b++) t=add(t,mm(W[b],cur[b])); acc[n]=t; }
      }
    }
    free(s); }
  u64 scale=powm((M%p)*(M%p)%p,p-2,p);
  for(int n=0;n<=L;n++){ u32 t=0; for(int k=0;k<nt;k++) t=add(t,accs[(size_t)k*(L+1)+n]);
    u64 v=mm(t,1);  /* from Montgomery */
    printf("%llu\n",(unsigned long long)(v*scale%p)); }
  return 0; }

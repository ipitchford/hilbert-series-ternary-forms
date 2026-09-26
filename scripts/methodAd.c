/* Weight counting for Sym^n(Sym^d C^3) mod p (p < 65536, 16-bit storage), then the Weyl alternating sum for the
   multiplicity of det^{k}, k = d n / 3 (zero unless 3 | d n). Generalises independent/methodA16.c (d = 7) to any d.
   State f[m][A][B] = number of multisets of m weights (a,b,c), a+b+c = d, with total weight (A, B, C = d m - A - B).
   Usage: methodAd d N p */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage: methodAd d N p\n");return 1;}
  int d=atoi(argv[1]), N=atoi(argv[2]); uint32_t p=(uint32_t)strtoul(argv[3],0,10);
  if(p<2||p>65535){fprintf(stderr,"p must be below 65536\n");return 1;}
  for(uint32_t q=2;q*q<=p;q++) if(p%q==0){fprintf(stderr,"p must be prime\n");return 1;}
  int L=d*N/3+2; long S=L+1; long plane=S*S;
  uint16_t *f=calloc((size_t)(N+1)*plane,sizeof(uint16_t));
  if(!f){fprintf(stderr,"oom\n");return 1;}
  f[0]=1;
  for(int a=0;a<=d;a++)for(int b=0;a+b<=d;b++){
    for(int m=1;m<=N;m++){
      uint16_t *cur=f+(size_t)m*plane,*prev=f+(size_t)(m-1)*plane;
      #pragma omp parallel for schedule(static)
      for(int A=a;A<=L;A++){
        int Blo=d*m-A-L; if(Blo<b)Blo=b; int Bhi=d*m-A; if(Bhi>L)Bhi=L;
        uint16_t *row=cur+(size_t)A*S; const uint16_t *src=prev+(size_t)(A-a)*S-b;
        for(int B=Blo;B<=Bhi;B++){ uint32_t x=row[B]+src[B]; if(x>=p)x-=p; row[B]=x; }
      }
    }
  }
  #define F(m,A,B,C) (((A)<0||(B)<0||(C)<0||(A)>L||(B)>L||(C)>L)?0u:f[(size_t)(m)*plane+(size_t)(A)*S+(B)])
  for(int n=0;n<=N;n++){
    uint64_t r=0;
    if((d*n)%3==0){int k=d*n/3; int m=n;
      uint64_t pos=(uint64_t)F(m,k,k,k)+F(m,k-1,k-1,k+2)+F(m,k-2,k+1,k+1);
      uint64_t neg=(uint64_t)F(m,k-1,k+1,k)+F(m,k,k-1,k+1)+F(m,k-2,k,k+2);
      r=(pos%p+(uint64_t)3*p-neg%p)%p;
    }
    printf("%d %llu\n",n,(unsigned long long)r);
  }
  return 0;
}

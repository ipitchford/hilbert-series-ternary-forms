/* Method A: weight-multiplicity DP for Sym^n(Sym^7 C^3) mod p, then
   Weyl/Kostant alternating sum to extract multiplicity of det^{k} (k=7n/3).
   State f[m][A][B] = # multisets of m weights of Sym^7 C^3 (weights (a,b,c), a+b+c=7)
   with total weight (A,B,C), C = 7m-A-B. Only A,B,C <= L are stored/needed
   (weights are nonnegative so coordinates only grow; targets have coords <= 7N/3+2). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
int main(int argc,char**argv){
  if(argc<3){fprintf(stderr,"usage: methodA16 N p   (p prime, p < 65536)\n");return 1;}
  int N=atoi(argv[1]); uint32_t p=(uint32_t)strtoul(argv[2],0,10);
  if(p<2||p>65535){fprintf(stderr,"p must be below 65536 (16-bit storage)\n");return 1;}
  for(uint32_t q=2;q*q<=p;q++) if(p%q==0){fprintf(stderr,"p must be prime\n");return 1;}
  int L=7*N/3+2; long S=L+1; long plane=S*S;
  uint16_t *f=calloc((size_t)(N+1)*plane,sizeof(uint16_t));
  if(!f){fprintf(stderr,"oom\n");return 1;}
  f[0]=1;
  for(int a=0;a<=7;a++)for(int b=0;a+b<=7;b++){int c=7-a-b;
    for(int m=1;m<=N;m++){
      uint16_t *cur=f+(size_t)m*plane,*prev=f+(size_t)(m-1)*plane;
      #pragma omp parallel for schedule(static)
      for(int A=a;A<=L;A++){
        int Blo=7*m-A-L; if(Blo<b)Blo=b; int Bhi=7*m-A; if(Bhi>L)Bhi=L;
        uint16_t *row=cur+(size_t)A*S; const uint16_t *src=prev+(size_t)(A-a)*S-b;
        for(int B=Blo;B<=Bhi;B++){ uint32_t x=row[B]+src[B]; if(x>=p)x-=p; row[B]=x; }
      }
      (void)c;
    }
  }
  #define F(m,A,B,C) (((A)<0||(B)<0||(C)<0||(A)>L||(B)>L||(C)>L)?0u:f[(size_t)(m)*plane+(size_t)(A)*S+(B)])
  for(int n=0;n<=N;n++){
    uint64_t r=0;
    if(n%3==0){int k=7*n/3; int m=n;
      uint64_t pos=(uint64_t)F(m,k,k,k)+F(m,k-1,k-1,k+2)+F(m,k-2,k+1,k+1);
      uint64_t neg=(uint64_t)F(m,k-1,k+1,k)+F(m,k,k-1,k+1)+F(m,k-2,k,k+2);
      r=(pos%p+ (uint64_t)3*p - neg%p)%p;
    }
    printf("%d %llu\n",n,(unsigned long long)r);
  }
  return 0;
}

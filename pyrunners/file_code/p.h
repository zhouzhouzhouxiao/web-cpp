bool primer(int p){
  for(int i=2;i<p;++i)
  {
    if (p%i == 0) return 0;
  }
  return 1;
}
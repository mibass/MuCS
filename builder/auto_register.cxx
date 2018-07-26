
//

//  microboone: auto_register
//

//  author : Leonidas N. Kalousis     
//  email  : kalousis@vt.edu 

//

#include "TApplication.h"

#include "iostream"

#include "iomanip"

#include "fstream"

#include "sstream"

#include "TROOT.h"

#include "TStyle.h"

#include "TColor.h"

#include "TMath.h"

#include "TFile.h"

#include "TTree.h"

#include "TChain.h"

#include "TNtuple.h"

#include "TCanvas.h"

#include "TH1F.h"

#include "TH2F.h"

#include "TGraph.h"

#include "TGraphErrors.h"

#include "TPaveLabel.h"

#include "TF1.h"

#include "TBox.h"

using namespace std;

Int_t auto_register( char *folder, char *rrr, Int_t n0 )
{  
  // ...
  
  string sline; 
  
  ifstream sum; sum.open( Form( "%s/summary.txt", folder ), ios::in );
  
  Int_t done = 0;
  
  std::vector<Int_t> run;
  
  while ( getline( sum, sline ) && done==0 ) 
    {
      UInt_t e1 = sline.length()-1;
      
      for ( UInt_t i=0; i<e1; i++ )
	{
	  char c1 = sline.at(i);
	  char c2 = sline.at(i+1);
	  UInt_t done2=0;
	  	  
	  if ( c1=='-' && c2=='>' ) 
	    {
	      UInt_t j=i+2;
	      UInt_t k=0;
	      
	      while( done2==0 )
		{
		  char cx = sline.at(j+k);
		  // cout << cx << endl;
		  if ( cx=='!' ) { done2=1; done=1; }
		  else 
		    {
		      Int_t icx = atoi(&cx);
		      run.push_back(icx);
		    
		    }
		  k++;
		  
		}
	      
	    }
	  
	  if ( done2==1 ) break;
	  	  
	}
            
    }
    
  sum.clear();
  
  sum.close();
  
  Int_t dec = run.size();
  
  Float_t x1=0.0;
  
  for ( Int_t i=0; i<dec; i++ )
    {
      Float_t pa1 = 1.0*run.at(i)*1.0;
            
      pa1 *= pow( 10.0, dec-i-1 );
            
      x1 += pa1;

    }
  
  Int_t w1 = (Int_t)x1;
  // ...
    
  std::string str(rrr);

  // cout << str << endl;
  
  UInt_t a1 = str.length();
  
  for ( UInt_t i=0; i<a1; i++ )
    {
      char cx = str[i];
      
      if ( cx=='_' ) str[i]=' ';
      
    }
  

  // cout << str << endl;
  
  istringstream iss;
  
  string location_; 
  
  Int_t run_=0;  Int_t seq_=0; 
  
  iss.str( str );
      
  iss >> location_ >> run_ >> seq_ ;
      
  iss.clear();
    
  // cout << run_ << ", " << seq_ << ", " << n0 << endl; 
    
  // cout << "" << endl; 
  
  ofstream output( "/uboone/app/users/kalousis/MuCS/preselection/lartf_logfile.txt", std::ofstream::app ); 
  
  output << w1 << setw(21) << run_ << setw(10) << seq_ << setw(10) << 0 << setw(10) << n0+1 << setw(10) << ( 1.0*(n0+1.0)*1.0 )*20.0 
	 << setw(10) << "LArTF" << setw(10) << 0 << endl;
  
  output.close();
  
  return 0;
  
}

int main( int argc, char *argv[] )  
{
  argc *= 1.0;
  
  TApplication theApp( "App", 0, 0 );
  
  char *folder = argv[1];
  
  char *run = argv[2];
  
  Int_t n0 = atoi( argv[3] );
  
  auto_register( folder, run, n0 );

}

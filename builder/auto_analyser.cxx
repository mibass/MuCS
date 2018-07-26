
//

//  microboone: auto_analyser
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

const TString out_path = "/uboone/data/users/kalousis/MuCS/muons/"; 
// const string out_path1 = "/uboone/data/users/kalousis/MuCS/muons/"; 

Int_t auto_analyser()
{  
  // ...
  
  ifstream sum; 
  
  string sline; istringstream iss;
  
  sum.open( "/uboone/app/users/kalousis/MuCS/preselection/lartf_logfile.txt", ios::in );
    
  Int_t ggg; 
      
  TString help_me_please; // !
  
  Int_t ind_run = -1; 
  
  getline( sum, sline ); getline( sum, sline ); 
  
  while ( getline( sum, sline ) ) 
    {
      iss.str( sline );
      
      iss >> ggg >> help_me_please >> help_me_please >> help_me_please >> help_me_please >> help_me_please >> help_me_please >> help_me_please >> help_me_please;
            
      iss.clear();
      
      if ( ggg>ind_run && ggg!=666 )
	{
	  cout << " - found seq : " << ggg << endl;
	  
	  TString data_path = out_path+Form( "/mega_micro_ana_%d_%.3f_%d.root", ggg, 0.3333, 0 );
	  
	  TFile *f2 = new TFile( data_path, "read" );
	  
	  if ( f2->IsZombie() ) 
	    { 
	      cout << " - to be analysed : " << ggg << endl;
	      
	      system( Form( "nohup /uboone/app/users/kalousis/MuCS/preselection/mega_micro_code %d %.3f %d >> /uboone/data/users/kalousis/MuCS/muons/log-%d.txt &", ggg, 0.3333, 0, ggg ) );
	      	      
	      
	    }
	  
	  ind_run = ggg;
	  
	}
      
    }
  
  sum.clear();
  
  sum.close();
    
  return 0;
  
  // ..
  
}

int main() // int argc, char *argv[] )  
{
  // argc *= 1.0;
  
  TApplication theApp( "App", 0, 0 );
    
  auto_analyser();

}


//

//  microBooNE: mega-micro analysis code
//  version 6.0 (August 2015) 

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

const TString txt_file = "/uboone/app/users/kalousis/MuCS/preselection/lartf_logfile.txt";

const TString file_path = "$MEGA_MICRO_DATA";

const TString out_path = "/uboone/data/users/kalousis/MuCS/muons/"; const string out_path1 = "/uboone/data/users/kalousis/MuCS/muons/"; 

// const TString out_path = "./results/"; const string out_path1 = "./results/"; 

// const TString out_path = "$results"; const string out_path1 = "$results"; 

const Int_t usb = 37;

const Double_t dur_sub = 20.80;

const Double_t wbin = 10.0;

const Float_t toler=4; // <--- default !

const Float_t thr4=4.0; 

const Int_t pas1=0; 

Double_t  my_g( Double_t *x, Double_t *par)
{
  Double_t xx = x[0];

  Double_t Norm = par[0];
  
  Double_t Q_0 = 1./par[1];
  
  Double_t s_0 = par[2];
        
  Double_t arg = 0.0; 
  
  if ( s_0!=0 ) arg = ( xx - Q_0 )/s_0;    
  
  else cout << "Error: The code tries to divide by zero." << endl;
  
  Double_t Result =  wbin*Norm/( sqrt( 2 * TMath::Pi() ) * s_0 ) * TMath::Exp( -0.5*arg*arg );
  
  return Result;

}

Double_t  my_m( Double_t *x, Double_t *par )
{
  Double_t xx = x[0];

  Double_t Norm = par[0];
  
  Double_t lambda = par[1];
  
  Double_t theta = par[2];
    
  Double_t s = lambda*(1+theta);
  
  Double_t Result = 0.0;
    
  if ( xx>0 ) Result =  wbin*Norm*s*pow( s*xx, theta )/TMath::Gamma( 1+theta )*TMath::Exp( -s*xx );
  
  return Result;
  
}

Float_t evd_x_x[24];
  
Float_t evd_x_y[24];

Float_t evd_y_x[24];
  
Float_t evd_y_y[24];

TH2F *h_evdx = new TH2F( "h_evdx", "x bi-layers", 1, -2, 52, 1, -8, 18 ); 

TH2F *h_evdy = new TH2F( "h_evdy", "y bi-layers", 1, -2, 52, 1, -8, 18 ); 

TBox *pixX[2][24]; TBox *pixY[2][24]; TBox *pixH[100];

void event_display( TCanvas *c1, Double_t pm7[24], Double_t pm2[24], Double_t pm3[24], Double_t pm1[24] ) 
{
  c1->cd(1);
   
  h_evdx->SetStats( 0 );
    
  h_evdx->Draw( "AH" );
  
  for ( Int_t i=0; i<24; i++ )
    {
      pixX[0][i] = new TBox( evd_x_x[i]-2.0, evd_x_y[i]-0.5+2.5-2.0, evd_x_x[i]+2.0, evd_x_y[i]+0.5+2.5-2.0 );
      
      pixX[0][i]->SetLineColor( kBlack ); pixX[0][i]->SetLineWidth( 3 ); pixX[0][i]->SetFillStyle( 0 );
      
      pixX[0][i]->Draw( "" );
      
      pixX[1][i] = new TBox( evd_x_x[i]-2.0, evd_x_y[i]-0.5+7.5+2.0, evd_x_x[i]+2.0, evd_x_y[i]+0.5+7.5+2.0 );
      
      pixX[1][i]->SetLineColor( kBlack ); pixX[1][i]->SetLineWidth( 3 ); pixX[1][i]->SetFillStyle( 0 );
      
      pixX[1][i]->Draw( "" );
            
    }
  
  TBox *bb1 = new TBox( 0.0, -0.5-2.0, 50.0, 1.5-2.0 ); bb1->SetFillColor( 18 ); bb1->Draw( "" );
  
  TBox *bb2 = new TBox( 0.0, 4.5+2.0, 50.0, 6.5+2.0 ); bb2->SetFillColor( 18 ); bb2->Draw( "" );
  
  c1->cd(2);
   
  h_evdy->SetStats( 0 );
    
  h_evdy->Draw( "AH" );
  
  for ( Int_t i=0; i<24; i++ )
    {
      pixY[0][i] = new TBox( evd_y_x[i]-2.0, evd_y_y[i]-0.5-2.0, evd_y_x[i]+2.0, evd_y_y[i]+0.5-2.0 );
      
      pixY[0][i]->SetLineColor( kBlack ); pixY[0][i]->SetLineWidth( 3 ); pixY[0][i]->SetFillStyle( 0 );
      
      pixY[0][i]->Draw( "" );
      
      pixY[1][i] = new TBox( evd_y_x[i]-2.0, evd_y_y[i]-0.5+5.0+2.0, evd_y_x[i]+2.0, evd_y_y[i]+0.5+5.0+2.0 );
      
      pixY[1][i]->SetLineColor( kBlack ); pixY[1][i]->SetLineWidth( 3 ); pixY[1][i]->SetFillStyle( 0 );
      
      pixY[1][i]->Draw( "" );
      
    }
  
  TBox *bb3 = new TBox( 0.0, 2.0-2.0, 50.0, 4.0-2.0 ); bb3->SetFillColor( 18 ); bb3->Draw( "" );
  
  TBox *bb4 = new TBox( 0.0, 7.0+2.0, 50.0, 9.0+2.0 ); bb4->SetFillColor( 18 ); bb4->Draw( "" );
    
  Int_t ind=0;
  
  c1->cd(1);
  
  for ( int i=0; i<24; i++ )
    {
      if ( pm7[ i ]>0 ) 
	{ 
	  pixH[ind] = new TBox( evd_x_x[i]-2.0, evd_x_y[i]-0.5+2.5-2.0, evd_x_x[i]+2.0, evd_x_y[i]+0.5+2.5-2.0 ); 
	  
	  pixH[ind]->SetFillColor( kAzure-9 ); pixH[ind]->Draw( "" ); pixX[0][i]->Draw( "" ); // 7
	  
	  ind++;
	
	} 
      
      if ( pm2[ i ]>0 ) 
	{ 
	  pixH[ind] = new TBox( evd_x_x[i]-2.0, evd_x_y[i]-0.5+7.5+2.0, evd_x_x[i]+2.0, evd_x_y[i]+0.5+7.5+2.0 ); 
	  
	  pixH[ind]->SetFillColor( kAzure-9 ); pixH[ind]->Draw( "" ); pixX[1][i]->Draw( "" ); // 2
	  
	  ind++;
	  
	} 
            
    }
  
  c1->cd(2);
   
  for ( int i=0; i<24; i++ )
    {
      if ( pm3[ i ]>0 ) 
	{ 
	  pixH[ind] = new TBox( evd_y_x[i]-2.0, evd_y_y[i]-0.5-2.0, evd_y_x[i]+2.0, evd_y_y[i]+0.5-2.0 );
	  
	  pixH[ind]->SetFillColor( kAzure-9 ); pixH[ind]->Draw( "" ); pixY[0][i]->Draw( "" ); // 3
	  
	  ind++;
	  
	} 
      
    }
  
  for ( int i=0; i<24; i++ )
    {
      if ( pm1[ i ]>0 ) 
	{ 
	  pixH[ind] = new TBox( evd_y_x[i]-2.0, evd_y_y[i]-0.5+5.0+2.0, evd_y_x[i]+2.0, evd_y_y[i]+0.5+5.0+2.0 ); 
	  
	  pixH[ind]->SetFillColor( kAzure-9 ); pixH[ind]->Draw( "" ); pixY[1][i]->Draw( "" ); // 1
	  
	  ind++;
	  
	} 
      
    }
  
  c1->cd(1);
    
}

Int_t mega_micro( Int_t group, Float_t pe, Int_t calib )
{  
  time_t start;  
  
  time( &start );
  
  Int_t method=1;
  
  for ( Int_t i=0; i<24; i++ )
    {
      if ( i<12 ) 
	{ 
	  evd_x_x[i] = 48.0-1.0*i*4.0;
	  
	  evd_x_y[i] = 0.0;
	  
	}
      
      if ( i>=12 ) 
	{ 
	  Double_t k = i-12;
	  
	  evd_x_x[i] = 46.0-1.0*k*4.0;
	  
	  evd_x_y[i] = 1.0;
	  
	}
      
      if ( i<12 ) 
	{ 
	  evd_y_x[i] = 2.0+1.0*i*4.0;
	  
	  evd_y_y[i] = 1.0;
	  
	}
      
      if ( i>=12 ) 
	{ 
	  Double_t k = i-12;
	  
	  evd_y_x[i] = 4.0+1.0*k*4.0;
	  
	  evd_y_y[i] = 0.0;
	  
	}
      
    }
  
  // Preample ...
  
  gROOT->Reset();
  
  gStyle->SetCanvasBorderMode( 0 );
  
  gStyle->SetCanvasColor( 0 );
  
  gStyle->SetPadColor( 0 );
  
  gStyle->SetPadBorderMode( 0 );
  
  gStyle->SetFrameBorderMode( 0 );
  
  gStyle->SetTitleColor( 0 );   
  
  gStyle->SetTitleFillColor( 0 );  
  
  gStyle->SetTitleBorderSize( 0 );
  
  gStyle->SetTitleX( 0.10 );
  
  gStyle->SetTitleY( 0.98 );
    
  gStyle->SetTitleFont( 22, "" );
  
  gStyle->SetTitleSize( 0.055, ""  );
        
  gStyle->SetStatColor( 0 );
    
  gStyle->SetStatFont( 22 );
  
  gStyle->SetStatBorderSize( 1 );
  
  gStyle->SetStatX( 0.90 );
  
  gStyle->SetStatY( 0.90 );
    
  gStyle->SetStatFontSize( 0.04 );
    
  gStyle->SetOptStat( 1110 );
  
  gStyle->SetTitleFont( 22, "XYZ"  );
  
  gStyle->SetTitleSize( 0.05, "XYZ"  );
  
  gStyle->SetTitleColor( kBlack, "XYZ"  );
  
  gStyle->SetTitleAlign(13);
  
  gStyle->SetLabelFont( 22, "XYZ"  );
  
  gStyle->SetLabelSize( 0.04, "XYZ"  );
    
  gStyle->SetOptStat( 1110 ); 
  
  gStyle->SetOptFit( 0 ); 
  
  gStyle->SetPalette( 1 ); 
  
  const Int_t NRGBs = 5;
  
  const Int_t NCont = 255;

  Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
  
  Double_t red[NRGBs]   = { 0.00, 0.00, 0.87, 1.00, 0.51 };
  
  Double_t green[NRGBs] = { 0.00, 0.81, 1.00, 0.20, 0.00 };
  
  Double_t blue[NRGBs]  = { 0.51, 1.00, 0.12, 0.00, 0.00 };
  
  TColor::CreateGradientColorTable( NRGBs, stops, red, green, blue, NCont );
  
  gStyle->SetNumberContours( NCont );
  
  gROOT->ForceStyle();
  
  // ... end of preample !
  
  TCanvas *c1 = new TCanvas( "c1", "" );
    
  TCanvas *c3 = new TCanvas( "c3", "Muon Counter System event display", 50, 50, 1250, 650 );
  
  c3->Divide(2,1);
  
  c1->cd();
  
  TString file0_path = out_path+Form( "/mega_micro_ana_%d_%.3f_%d.root", group, pe, calib );
  
  TString pdf_path = out_path+Form( "/mega_micro_pdf_%d_%.3f_%d.pdf", group, pe, calib );
  
  TString f_g =  out_path+Form( "/mega_micro_ana_%d_%.3f_1.root", group, 0.3333 );
  
  string txt1 =  out_path1+Form( "/mega_micro_gains_%d_%.3f_%d.txt", group, 0.333, 0 );
  
  string txt2 =  out_path1+Form( "/mega_micro_gains_%d_%.3f_%d.txt", group, pe, calib );
  
  TFile *f = new TFile( file0_path, "RECREATE" );
  
  f->cd();
  
  // TGraphErrors *gr_bs_1; TGraphErrors *gr_bs_2; TGraphErrors *gr_bs_3; TGraphErrors *gr_bs_7; 
  
  Double_t offset12;
  
  Double_t offset37;
  
  Int_t nseq = 0;
  
  Int_t nseq0 = 0;
  
  Int_t tot_files = 0;
  
  Int_t tot_events = 0;
  
  Double_t ttime = 0;
  
  Int_t totbilayer = 0;
  
  Int_t totxy1 = 0;
  
  Int_t totxy3 = 0;
  
  Double_t tra1 = 0;
  
  Double_t tra2 = 0;
  
  Double_t tra3 = 0;
  
  Double_t tra7 = 0;
  
  Double_t g1[24]; Double_t g2[24];
  
  Double_t g3[24]; Double_t g7[24];
  
  Double_t co_shift = 1.0;
  
  for( Int_t i=0; i<24; i++ )
    {
      g1[i] = 200.0; g2[i] = 200.0;
      
      g3[i] = 200.0; g7[i] = 200.0;
      
    }
    
  f->cd();
  
  TH1D *h_off13 = new TH1D( "h_off13", "Offset #DeltaT ( 1, 3 ); Time ticks", 100000, 0.0, 100000.0 ); 
  
  TH1D *h_off17 = new TH1D( "h_off17", "Offset #DeltaT ( 1, 7 ); Time ticks", 100000, 0.0, 100000.0 ); 
  
  TH1D *h_off23 = new TH1D( "h_off23", "Offset #DeltaT ( 2, 3 ); Time ticks", 100000, 0.0, 100000.0 ); 
  
  Int_t apix[24] = { 8, 7, 5, 3, 1, 13, 11, 9, 24, 30, 25, 40, 36, 35, 46, 43, 41, 56, 52, 64, 62, 60, 58, 57 }; 
    
  Int_t top[24] = { 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 }; 
  
  Int_t right[24] = { 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 };
  
  Int_t left[24]  = { -1, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1, -1, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 };
  
  TH1F *h_hits_pmt1 = new TH1F( "h_hits_pmt1", "Hits per channel in pmt-1; Channel number; Number of hits", 65, -.5, 64.5  );
  
  TH1F *h_hits_pmt2 = new TH1F( "h_hits_pmt2", "Hits per channel in pmt-2; Channel number; Number of hits", 65, -.5, 64.5  );
  
  TH1F *h_hits_pmt3 = new TH1F( "h_hits_pmt3", "Hits per channel in pmt-3; Channel number; Number of hits", 65, -.5, 64.5  );

  TH1F *h_hits_pmt7 = new TH1F( "h_hits_pmt7", "Hits per channel in pmt-7; Channel number; Number of hits", 65, -.5, 64.5  );
    
  Double_t offx[100];
  
  Double_t offy12[100]; Double_t offy37[100];
  
  Int_t noff = 0;
  
  Double_t ratexy1[100]; Double_t ratexy1_e[100]; 
  
  Double_t ratexy3[100]; Double_t ratexy3_e[100]; 
  
  Double_t rt1[100]; Double_t rt2[100]; 
    
  TH1F *h_pmt1[24]; TH1F *h_pmt2[24]; TH1F *h_pmt3[24]; TH1F *h_pmt7[24]; 
  
  TH1F *h_all; 
  
  TH1D *h12 = new TH1D( "h12", "#DeltaT ( 1, 2 ); Time ticks", 40, -20, 20 );
	  
  TH1D *h37 = new TH1D( "h37", "#DeltaT ( 3, 7 ); Time ticks", 40, -20, 20 );
	  
  TH1D *h13 = new TH1D( "h13", "#DeltaT ( 1, 3 ); Time ticks", 40, -20, 20 );
  
  
  for ( Int_t i=0; i<24; i++ )
    {
      Int_t ch = apix[i];
      
      h_pmt1[i] = new TH1F( Form( "h_pmt1_%d", ch ), Form( "ADC distribution for pmt-1, ch-%d; ADC amplitude", ch ), 201, -5, 2005 );
      
      // 201, -5, 2005 );
      
      // 101, -5, 1005 );
      
      h_pmt2[i] = new TH1F( Form( "h_pmt2_%d", ch ), Form( "ADC distribution for pmt-2, ch-%d; ADC amplitude", ch ), 201, -5, 2005 );
      
      h_pmt3[i] = new TH1F( Form( "h_pmt3_%d", ch ), Form( "ADC distribution for pmt-3, ch-%d; ADC amplitude", ch ), 201, -5, 2005 );
      
      h_pmt7[i] = new TH1F( Form( "h_pmt7_%d", ch ), Form( "ADC distribution for pmt-7, ch-%d; ADC amplitude", ch ), 201, -5, 2005 );
      
    }
  
  h_all = new TH1F( "h_all", "ADC distribution for all pmts; ADC amplitude", 201, -5, 2005 );
  
  Int_t start1 = 0;
  
  Int_t start3 = 0;
  
  TTree *my_tree12 = new TTree( "my_tree12", "" );
	  
  TTree *my_tree37 = new TTree( "my_tree37", "" );
  /*
    Int_t length;
    
    my_tree->Branch( "length", &length, "length/I" );
  */
  
  Double_t gc01=0.0;
  
  Double_t tt01=-1.0;
  
  my_tree12->Branch( "t0", &tt01, "t0/D" );
  
  my_tree12->Branch( "seq", &nseq0, "seq/I" );
  
  Int_t ni;
  
  my_tree12->Branch( "ni", &ni, "ni/I" );
  
  my_tree37->Branch( "ni", &ni, "ni/I" );
  
  Int_t mod;
  
  my_tree12->Branch( "module", &mod, "module/I" );
  
  my_tree37->Branch( "module", &mod, "module/I" );
  
  Float_t sec_hi;
  
  my_tree12->Branch( "sec_hi", &sec_hi, "sec_hi/F" );
  
  my_tree37->Branch( "sec_hi", &sec_hi, "sec_hi/F" );
  
  Float_t sec_low;
  
  my_tree12->Branch( "sec_low", &sec_low, "sec_low/F" );
  
  my_tree37->Branch( "sec_low", &sec_low, "sec_low/F" );
  
  Float_t high_time;
  
  my_tree12->Branch( "high_time", &high_time, "high_time/F" );
  
  my_tree37->Branch( "high_time", &high_time, "high_time/F" );
  
  Float_t low_time;
  
  my_tree12->Branch( "low_time", &low_time, "low_time/F" );
  
  my_tree37->Branch( "low_time", &low_time, "low_time/F" );
  
  Double_t fadc[24];
  
  my_tree12->Branch( "fadc", &fadc, "fadc[24]/D" );
  
  my_tree37->Branch( "fadc", &fadc, "fadc[24]/D" );
  
  Int_t hits;
  
  my_tree12->Branch( "hits", &hits, "hits/I"  );
  
  my_tree37->Branch( "hits", &hits, "hits/I"  );
  
  Int_t max_hits[24];
  
  my_tree12->Branch( "max_hits", &max_hits, "max_hits[24]/I" );
  
  my_tree37->Branch( "max_hits", &max_hits, "max_hits[24]/I" );
  
  Int_t bi_hits[24];
  
  my_tree12->Branch( "bi_hits", &bi_hits, "bi_hits[24]/I" );
  
  my_tree37->Branch( "bi_hits", &bi_hits, "bi_hits[24]/I" );
  
  Int_t is_hit;
  
  my_tree12->Branch( "is_hit", &is_hit, "is_hit/I" );
  
  my_tree37->Branch( "is_hit", &is_hit, "is_hit/I" );
  
  Int_t is_hit_4;
  
  my_tree12->Branch( "is_hit_4", &is_hit_4, "is_hit_4/I" );
  
  my_tree37->Branch( "is_hit_4", &is_hit_4, "is_hit_4/I" );
    
  
  TTree *my_tree_xy_1 = new TTree( "my_tree_xy_1", "" );
  
  my_tree_xy_1->Branch( "t0", &tt01, "t0/D" );
  
  my_tree_xy_1->Branch( "seq", &nseq0, "seq/I" );
  
  Int_t nxy1;
  
  my_tree_xy_1->Branch( "ni1", &nxy1, "ni1/I" );
  
  Int_t nxy2;
  
  my_tree_xy_1->Branch( "ni2", &nxy2, "ni2/I" );
  
  Float_t sec_hi_xy_1;
  
  my_tree_xy_1->Branch( "sec_hi_1", &sec_hi_xy_1, "sec_hi_1/F" );
  
  Float_t sec_low_xy_1;
  
  my_tree_xy_1->Branch( "sec_low_1", &sec_low_xy_1, "sec_low_1/F" );
  
  Float_t high_time_xy_1;
  
  my_tree_xy_1->Branch( "high_time_1", &high_time_xy_1, "high_time_1/F" );
  
  Float_t low_time_xy_1;
  
  my_tree_xy_1->Branch( "low_time_1", &low_time_xy_1, "low_time_1/F" );
  
  Float_t sec_hi_xy_2;
  
  my_tree_xy_1->Branch( "sec_hi_2", &sec_hi_xy_2, "sec_hi_2/F" );
  
  Float_t sec_low_xy_2;
  
  my_tree_xy_1->Branch( "sec_low_2", &sec_low_xy_2, "sec_low_2/F" );
  
  Float_t high_time_xy_2;
  
  my_tree_xy_1->Branch( "high_time_2", &high_time_xy_2, "high_time_2/F" );
  
  Float_t low_time_xy_2;
  
  my_tree_xy_1->Branch( "low_time_2", &low_time_xy_2, "low_time_2/F" );
  
  Double_t fadc1[24];
  
  my_tree_xy_1->Branch( "fadc1", &fadc1, "fadc1[24]/D" );
  
  Double_t bi_hits1[24];
  
  my_tree_xy_1->Branch( "bi_hits1", &bi_hits1, "bi_hits1[24]/D" );
  
  Double_t max_hits1[24];
  
  my_tree_xy_1->Branch( "max_hits1", &max_hits1, "max_hits1[24]/D" );
  
  Double_t fadc2[24];
  
  my_tree_xy_1->Branch( "fadc2", &fadc2, "fadc2[24]/D" );
  
  Double_t bi_hits2[24];
  
  my_tree_xy_1->Branch( "bi_hits2", &bi_hits2, "bi_hits2[24]/D" );
  
  Double_t max_hits2[24];
  
  my_tree_xy_1->Branch( "max_hits2", &max_hits2, "max_hits2[24]/D" );
  
  Int_t is_hit_4_1; 
  
  my_tree_xy_1->Branch( "is_hit_4_1", &is_hit_4_1, "is_hit_4_1/I" );
  
  Int_t is_hit_4_2; 
  
  my_tree_xy_1->Branch( "is_hit_4_2", &is_hit_4_2, "is_hit_4_2/I" );
  
  
  
  TTree *my_tree_xy_3 = new TTree( "my_tree_xy_3", "" );
  
  Int_t nxy3;
  
  my_tree_xy_3->Branch( "ni3", &nxy3, "ni3/I" );
  
  Int_t nxy7;
  
  my_tree_xy_3->Branch( "ni7", &nxy7, "ni7/I" );
  
  Float_t sec_hi_xy_3;
	  
  my_tree_xy_3->Branch( "sec_hi_3", &sec_hi_xy_3, "sec_hi_3/F" );
  
  Float_t sec_low_xy_3;
  
  my_tree_xy_3->Branch( "sec_low_3", &sec_low_xy_3, "sec_low_3/F" );
  
  Float_t high_time_xy_3;
  
  my_tree_xy_3->Branch( "high_time_3", &high_time_xy_3, "high_time_3/F" );
  
  Float_t low_time_xy_3;
  
  my_tree_xy_3->Branch( "low_time_3", &low_time_xy_3, "low_time_3/F" );
  
  Float_t sec_hi_xy_7;
	  
  my_tree_xy_3->Branch( "sec_hi_7", &sec_hi_xy_7, "sec_hi_7/F" );
  
  Float_t sec_low_xy_7;
  
  my_tree_xy_3->Branch( "sec_low_7", &sec_low_xy_7, "sec_low_7/F" );
  
  Float_t high_time_xy_7;
  
  my_tree_xy_3->Branch( "high_time_7", &high_time_xy_7, "high_time_7/F" );
  
  Float_t low_time_xy_7;
  
  my_tree_xy_3->Branch( "low_time_7", &low_time_xy_7, "low_time_7/F" );
  
  Double_t fadc3[24];
  
  my_tree_xy_3->Branch( "fadc3", &fadc3, "fadc3[24]/D" );
  
  Double_t bi_hits3[24];
  
  my_tree_xy_3->Branch( "bi_hits3", &bi_hits3, "bi_hits3[24]/D" );
  
  Double_t max_hits3[24];
  
  my_tree_xy_3->Branch( "max_hits3", &max_hits3, "max_hits3[24]/D" );
  
  Double_t fadc7[24];
  
  my_tree_xy_3->Branch( "fadc7", &fadc7, "fadc7[24]/D" );
  
  Double_t bi_hits7[24];
  
  my_tree_xy_3->Branch( "bi_hits7", &bi_hits7, "bi_hits7[24]/D" );
  
  Double_t max_hits7[24];
  
  my_tree_xy_3->Branch( "max_hits7", &max_hits7, "max_hits7[24]/D" );
  
  Int_t is_hit_4_3; 
  
  my_tree_xy_3->Branch( "is_hit_4_3", &is_hit_4_3, "is_hit_4_3/I" );
  
  Int_t is_hit_4_7; 
  
  my_tree_xy_3->Branch( "is_hit_4_7", &is_hit_4_7, "is_hit_4_7/I" );
  
  // Main pre-selection tree
  
  // !!!
  
  TTree *my_tree = new TTree( "preselected", "" );
    
  my_tree->Branch( "seq", &nseq0, "seq/I" );
    
  my_tree->Branch( "time_sec_high", &sec_hi_xy_1, "time_sec_high/F" );
    
  my_tree->Branch( "time_sec_low", &sec_low_xy_1, "time_sec_low/F" );
  
  my_tree->Branch( "time_16ns_high", &high_time_xy_1, "time_16ns_high/F" );
    
  my_tree->Branch( "time_16ns_low", &low_time_xy_1, "time_16ns_low/F" );
    
  my_tree->Branch( "t0", &tt01, "t0/D" );
  
  my_tree->Branch( "ADC1", &fadc1, "ADC1[24]/D" );
  
  my_tree->Branch( "ADC2", &fadc2, "ADC2[24]/D" );
  
  my_tree->Branch( "ADC3", &fadc3, "ADC3[24]/D" );
  
  my_tree->Branch( "ADC7", &fadc7, "ADC7[24]/D" );
  
  std::vector<Int_t> *hit1 = new std::vector<Int_t>; hit1->clear();
  
  my_tree->Branch( "hits1", &hit1 ); // , "hit1/I" );
  
  std::vector<Int_t> *hit2 = new std::vector<Int_t>; hit2->clear();
  
  my_tree->Branch( "hits2", &hit2 ); // , "hit2/I" );
  
  std::vector<Int_t> *hit3 = new std::vector<Int_t>; hit3->clear();
  
  my_tree->Branch( "hits3", &hit3 ); // , "hit3/I" );
  
  std::vector<Int_t> *hit7 = new std::vector<Int_t>; hit7->clear();
  
  my_tree->Branch( "hits7", &hit7 ); // , "hit7/I" );
  
  // <--- !!!
    
  
  // Printing run and analysis info ...
  
  cout << "" << endl;
  
  cout << "" << endl;
    
  cout << setw(40) << " mega-micro analysis software." << endl;
      
  cout << "" << endl;
  
  cout << setw(40) << " version 6.0" << endl;
      
  cout << "" << endl;
  
  cout << "" << endl;
  
  cout << setw(40) << " Trivia." << endl;
    
  cout << "" << endl;
  
  cout << setw(40) << " Group : " << setw(40) << group << endl;
  
  cout << "" << endl;
    
  string sline; istringstream iss;
  
  ifstream sum; sum.open( txt_file, ios::in );
  
  Int_t group_; string location_; TString buffer_; 
  
  Int_t ind_=0; 

  getline( sum, sline ); getline( sum, sline ); 
  
  while ( getline( sum, sline ) ) 
    {
      iss.str( sline );
      
      iss >> group_ >> buffer_ >> buffer_ >> buffer_ >> buffer_ >> buffer_ >> location_ >> buffer_ >> buffer_;
      
      iss.clear();
      
      if ( group_==group ) { ind_ = 1; break; }
      
    }
    
  sum.clear();
  
  sum.close();
  
  if ( ind_==0 )
    {
      cout << " Error : Group number not found !" << endl;
      
      cout << "" << endl;
      
      cout << "" << endl;
      
      return -1;
    
    }
  
  cout << setw(40) << " Location : " << setw(40) << location_ << endl;
  
  cout << "" << endl;
    
  cout << setw(40) << " P.E. threshold : " << setw(40) << pe << endl;
    
  cout << "" << endl;
  
  cout << setw(40) << " Calibration step : " << setw(40) << calib << endl;
    
  cout << "" << endl;
    
  c1->cd();
  
  TPaveLabel *label = new TPaveLabel( 0.15, 0.4, 0.85, 0.6, Form( "location %s (%d), threshold %.3f PE, method %d ", location_.c_str(), group, pe, method ) );
  
  label->SetTextFont( 22 );
  
  label->SetFillColor( 0 );
  
  label->SetShadowColor( 0 );
  
  label->Draw();
  
  // c1->Update();
      
  // c1->WaitPrimitive();
  
  c1->Print( pdf_path+"(", "pdf" );
  
  cout << "" << endl;
    
  cout << "" << endl;
    
  c1->cd();
  
  c1->SetGrid( 1, 1 );
  
  // ... done !
    
  if ( calib==2 )
    {
      TFile *f_i = new TFile( f_g, "read" ); 
      
      TH1F *h_c2 = (TH1F*)f_i->Get( "h_all" );
      
      h_c2->SetName( "h_new" );
      
      h_c2->SetLineColor( kBlack ); h_c2->SetMarkerColor( kBlack ); h_c2->SetMarkerStyle( 20 ); h_c2->SetMarkerSize( 1.0 );
      
      h_c2->Draw( "pe" );
      
      // c1->Update();
      
      // c1->WaitPrimitive();
      
      TF1 *my_func  = new TF1( "my_func" , my_m, 0, 1000, 3 );
  
      my_func->SetParNames( "Norm", "#lambda", "#theta" );
      
      //my_func->SetParNames( "Norm", "Q", "#sigma" );
      
      my_func->SetLineColor( kAzure+6 );
      
      Double_t norm1 = h_c2->GetEntries(); 
      
      my_func->SetParameter( 0, norm1 ); my_func->SetParLimits( 0, 0.05*norm1, 5.0*norm1 ); 
      
      Double_t mean1 = 1/200.0;
      
      my_func->SetParameter( 1, mean1 ); my_func->SetParLimits( 1, 0.05*mean1, 5.0*mean1 ); 
            
      Double_t var1 = 5; //h_c2->GetRMS();
      
      my_func->SetParameter( 2, var1 ); my_func->SetParLimits( 2, 0.05*var1, 100*var1 );  
      
      Double_t low_e = h_c2->GetMean()-1.2*h_c2->GetRMS();
      
      if ( low_e<0 ) low_e = 0.0;
      
      Double_t max_e = h_c2->GetMean()+0.8*h_c2->GetRMS(); 
            
      h_c2->Fit( "my_func", "", "", low_e, max_e );  
      
      Double_t *par_c2 = my_func->GetParameters();
      
      cout << "" << endl;
      
      cout << "" << endl;
      
      // cout << par_c2[2]/(par_c2[2]+1.0)/par_c2[1] << endl;
      
      Double_t peak=par_c2[2]/(par_c2[2]+1.0)/par_c2[1];
      
      h_c2->Draw( "pe" );
      
      my_func->SetRange( low_e, max_e );
      
      my_func->Draw( "SAME" );
      
      // c1->Update();
      
      // c1->WaitPrimitive();
      
      f_i->Close();
            
      f->cd();
      
      c1->Write( "calib_2" );
      
      co_shift=200.0/peak;
                  
      // delete h_c2;
            
    }
  
  if ( calib==1 || calib==2 )
    {
      ifstream gains_input;
      
      gains_input.open( txt1.c_str() );
      
      if ( ! gains_input ) 
	{
	  cout << " Error : Gain file not found !" << endl;
	  
	  cout << "" << endl;
	  
	  cout << "" << endl;
	  
	  return -1;
	
	}
            
      getline( gains_input, sline ); getline( gains_input, sline ); 
  
      while ( getline( gains_input, sline ) ) 
	{
	  iss.str( sline );
	  
	  Float_t a1, a3, a4; 
	  
	  Int_t a2;
	  
	  iss >> a1 >> a2 >> a3 >> a4;
	  
	  // cout << a1 << ", " << a2 << ", " << a3 << ", " << a4 << endl; getchar();
	  
	  if ( a1==1 ) g1[ a2 ] = a3;
	  
	  if ( a1==2 ) g2[ a2 ] = a3;
	  
	  if ( a1==3 ) g3[ a2 ] = a3;
	  
	  if ( a1==7 ) g7[ a2 ] = a3;
	  
	  iss.clear();
	  
	}
	
    }
  
  sum.open( txt_file, ios::in ); 
  
  getline( sum, sline ); getline( sum, sline ); 

  Int_t group0, run, seq; TString tag;
  
  Int_t no_high; Int_t no_low; 
   
  cout << setw(40) << " Analyze files." << endl;
      
  cout << "" << endl;
  
  cout << "" << endl;
  
  // Main while loop ...
  
  while ( getline( sum, sline ) ) 
    {
      iss.str( sline );
                  
      iss >> group0 >> run >> seq >> no_low >> no_high >> buffer_ >> buffer_ >> buffer_ >> tag;
      
      if ( group0==group )
	{
	  // Analyse each sequence file separately ...
	  
	  // Start with the baseline files ...
	  
	  nseq++;
	  
	  nseq0 = nseq;
	  
	  cout << setw(40) << " Run : " << setw(40) << run << endl;
      
	  cout << "" << endl;
	  
	  cout << setw(40) << " Sequence : " << setw(40) << seq << endl;
      
	  cout << "" << endl;
  
	  TString data_path;
          
          TString empty_ = "";

	  if ( strcmp( tag, empty_ ) != 0 ) { data_path = file_path+Form( "/Run_%d_%d", run, seq ); data_path+="_"+tag+Form( "/USB_%d/", usb ); } 
	  
	  else data_path = file_path+Form( "/Run_%d_%d/USB_%d/", run, seq, usb ); 
	  
	  TString bs_file = data_path + "baselines.root";
	  
	  TFile *f1 = new TFile( bs_file, "read" );
	  
	  TNtuple *bs_tree = (TNtuple*)f1->Get( "ntuple_sig" );
	  
	  // bs_tree->Print(); 
	  
	  // Double_t ch_row[24] = { 0 };
	  
	  Double_t bs_3[24]; Double_t bs_7[24]; Double_t bs_1[24]; Double_t bs_2[24];
	  
	  // Double_t rms_3[24]; Double_t rms_7[24]; Double_t rms_1[24]; Double_t rms_2[24];

	  for ( Int_t i=0; i<24; i++ )
	    {
	      bs_3[i]=0.0; bs_7[i]=0.0; bs_1[i]=0.0; bs_2[i]=0.0; 
	      
	      // rms_3[i]=0.0; rms_7[i]=0.0; rms_1[i]=0.0; rms_2[i]=0.0; 
	    
	    }
	  	  
	  TH1F *h_bs_3; TH1F *h_bs_7; TH1F *h_bs_1; TH1F *h_bs_2;
	  
	  for( Int_t i=0; i<24; i++ ) 
	    {
	      Int_t chx = apix[i];
	      
	      // ch_row[i] = chx;
	      
	      h_bs_1 = new TH1F( Form( "h_bs_1_%d", chx ), Form( "Baseline for pmt-1, ch-%d; Pulse amplitude in ADC", chx ), 100, 1000, 2000 ); 
	      
	      bs_tree->Draw( Form( "s%d>>h_bs_1_%d", chx, chx ), Form( "s%d>0 && smodule==1", chx ), "goff" );
	      
	      h_bs_1->Draw( "" );
	      
	      // c1->Update();
		
	      // c1->WaitPrimitive();
	      
	      bs_1[ i ] = h_bs_1->GetMean();
	      
	      // rms_1[ i ] = h_bs_1->GetRMS();
	      
	      // f->cd();
	      
	      // h_bs_1->Write( Form( "h_bs_1_%d", chx ) );
	      
	      h_bs_1->Reset();
	      
	      // delete h_bs_1;
	      
	    }
	  
	  for( Int_t i=0; i<24; i++ ) 
	    {
	      Int_t chx = apix[i];
	      
	      h_bs_2 = new TH1F( Form( "h_bs_2_%d", chx ), Form( "Baseline for pmt-2, ch-%d; Pulse amplitude in ADC", chx ), 100, 1000, 2000 ); 
	      
	      bs_tree->Draw( Form( "s%d>>h_bs_2_%d", chx, chx ), Form( "s%d>0 && smodule==2", chx ), "goff" );
	      
	      h_bs_2->Draw( "" );
	      /*
	      c1->Update();
	      
	      c1->WaitPrimitive();
	      */
	      bs_2[ i ] = h_bs_2->GetMean();
	      
	      // rms_2[ i ] = h_bs_2->GetRMS();
	      
	      // f->cd();
	      
	      // h_bs_2->Write( Form( "h_bs_2_%d", chx ) );
	      
	      h_bs_2->Reset();
	      
	      // delete h_bs_2;
	      
	    }
	  
	  for( Int_t i=0; i<24; i++ ) 
	    {
	      Int_t chx = apix[i];
	      	      
	      h_bs_3 = new TH1F( Form( "h_bs_3_%d", chx ), Form( "Baseline for pmt-3, ch-%d; Pulse amplitude in ADC", chx ), 300, 1000, 2000 );
	      
	      bs_tree->Draw( Form( "s%d>>h_bs_3_%d", chx, chx ), Form( "s%d>0 && smodule==3", chx ), "goff" );
	      
	      h_bs_3->Draw( "" );
	      
	      // c1->Update();
	      
	      // c1->WaitPrimitive();
	      
	      bs_3[ i ] = h_bs_3->GetMean();
	      
	      // rms_3[ i ] = h_bs_3->GetRMS();
	      
	      // f->cd();
	      
	      // h_bs_3->Write( Form( "h_bs_3_%d", chx ) );
	      
	      h_bs_3->Reset();
	      
	      delete h_bs_3;
	      
	    }
	  
	  for( Int_t i=0; i<24; i++ ) 
	    {
	      Int_t chx = apix[i];
	       
	      h_bs_7 = new TH1F( Form( "h_bs_7_%d", chx ), Form( "Baseline for pmt-7, ch-%d; Pulse amplitude in ADC", chx ), 100, 1000, 2000 ); 
	      
	      bs_tree->Draw( Form( "s%d>>h_bs_7_%d", chx, chx ), Form( "s%d>0 && smodule==7", chx ), "goff" );
	      
	      h_bs_7->Draw( "" );
	      
	      // c1->Update();
	      
	      // c1->WaitPrimitive();
	      
	      bs_7[ i ] = h_bs_7->GetMean();
	      
	      // rms_7[ i ] = h_bs_7->GetRMS();
	      
	      // f->cd();
	      
	      // h_bs_7->Write( Form( "h_bs_7_%d", chx ) );
	      
	      h_bs_7->Reset();
	      
	      delete h_bs_7;
	      
	    }
	  	  	  
	  f1->Close();
	  /*
	  gr_bs_1 = new TGraphErrors( 24, ch_row, bs_1, 0, rms_1 );
	  
	  gr_bs_1->SetLineColor( kBlack ); gr_bs_1->SetMarkerColor( kBlack ); gr_bs_1->SetMarkerStyle( 20 ); gr_bs_1->SetMarkerSize( 1.0 );
	  
	  gr_bs_1->SetTitle( "Baseline per channel for pmt-1; Channel number; Baseline in ADC" ); 
	  
	  gr_bs_1->GetXaxis()->SetLimits( 0, 65 );
  
	  gr_bs_1->SetMaximum( 2000 );
	  
	  gr_bs_1->SetMinimum( 1000 );
    
	  gr_bs_1->Draw( "APZ" );
	  	  
	  c1->Update();
	      
	  c1->WaitPrimitive();
	  
	  delete gr_bs_1;
	  
	  gr_bs_2 = new TGraphErrors( 24, ch_row, bs_2, 0, rms_2 );
	  
	  gr_bs_2->SetLineColor( kBlack ); gr_bs_2->SetMarkerColor( kBlack ); gr_bs_2->SetMarkerStyle( 20 ); gr_bs_2->SetMarkerSize( 1.0 );
	  
	  gr_bs_2->SetTitle( "Baseline per channel for pmt-2; Channel number; Baseline in ADC" ); 
	  
	  gr_bs_2->GetXaxis()->SetLimits( 0, 65 );
  
	  gr_bs_2->SetMaximum( 2000 );
	  
	  gr_bs_2->SetMinimum( 1000 );
    
	  gr_bs_2->Draw( "APZ" );
	  
	  c1->Update();
	      
	  c1->WaitPrimitive();
	  
	  delete gr_bs_2;
	  
	  gr_bs_3 = new TGraphErrors( 24, ch_row, bs_3, 0, rms_3 );
	  
	  gr_bs_3->SetLineColor( kBlack ); gr_bs_3->SetMarkerColor( kBlack ); gr_bs_3->SetMarkerStyle( 20 ); gr_bs_3->SetMarkerSize( 1.0 );
	  
	  gr_bs_3->SetTitle( "Baseline per channel for pmt-3; Channel number; Baseline in ADC" ); 
	  
	  gr_bs_3->GetXaxis()->SetLimits( 0, 65 );
  
	  gr_bs_3->SetMaximum( 2000 );
	  
	  gr_bs_3->SetMinimum( 1000 );
    
	  gr_bs_3->Draw( "APZ" );
	  	  
	  c1->Update();
	      
	  c1->WaitPrimitive();
	  
	  delete gr_bs_3;
	  
	  gr_bs_7 = new TGraphErrors( 24, ch_row, bs_7, 0, rms_7 );
	  
	  gr_bs_7->SetLineColor( kBlack ); gr_bs_7->SetMarkerColor( kBlack ); gr_bs_7->SetMarkerStyle( 20 ); gr_bs_7->SetMarkerSize( 1.0 );
	  
	  gr_bs_7->SetTitle( "Baseline per channel for pmt-7; Channel number; Baseline in ADC" ); 
	  
	  gr_bs_7->GetXaxis()->SetLimits( 0, 65 );
  
	  gr_bs_7->SetMaximum( 2000 );
	  
	  gr_bs_7->SetMinimum( 1000 );
    
	  gr_bs_7->Draw( "APZ" );
	  
	  c1->Update();
	      
	  c1->WaitPrimitive();
	  	  
	  delete gr_bs_7;
	  */
	  // ... done with the baselines !
	  
	  // Chain all sub-files and find run-time ...
	  
	  TChain *my_chain = new TChain( "ntuple_sig" );  
	  
	  Int_t ch_files = 0;
	  
	  Double_t rtime = 0;
	  
	  Int_t no_files = no_high; 
	  
	  for ( Int_t i=no_low; i<no_files; i++ ) 
	    {
	      TString data_file = data_path + Form( "signal_%d.root", i );
	      
	      TFile *f2 = new TFile( data_file, "read" );
	      
	      if ( f2->IsZombie() ) { cout << " File " << data_path  << " is Zombie, OU OU OU ! ! ! " << endl; cout << "" << endl; } 
	      
	      else 
		{ 
		  TTree *tr1 = (TTree*)f2->Get( "ntuple_sig" );
		  
		  if ( tr1->GetEntries()>0 )
		    {	                  
		      tr1->SetBranchStatus( "*", 0 );
		      
		      tr1->SetBranchStatus( "smodule", 1 );
		      
		      tr1->SetBranchStatus( "stime_16ns_low", 1 );
		      
		      tr1->SetBranchStatus( "stime_16ns_high", 1 );
		      
		      Float_t m1; 
		      
		      tr1->SetBranchAddress( "smodule", &m1 );
		      
		      Float_t t1; 
		      
		      tr1->SetBranchAddress( "stime_16ns_low", &t1 );
		      
		      Float_t t2; 
		      
		      tr1->SetBranchAddress( "stime_16ns_high", &t2 );
		      
		      tr1->GetEntry( 0 ); Double_t t_st = t2*65536.0+t1;
		      
		      Int_t ent1 = tr1->GetEntries();
		      tr1->GetEntry( ent1 ); Double_t t_en = t2*65536.0+t1;
		      
		      Double_t count = 0.0;
		      // cout << "t_st : " << t_st << ", " << "t_en : " << t_en << endl;
		      // cout << "" << endl;
		      // if ( t_en<t_st ) count++;
	      	      
		      Double_t t_p = t_st;
		      Double_t t_0 = t_st;		      
		      		      
		      for ( Int_t r=1; r<ent1; r++ )
			{
			  tr1->GetEntry( r );
			  
			  if ( m1==1 ) 
			    {
			      t_0 = t2*65536.0+t1;
			      
			      if ( ( ( t_p-t_0 )*16.0e-9 )>0.5 )
				{
				  count+=10.0;
				  
				  // cout << ( t_p-t_0 )*16.0e-9 << ", " << r << endl; getchar();
				  
				}
			      
			      t_p = t_0;
			      
			    }
			  
			}
		      
		      rtime += (t_en-t_st)*16.0e-9 + ( 1.0*count*1.0 ); 
		      
		      //h_rtime->Fill( rtime );
		      
		      //cout << "r_time : " << rtime << endl;
	      	      
		      //cout << "" << endl;
	      	      
		      //getchar();
		      
		      my_chain->Add( data_file ); 
		      
		      ch_files++; 
		      
		    }
		  
		  delete tr1;
		  
		}
	      
	      f2->Close();
	      
	      f2->Clear();
	      
	    }
	  	  
	  cout << setw(40) << " Chained files : " << setw(40) << ch_files << endl;
	  
	  cout << "" << endl;
	  
	  tot_files += ch_files;
	  
	  Double_t entries = my_chain->GetEntries();
	  
	  tot_events+= entries; 
	  
	  cout << setw(40) << " Total number of events : " << setw(40) << Form( "%.0f", entries ) << endl;
	  
	  cout << "" << endl;
	  
	  cout << setw(40) << " Run-time (sec, DAQ clock) : " << setw(40) << rtime << endl; 
      
	  cout << "" << endl;
	  
	  ttime += rtime;
	  
	  cout << setw(40) << " Run-time (sec, chained files) : " << setw(40) << ch_files*dur_sub << endl; 
	  
	  cout << "" << endl;
	  
	  rt1[noff] = rtime;
	  
	  rt2[noff] = ch_files*dur_sub; 
	  	  
	  // ... done !
	  	  
	  // Hit finding ...
	  
	  f->cd();
	  	  
	  // TH1D *h_off12 = new TH1D( "h_off12", "Offset #DeltaT ( 1, 2 )", 100000, 0.0, 100000.0 ); // 200000, -100000.0, 100000.0 );
	  
	  TH1D *h_off12 = new TH1D( "h_off12", "Offset #DeltaT ( 1, 2 ); Time ticks", 100000, 0.0, 100000.0 ); 
	   
	  TH1D *h_off37 = new TH1D( "h_off37", "Offset #DeltaT ( 3, 7 ); Time ticks", 100000, 0.0, 100000.0 ); 
	  	  
	  // ..
	  
	  Float_t sig[24];
	  
	  Float_t smodule, slen, stime_16ns_high, stime_16ns_low, stime_sec_high, stime_sec_low;
	  
	  my_chain->SetBranchStatus( "*", 0 ); 
	  
	  my_chain->SetBranchStatus( "smodule", 1 );
	  
	  my_chain->SetBranchStatus( "slen", 1 );
	  
	  my_chain->SetBranchStatus( "stime_sec_low", 1 );
	  
	  my_chain->SetBranchStatus( "stime_sec_high", 1 );
	  
	  my_chain->SetBranchStatus( "stime_16ns_low", 1 );
	  
	  my_chain->SetBranchStatus( "stime_16ns_high", 1 );
	  
	  my_chain->SetBranchAddress( "smodule", &smodule );
	  
	  my_chain->SetBranchAddress( "slen", &slen );
	  
	  my_chain->SetBranchAddress( "stime_sec_low", &stime_sec_low );
	  
	  my_chain->SetBranchAddress( "stime_sec_high", &stime_sec_high );
	  
	  my_chain->SetBranchAddress( "stime_16ns_low", &stime_16ns_low );
	  
	  my_chain->SetBranchAddress( "stime_16ns_high", &stime_16ns_high );
	  
	  for ( Int_t i=0; i<24; i++ ) 
	    { 
	      Int_t chx = apix[i]; 
	      
	      my_chain->SetBranchAddress( Form( "s%d", chx ), &( sig[i] ) ); 
	      
	    } 
	  
	  Int_t ind0 = 0;
	  
	  vector<Float_t> pack;
	  
	  vector< vector<Float_t> > p_mod1, p_mod2, p_mod3, p_mod7;
	  
	  Double_t tpi=0.0;
	  
	  Double_t ra1=0;
	  
	  Double_t ra2=0;
	  
	  Double_t ra3=0;
	  
	  Double_t ra7=0;
	  	  
	  for( Int_t i=0; i<entries; i++ ) 
	    {
	      my_chain->GetEntry( i );
	      
	      Int_t ind1 = 10*i/entries;
	      
	      if ( ind1!=ind0 ) 
		{ 
		  cout << setw(15) << " [  " << ind1*10 << " % of data processed ]" << endl; 
		  
		  cout << "" << endl;
		  
		  ind0=ind1; 
		  
		}
	      
	      ni = i;
	      
	      mod = -1;
	      
	      sec_hi = stime_sec_high;
	      
	      sec_low = stime_sec_low;
	      
	      high_time = stime_16ns_high;
	      
	      low_time = stime_16ns_low;
	      
	      hits = 0; 
	      
	      Double_t tt11 = (high_time*65536.0+low_time)*16.0;
	      
	      if ( ( (tpi-tt11)*1.0e-9 )>7.5 ) gc01+=10.0;
	      
	      tt01 = tt11+gc01*1.0e+9;
	      
	      for( Int_t j=0; j<24; j++ ) { fadc[j] = 0; max_hits[j] = 0; bi_hits[j] = 0; }
	      
	      // length = slen; 
	      
	      is_hit = 0;
	      
	      is_hit_4 = 0;
	      
	      if ( smodule==1 ) 
		{
		  mod = 1;
		  
		  for( Int_t j=0; j<24; j++ ) 
		    {  
		      Double_t xxx = (sig[j]-bs_1[j])*(200.0/g1[j]*co_shift);
		      
		      if ( xxx>0 && xxx>(15.0*pe) ) { fadc[j] = xxx; hits++; }
		      
		      else fadc[j] = 0.0;
		      
		    }
		  
		  Int_t off1 = 0;
		  
		  for( Int_t j=off1; j<off1+12; j++ ) 
		    {  
		      Int_t ch1 = left[j];
		      
		      Double_t fadc1 = 0.0;
		      
		      if ( ch1!=-1 ) fadc1 = fadc[ ch1 ];
		      
		      if ( fadc[ top[j] ]>0. && ( fadc1>0. || fadc[ right[j] ]>0. ) )
			{
			  is_hit++; ra1++;
			  
			  Float_t max = TMath::Max( fadc1, fadc[ right[j] ] );
			  
			  if ( fadc[ top[j] ]>max ) max_hits[ top[j] ] = 1; 
			  			  
			  else if ( fadc1 > fadc[ right[j] ] ) max_hits[ ch1 ] = 1;
			  			  
			  else max_hits[ right[j] ] = 1;
			  
			  if ( bi_hits[ top[j] ]==0 ) { h_hits_pmt1->Fill( apix[ top[j] ] ); bi_hits[ top[j] ]=1; }
			  
			  if ( fadc1 > fadc[ right[j] ] )
			    {
			      if ( bi_hits[ ch1 ]==0 ) { h_hits_pmt1->Fill( apix[ ch1 ] ); bi_hits[ ch1 ]=1; }
			      
			      if ( fadc[  right[j] ]>0 && bi_hits[ right[j] ]==0 ) { h_hits_pmt1->Fill( apix[ right[j] ] ); bi_hits[ right[j] ]=1; }
			      
			    }
			  else
			    {
			      if ( bi_hits[ right[j] ]==0 ) { h_hits_pmt1->Fill( apix[ right[j] ] ); bi_hits[ right[j] ]=1; }
			      
			      if ( fadc1>0 && bi_hits[ ch1 ]==0 ) { h_hits_pmt1->Fill( apix[ ch1 ] ); bi_hits[ ch1 ]=1; }
			      
			    }
			  
			}
		      	
		      Double_t v0 = ( 15.0*thr4 );
		      
		      if ( fadc[ top[j] ]>v0 && ( fadc1>v0 || fadc[ right[j] ]>v0 ) ) is_hit_4++;
			
		    }
		  		   
		}
	      
	      else if ( smodule==2 ) 
		{
		  mod = 2;
		  
		  for( Int_t j=0; j<24; j++ ) 
		    {  
		      Double_t xxx = (sig[j]-bs_2[j])*(200.0/g2[j]*co_shift);
		      
		      if ( xxx>0 && xxx>(15.0*pe) ) { fadc[j] = xxx; hits++; }
		      
		      else fadc[j] = 0.0;
		      
		    }
		  
		  Int_t off1 = 0;
		  
		  for( Int_t j=off1; j<off1+12; j++ ) 
		    {  
		      Int_t ch1 = left[j];
		      
		      Double_t fadc1 = 0.0;
		      
		      if ( ch1!=-1 ) fadc1 = fadc[ ch1 ];
		      
		      if ( fadc[ top[j] ]>0. && ( fadc1>0. || fadc[ right[j] ]>0. ) )
			{
			  is_hit++; ra2++;
			  
			  Float_t max = TMath::Max( fadc1, fadc[ right[j] ] );
			  
			  if ( fadc[ top[j] ]>max ) max_hits[ top[j] ] = 1; 
			  			  
			  else if ( fadc1 > fadc[ right[j] ] ) max_hits[ ch1 ] = 1;
			  			  
			  else max_hits[ right[j] ] = 1;
			  
			  if ( bi_hits[ top[j] ]==0 ) { h_hits_pmt2->Fill( apix[ top[j] ] ); bi_hits[ top[j] ]=1; }
			  
			  if ( fadc1 > fadc[ right[j] ] )
			    {
			      if ( bi_hits[ ch1 ]==0 ) { h_hits_pmt2->Fill( apix[ ch1 ] ); bi_hits[ ch1 ]=1; }
			      
			      if ( fadc[  right[j] ]>0 && bi_hits[ right[j] ]==0 ) { h_hits_pmt2->Fill( apix[ right[j] ] ); bi_hits[ right[j] ]=1; }
			      
			    }
			  else
			    {
			      if ( bi_hits[ right[j] ]==0 ) { h_hits_pmt2->Fill( apix[ right[j] ] ); bi_hits[ right[j] ]=1; }
			      
			      if ( fadc1>0 && bi_hits[ ch1 ]==0 ) { h_hits_pmt2->Fill( apix[ ch1 ] ); bi_hits[ ch1 ]=1; }
			      
			    }
			  
			}
		      
		      Double_t v0 = ( 15.0*thr4 );
		      
		      if ( fadc[ top[j] ]>v0 && ( fadc1>v0 || fadc[ right[j] ]>v0 ) ) is_hit_4++;
		      
		    }
		  		   
		}
	      
	      else if ( smodule==3 ) 
		{
		  mod = 3;
		  
		  for( Int_t j=0; j<24; j++ ) 
		    {  
		      Double_t xxx = (sig[j]-bs_3[j])*(200.0/g3[j]*co_shift);
		      
		      if ( xxx>0 && xxx>(15.0*pe) ) { fadc[j] = xxx; hits++; }
		      
		      else fadc[j] = 0.0;
		      
		    }
		  
		  Int_t off1 = 0;
		  
		  for( Int_t j=off1; j<off1+12; j++ ) 
		    {  
		      Int_t ch1 = left[j];
		      
		      Double_t fadc1 = 0.0;
		      
		      if ( ch1!=-1 ) fadc1 = fadc[ ch1 ];
		      
		      if ( fadc[ top[j] ]>0. && ( fadc1>0. || fadc[ right[j] ]>0. ) )
			{
			  is_hit++; ra3++;
			  
			  Float_t max = TMath::Max( fadc1, fadc[ right[j] ] );
			  
			  if ( fadc[ top[j] ]>max ) max_hits[ top[j] ] = 1; 
			  			  
			  else if ( fadc1 > fadc[ right[j] ] ) max_hits[ ch1 ] = 1;
			  			  
			  else max_hits[ right[j] ] = 1;
			  
			  if ( bi_hits[ top[j] ]==0 ) { h_hits_pmt3->Fill( apix[ top[j] ] ); bi_hits[ top[j] ]=1; }
			  
			  if ( fadc1 > fadc[ right[j] ] )
			    {
			      if ( bi_hits[ ch1 ]==0 ) { h_hits_pmt3->Fill( apix[ ch1 ] ); bi_hits[ ch1 ]=1; }
			      
			      if ( fadc[  right[j] ]>0 && bi_hits[ right[j] ]==0 ) { h_hits_pmt3->Fill( apix[ right[j] ] ); bi_hits[ right[j] ]=1; }
			      
			    }
			  else
			    {
			      if ( bi_hits[ right[j] ]==0 ) { h_hits_pmt3->Fill( apix[ right[j] ] ); bi_hits[ right[j] ]=1; }
			      
			      if ( fadc1>0 && bi_hits[ ch1 ]==0 ) { h_hits_pmt3->Fill( apix[ ch1 ] ); bi_hits[ ch1 ]=1; }
			      
			    }
			  
			}
		      
		      Double_t v0 = ( 15.0*thr4 );
		      
		      if ( fadc[ top[j] ]>v0 && ( fadc1>v0 || fadc[ right[j] ]>v0 ) ) is_hit_4++;
		      
		    }
		  		   
		}
	      
	      else if ( smodule==7 ) 
		{
		  mod = 7; 
		  
		  for( Int_t j=0; j<24; j++ ) 
		    {  
		      Double_t xxx = (sig[j]-bs_7[j])*(200.0/g7[j]*co_shift);
		      
		      if ( xxx>0 && xxx>(15.0*pe) ) { fadc[j] = xxx; hits++; }
		      
		      else fadc[j] = 0.0;
		      
		    }
		  
		  Int_t off1 = 0;
		  
		  for( Int_t j=off1; j<off1+12; j++ ) 
		    {  
		      Int_t ch1 = left[j];
		      
		      Double_t fadc1 = 0.0;
		      
		      if ( ch1!=-1 ) fadc1 = fadc[ ch1 ];
		      
		      if ( fadc[ top[j] ]>0. && ( fadc1>0. || fadc[ right[j] ]>0. ) )
			{
			  is_hit++; ra7++;
			  
			  Float_t max = TMath::Max( fadc1, fadc[ right[j] ] );
			  
			  if ( fadc[ top[j] ]>max ) max_hits[ top[j] ] = 1; 
			  			  
			  else if ( fadc1 > fadc[ right[j] ] ) max_hits[ ch1 ] = 1;
			  			  
			  else max_hits[ right[j] ] = 1;
			  
			  if ( bi_hits[ top[j] ]==0 ) { h_hits_pmt7->Fill( apix[ top[j] ] ); bi_hits[ top[j] ]=1; }
			  
			  if ( fadc1 > fadc[ right[j] ] )
			    {
			      if ( bi_hits[ ch1 ]==0 ) { h_hits_pmt7->Fill( apix[ ch1 ] ); bi_hits[ ch1 ]=1; }
			      
			      if ( fadc[  right[j] ]>0 && bi_hits[ right[j] ]==0 ) { h_hits_pmt7->Fill( apix[ right[j] ] ); bi_hits[ right[j] ]=1; }
			      
			    }
			  else
			    {
			      if ( bi_hits[ right[j] ]==0 ) { h_hits_pmt7->Fill( apix[ right[j] ] ); bi_hits[ right[j] ]=1; }
			      
			      if ( fadc1>0 && bi_hits[ ch1 ]==0 ) { h_hits_pmt7->Fill( apix[ ch1 ] ); bi_hits[ ch1 ]=1; }
			      
			    }
			  
			}
		      
		      Double_t v0 = ( 15.0*thr4 );
		      
		      if ( fadc[ top[j] ]>v0 && ( fadc1>v0 || fadc[ right[j] ]>v0 ) ) is_hit_4++;
		      
		    }
		  		  
		}
	      
	      tpi = tt11; // (high_time*65536.0+low_time)*16.0;
	      
	      if ( is_hit>0 && ( mod==1 || mod==2 ) ) my_tree12->Fill();
	      
	      if ( is_hit>0 && ( mod==3 || mod==7 ) ) my_tree37->Fill();
	      	      
	      pack.clear();
	      
	      pack.push_back( stime_sec_low ); pack.push_back( stime_sec_high ); pack.push_back( stime_16ns_low ); 
	      
	      if ( mod==1 && slen>=4 && is_hit>0 ) p_mod1.push_back( pack );
	      
	      if ( mod==2 && slen>=4 && is_hit>0 ) p_mod2.push_back( pack );
	      
	      if ( mod==3 && slen>=4 && is_hit>0 ) p_mod3.push_back( pack );
	      
	      if ( mod==7 && slen>=4 && is_hit>0 ) p_mod7.push_back( pack );
	      
	    }
	  
	  cout << setw(14) << " [ " << 100 << " % of data processed ]" << endl; 
	  
	  cout << " " << endl; 
	  
	  Int_t nbilayer1 = my_tree12->GetEntries()-start1;
	  
	  Int_t nbilayer2 = my_tree37->GetEntries()-start3;
	  
	  Int_t nbilayer = nbilayer1+nbilayer2; 
	  
	  totbilayer += nbilayer;
	  	  
	  cout << setw(40) << " Number of bi-layer coincidences : " << setw(40) << nbilayer << setw( 40 ) << " ( " << setw( 3 ) << Form( "%.1f", nbilayer/entries*100.0 ) << " % ) " << endl;
	  
	  cout << " " << endl; 
	  
	  cout << setw(40) << " Rate in module 1 : " << setw(40) << ra1/rtime << " +/- " << sqrt(ra1)/rtime << " Hz " << endl;
	  	  
	  cout << " " << endl; 
	  
	  cout << setw(40) << " Rate in module 2 : " << setw(40) << ra2/rtime << " +/- " << sqrt(ra2)/rtime << " Hz " << endl;
	  	  
	  cout << " " << endl; 
	  
	  cout << setw(40) << " Rate in module 3 : " << setw(40) << ra3/rtime << " +/- " << sqrt(ra3)/rtime << " Hz " << endl;
	  
	  cout << " " << endl; 
	  
	  cout << setw(40) << " Rate in module 7 : " << setw(40) << ra7/rtime << " +/- " << sqrt(ra7)/rtime << " Hz " << endl;
	  
	  cout << " " << endl; 
	  
	  tra1+=ra1; tra2+=ra2;
	  
	  tra3+=ra3; tra7+=ra3;
	   
	  // ... done !
	  
	  // Offsets calculation ...
	  
	  Int_t ntot10 = p_mod1.size();
	  
	  Int_t ntot2 = p_mod2.size();
	  
	  for( Int_t i=0; i<ntot10; i++ ) 
	    {
	      //cout << i << endl;
	      
	      for( Int_t j=0; j<ntot2; j++ ) 
		{
		  //cout << j << endl;
		  
		  if ( p_mod1[i].at(0)==p_mod2[j].at(0) && p_mod1[i].at(1)==p_mod2[j].at(1) ) h_off12->Fill( p_mod1[i].at(2)-p_mod2[j].at(2) );
		  
		}
	      
	    }
	  	  
	  pack.clear(); 
	  
	  p_mod1.clear(); p_mod2.clear();
	  
	  Int_t ntot3 = p_mod3.size();
	  
	  Int_t ntot7 = p_mod7.size();
	  
	  for( Int_t i=0; i<ntot3; i++ ) 
	    {
	      //cout << i << endl;
	      
	      for( Int_t j=0; j<ntot7; j++ ) 
		{
		  //cout << j << endl;
		  
		  if ( p_mod3[i].at(0)==p_mod7[j].at(0) && p_mod3[i].at(1)==p_mod7[j].at(1) ) h_off37->Fill( p_mod3[i].at(2)-p_mod7[j].at(2) );
		  
		}
	      
	    }
	  
	  pack.clear(); 
	  	  
	  p_mod3.clear(); p_mod7.clear();
	  
	  offset12 = (Double_t)h_off12->GetBinLowEdge( h_off12->GetMaximumBin() );
	        	
	  cout << setw(40) << " Time offset ( 1, 2 ) : " << setw(40) << offset12 << endl;
	  
	  cout << "" << endl;
	  
	  h_off12->Draw( "" );
	  	  
	  offx[noff] = noff+1;
	  
	  offy12[noff] = offset12;
	  
	  // c1->Update();
	  
	  // c1->WaitPrimitive();
	  
	  delete h_off12; 
	  
	  offset37 = (Double_t)h_off37->GetBinLowEdge( h_off37->GetMaximumBin() );
	        	
	  cout << setw(40) << " Time offset ( 3, 7 ) : " << setw(40) << offset37 << endl;
	  
	  cout << "" << endl;
	  
	  h_off37->Draw( "" );
	  
	  offy37[noff] = offset37;
	  	  
	  // c1->Update();
      
	  // c1->WaitPrimitive();
	  	  
	  delete h_off37; 
	  
	  // ... done !
	  
	  // common variables
	  
	  Int_t p_mod = -1;
	  
	  Float_t p1 = -1;
	  
	  Float_t p2 = -1;
	  
	  Float_t p3 = -1;
	  
	  Float_t p4[24]; 
	  	  	  
	  Float_t p5 = -1;
	  
	  Float_t p6[24]; 
	  
	  Float_t p7[24]; 
	  
	  Float_t p8; 
	  
	  Float_t p9; 
	  	  
	  Int_t s_sw = 0;
	  
	  // Two bilayer-coinc to be found in PMT 1 && 2 ...
	  
	  // :)
	  
	  my_tree12->GetEntry( start1 );
	  
	  p_mod = mod;
	  
	  p1 = sec_hi; p2 = sec_low; p3 = low_time; p5 = high_time;
	  
	  p8 = ni;
	  
	  p9 = is_hit_4; s_sw = 1;
	  
	  for ( Int_t i=0; i<24; i++ ) { p4[i] = fadc[i]; p6[i] = bi_hits[i]; p7[i] = max_hits[i]; } 
	  	  	  
	  Int_t mn1 = (start1+nbilayer1);
	  
	  for ( Int_t i=(start1+1); i<mn1; i++ )
	    {
	      //cout << i < endl;
	      
	      my_tree12->GetEntry( i );
	      
	      if ( mod==1 && p_mod==2 )
		{
		  Float_t dt = low_time-p3; if ( dt<0 && offset12!=0 ) dt += 65536;
		  
		  h12->Fill( dt-offset12 );
		  
		  if ( pow( dt-offset12, 2 )<=toler && s_sw==1 && p1 == sec_hi && p2 == sec_low )
		    {
		      s_sw=2;
		      
		      nxy1 = ni;
		      
		      nxy2 = p8;
		      
		      sec_hi_xy_1 = sec_hi;
		      
		      sec_low_xy_1 = sec_low;
		      
		      high_time_xy_1 = high_time;
		      
		      low_time_xy_1 = low_time;
		      
		      sec_hi_xy_2 = p1;
		      
		      sec_low_xy_2 = p2;
		      
		      high_time_xy_2 = p3;
		      
		      low_time_xy_2 = p5;
		      		      		      
		      for ( Int_t j=0; j<24; j++ ) 
			{
			  fadc1[j] = fadc[j];
			  
			  bi_hits1[j] = bi_hits[j];
			  
			  max_hits1[j] = max_hits[j];
			  			  
			  fadc2[j] = p4[j];
			  
			  bi_hits2[j] = p6[j];
			  
			  max_hits2[j] = p7[j];
			  			  
			}
		      
		      is_hit_4_1 = is_hit_4;
		      is_hit_4_2 = p9;
		      		      
		      if ( TMath::Abs( nxy1 - nxy2 )<4 )
		      my_tree_xy_1->Fill();
		      
		    }
		  
		}
	      
	      if ( mod==2 && p_mod==1 )
		{
		  Float_t dt = p3-low_time; if ( dt<0 && offset12!=0 ) dt += 65536;
		  
		  h12->Fill( dt-offset12 );
		  
		  if ( pow( dt-offset12, 2 )<=toler && s_sw==1 && p1 == sec_hi && p2 == sec_low )
		    {
		      s_sw=2;
		      
		      nxy1 = p8;
		      
		      nxy2 = ni;
		      
		      sec_hi_xy_1 = p1;
		      
		      sec_low_xy_1 = p2;
		      
		      low_time_xy_1 = p3;
		      
		      high_time_xy_1 = p5;
		      
		      sec_hi_xy_2 = sec_hi;
		      
		      sec_low_xy_2 = sec_low;
		      
		      high_time_xy_2 = high_time;
		      
		      low_time_xy_2 = low_time;
		      		      
		      for ( Int_t j=0; j<24; j++ ) 
			{
			  fadc1[j] = p4[j];
			  
			  bi_hits1[j] = p6[j];
			  
			  max_hits1[j] = p7[j];
			  
			  fadc2[j] = fadc[j];
			  
			  bi_hits2[j] = bi_hits[j];
		      
			  max_hits2[j] = max_hits[j];
			  
			}
		      
		      is_hit_4_2 = is_hit_4;
		      is_hit_4_1 = p9;
		      
		      if ( TMath::Abs( nxy1 - nxy2 )<4 ) 
			my_tree_xy_1->Fill();
		      
		    }
		  
		}
	      
	      if ( s_sw==0 ) s_sw=1;
	  
	      if ( s_sw==2 ) s_sw=0;
	      
	      p_mod = mod;
	      
	      p1 = sec_hi; p2 = sec_low; p3 = low_time; p5 = high_time;
	      
	      for ( Int_t j=0; j<24; j++ ) { p4[j] = fadc[j]; p6[j] = bi_hits[j]; p7[j] = max_hits[j]; } 
	      
	      p8 = ni;
	      
	      p9 = is_hit_4;
	      
	    }
	  
	  Int_t ptot1 = totxy1;
	  
	  Int_t n_xy_1 = my_tree_xy_1->GetEntries() - totxy1;
	  
	  cout << setw(40) << " Number of x-y coincidences ( 1, 2 ) : " << setw(40) << n_xy_1 << setw( 40 ) << " ( " << setw( 3 ) << Form( "%.1f", n_xy_1/entries*100.0 ) << " % ) " << endl;
	  
	  cout << " " << endl; 
	  
	  cout << setw(40) << " x-y rate ( 1, 2 ) : " << setw(40) << Form( "%.3f", n_xy_1/rtime ) << " +/- " << Form( "%.3f", sqrt(n_xy_1)/rtime ) << " Hz" << endl;
	  
	  cout << " " << endl; 
	  
	  totxy1 += n_xy_1;
	  
	  ratexy1[noff] = n_xy_1/rtime;
	  
	  ratexy1_e[noff] = sqrt( n_xy_1 )/rtime;
	  
	  // ... done 
	  	  
	  // Same for PMT 3 && 7 ...
	  
	  my_tree37->GetEntry( start3 );
	  
	  p_mod = mod;
	  
	  p1 = sec_hi; p2 = sec_low; p3 = low_time; p5 = high_time;
	  
	  for ( Int_t i=0; i<24; i++ ) { p4[i] = fadc[i]; p6[i] = bi_hits[i]; p7[i] = max_hits[i]; } 
	  
	  p8 = ni;
	  
	  p9 = is_hit_4; s_sw = 1;
	  	  
	  Int_t mn2 = nbilayer2+start3;
	  
	  for ( Int_t i=(start3+1); i<mn2; i++ )
	    {
	      //cout << i < endl;
	      
	      my_tree37->GetEntry( i );
	      
	      if ( mod==3 && p_mod==7 )
		{
		  Float_t dt = low_time-p3; if ( dt<0 && offset37!=0 ) dt += 65536;
		  
		  h37->Fill( dt-offset37 );
		  
		  if ( pow( dt-offset37, 2 )<=toler && s_sw==1 && p1 == sec_hi && p2 == sec_low )
		    {
		      s_sw=2;
		      
		      nxy3 = ni;
		      
		      nxy7 = p8;
		      
		      sec_hi_xy_3 = sec_hi;
		      
		      sec_low_xy_3 = sec_low;
		      
		      low_time_xy_3 = low_time;
		      
		      high_time_xy_3 = high_time;
		      
		      sec_hi_xy_7 = p1;
		      
		      sec_low_xy_7 = p2;
		      
		      high_time_xy_7 = p3;
		      
		      low_time_xy_7 = p5;
		      		      
		      for ( Int_t j=0; j<24; j++ ) 
			{
			  fadc3[j] = fadc[j];
			  
			  bi_hits3[j] = bi_hits[j];
			  
			  max_hits3[j] = max_hits[j];
			  			  
			  fadc7[j] = p4[j];
			  
			  bi_hits7[j] = p6[j];
			  
			  max_hits7[j] = p7[j];
			  
			}
		      
		      is_hit_4_3 = is_hit_4;
		      is_hit_4_7 = p9;
		      
		      if ( TMath::Abs( nxy3 - nxy7 )<4 ) 
			my_tree_xy_3->Fill();
		      
		    }
		  
		}
	      
	      if ( mod==7 && p_mod==3 )
		{
		  Float_t dt = p3-low_time; if ( dt<0 && offset37!=0 ) dt += 65536;
		  
		  h37->Fill( dt-offset37 );
		  
		  if ( pow( dt-offset37, 2 )<=toler && s_sw==1 && p1 == sec_hi && p2 == sec_low )
		    {
		      s_sw=2;
		      
		      nxy3 = p8;
		      
		      nxy7 = ni;
		      		      
		      sec_hi_xy_3 = p1;
		      
		      sec_low_xy_3 = p2;
		      
		      low_time_xy_3 = p3;
		      
		      high_time_xy_3 = p5;
		      
		      sec_hi_xy_7 = sec_hi;
		      
		      sec_low_xy_7 = sec_low;
		      
		      high_time_xy_7 = high_time;
		      
		      low_time_xy_7 = low_time;
		      
		      for ( Int_t j=0; j<24; j++ ) 
			{
			  fadc3[j] = p4[j];
			  
			  bi_hits3[j] = p6[j];
			  
			  max_hits3[j] = p7[j];
			  
			  fadc7[j] = fadc[j];
			  
			  bi_hits7[j] = bi_hits[j];
			  
			  max_hits7[j] = max_hits[j];
			  
			}
		      
		      is_hit_4_7 = is_hit_4;
		      is_hit_4_3 = p9;
		      
		      if ( TMath::Abs( nxy3 - nxy7 )<4 ) 
			my_tree_xy_3->Fill();
		      
		    }
		  
		}
	      
	      if ( s_sw==0 ) s_sw=1;
	      
	      if ( s_sw==2 ) s_sw=0;
	      
	      p_mod = mod;
	      
	      p1 = sec_hi; p2 = sec_low; p3 = low_time; p5 = high_time;
	      
	      for ( Int_t j=0; j<24; j++ ) { p4[j] = fadc[j]; p6[j] = bi_hits[j]; p7[j] = max_hits[j]; } 
	      
	      p8 = ni; p9 = is_hit_4;
	      
	    }
	  
	  // my_tree12->Write();
	  // delete my_tree12;
	  start1 = my_tree12->GetEntries();
	  	  
	  // my_tree37->Write();
	  // delete my_tree37;
	  start3 = my_tree37->GetEntries();
	  
	  
	  Int_t ptot3 = totxy3;
	  
	  Int_t n_xy_3 = my_tree_xy_3->GetEntries() - totxy3;
	  
	  cout << setw(40) << " Number of x-y coincidences ( 3, 7 ) : " << setw(40) << n_xy_3 << setw( 40 ) << " ( " << setw( 3 ) << Form( "%.1f", n_xy_3/entries*100.0 ) << " % ) " << endl;
	  
	  cout << " " << endl; 
	  
	  cout << setw(40) << " x-y rate ( 3, 7 ) : " << setw(40) << Form( "%.3f", n_xy_3/rtime ) << " +/- " << Form( "%.3f", sqrt(n_xy_3)/rtime ) << " Hz" << endl;
	  
	  cout << " " << endl; 
	  
	  totxy3 += n_xy_3;
	  
	  ratexy3[noff] = n_xy_3/rtime;
	  
	  ratexy3_e[noff] = sqrt( n_xy_3 )/rtime;
	  
	  // ... done 
	  
	  noff++;
	  
	  // <---
	  
	  // 1 - 2
	  
	  pack.clear();
	  
	  p_mod1.clear();
	  	  	    
	  Int_t entries_xy_1 = my_tree_xy_1->GetEntries();
	  	  
	  for ( Int_t j=ptot1; j<entries_xy_1; j++ )
	    {
	      my_tree_xy_1->GetEntry(j);
	      
	      pack.clear();
	      
	      pack.push_back( sec_low_xy_1 ); pack.push_back( sec_hi_xy_1 ); pack.push_back( low_time_xy_1 ); 
	      
	      p_mod1.push_back( pack );
	      
	    }
	  
	  pack.clear();
	  
	  p_mod3.clear();
	  
	  Int_t entries_xy_3 = my_tree_xy_3->GetEntries();
	  
	  for ( Int_t j=ptot3; j<entries_xy_3; j++ )
	    {
	      my_tree_xy_3->GetEntry(j);
	      
	      pack.clear();
	      
	      pack.push_back( sec_low_xy_3 ); pack.push_back( sec_hi_xy_3 ); pack.push_back( low_time_xy_3 ); 
	      	      
	      p_mod3.push_back( pack );
	      
	    }
	  
	  Int_t nto1 = p_mod1.size(); 
	  
	  Int_t nto3 = p_mod3.size();
	  
	  for( Int_t i=0; i<nto1; i++ ) 
	    {
	      // cout << i << endl;
	      
	      for( Int_t j=0; j<nto3; j++ ) 
		{
		  // cout << j << endl; getchar();
		  
		  if ( p_mod1[i].at(0)==p_mod3[j].at(0) && p_mod1[i].at(1)==p_mod3[j].at(1) ) 
		    {
		      Float_t dt = p_mod1[i].at(2)-p_mod3[j].at(2); if ( dt<0 ) dt += 65536;
		      
		      h_off13->Fill( dt );
		      
		    }
		  
		}
	      
	    }
	  
	  pack.clear(); 
	  
	  p_mod1.clear(); p_mod3.clear();
	  
	  // 1 - 7 !
	  
	  pack.clear();
	  
	  p_mod1.clear();
	  	  	  
	  for ( Int_t j=ptot1; j<entries_xy_1; j++ )
	    {
	      my_tree_xy_1->GetEntry(j);
	      
	      pack.clear();
	      
	      pack.push_back( sec_low_xy_1 ); pack.push_back( sec_hi_xy_1 ); pack.push_back( low_time_xy_1 ); 
	      
	      p_mod1.push_back( pack );
	      
	    }
	  
	  pack.clear();
	  
	  p_mod7.clear();
	  
	  for ( Int_t j=ptot3; j<entries_xy_3; j++ )
	    {
	      my_tree_xy_3->GetEntry(j);
	      
	      pack.clear();
	      
	      pack.push_back( sec_low_xy_7 ); pack.push_back( sec_hi_xy_7 ); pack.push_back( low_time_xy_7 ); 
	      
	      p_mod7.push_back( pack );
	      
	    }
	  
	  Int_t nto10 = p_mod1.size(); 
	  
	  Int_t nto7 = p_mod7.size();
	  
	  for( Int_t i=0; i<nto10; i++ ) 
	    {
	      // cout << i << endl;
	      
	      for( Int_t j=0; j<nto7; j++ ) 
		{
		  // cout << j << endl; getchar();
		  
		  if ( p_mod1[i].at(0)==p_mod7[j].at(0) && p_mod1[i].at(1)==p_mod7[j].at(1) ) 
		    {
		      Float_t dt = p_mod1[i].at(2)-p_mod7[j].at(2); if ( dt<0 ) dt += 65536;
		      
		      h_off17->Fill( dt );
		      
		    }
		  
		}
	      
	    }
	  
	  pack.clear(); 
	  
	  p_mod1.clear(); p_mod7.clear();
	  
	  // 2 - 3 !
	  
	  pack.clear();
	  
	  p_mod2.clear();
	  	  	  
	  for ( Int_t j=ptot1; j<entries_xy_1; j++ )
	    {
	      my_tree_xy_1->GetEntry(j);
	      
	      pack.clear();
	      
	      pack.push_back( sec_low_xy_2 ); pack.push_back( sec_hi_xy_2 ); pack.push_back( low_time_xy_2 ); 
	      
	      p_mod2.push_back( pack );
	      
	    }
	  
	  pack.clear();
	  
	  p_mod3.clear();
	  
	  for ( Int_t j=ptot3; j<entries_xy_3; j++ )
	    {
	      my_tree_xy_3->GetEntry(j);
	      
	      pack.clear();
	      
	      pack.push_back( sec_low_xy_3 ); pack.push_back( sec_hi_xy_3 ); pack.push_back( low_time_xy_3 ); 
	      
	      p_mod3.push_back( pack );
	      
	    }
	  
	  Int_t nto2 = p_mod2.size(); 
	  
	  nto3 = p_mod3.size();
	  
	  for( Int_t i=0; i<nto2; i++ ) 
	    {
	      // cout << i << endl;
	      
	      for( Int_t j=0; j<nto3; j++ ) 
		{
		  // cout << j << endl; getchar();
		  
		  if ( p_mod2[i].at(0)==p_mod3[j].at(0) && p_mod2[i].at(1)==p_mod3[j].at(1) ) 
		    {
		      Float_t dt = p_mod2[i].at(2)-p_mod3[j].at(2); if ( dt<0 ) dt += 65536;
		      
		      h_off23->Fill( dt );
		      
		    }
		  
		}
	      
	    }
	  
	  pack.clear(); 
	  
	  p_mod2.clear(); p_mod3.clear();
	  
	  // <---
	  
	  cout << "" << endl;
	  
	  // ... extra cout !
	  
	}
      
      iss.clear();
      
    }
  
  f->cd();
  
  // my_tree_xy_1->Write();
  
  // my_tree_xy_3->Write();
      
  cout << setw(40) << " Summary." << endl;
  
  cout << "" << endl;
  
  cout << setw(40) << " Number of sequences : " << setw(40) << nseq << endl;
	  
  cout << "" << endl;
  
  cout << setw(40) << "Total number of files : " << setw(40) << tot_files << endl;
	  
  cout << "" << endl;
  
  cout << setw(40) << " Total number of events : " << setw(40) << tot_events << endl;
  
  cout << "" << endl;
    
  cout << setw(40) << " Total run-time (sec, DAQ clock) : " << setw(40) << ttime <<  setw( 40 ) << " ( " << setw( 3 ) << Form( "%.1f", ttime/3600.0 ) << " h ) " << endl; 
  
  cout << "" << endl;
  
  cout << setw(40) << " Total run-time (sec, chained files) : " << setw(40) << tot_files*dur_sub << setw(40) << " ( " << setw( 3 ) << Form( "%.1f", ( tot_files*dur_sub )/3600.0 ) << " h ) " << endl; 
  
  cout << "" << endl;
  
  cout << setw(40) << " Total number of bi-layer coinc. : " << setw(40) << totbilayer << setw( 40 ) << " ( " << setw( 3 ) << Form( "%.1f", 1.0*totbilayer/(1.0*tot_events)*100.0 ) << " % ) " << endl;
  
  cout << " " << endl; 
  
  cout << setw(40) << " Total rate in module 1 : " << setw(40) << tra1/ttime << " +/- " << sqrt(tra1)/ttime << " Hz " << endl;
  
  cout << " " << endl; 
  
  cout << setw(40) << " Total rate in module 2 : " << setw(40) << tra2/ttime << " +/- " << sqrt(tra2)/ttime << " Hz " << endl;
  
  cout << " " << endl; 
  
  cout << setw(40) << " Total rate in module 3 : " << setw(40) << tra3/ttime << " +/- " << sqrt(tra3)/ttime << " Hz " << endl;
  
  cout << " " << endl; 
  
  cout << setw(40) << " Total rate in module 7 : " << setw(40) << tra7/ttime << " +/- " << sqrt(tra7)/ttime << " Hz " << endl;
  
  cout << " " << endl; 
  
  cout << setw(40) << " Total number of x-y coinc. ( 1, 2 ) : " << setw(40) << totxy1 << setw( 40 ) << " ( " << setw( 3 ) << Form( "%.1f", 1.0*totxy1/(1.0*tot_events)*100.0 ) << " % ) " << endl;
	  
  cout << " " << endl; 
  
  cout << setw(40) << " Total x-y rate ( 1, 2 ) : " << setw(40) << Form( "%.3f", totxy1/ttime )<< " +/- " << Form( "%.3f", sqrt(totxy1)/ttime ) << " Hz" << endl;
  
  cout << " " << endl; 
     
  cout << setw(40) << " Total number of x-y coinc. ( 3, 7 ) : " << setw(40) << totxy3 << setw( 40 ) << " ( " << setw( 3 ) << Form( "%.1f", 1.0*totxy3/(1.0*tot_events)*100.0 ) << " % ) " << endl;
    
  cout << " " << endl; 
  
  cout << setw(40) << " Total x-y rate ( 3, 7 ) : " << setw(40) << Form( "%.3f", totxy3/ttime ) << " +/- " << Form( "%.3f", sqrt(totxy3)/ttime ) << " Hz" << endl;
  	  
  cout << " " << endl; 
      
  Double_t tmin = 1000000000;  
  
  Double_t tmax = -1;
  
  for ( Int_t i=0; i<noff; i++ )
    {
      
      Double_t yyy = rt1[i];
      
      Double_t xxx = rt2[i];
      
      
      if ( yyy>tmax ) tmax = yyy;
      
      if ( xxx>tmax ) tmax = xxx;
      
      
      if ( yyy<tmin ) tmin = yyy;
      
      if ( xxx<tmin ) tmin = xxx;
      
    }
  
  TGraph* gr_rt1 = new TGraph( noff, offx, rt1 );
  
  gr_rt1->SetLineColor( kBlack ); gr_rt1->SetMarkerColor( kAzure+6 ); gr_rt1->SetMarkerStyle( 20 ); gr_rt1->SetMarkerSize( 1.0 );
  
  gr_rt1->SetTitle( "Run time per Run; Run number; Run time in sec" ); 
  
  gr_rt1->SetMinimum( 0.5*tmin ); gr_rt1->SetMaximum( 1.5*tmax );
  
  gr_rt1->GetXaxis()->SetLimits( 0, noff+1 );
  
  gr_rt1->Draw( "APZ" );
  
  gr_rt1->Write( "gr_rt1" );
  
  // c1->Print( Form( "/uboone/data/users/kalousis/MuCS/muons/mega_micro_pdf_%d_%.3f_%d.pdf(", group, pe, calib ) , "pdf" );
  
  // cout << "" << endl;
  
  // c1->Update();
  
  // c1->WaitPrimitive();
  
  TGraph* gr_rt2 = new TGraph( noff, offx, rt2 );
  
  gr_rt2->SetLineColor( kBlack ); gr_rt2->SetMarkerColor( kBlack ); gr_rt2->SetMarkerStyle( 24 ); gr_rt2->SetMarkerSize( 1.0 );
  
  gr_rt2->SetTitle( "Run time per Run; Run number; Run time in sec" ); 
  
  gr_rt2->SetMinimum( 0.5*tmin ); gr_rt2->SetMaximum( 1.5*tmax );
  
  gr_rt2->GetXaxis()->SetLimits( 0, noff+1 );
  
  gr_rt2->Draw( "PZ,SAME" );
  
  gr_rt2->Write( "gr_rt2" );
  
  c1->Print( pdf_path, "pdf" );
  
  cout << "" << endl;
  
  // c1->Update();
  
  // c1->WaitPrimitive();
      
  Double_t omin = 1000000000;  
  
  Double_t omax = -1;
  
  for ( Int_t i=0; i<noff; i++ )
    {
      Double_t yyy = offy12[i];
      
      if ( yyy>omax ) omax = yyy;
      
      if ( yyy<omin ) omin = yyy;
      
    }
  
  TGraph* gr_o_12 = new TGraph( noff, offx, offy12 );
  
  gr_o_12->SetLineColor( kBlack ); gr_o_12->SetMarkerColor( kBlack ); gr_o_12->SetMarkerStyle( 20 ); gr_o_12->SetMarkerSize( 1.0 );
  
  gr_o_12->SetTitle( "Time offset ( 1, 2 ) per Run; Run number; Time offset" ); 
  
  gr_o_12->SetMinimum( 0.5*omin-10.0 ); gr_o_12->SetMaximum( 1.5*omax+10.0 );
  
  gr_o_12->GetXaxis()->SetLimits( 0, noff+1 );
  
  gr_o_12->Draw( "APZ" );
  
  gr_o_12->Write( "gr_o_12" );
  
  c1->Print( pdf_path, "pdf" );
  
  cout << "" << endl;
  
  // c1->Update();
  
  // c1->WaitPrimitive();
  
  omin = 1000000000;  
  
  omax = -1;
  
  for ( Int_t i=0; i<noff; i++ )
    {
      Double_t yyy = offy37[i];
      
      if ( yyy>omax ) omax = yyy;
      
      if ( yyy<omin ) omin = yyy;
      
    }
  
  TGraph* gr_o_37 = new TGraph( noff, offx, offy37 );
  
  gr_o_37->SetLineColor( kBlack ); gr_o_37->SetMarkerColor( kBlack ); gr_o_37->SetMarkerStyle( 20 ); gr_o_37->SetMarkerSize( 1.0 );
  
  gr_o_37->SetTitle( "Time offset ( 3, 7 ) per Run; Run number; Time offset" ); 
  
  gr_o_37->SetMinimum( 0.5*omin-10.0 ); gr_o_37->SetMaximum( 1.5*omax+10.0 );
  
  gr_o_37->GetXaxis()->SetLimits( 0, noff+1 );
    
  gr_o_37->Draw( "APZ" );
  
  gr_o_37->Write( "gr_o_37" );
  
  c1->Print( pdf_path, "pdf" );
  
  cout << "" << endl;
  
  // c1->Update();
  
  // c1->WaitPrimitive();
  
  omin = 1000000000;  
  
  omax = -1;
  
  for ( Int_t i=0; i<noff; i++ )
    {
      Double_t yyy = ratexy1[i];
      
      if ( yyy>omax ) omax = yyy;
      
      if ( yyy<omin ) omin = yyy;
      
    }
  
  TGraphErrors* gr_ratexy1 = new TGraphErrors( noff, offx, ratexy1, 0, ratexy1_e );
  
  gr_ratexy1->SetLineColor( kBlack ); gr_ratexy1->SetMarkerColor( kBlack ); gr_ratexy1->SetMarkerStyle( 20 ); gr_ratexy1->SetMarkerSize( 1.0 );
  
  gr_ratexy1->SetTitle( "x-y rate ( 1, 2 ) per Run; Run number; Rate in Hz" ); 
  
  gr_ratexy1->SetMinimum( 0.5*omin ); gr_ratexy1->SetMaximum( 1.5*omax );
  
  gr_ratexy1->GetXaxis()->SetLimits( 0, noff+1 );
  
  gr_ratexy1->Draw( "APZ" );
  
  gr_ratexy1->Write( "gr_ratexy1" );
  
  c1->Print( pdf_path, "pdf" );
  
  cout << "" << endl;
  
  // c1->Update();
							  
  // c1->WaitPrimitive();
  
   omin = 1000000000;  
  
  omax = -1;
  
  for ( Int_t i=0; i<noff; i++ )
    {
      Double_t yyy = ratexy3[i];
      
      if ( yyy>omax ) omax = yyy;
      
      if ( yyy<omin ) omin = yyy;
      
    }
  
  TGraphErrors* gr_ratexy3 = new TGraphErrors( noff, offx, ratexy3, 0, ratexy3_e );
  
  gr_ratexy3->SetLineColor( kBlack ); gr_ratexy3->SetMarkerColor( kBlack ); gr_ratexy3->SetMarkerStyle( 20 ); gr_ratexy3->SetMarkerSize( 1.0 );
  
  gr_ratexy3->SetTitle( "x-y rate ( 3, 7 ) per Run; Run number; Rate in Hz" ); 
  
  gr_ratexy3->SetMinimum( 0.5*omin ); gr_ratexy3->SetMaximum( 1.5*omax );
  
  gr_ratexy3->GetXaxis()->SetLimits( 0, noff+1 );
  
  gr_ratexy3->Draw( "APZ" );
  
  gr_ratexy3->Write( "gr_ratexy3" );
  
  c1->Print( pdf_path, "pdf" );
  
  cout << "" << endl;
      
  // c1->Update();
							  
  // c1->WaitPrimitive();
  
  h_hits_pmt1->SetLineColor( kBlack ); h_hits_pmt1->SetMarkerColor( kBlack ); h_hits_pmt1->SetMarkerStyle( 20 ); h_hits_pmt1->SetMarkerSize( 1.0 );
  
  Double_t hm = 1.6*h_hits_pmt1->GetBinContent( h_hits_pmt1->GetMaximumBin() );
  
  h_hits_pmt1->SetMinimum(0); h_hits_pmt1->SetMaximum( hm );
  
  h_hits_pmt1->Draw( "pe" );
  
  c1->Print( pdf_path, "pdf" );
  
  cout << "" << endl;
  
  // c1->Update();
	  
  // c1->WaitPrimitive();
  
  h_hits_pmt2->SetLineColor( kBlack ); h_hits_pmt2->SetMarkerColor( kBlack ); h_hits_pmt2->SetMarkerStyle( 20 ); h_hits_pmt2->SetMarkerSize( 1.0 );
  
  hm = 1.6*h_hits_pmt2->GetBinContent( h_hits_pmt2->GetMaximumBin() );
  
  h_hits_pmt2->SetMinimum(0); h_hits_pmt2->SetMaximum( hm );
  
  h_hits_pmt2->Draw( "pe" );
  
  c1->Print( pdf_path, "pdf" );
  
  cout << "" << endl;
  
  // c1->Update();
	  
  // c1->WaitPrimitive();
  
  h_hits_pmt3->SetLineColor( kBlack ); h_hits_pmt3->SetMarkerColor( kBlack ); h_hits_pmt3->SetMarkerStyle( 20 ); h_hits_pmt3->SetMarkerSize( 1.0 );
  
  hm = 1.6*h_hits_pmt3->GetBinContent( h_hits_pmt3->GetMaximumBin() );
  
  h_hits_pmt3->SetMinimum(0); h_hits_pmt3->SetMaximum( hm );
  
  h_hits_pmt3->Draw( "pe" );
  
  c1->Print( pdf_path, "pdf" );
  
  cout << "" << endl;
  
  // c1->Update();
	  
  // c1->WaitPrimitive();
  
  h_hits_pmt7->SetLineColor( kBlack ); h_hits_pmt7->SetMarkerColor( kBlack ); h_hits_pmt7->SetMarkerStyle( 20 ); h_hits_pmt7->SetMarkerSize( 1.0 );
  
  hm = 1.6*h_hits_pmt7->GetBinContent( h_hits_pmt7->GetMaximumBin() );
  
  h_hits_pmt7->SetMinimum(0); h_hits_pmt7->SetMaximum( hm );
  
  h_hits_pmt7->Draw( "pe" );
  
  c1->Print( pdf_path, "pdf" );
  
  cout << "" << endl;
  
  // c1->Update();
	  
  // c1->WaitPrimitive();
  
  f->cd();
  /*
  Int_t nentries_xy_1 = my_tree_xy_1->GetEntries();
  
  for ( Int_t i=1; i<nentries_xy_1; i++ )
    {
      my_tree_xy_1->GetEntry(i);
      
      for ( Int_t j=1; j<24; j++ )
	{
	  if ( max_hits1[j]>0 ) h_pmt1[j]->Fill( fadc1[j] );
	  
	  if ( max_hits2[j]>0 ) h_pmt2[j]->Fill( fadc2[j] );
	  	
	}
            
    }
  
  for ( Int_t i=1; i<24; i++ )
    {
      h_pmt1[i]->SetLineColor( kBlack ); h_pmt1[i]->SetMarkerColor( kBlack ); h_pmt1[i]->SetMarkerStyle( 20 ); h_pmt1[i]->SetMarkerSize( 1.0 ); 
      
      h_pmt1[i]->Draw( "PE" ); 
      
      c1->Print( Form( "/uboone/data/users/kalousis/MuCS/muons/mega_micro_pdf_%d_%.3f_%d.pdf", group, pe, calib ) , "pdf" );
      
      cout << "" << endl;
            
    }
  
  for ( Int_t i=1; i<24; i++ )
    {
      h_pmt2[i]->SetLineColor( kBlack ); h_pmt2[i]->SetMarkerColor( kBlack ); h_pmt2[i]->SetMarkerStyle( 20 ); h_pmt2[i]->SetMarkerSize( 1.0 ); 
      
      h_pmt2[i]->Draw( "PE" ); 
      
      c1->Print( Form( "/uboone/data/users/kalousis/MuCS/muons/mega_micro_pdf_%d_%.3f_%d.pdf", group, pe, calib ) , "pdf" );
      
      cout << "" << endl;
            
    }
  
  Int_t nentries_xy_3 = my_tree_xy_3->GetEntries();
  
  for ( Int_t i=1; i<nentries_xy_3; i++ )
    {
      my_tree_xy_3->GetEntry(i);
      
      for ( Int_t j=1; j<24; j++ )
	{
	  if ( max_hits3[j]>0 ) h_pmt3[j]->Fill( fadc3[j] );
	  
	  if ( max_hits7[j]>0 ) h_pmt7[j]->Fill( fadc7[j] );
	  
	}
            
    }
  
  for ( Int_t i=1; i<24; i++ )
    {
      h_pmt3[i]->SetLineColor( kBlack ); h_pmt3[i]->SetMarkerColor( kBlack ); h_pmt3[i]->SetMarkerStyle( 20 ); h_pmt3[i]->SetMarkerSize( 1.0 ); 
      
      h_pmt3[i]->Draw( "PE" ); 
      
      c1->Print( Form( "/uboone/data/users/kalousis/MuCS/muons/mega_micro_pdf_%d_%.3f_%d.pdf", group, pe, calib ) , "pdf" );
      
      cout << "" << endl;
            
    }
  
  for ( Int_t i=1; i<24; i++ )
    {
      h_pmt7[i]->SetLineColor( kBlack ); h_pmt7[i]->SetMarkerColor( kBlack ); h_pmt7[i]->SetMarkerStyle( 20 ); h_pmt7[i]->SetMarkerSize( 1.0 ); 
      
      h_pmt7[i]->Draw( "PE" ); 
      
      c1->Print( Form( "/uboone/data/users/kalousis/MuCS/muons/mega_micro_pdf_%d_%.3f_%d.pdf", group, pe, calib ) , "pdf" );
      
      cout << "" << endl;
            
    }
  */
  
  vector<Float_t> pack;
  
  vector< vector<Float_t> > p_mod1, p_mod3, p_mod2, p_mod7; 
  
  pack.clear();
  
  p_mod1.clear();
  
  Int_t nentries_xy_1 = my_tree_xy_1->GetEntries();
  
  for ( Int_t i=0; i<nentries_xy_1; i++ )
    {
      my_tree_xy_1->GetEntry(i);
      
      pack.clear();
      
      pack.push_back( sec_low_xy_1 ); pack.push_back( sec_hi_xy_1 ); pack.push_back( low_time_xy_1 ); 
      
      pack.push_back( nxy1 ); pack.push_back( nxy2 ); 
      
      p_mod1.push_back( pack );
      
    }
  
  pack.clear();
  
  p_mod3.clear();
  
  Int_t nentries_xy_3 = my_tree_xy_3->GetEntries();
  
  for ( Int_t i=0; i<nentries_xy_3; i++ )
    {
      my_tree_xy_3->GetEntry(i);
      
      pack.clear();
      
      pack.push_back( sec_low_xy_3 ); pack.push_back( sec_hi_xy_3 ); pack.push_back( low_time_xy_3 ); 
      
      pack.push_back( nxy3 ); pack.push_back( nxy7 );
      
      p_mod3.push_back( pack );
      
    }
  
  Double_t offset13 = (Double_t)h_off13->GetBinLowEdge( h_off13->GetMaximumBin() );
  
  cout << setw(40) << " Time offset ( 1, 3 ) : " << setw(40) << offset13 << endl;
  
  cout << "" << endl;
  
  h_off13->Draw( "" );
  
  // c1->Update();
  
  // c1->WaitPrimitive();
  
  Double_t offset17 = (Double_t)h_off17->GetBinLowEdge( h_off17->GetMaximumBin() );
  
  cout << setw(40) << " Time offset ( 1, 7 ) : " << setw(40) << offset17 << endl;
  
  cout << "" << endl;
  
  h_off17->Draw( "" );
  
  // c1->Update();
  
  // c1->WaitPrimitive();
  
  Double_t offset23 = (Double_t)h_off23->GetBinLowEdge( h_off23->GetMaximumBin() );
  
  cout << setw(40) << " Time offset ( 2, 3 ) : " << setw(40) << offset23 << endl;
  
  cout << "" << endl;
  
  h_off23->Draw( "" );
  
  // c1->Update();
  
  // c1->WaitPrimitive();
  
  // ...
  
  time_t med;  
  
  time( &med );
  
  // 8-fold calculation !
  
  Double_t ne1 = 0.0;
  Double_t ne2 = 0.0;
  Double_t ne3 = 0.0;
  Double_t ne7 = 0.0;
  
  Double_t de1 = 0.0;
  Double_t de2 = 0.0;
  Double_t de3 = 0.0;
  Double_t de7 = 0.0;
  
  Int_t ncoinc = 0;
    
  Int_t ntot1 = p_mod1.size();
  
  Int_t ntot3 = p_mod3.size();
  
  Int_t nti1 = 0;
  
  Float_t acc1 = 0.0;
  
  offset13 += acc1;
  
  Int_t jmin = 0;
  
  for( Int_t i=0; i<ntot1; i++ ) 
    {
      Int_t nti = 0;
	  
      for( Int_t j=jmin; j<ntot3; j++ ) 
	{
	  if ( p_mod1[i].at(0)==p_mod3[j].at(0) && p_mod1[i].at(1)==p_mod3[j].at(1) && p_mod1[i].at(0)!=0.0 && p_mod1[i].at(1)!=0.0 ) 
	    {
	      Float_t dt = ( p_mod1[i].at(2)-p_mod3[j].at(2) );
	      
	      if ( dt<0 && offset13!=0 ) dt += 65536;
	      
	      h13->Fill( dt-offset13 );
	      
	      if ( pow( dt-offset13, 2 )<=toler )
		{
		  Double_t n1 = p_mod1[i].at(3); Double_t n2 = p_mod1[i].at(4);
		  
		  Double_t n3 = p_mod3[j].at(3); Double_t n7 = p_mod3[j].at(4);
		  
		  Double_t sort1[4] = { n1, n2, n3, n7 };
		  
		  Double_t min0 = -1.0;
		  
		  for ( Int_t k=0; k<4; k++ ) 
		    {
		      Double_t qqq = sort1[k];
		      
		      if ( qqq>min0 ) min0 = qqq;
		      
		    }
		  
		  Double_t min1 = -1;
		  
		  for ( Int_t k=0; k<4; k++ ) 
		    {
		      Double_t qqq1 = sort1[k];
		      
		      if ( qqq1>min1 && qqq1<min0 ) min1 = qqq1;
		      
		    }
		  
		  Double_t min2 = -1;
		  
		  for ( Int_t k=0; k<4; k++ ) 
		    {
		      Double_t qqq2 = sort1[k];
		      
		      if ( qqq2>min2 && qqq2<min1 ) min2 = qqq2;
		      
		    }
		  
		  Double_t min3 = -1;
		  
		  for ( Int_t k=0; k<4; k++ ) 
		    {
		      Double_t qqq3 = sort1[k];
		      
		      if ( qqq3>min3 && qqq3<min2 ) min3 = qqq3;
		      
		    }
		  /*		  
		  cout << n1 << ", " << n2 << ", " << n3 << ", " << n7 << endl;
		  
		  cout << "" << endl;
		  
		  cout << min0 << ", " << min1 << ", " << min2 << ", " << min3 << endl;
		  
		  cout << "" << endl;
		  */
		  
		  Double_t che1 = min0-min1;
		  Double_t che2 = min1-min2;
		  Double_t che3 = min2-min3;
		  
		  if ( che1==1.0 && che2==1.0 && che3==1.0 )
		    {
		      // h13->Fill( dt-offset13 );
		  
		  ncoinc++;
		  
		  if ( is_hit_4_2 && is_hit_4_3 && is_hit_4_7 ) ne1++;
		  
		  if ( is_hit_4_1 && is_hit_4_3 && is_hit_4_7 ) ne2++;
		  
		  if ( is_hit_4_1 && is_hit_4_2 && is_hit_4_7 ) ne3++;
		  
		  if ( is_hit_4_1 && is_hit_4_2 && is_hit_4_3 ) ne7++;
		  
		  /*
		  cout << Form( "%.0f", n1 ) << ", " <<  Form( "%.0f", n2 ) << ", " <<  Form( "%.0f", n3 ) << ", " <<  Form( "%.0f", n7 ) << endl;
		  
		  cout << "" << endl;
		  
		  cout << " Found a muon !!! ( " << ncoinc << " ) " << endl;
		  
		  cout << "" << endl;
		  */
		  // getchar();
		  
		  nti++;
		  		  
		  if ( nti>=2 ) { nti1++; }
		  
		  // if ( nti>=2 ) { nti1++; cout << " Ouch ! ( " << nti1 << " ) " << endl; }
		  
		  my_tree_xy_1->GetEntry(i);
		  
		  my_tree_xy_3->GetEntry(j);
		  		  
		  hit1->clear(); hit2->clear(); hit3->clear(); hit7->clear();
		  
		  for( Int_t k=0; k<24; k++ ) 
		    {
		      if ( max_hits1[k]>0 ) { h_pmt1[k]->Fill( fadc1[k] ); h_all->Fill( fadc1[k] ); }
		      
		      if ( max_hits2[k]>0 ) { h_pmt2[k]->Fill( fadc2[k] ); h_all->Fill( fadc2[k] ); }
		      
		      if ( max_hits3[k]>0 ) { h_pmt3[k]->Fill( fadc3[k] ); h_all->Fill( fadc3[k] ); }
		      
		      if ( max_hits7[k]>0 ) { h_pmt7[k]->Fill( fadc7[k] ); h_all->Fill( fadc7[k] ); }
		      
		      if ( bi_hits1[k]>0 ) hit1->push_back( apix[k] );
		      
		      if ( bi_hits2[k]>0 ) hit2->push_back( apix[k] );
		      
		      if ( bi_hits3[k]>0 ) hit3->push_back( apix[k] );
		      
		      if ( bi_hits7[k]>0 ) hit7->push_back( apix[k] );
		      		      
		    }
		  
		  jmin = j+1;
		  
		  my_tree->Fill();
		  /*
		  c3->cd(1);
		      
		  gStyle->SetFrameLineColor( 10 );
		  
		  event_display( c3, fadc7, fadc2, fadc3, fadc1 );
		  
		  // cout << "SONIC BOOOOOOOMMMMM!!!!!" << endl;
		  
		  //for ( UInt_t op=0; op<hit7->size(); op++ ) cout << hit7->at( op ) << ", ";
		  //cout << "" << endl;
		  
		  
		  c3->Update();
		  
		  c3->WaitPrimitive();
		  
		  gStyle->SetFrameLineColor( 1 );

		  c1->cd();
		  */    
		  // Break here ! 
		  		  
		  break;
		  
		    }
		  
		}
	      
	    }
	  
	}
      
    }
  
  // 8-fold rate per run seq. 
  
  TH1F *hn = new TH1F( "hn", "", 100, -1, 1001 );
  
  Int_t lastseq = my_tree->GetEntries()-1;
  
  my_tree->GetEntry(lastseq);
  
  Int_t nseq2 = nseq0;
  
  // cout << nseq2 << endl; getchar();
  
  Double_t rate8[1000];
  
  Double_t rate8_e[1000];
  
  Double_t min8=10000000.0;
  
  Double_t max8=-10000000.0;
  
  for ( Int_t i=0; i<nseq2; i++ )
    {
      my_tree->Draw( "seq>>hn", Form( "seq==%d", i+1 ), "goff" );
      
      Int_t r8 = hn->GetEntries();
      
      // cout << " - " << r8 << endl;
      
      rate8[i] = ( 1.0*r8*1.0 )/rt1[i];
      
      rate8_e[i] = sqrt( 1.0*r8*1.0 )/rt1[i];
      
      if ( rate8[i]>max8 ) max8 = rate8[i];
      
      if ( rate8[i]<min8 ) min8 = rate8[i];
      
      hn->Reset();
      
    }
  
  TGraphErrors* gr_rate8 = new TGraphErrors( noff, offx, rate8, 0, rate8_e );
  
  gr_rate8->SetLineColor( kBlack ); gr_rate8->SetMarkerColor( kBlack ); gr_rate8->SetMarkerStyle( 20 ); gr_rate8->SetMarkerSize( 1.0 );
  
  gr_rate8->SetTitle( "Tow counter coinc. rate per Run; Run number; Rate in Hz" ); 
  
  gr_rate8->SetMinimum( 0.5*min8 ); gr_rate8->SetMaximum( 1.5*max8 );
  
  gr_rate8->GetXaxis()->SetLimits( 0, noff+1 );
  
  gr_rate8->Draw( "APZ" );
  
  gr_rate8->Write( "gr_rate8" );
  
  c1->Print( pdf_path, "pdf" );
    
  cout << "" << endl;
  
  // <--- !!!
  
  cout << setw(40) << " Oops : " << setw(40) << nti1 << endl;
  
  cout << " " << endl; 
    
  cout << setw(40) << " Total number of two counter coinc. : " << setw(40) << ncoinc << setw( 40 ) << " ( " << setw( 3 ) << Form( "%.1f", 1.0*ncoinc/(1.0*tot_events)*100.0 ) << " % ) " << endl;
  
  cout << " " << endl; 
  
  Double_t rate0 = ncoinc/ttime;
  
  Double_t rate0_e = sqrt(ncoinc)/ttime;
  
  cout << setw(40) << " rate of two counter coinc. : " << setw(40) << Form( "%.6f", rate0 ) << " +/- " << Form( "%.3f", rate0_e ) << " Hz" << endl;
  
  cout << " " << endl; 
  
  c1->cd();
  
  for( Int_t k=0; k<24; k++ ) 
    {
      h_pmt1[k]->SetLineColor( kBlack ); h_pmt1[k]->SetMarkerColor( kBlack ); h_pmt1[k]->SetMarkerStyle( 20 ); h_pmt1[k]->SetMarkerSize( 1.0 ); 
      
      h_pmt1[k]->Draw( "pe" );
      
      c1->Print( pdf_path, "pdf" );
      
      cout << "" << endl;
            
    }
  
  for( Int_t k=0; k<24; k++ ) 
    {
      h_pmt2[k]->SetLineColor( kBlack ); h_pmt2[k]->SetMarkerColor( kBlack ); h_pmt2[k]->SetMarkerStyle( 20 ); h_pmt2[k]->SetMarkerSize( 1.0 ); 
      
      h_pmt2[k]->Draw( "pe" );
      
      c1->Print( pdf_path, "pdf" );
      
      cout << "" << endl;
            
    }
  
  for( Int_t k=0; k<24; k++ ) 
    {
      h_pmt3[k]->SetLineColor( kBlack ); h_pmt3[k]->SetMarkerColor( kBlack ); h_pmt3[k]->SetMarkerStyle( 20 ); h_pmt3[k]->SetMarkerSize( 1.0 ); 
      
      h_pmt3[k]->Draw( "pe" );
      
      c1->Print( pdf_path, "pdf" );
      
      cout << "" << endl;
            
    }
  
  for( Int_t k=0; k<24; k++ ) 
    {
      h_pmt7[k]->SetLineColor( kBlack ); h_pmt7[k]->SetMarkerColor( kBlack ); h_pmt7[k]->SetMarkerStyle( 20 ); h_pmt7[k]->SetMarkerSize( 1.0 ); 
      
      h_pmt7[k]->Draw( "pe" );
      
      c1->Print( pdf_path, "pdf" );
      
      cout << "" << endl;
            
    }
  
  h_all->SetLineColor( kBlack ); h_all->SetMarkerColor( kBlack ); h_all->SetMarkerStyle( 20 ); h_all->SetMarkerSize( 1.0 ); 
  
  h_all->Draw( "pe" );
  
  c1->Print( pdf_path, "pdf" );
  
  cout << "" << endl;
  
  // ... done with the eight-fold
  
  // gains 0 to 1 ...
  
  TH1F *h_gains = new TH1F( "h_gains", "ADC means; ADC amplitude", 101, -5, 1005 );
  
  ofstream gains_output( txt2.c_str() );
  
  gains_output << setw(20) << "pmt" << setw(20) << "channel" << setw(20) << "gain" << setw(20) << "variance" << endl;
  
  gains_output << "." << endl;
  
  for( Int_t k=0; k<24; k++ ) 
    {
      Double_t QQQ = h_pmt1[k]->GetMean();
      
      Double_t SSS = h_pmt1[k]->GetRMS();
      
      Int_t ch9 = k;
            
      gains_output << setw(20) << 1.0 << setw(20) << ch9 << setw(20) << QQQ << setw(20) << SSS << endl;
      
      h_gains->Fill( QQQ );
            
    }
  
  for( Int_t k=0; k<24; k++ ) 
    {
      Double_t QQQ = h_pmt2[k]->GetMean();
      
      Double_t SSS = h_pmt2[k]->GetRMS();
      
      Int_t ch9 = k;
            
      gains_output << setw(20) << 2.0 << setw(20) << ch9 << setw(20) << QQQ << setw(20) << SSS << endl;
      
      h_gains->Fill( QQQ );
      
    }
  
  for( Int_t k=0; k<24; k++ ) 
    {
      Double_t QQQ = h_pmt3[k]->GetMean();
      
      Double_t SSS = h_pmt3[k]->GetRMS();
      
      Int_t ch9 = k;
      
      gains_output << setw(20) << 3.0 << setw(20) << ch9 << setw(20) << QQQ << setw(20) << SSS << endl;
      
      h_gains->Fill( QQQ );
      
    }
  
  for( Int_t k=0; k<24; k++ ) 
    {
      Double_t QQQ = h_pmt7[k]->GetMean();
      
      Double_t SSS = h_pmt7[k]->GetRMS();
      
      Int_t ch9 = k;
            
      gains_output << setw(20) << 7.0 << setw(20) << ch9 << setw(20) << QQQ << setw(20) << SSS << endl;
      
      h_gains->Fill( QQQ );
      
    }
  
  gains_output.close();
  
  h_gains->SetLineColor( kBlack ); h_gains->SetMarkerColor( kBlack ); h_gains->SetMarkerStyle( 20 ); h_gains->SetMarkerSize( 1.0 ); 
  
  h_gains->Draw( "" );
  
  c1->Print( pdf_path, "pdf" );
  
  cout << "" << endl;
  
  // ... done with gains !
  
  // Detector efficiencies 
  /*
  Double_t offset23 = offset13-offset12;
  
  if ( offset23<0 ) offset23 += 65536;
      
  cout << setw(40) << " Time offset ( 2, 3 ) : " << setw(40) << offset23 << endl;
  
  cout << "" << endl;
    
  Double_t offset17 = offset13+offset37;
  
  if ( offset17>65536 ) offset17 -= 65536;
    
  cout << setw(40) << " Time offset ( 1, 7 ) : " << setw(40) << offset17 << endl;
  
  cout << "" << endl;
  */
  // cout << "" << endl;
  
  /* efficiencies */
  
  // cout << ne1 << ", " << ne2 << ", " << ne3 << ", " << ne7 << endl;
  
  // cout << "" << endl; getchar();
  
  if ( pas1==0 )
    {
  pack.clear();
  
  p_mod1.clear();
    
  Int_t n000 = my_tree12->GetEntries();
  
  for ( Int_t i=0; i<n000; i++ )
    {
      my_tree12->GetEntry(i);
      
      if ( mod==1 )
	{
	  pack.clear();
	  
	  pack.push_back( sec_low ); pack.push_back( sec_hi ); pack.push_back( low_time ); 
	  
	  pack.push_back( ni ); pack.push_back( i );
	  
	  p_mod1.push_back( pack );
	  
	}
      
    }
  
  ntot1 = p_mod1.size();
  
  for( Int_t i=0; i<ntot1; i++ ) 
    {
      // cout << i << endl;
            
      for( Int_t j=0; j<ntot3; j++ ) 
	{
	  if ( p_mod1[i].at(0)==p_mod3[j].at(0) && p_mod1[i].at(1)==p_mod3[j].at(1) && p_mod1[i].at(0)!=0.0 && p_mod1[i].at(1)!=0.0 ) 
	    {
	      Float_t dt = ( p_mod1[i].at(2)-p_mod3[j].at(2) );
	      
	      if ( dt<0 && offset13!=0 ) dt += 65536;
	      
	      if ( pow( dt-offset13, 2 )<=toler )
		{
		  Double_t n1 = p_mod1[i].at(3); 
		  
		  Double_t n3 = p_mod3[j].at(3); Double_t n7 = p_mod3[j].at(4);
		  
		  Double_t sort1[3] = { n1, n3, n7 };
		  
		  Double_t min0 = -1.0;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq = sort1[k];
		      
		      if ( qqq>min0 ) min0 = qqq;
		      
		    }
		  
		  Double_t min1 = -1;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq1 = sort1[k];
		      
		      if ( qqq1>min1 && qqq1<min0 ) min1 = qqq1;
		      
		    }
		  
		  Double_t min2 = -1;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq2 = sort1[k];
		      
		      if ( qqq2>min2 && qqq2<min1 ) min2 = qqq2;
		      
		    }
		  
		  /*		  
		  cout << n1 << ", " << n3 << ", " << n7 << endl;
		  
		  cout << "" << endl;
		  
		  cout << min0 << ", " << min1 << ", " << min2 << endl;
		  
		  cout << "" << endl; getchar();
		  */
		  if ( TMath::Abs( min0-min2 )<4 )
		    {
		      my_tree12->GetEntry( p_mod1[i].at(4) );
		      
		      my_tree_xy_3->GetEntry(j);
		      
		      if ( is_hit_4>0 && is_hit_4_3>0 && is_hit_4_7>0 ) de2++;
		      
		      break;
		      
		    }
		
		}
	      
	    }
	  
	}
      
    }
  
  Double_t eff_2 = ne2/de2;
  
  Double_t eff_2_e = sqrt( eff_2*(1.0-eff_2)/de2 );
  
  cout << setw(40) << " efficiency 2 : " << setw(40) << eff_2 << " +/- " << eff_2_e << endl;
  
  cout << "" << endl; 
  
  pack.clear();
  
  p_mod1.clear();
    
  for ( Int_t i=0; i<nentries_xy_1; i++ )
    {
      my_tree_xy_1->GetEntry(i);
      
      pack.clear();
      
      pack.push_back( sec_low_xy_1 ); pack.push_back( sec_hi_xy_1 ); pack.push_back( low_time_xy_1 ); 
      
      pack.push_back( nxy1 ); pack.push_back( nxy2 ); 
      
      p_mod1.push_back( pack );
      
    }
  
  p_mod3.clear();
  
  Int_t n111 = my_tree37->GetEntries();
  
  for ( Int_t i=0; i<n111; i++ )
    {
      my_tree37->GetEntry(i);
      
      if ( mod==3 )
	{
	  pack.clear();
	  
	  pack.push_back( sec_low ); pack.push_back( sec_hi ); pack.push_back( low_time ); 
	  
	  pack.push_back( ni ); pack.push_back( i );
	  
	  p_mod3.push_back( pack );
	  
	}
      
    }
  
  ntot1 = p_mod1.size();
  
  ntot3 = p_mod3.size();
  
  for( Int_t i=0; i<ntot1; i++ ) 
    {
      // cout << i << endl;
            
      for( Int_t j=0; j<ntot3; j++ ) 
	{
	  if ( p_mod1[i].at(0)==p_mod3[j].at(0) && p_mod1[i].at(1)==p_mod3[j].at(1) && p_mod1[i].at(0)!=0.0 && p_mod1[i].at(1)!=0.0 ) 
	    {
	      Float_t dt = ( p_mod1[i].at(2)-p_mod3[j].at(2) );
	      
	      if ( dt<0 && offset13!=0 ) dt += 65536;
	      	      
	      if ( pow( dt-offset13, 2 )<=toler )
		{
		  Double_t n1 = p_mod3[j].at(3); 
		  
		  Double_t n3 = p_mod1[i].at(3); Double_t n7 = p_mod1[i].at(4);
		  
		  Double_t sort1[3] = { n1, n3, n7 };
		  
		  Double_t min0 = -1.0;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq = sort1[k];
		      
		      if ( qqq>min0 ) min0 = qqq;
		      
		    }
		  
		  Double_t min1 = -1;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq1 = sort1[k];
		      
		      if ( qqq1>min1 && qqq1<min0 ) min1 = qqq1;
		      
		    }
		  
		  Double_t min2 = -1;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq2 = sort1[k];
		      
		      if ( qqq2>min2 && qqq2<min1 ) min2 = qqq2;
		      
		    }
		  
		  /*		  
		  cout << n1 << ", " << n3 << ", " << n7 << endl;
		  
		  cout << "" << endl;
		  
		  cout << min0 << ", " << min1 << ", " << min2 << endl;
		  
		  cout << "" << endl; getchar();
		  */
		  if ( TMath::Abs( min0-min2 )<4 )
		    {
		      my_tree37->GetEntry( p_mod3[j].at(4) );
		      
		      my_tree_xy_1->GetEntry(i);
		      
		      if ( is_hit_4>0 && is_hit_4_1>0 && is_hit_4_2>0 ) de7++;
		      
		      break;
		      
		    }
		
		}
	      
	    }
	  
	}
      
    }
  
  Double_t eff_7 = ne7/de7;
  
  Double_t eff_7_e = sqrt( eff_7*(1.0-eff_7)/de7 );
  
  cout << setw(40) << " efficiency 7 : " << setw(40) << eff_7 << " +/- " << eff_7_e << endl;
  
  cout << "" << endl; 
  
  pack.clear();
  
  p_mod3.clear();
    
  for ( Int_t i=0; i<nentries_xy_3; i++ )
    {
      my_tree_xy_3->GetEntry(i);
      
      pack.clear();
      
      pack.push_back( sec_low_xy_3 ); pack.push_back( sec_hi_xy_3 ); pack.push_back( low_time_xy_3 ); 
      
      pack.push_back( nxy3 ); pack.push_back( nxy7 ); 
      
      p_mod3.push_back( pack );
      
    }
  
  p_mod2.clear();
    
  for ( Int_t i=0; i<n000; i++ )
    {
      my_tree12->GetEntry(i);
      
      if ( mod==2 )
	{
	  pack.clear();
	  
	  pack.push_back( sec_low ); pack.push_back( sec_hi ); pack.push_back( low_time ); 
	  
	  pack.push_back( ni ); pack.push_back( i );
	  
	  p_mod2.push_back( pack );
	  
	}
      
    }
  
  Int_t ntot2 = p_mod2.size();
  
  ntot3 = p_mod3.size();
  
  for( Int_t i=0; i<ntot2; i++ ) 
    {
      // cout << i << endl;
            
      for( Int_t j=0; j<ntot3; j++ ) 
	{
	  if ( p_mod2[i].at(0)==p_mod3[j].at(0) && p_mod2[i].at(1)==p_mod3[j].at(1) && p_mod2[i].at(0)!=0.0 && p_mod2[i].at(1)!=0.0 ) 
	    {
	      Float_t dt = ( p_mod2[i].at(2)-p_mod3[j].at(2) );
	      
	      if ( dt<0 && offset23!=0 ) dt += 65536;
	      
	      if ( pow( dt-offset23, 2 )<=toler )
		{
		  Double_t n1 = p_mod2[i].at(3); 
		  
		  Double_t n3 = p_mod3[j].at(3); Double_t n7 = p_mod3[j].at(4);
		  
		  Double_t sort1[3] = { n1, n3, n7 };
		  
		  Double_t min0 = -1.0;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq = sort1[k];
		      
		      if ( qqq>min0 ) min0 = qqq;
		      
		    }
		  
		  Double_t min1 = -1;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq1 = sort1[k];
		      
		      if ( qqq1>min1 && qqq1<min0 ) min1 = qqq1;
		      
		    }
		  
		  Double_t min2 = -1;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq2 = sort1[k];
		      
		      if ( qqq2>min2 && qqq2<min1 ) min2 = qqq2;
		      
		    }
		  
		  /*		  
		  cout << n1 << ", " << n3 << ", " << n7 << endl;
		  
		  cout << "" << endl;
		  
		  cout << min0 << ", " << min1 << ", " << min2 << endl;
		  
		  cout << "" << endl; getchar();
		  */
		  if ( TMath::Abs( min0-min2 )<4 )
		    {
		      my_tree12->GetEntry( p_mod2[i].at(4) );
		      
		      my_tree_xy_3->GetEntry(j);
		      
		      if ( is_hit_4>0 && is_hit_4_3>0 && is_hit_4_7>0 ) de1++;
		      
		      break;
		      
		    }
		
		}
	      
	    }
	  
	}
      
    }
  
  Double_t eff_1 = ne1/de1;
  
  Double_t eff_1_e = sqrt( eff_1*(1.0-eff_1)/de1 );
  
  cout << setw(40) << " efficiency 1 : " << setw(40) << eff_1 << " +/- " << eff_1_e << endl;
  
  cout << "" << endl; 
  
  pack.clear();
  
  p_mod1.clear();
    
  for ( Int_t i=0; i<nentries_xy_1; i++ )
    {
      my_tree_xy_1->GetEntry(i);
      
      pack.clear();
      
      pack.push_back( sec_low_xy_1 ); pack.push_back( sec_hi_xy_1 ); pack.push_back( low_time_xy_1 ); 
      
      pack.push_back( nxy1 ); pack.push_back( nxy2 ); 
      
      p_mod1.push_back( pack );
      
    }
  
  p_mod7.clear();
    
  for ( Int_t i=0; i<n111; i++ )
    {
      my_tree37->GetEntry(i);
      
      if ( mod==7 )
	{
	  pack.clear();
	  
	  pack.push_back( sec_low ); pack.push_back( sec_hi ); pack.push_back( low_time ); 
	  
	  pack.push_back( ni ); pack.push_back( i );
	  
	  p_mod7.push_back( pack );
	  
	}
      
    }
  
  ntot1 = p_mod1.size();
  
  Int_t ntot7 = p_mod7.size();
  
  for( Int_t i=0; i<ntot1; i++ ) 
    {
      // cout << i << endl;
            
      for( Int_t j=0; j<ntot7; j++ ) 
	{
	  if ( p_mod1[i].at(0)==p_mod7[j].at(0) && p_mod1[i].at(1)==p_mod7[j].at(1) && p_mod1[i].at(0)!=0.0 && p_mod1[i].at(1)!=0.0 ) 
	    {
	      Float_t dt = ( p_mod1[i].at(2)-p_mod7[j].at(2) );
	      
	      if ( dt<0 && offset17!=0 ) dt += 65536;
	      
	      if ( pow( dt-offset17, 2 )<=toler )
		{
		  Double_t n1 = p_mod7[j].at(3); 
		  
		  Double_t n3 = p_mod1[i].at(3); Double_t n7 = p_mod1[i].at(4);
		  
		  Double_t sort1[3] = { n1, n3, n7 };
		  
		  Double_t min0 = -1.0;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq = sort1[k];
		      
		      if ( qqq>min0 ) min0 = qqq;
		      
		    }
		  
		  Double_t min1 = -1;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq1 = sort1[k];
		      
		      if ( qqq1>min1 && qqq1<min0 ) min1 = qqq1;
		      
		    }
		  
		  Double_t min2 = -1;
		  
		  for ( Int_t k=0; k<3; k++ ) 
		    {
		      Double_t qqq2 = sort1[k];
		      
		      if ( qqq2>min2 && qqq2<min1 ) min2 = qqq2;
		      
		    }
		  
		  /*		  
		  cout << n1 << ", " << n3 << ", " << n7 << endl;
		  
		  cout << "" << endl;
		  
		  cout << min0 << ", " << min1 << ", " << min2 << endl;
		  
		  cout << "" << endl; getchar();
		  */
		  if ( TMath::Abs( min0-min2 )<4 )
		    {
		      my_tree37->GetEntry( p_mod7[j].at(4) );
		      
		      my_tree_xy_1->GetEntry(i);
		      
		      if ( is_hit_4>0 && is_hit_4_1>0 && is_hit_4_2>0 ) de3++;
		      
		      break;
		      
		    }
		
		}
	      
	    }
	  
	}
      
    }
  
  Double_t eff_3 = ne3/de3;
  
  Double_t eff_3_e = sqrt( eff_3*(1.0-eff_3)/de3 );
  
  cout << setw(40) << " efficiency 3 : " << setw(40) << eff_3 << " +/- " << eff_3_e << endl;
  
  cout << "" << endl; 
       
  /* efficiencies */
  
  /* total eff. ! */
  
  Double_t eff_t = eff_1*eff_2*eff_3*eff_7;
  
  Double_t e_eff_t = sqrt( pow( eff_2*eff_3*eff_7*eff_1_e, 2 )+pow( eff_1*eff_3*eff_7*eff_2_e, 2 )+pow( eff_1*eff_2*eff_7*eff_3_e, 2 )+pow( eff_1*eff_2*eff_3*eff_7_e, 2 ) );
    
  cout << setw(40) << " total efficiency : " << setw(40) << eff_t << " +/- " << e_eff_t << endl;
  
  cout << "" << endl;
  
  /* ... */
  
  Double_t rate1 = rate0/eff_t; 
  
  Double_t rate1_e = sqrt( pow( rate0_e/eff_t, 2 )+pow( rate0/(eff_t*eff_t)*e_eff_t, 2 ) );
  
  cout << setw(40) << " Corrected muon rate : " << setw(40) << rate1 <<  " +/- " << rate1_e << " Hz" << endl;
  
  cout << "" << endl;
  
  cout << " ***************************  " << endl;
    
  cout << "" << endl;
  
  cout << setw(40) << " Muon rate (Hz) per m^2 : " << setw(40) << rate1/(0.46*0.46) <<  " +/- " << rate1_e/(0.46*0.46) << " Hz/m^2" << endl;
  
  cout << "" << endl;
  
  cout << " ***************************  " << endl;
    
  cout << "" << endl;
  
  my_tree->GetEntry( 0 ); Double_t tsta1=tt01; Double_t tsta2 = sec_hi_xy_1*65536.0+sec_low_xy_1;
  
  my_tree->GetEntry( 0 ); tsta1=tt01; tsta2 = sec_hi_xy_1*65536.0+sec_low_xy_1;
    
  my_tree->GetEntry( my_tree->GetEntries()-1 ); Double_t tend1=tt01; Double_t tend2 = sec_hi_xy_1*65536.0+sec_low_xy_1;
    
  cout << setw(40) << " Time from t0 : " << setw(40) << ( tend1-tsta1 )*1.0e-9 << endl;
  
  cout << "" << endl;
  
  cout << setw(40) << " Time from UNIX : " << setw(40) << ( tend2-tsta2 ) << endl;
  
  cout << "" << endl;
  
    }
  
  h12->Draw();
  /*
  c1->Update();
      
  c1->WaitPrimitive();
  */
  
  h37->Draw();
  /*
  c1->Update();
      
  c1->WaitPrimitive();
  */
  
  h13->Draw();
  /*
  c1->Update();
      
  c1->WaitPrimitive();
  */
  /* ... */
  
  TCanvas *c2 = new TCanvas( "c2", "" );
  
  c2->cd();
  
  TPaveLabel *label_1 = new TPaveLabel( 0.15, 0.4, 0.85, 0.6, "The End" );
  
  label_1->SetTextFont( 22 );
  
  label_1->SetFillColor( 0 );
  
  label_1->SetShadowColor( 0 );
  
  label_1->Draw();
  
  c2->Print( pdf_path+")", "pdf" );
  
  cout << "" << endl;
  
  time_t end;      
  
  time( &end );
  
  Int_t dura0 = difftime( end, med );      
  
  Int_t min0 = dura0 / 60; Int_t sec0 = dura0 % 60;
    
  Int_t dura = difftime( end, start );      
  
  Int_t min = dura / 60; Int_t sec = dura % 60;
  
  cout << setw(40) << " duration ---> " << Form( "%02d:%02d", min, sec ) << endl;  
  
  cout << "" << endl;
  
  cout << setw(40) << " ---> "<< Form( "%02d:%02d", min0, sec0 ) << endl;  
    
  cout << "" << endl;
  
  delete my_tree12;
  delete my_tree37;
  
  delete my_tree_xy_1; 
  delete my_tree_xy_3;
      
  f->Write();
  
  f->Close();
  
  return 0;
  
}

int main( int argc, char *argv[] )  
{
  argc *= 1.0;
  
  TApplication theApp( "App", 0, 0 );
    
  Int_t group = atoi( argv[1] );
  
  Float_t pe = atof( argv[2] );
  
  Int_t calib = atoi( argv[3] );
                
  mega_micro( group, pe, calib );

}

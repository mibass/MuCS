//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Jul 14 11:39:08 2015 by ROOT version 5.34/25
// from TTree anatree/analysis tree
// found on file: /uboone/data/uboonerd/cosmogenics/cosmics_newgeom_noOB_10MeVcut_merged_anahist.root
//////////////////////////////////////////////////////////

#ifndef anatree_h
#define anatree_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include <vector>

// Fixed size dimensions of array or collections stored in the TTree if any.

class anatree {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Int_t           run;
   Int_t           subrun;
   Int_t           event;
   Double_t        evttime;
   Double_t        beamtime;
   Double_t        pot;
   Char_t          isdata;
   Double_t        taulife;
   Int_t           mcevts_truthcry;
   Int_t           cry_no_primaries;
   Int_t           cry_primaries_pdg[352];   //[cry_no_primaries]
   Float_t         cry_Eng[352];   //[cry_no_primaries]
   Float_t         cry_Px[352];   //[cry_no_primaries]
   Float_t         cry_Py[352];   //[cry_no_primaries]
   Float_t         cry_Pz[352];   //[cry_no_primaries]
   Float_t         cry_P[352];   //[cry_no_primaries]
   Float_t         cry_StartPointx[352];   //[cry_no_primaries]
   Float_t         cry_StartPointy[352];   //[cry_no_primaries]
   Float_t         cry_StartPointz[352];   //[cry_no_primaries]
   Int_t           cry_status_code[352];   //[cry_no_primaries]
   Float_t         cry_mass[352];   //[cry_no_primaries]
   Int_t           cry_trackID[352];   //[cry_no_primaries]
   Int_t           cry_ND[352];   //[cry_no_primaries]
   Int_t           cry_mother[352];   //[cry_no_primaries]
   Int_t           no_primaries;
   Int_t           geant_list_size;
   Int_t           geant_list_size_in_tpcAV;
   Int_t           pdg[1005003];   //[geant_list_size]
   Int_t           status[1005003];   //[geant_list_size]
   Float_t         Mass[1005003];   //[geant_list_size]
   Float_t         Eng[1005003];   //[geant_list_size]
   Float_t         Px[1005003];   //[geant_list_size]
   Float_t         Py[1005003];   //[geant_list_size]
   Float_t         Pz[1005003];   //[geant_list_size]
   Float_t         P[1005003];   //[geant_list_size]
   Float_t         StartPointx[1005003];   //[geant_list_size]
   Float_t         StartPointy[1005003];   //[geant_list_size]
   Float_t         StartPointz[1005003];   //[geant_list_size]
   Float_t         StartT[1005003];   //[geant_list_size]
   Float_t         EndPointx[1005003];   //[geant_list_size]
   Float_t         EndPointy[1005003];   //[geant_list_size]
   Float_t         EndPointz[1005003];   //[geant_list_size]
   Float_t         EndT[1005003];   //[geant_list_size]
   Float_t         theta[1005003];   //[geant_list_size]
   Float_t         phi[1005003];   //[geant_list_size]
   Float_t         theta_xz[1005003];   //[geant_list_size]
   Float_t         theta_yz[1005003];   //[geant_list_size]
   Float_t         pathlen[1005003];   //[geant_list_size]
   Int_t           inTPCActive[1005003];   //[geant_list_size]
   Float_t         StartPointx_tpcAV[1005003];   //[geant_list_size]
   Float_t         StartPointy_tpcAV[1005003];   //[geant_list_size]
   Float_t         StartPointz_tpcAV[1005003];   //[geant_list_size]
   Float_t         EndPointx_tpcAV[1005003];   //[geant_list_size]
   Float_t         EndPointy_tpcAV[1005003];   //[geant_list_size]
   Float_t         EndPointz_tpcAV[1005003];   //[geant_list_size]
   Int_t           NumberDaughters[1005003];   //[geant_list_size]
   Int_t           Mother[1005003];   //[geant_list_size]
   Int_t           TrackId[1005003];   //[geant_list_size]
   Int_t           MergedId[1005003];   //[geant_list_size]
   Int_t           process_primary[1005003];   //[geant_list_size]
   vector<string>  *processname;

   // List of branches
   TBranch        *b_run;   //!
   TBranch        *b_subrun;   //!
   TBranch        *b_event;   //!
   TBranch        *b_evttime;   //!
   TBranch        *b_beamtime;   //!
   TBranch        *b_pot;   //!
   TBranch        *b_isdata;   //!
   TBranch        *b_taulife;   //!
   TBranch        *b_mcevts_truthcry;   //!
   TBranch        *b_cry_no_primaries;   //!
   TBranch        *b_cry_primaries_pdg;   //!
   TBranch        *b_cry_Eng;   //!
   TBranch        *b_cry_Px;   //!
   TBranch        *b_cry_Py;   //!
   TBranch        *b_cry_Pz;   //!
   TBranch        *b_cry_P;   //!
   TBranch        *b_cry_StartPointx;   //!
   TBranch        *b_cry_StartPointy;   //!
   TBranch        *b_cry_StartPointz;   //!
   TBranch        *b_cry_status_code;   //!
   TBranch        *b_cry_mass;   //!
   TBranch        *b_cry_trackID;   //!
   TBranch        *b_cry_ND;   //!
   TBranch        *b_cry_mother;   //!
   TBranch        *b_no_primaries;   //!
   TBranch        *b_geant_list_size;   //!
   TBranch        *b_geant_list_size_in_tpcAV;   //!
   TBranch        *b_pdg;   //!
   TBranch        *b_status;   //!
   TBranch        *b_Mass;   //!
   TBranch        *b_Eng;   //!
   TBranch        *b_Px;   //!
   TBranch        *b_Py;   //!
   TBranch        *b_Pz;   //!
   TBranch        *b_P;   //!
   TBranch        *b_StartPointx;   //!
   TBranch        *b_StartPointy;   //!
   TBranch        *b_StartPointz;   //!
   TBranch        *b_StartT;   //!
   TBranch        *b_EndPointx;   //!
   TBranch        *b_EndPointy;   //!
   TBranch        *b_EndPointz;   //!
   TBranch        *b_EndT;   //!
   TBranch        *b_theta;   //!
   TBranch        *b_phi;   //!
   TBranch        *b_theta_xz;   //!
   TBranch        *b_theta_yz;   //!
   TBranch        *b_pathlen;   //!
   TBranch        *b_inTPCActive;   //!
   TBranch        *b_StartPointx_tpcAV;   //!
   TBranch        *b_StartPointy_tpcAV;   //!
   TBranch        *b_StartPointz_tpcAV;   //!
   TBranch        *b_EndPointx_tpcAV;   //!
   TBranch        *b_EndPointy_tpcAV;   //!
   TBranch        *b_EndPointz_tpcAV;   //!
   TBranch        *b_NumberDaughters;   //!
   TBranch        *b_Mother;   //!
   TBranch        *b_TrackId;   //!
   TBranch        *b_MergedId;   //!
   TBranch        *b_process_primary;   //!
   TBranch        *b_processname;   //!

   anatree(TTree *tree=0);
   virtual ~anatree();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);

};

#endif

#ifdef anatree_cxx
anatree::anatree(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/uboone/data/users/mibass/corsika/corsikaTFG/anatree_corsikaF_CMC_20k_NoXCorrection_noOB_10MeV_v04_14_00.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("/uboone/data/users/mibass/corsika/corsikaTFG/anatree_corsikaF_CMC_20k_NoXCorrection_noOB_10MeV_v04_14_00.root");
      }
      TDirectory * dir = (TDirectory*)f->Get("/uboone/data/users/mibass/corsika/corsikaTFG/anatree_corsikaF_CMC_20k_NoXCorrection_noOB_10MeV_v04_14_00.root:/analysistree");
      dir->GetObject("anatree",tree);

   }
   Init(tree);
}

anatree::~anatree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t anatree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t anatree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void anatree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   processname = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("subrun", &subrun, &b_subrun);
   fChain->SetBranchAddress("event", &event, &b_event);
   fChain->SetBranchAddress("evttime", &evttime, &b_evttime);
   fChain->SetBranchAddress("beamtime", &beamtime, &b_beamtime);
   fChain->SetBranchAddress("pot", &pot, &b_pot);
   fChain->SetBranchAddress("isdata", &isdata, &b_isdata);
   fChain->SetBranchAddress("taulife", &taulife, &b_taulife);
   fChain->SetBranchAddress("mcevts_truthcry", &mcevts_truthcry, &b_mcevts_truthcry);
   fChain->SetBranchAddress("cry_no_primaries", &cry_no_primaries, &b_cry_no_primaries);
   fChain->SetBranchAddress("cry_primaries_pdg", cry_primaries_pdg, &b_cry_primaries_pdg);
   fChain->SetBranchAddress("cry_Eng", cry_Eng, &b_cry_Eng);
   fChain->SetBranchAddress("cry_Px", cry_Px, &b_cry_Px);
   fChain->SetBranchAddress("cry_Py", cry_Py, &b_cry_Py);
   fChain->SetBranchAddress("cry_Pz", cry_Pz, &b_cry_Pz);
   fChain->SetBranchAddress("cry_P", cry_P, &b_cry_P);
   fChain->SetBranchAddress("cry_StartPointx", cry_StartPointx, &b_cry_StartPointx);
   fChain->SetBranchAddress("cry_StartPointy", cry_StartPointy, &b_cry_StartPointy);
   fChain->SetBranchAddress("cry_StartPointz", cry_StartPointz, &b_cry_StartPointz);
   fChain->SetBranchAddress("cry_status_code", cry_status_code, &b_cry_status_code);
   fChain->SetBranchAddress("cry_mass", cry_mass, &b_cry_mass);
   fChain->SetBranchAddress("cry_trackID", cry_trackID, &b_cry_trackID);
   fChain->SetBranchAddress("cry_ND", cry_ND, &b_cry_ND);
   fChain->SetBranchAddress("cry_mother", cry_mother, &b_cry_mother);
   fChain->SetBranchAddress("no_primaries", &no_primaries, &b_no_primaries);
   fChain->SetBranchAddress("geant_list_size", &geant_list_size, &b_geant_list_size);
   fChain->SetBranchAddress("geant_list_size_in_tpcAV", &geant_list_size_in_tpcAV, &b_geant_list_size_in_tpcAV);
   fChain->SetBranchAddress("pdg", pdg, &b_pdg);
   fChain->SetBranchAddress("status", status, &b_status);
   fChain->SetBranchAddress("Mass", Mass, &b_Mass);
   fChain->SetBranchAddress("Eng", Eng, &b_Eng);
   fChain->SetBranchAddress("Px", Px, &b_Px);
   fChain->SetBranchAddress("Py", Py, &b_Py);
   fChain->SetBranchAddress("Pz", Pz, &b_Pz);
   fChain->SetBranchAddress("P", P, &b_P);
   fChain->SetBranchAddress("StartPointx", StartPointx, &b_StartPointx);
   fChain->SetBranchAddress("StartPointy", StartPointy, &b_StartPointy);
   fChain->SetBranchAddress("StartPointz", StartPointz, &b_StartPointz);
   fChain->SetBranchAddress("StartT", StartT, &b_StartT);
   fChain->SetBranchAddress("EndPointx", EndPointx, &b_EndPointx);
   fChain->SetBranchAddress("EndPointy", EndPointy, &b_EndPointy);
   fChain->SetBranchAddress("EndPointz", EndPointz, &b_EndPointz);
   fChain->SetBranchAddress("EndT", EndT, &b_EndT);
   fChain->SetBranchAddress("theta", theta, &b_theta);
   fChain->SetBranchAddress("phi", phi, &b_phi);
   fChain->SetBranchAddress("theta_xz", theta_xz, &b_theta_xz);
   fChain->SetBranchAddress("theta_yz", theta_yz, &b_theta_yz);
   fChain->SetBranchAddress("pathlen", pathlen, &b_pathlen);
   fChain->SetBranchAddress("inTPCActive", inTPCActive, &b_inTPCActive);
   fChain->SetBranchAddress("StartPointx_tpcAV", StartPointx_tpcAV, &b_StartPointx_tpcAV);
   fChain->SetBranchAddress("StartPointy_tpcAV", StartPointy_tpcAV, &b_StartPointy_tpcAV);
   fChain->SetBranchAddress("StartPointz_tpcAV", StartPointz_tpcAV, &b_StartPointz_tpcAV);
   fChain->SetBranchAddress("EndPointx_tpcAV", EndPointx_tpcAV, &b_EndPointx_tpcAV);
   fChain->SetBranchAddress("EndPointy_tpcAV", EndPointy_tpcAV, &b_EndPointy_tpcAV);
   fChain->SetBranchAddress("EndPointz_tpcAV", EndPointz_tpcAV, &b_EndPointz_tpcAV);
   fChain->SetBranchAddress("NumberDaughters", NumberDaughters, &b_NumberDaughters);
   fChain->SetBranchAddress("Mother", Mother, &b_Mother);
   fChain->SetBranchAddress("TrackId", TrackId, &b_TrackId);
   fChain->SetBranchAddress("MergedId", MergedId, &b_MergedId);
   fChain->SetBranchAddress("process_primary", process_primary, &b_process_primary);
   fChain->SetBranchAddress("processname", &processname, &b_processname);
   Notify();
}

Bool_t anatree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void anatree::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t anatree::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef anatree_cxx

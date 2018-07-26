#define anatree_cxx
#include "anatree.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <vector>
#include <iostream>


Long64_t getMother(Long64_t ngeant, Int_t MotherTrackId, Int_t* TrackId){
  //go up in ngeant list until mother is found
  Long64_t n=ngeant;
  while(n>0){
    if(TrackId[n]==MotherTrackId) return n;
    n--; //assume mother comes before daughter
  }
  return 0;
}

Long64_t getPrimary(Long64_t ngeant, Int_t MotherTrackId, Int_t* TrackId, Int_t* Mother,Long64_t &lastDaughter){
  //go up in ngeant list until Mother=0 is found
  Long64_t n=ngeant;
  lastDaughter=ngeant;
  while(n>0){
    if(TrackId[n]==MotherTrackId){
      if(Mother[n]==0) return n; //this is the primary
      MotherTrackId=Mother[n];
      lastDaughter=n;
    }
    n--; //assumes mother comes before daughter
  }
  return 0;
}

void anatree::Loop()
{
//   In a ROOT session, you can do:
//      Root > .L anatree.C
//      Root > anatree t
//      Root > t.GetEntry(12); // Fill t data members with entry number 12
//      Root > t.Show();       // Show values of entry 12
//      Root > t.Show(16);     // Read and show values of entry 16
//      Root > t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();
    //nentries=10;
   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      
      for(int ngeant=0; ngeant< geant_list_size; ngeant++){
        if(inTPCActive[ngeant]==1 && (processname->at(ngeant) == "conv" || processname->at(ngeant) == "compt")){
          Long64_t lastDaughter; //holds the daughter created by the muon, get muon's position from start point
          Long64_t motherngeant=getMother(ngeant,Mother[ngeant],TrackId);
          Long64_t primaryngeant=getPrimary(ngeant,Mother[ngeant],TrackId,Mother,lastDaughter);
          Long64_t mothercheckngeant=getMother(lastDaughter,Mother[lastDaughter],TrackId);
          cout<<jentry<<" "<<ngeant<<" "<<pdg[ngeant]<<" "<<Mother[ngeant]<<" "<<TrackId[ngeant]<<" "<<processname->at(ngeant)<<" "<<Eng[ngeant]<<" "<<motherngeant<<" "<<pdg[motherngeant]<<" "<<Eng[motherngeant]<<" "<<primaryngeant<<" "<<pdg[primaryngeant]<<" "<<Eng[primaryngeant]<<" "<<StartPointx[lastDaughter]<<" "<<StartPointy[lastDaughter]<<" "<<StartPointz[lastDaughter]<<endl;
        }
      }
   }
}


import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.0),
                         ##crossSection = cms.untracked.double(54000000000), # Given by PYTHIA after running
                         ##filterEfficiency = cms.untracked.double(0.004), # Given by PYTHIA after running
                         maxEventsToPrint = cms.untracked.int32(0),


                         ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            #user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/Bd_Psi2SKstar_mumuKpi.dec'),
            user_decay_embedded= cms.vstring('###########################################################',
'# Descriptor: [B0 -> Psi(2S) (mu+ mu-) K*0 (K+ pi-)] + cc #',
'###########################################################',
'Alias      MyB0        B0',
'Alias      Myanti-B0   anti-B0',
'ChargeConj MyB0        Myanti-B0',
'Alias      MyPsi       psi(2S)',
'ChargeConj MyPsi       MyPsi',
'Alias      MyK*0       K*0',
'Alias      Myanti-K*0  anti-K*0',
'ChargeConj MyK*0       Myanti-K*0',
'#',
'Decay MyB0',
'1.000    MyPsi       MyK*0             SVV_HELAMP 0.159 1.563 0.775 0.0 0.612 2.712;',
'Enddecay',
'Decay Myanti-B0',
'1.000    MyPsi       Myanti-K*0        SVV_HELAMP 0.159 1.563 0.775 0.0 0.612 2.712;',
'Enddecay',
'#',
'Decay MyPsi',
'1.000         mu+       mu-            PHOTOS VLL;',
'Enddecay',
'#',
'Decay MyK*0',
'1.000        K+        pi-             VSS;',
'Enddecay',
'Decay Myanti-K*0',
'1.000        K-        pi+             VSS;',
'Enddecay',
'End'),
            list_forced_decays = cms.vstring('MyB0','Myanti-B0'),
            operates_on_particles = cms.vint32()
            ),
        parameterSets = cms.vstring('EvtGen130')
        ),


                         PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
                                                     pythia8CP5SettingsBlock,
                                                     ## check this (need extra parameters?)
                                                     processParameters = cms.vstring('SoftQCD:nonDiffractive = on',
                                                                                     'PTFilter:filter = on', # this turn on the filter
                                                                                     'PTFilter:quarkToFilter = 5', # PDG id of q quark (can be any other)
                                                                                     'PTFilter:scaleToFilter = 1.0' ),
                                                     parameterSets = cms.vstring('pythia8CommonSettings',
                                                                                 'pythia8CP5Settings',
                                                                                 'processParameters',
                                                                                 )
                                                     )
                         )

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    name = cms.untracked.string('$Source: Configuration/Generator/python/PYTHIA8_Bd2Psi2sKstar_EtaPtFilter_CUEP8M1_13TeV_cff.py  $'),
    annotation = cms.untracked.string('Summer16: Pythia8+EvtGen130 generation of Bd --> Psi2S(-> mu+ mu-) K*(892)(K+ pi-) , 13TeV, Tune CUETP8M1')
    )

###########
# Filters #
###########

bfilter = cms.EDFilter(
    "PythiaFilter", 
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(511) ## Bd
    )

psi2sfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1), 
    NumberDaughters = cms.untracked.int32(2), 
    MotherID        = cms.untracked.int32(511), ## Bd  
    ParticleID      = cms.untracked.int32(100443),  ## psi'
    DaughterIDs     = cms.untracked.vint32(13, -13),
    MinPt           = cms.untracked.vdouble(2.5, 2.5), 
    MinEta          = cms.untracked.vdouble(-2.5, -2.5), 
    MaxEta          = cms.untracked.vdouble( 2.5,  2.5)
    )

kstarfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(511),  ## Bd                                                                                          
    ParticleID      = cms.untracked.int32(313),  ## K*^0(892)                                                                              
    DaughterIDs     = cms.untracked.vint32(321, -211),  ## K+, pi-                                                       
    MinPt           = cms.untracked.vdouble(0.4, 0.4),
    MinEta          = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta          = cms.untracked.vdouble( 2.5,  2.5)
    )


ProductionFilterSequence = cms.Sequence(generator*bfilter*psi2sfilter*kstarfilter)

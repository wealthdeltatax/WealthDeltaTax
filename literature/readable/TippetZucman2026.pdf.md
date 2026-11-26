> **Reading copy** of `literature/TippetZucman2026.pdf` (2.1 MB, 33 pages). Route: markitdown; tool: markitdown 0.1.7; converted 2026-11-26.
> Generated, not edited. Quote numbers from the source file, not from this text.

Working Paper n°46
July 2026
Taxing Extreme Wealth in the
United Kingdom: Revenue
Estimates for a 2% Minimum
Tax on Ultra-High-Net-Worth
Households
Ben Tippet, Gabriel Zucman
The views expressed here are those of the author(s) and do not necessarily
reflect those of the International Tax Observatory. International Tax Observatory
working papers are circulated for discussion and comment purposes only.
They have not been subject to peer review or the internal review process that
accompanies official International Tax Observatory publications.
International Tax Observatory is part of the Paris School of Economics

Taxing Extreme Wealth in the United Kingdom: Revenue
Estimates for a 2% Minimum Tax on Ultra-High-Net-Worth
Households
BenTippet* andGabrielZucman**
*King’sCollegeLondon
**ParisSchoolofEconomics;UniversityofCalifornia,Berkeley
July2026
Abstract
The super-rich in the UK, like in many OECD countries, pay lower effective tax rates than ordinary
workers. Atthesametime,thewealthoftherichest300householdshasincreasedfromaround5%ofGDP
in1989to16%today. Thisreportpresentsaresponsetothesechallenges: aminimum2%averageannual
taxonthetotalwealthofhouseholdswithmorethan£100millioninwealth. Thetaxwouldraisearound
£10billionin2026, equivalentto0.3%ofGDPandalmostone-thirdoftheprojectedgovernmentcurrent
budget deficit. As only the richest 1000 households would be taxed, the usual criticisms against historic
wealthtaxes-administrativeinfeasibility,taxevasion,valuationproblems,illiquidassetsandadampening
ofbusinessinnovation-donothold. Theproposalwouldincludea10yearpost-emigrationperiodunder
whichhouseholdswouldremainliableforthetax,buildingonrecentsimiliarchangestoinheritancetaxes.
Giventhesmallnumbersofhouseholdsinvolved,thetaxcouldbeimplementedquicklytostoppreemptive
flight. Revenuesremainsubstantialunderarangeofalternativeassumptionsregardingthetaxmodeland
behaviouralresponses.
1TheoriginaldatasettoconstructthisworkwasfundedbyBritishAcademy/LeverhulmeSmallGrantSRG2223. Wewouldliketo
thankAliBerkKokbudakandJakeHowardforhelpingtoconstructthedataset,andDrRafaelWildauerforhelponpreviousanalysesof
therichlist.WewouldalsoliketothankDrArunAdvaniandco-authorsforthe2020listoftaxresidentsontherichlist.

Contents
1 ExecutiveSummary 3
2 Introduction 4
3 Taxdesign 5
4 DataandMethods 6
5 Results:RevenuesandImpactonWealthConcentration 7
6 Addressingthequestionsofawealthtax 9
6.1 Pastfailures . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
6.2 Administrativecostsanddifficulties . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
6.3 TaxAvoidance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
6.4 Valuation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
6.5 BusinessInnovation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
6.6 CapitalStock . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
6.7 ForeignOwnership . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
6.8 OtherTaxRevenues . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
7 Appendix 14
7.1 Data. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
7.1.1 TheTaxUnit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
7.1.2 Residents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
7.1.3 Imputationofmissingwealthvariables . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
7.2 Method . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
7.2.1 ParetoExtrapolation:theory. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
7.2.2 ParetoExtrapolation:applicationto2026data . . . . . . . . . . . . . . . . . . . . . . . 16
7.2.3 ParetoExtrapolation:validationwith2015and2020data . . . . . . . . . . . . . . . . . 17
7.2.4 Simulationswithoutawealthtax . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
7.2.5 Simulationswithawealthtax . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
7.2.6 Sensitivity:changingnumberofhouseholdsperfamily . . . . . . . . . . . . . . . . . 19
7.2.7 Sensitivity:modelingfragmentation . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
7.2.8 Sensitivity:changingthresholds. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
7.2.9 Sensitivity:changing0.2%existingaveragetaxrate . . . . . . . . . . . . . . . . . . . . 21
7.3 AdditionalTablesandFigures . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
7.3.1 Sensitivity:2%marginalwealthtaxabove£100million . . . . . . . . . . . . . . . . . . 23
2

1 Executive Summary
Thisreportmodelstherevenuepotentialofaminimum2%averageannualtaxonthetotalwealthofhouse-
holdswithmorethan£100millioninwealth.Wefindthatthetaxwouldbe:
• Revenue-generating:A2%minimumtaxonthesuper-richwouldraise£10bnin2026-0.3%ofGDP-
afterbehaviouralresponsesandadministrativecosts.Thiswouldreducethe2026currentbudgetdeficit
-akeymetricintheUKGovernment’sfiscalrules-bynearlyathird.
• Administratively feasible: Fewer than 1,000 households would be subject to the tax, substantially
limitingadministrativecosts,whichareestimatedatlessthan1%ofrevenues.Compliancecouldbesup-
portedthroughcomprehensiveauditpowers,whilehouseholdswithmorethan£100millioninwealth
wouldremainwithinthescopeofthetaxforuptotenyearsafterceasingUKresidence-buildingon
theprinciplerecentlyintroducedfortheUKinheritancetax.
• Sustainable: Overthenext10yearstherevenueswouldincreasefrom0.3%to0.4%ofGDPeachyear,
ifthetrendsofthewealthofthesuper-richandGDPprojectionsoverthelast10yearscontinue.
• Inequality-dampening:Thesuper-richpaylowereffectivetaxratesthanordinaryworkers,whilethe
wealthofthetop3001 householdshasovertripledfrom5%to16%ofGDPbetween1989andtoday. If
currenttrendscontinue,thewealthatthetopwillriseto22%ofGDPby2036. A2%minimumwealth
taxwouldstillseetheirwealthrelativetoGDPrise,butto17.5%.
• Taxingfinanceandrealestate:Over45%oftaxrevenueswillbefromwealthyhouseholdswhohave
primarilymadetheirmoneyinfinance,realestateandland.
1Therichest300householdsmakeupthetop0.001%ofthepopulation.Wepresenthistoricaltimeserieswithjustthetop300house-
holds,ratherthanthefull1000householdsimpactedbythetax,duetodatalimitationsinpreviousversionsoftheSundayTimesRich
List.
3

2 Introduction
Most people accept the simple principle that the very wealthiest in society should not face lower tax rates
thaneveryoneelse. YetthisbasicprincipleisbeingviolatedintheUKtoday. Therichesttaxpayerspayless
than 25% of their income in taxes, much below the average person and the top income tax bracket of 45%
(Advani,Hughson,etal.,2023).2 Atthesametime,wealthconcentrationhasrisendramatically:thewealthof
therichest300householdshastripledfrom5%ofGDPin1989tojustover16%ofGDPtoday(Figure1). The
result is a tax system that raises too little revenue from those most able to contribute at a time when fiscal
pressuresaremounting.
Inresponsetothesechallenges,thisreportoutlinesaproposalfora2%minimumaverageannualtaxonthe
totalwealthofhouseholdswithmorethan£100millioninnetwealth.Underthisproposal,householdsabove
the£100millionthresholdwouldberequiredtopayaminimumaveragetaxrateof2%oftheirtotalwealth
eachyear,discountinganypersonalincometaxestheyalreadypayagainsttheirtaxbill. Householdswhose
existingincometaxpaymentsalreadyexceedtheequivalentof2%oftheirwealthwouldpaynoadditionaltax,
whilethosepayinglesswouldpayonlythedifference. Thistaxwouldensurethatthewealthiesthouseholds
faceaminimumeffectivetaxratecomparabletothatpaidbytherestofsociety.
Theproposalisdeliberatelynarrow. Fewerthan1,000householdswouldbeaffected,representingatiny
fractionofthepopulationbutcontrollingagrowingshareofUKwealth.Theobjectiveisnottocreateabroad-
basedwealthtaxaffectingmillionsofhouseholdsbutratherafocusedtaxonextremewealththatcanmake
billionairespaythesametaxratesastherest,raisemeaningfulrevenuesanddampenrunawayinequality.
The results suggest that such a tax could make a meaningful contribution to the UK’s fiscal position -
approximately £10 billion in 2026 or 0.3% of GDP. This revenue would reduce the current budget deficit by
nearlyathird,akeymetricoftheUKfiscalrules.3 Moreover,theserevenueswouldcontinuetobegenerated
over the coming decade. Assuming past trends of wealth at the top and official projections for GDP from
the Office of Budget Responsibility (OBR), the tax would generate 0.4% of GDP by 2036. Nearly half of the
revenues(45%)wouldberaisedfromwealthprimarilymadeinfinance,realestateandland.
Todelivertheserevenues,thetaxmustbebuiltaroundtwosimpleprinciples. First,theproposalwould
apply a ten-year post-emigration period, under which households with more than £100 million in wealth
wouldremainliablefortheminimumtaxforuptotenyearsafterleavingtheUnitedKingdom.Thisapproach
would prevent billionaires from simply avoiding the tax by relocating abroad. There is a precedent for this
inUKtaxlaw. SinceApril2025,individualswhomeettheUK’slong-termresidencetestforinheritancetax
remainwithinthescopeofUKinheritancetaxforuptotenyearsafterceasingUKresidence.4
Second,thetaxbasemustbecomprehensive. Allformsofnetwealthshouldbeincluded,withoutexcep-
tion. Thehistoryofwealthtaxationshowsthattheeasiestwayforthesuper-richtoavoidawealthtaxisto
lobbyforexemptions,ultimatelyerodingrevenuesandpublicsupport(Perret,2020).
Most importantly, a wealth tax with a £100 million threshold is administratively feasible and could be
implementedquickly. Thetaxwouldapplytofewerthan1,000households, allowingHMRCtoconcentrate
resourcesonvaluation,auditingandenforcement.Manyofthepracticaldifficultiesassociatedwithhistorical
wealth taxes arose because they attempted to tax large sections of the population through systems charac-
terised by numerous exemptions and limited administrative capacity. By focusing exclusively on extreme
wealth,ahigh-thresholdwealthtaxavoidsmanyoftheseproblemswhiletargetingagroupwhosewealthhas
grownparticularlyrapidlyoverrecentdecades.
Without a 2% minimum average wealth tax on households with more than £100 million, the super-rich
willcontinuetopayloweraveragetaxratesthantherestofsociety,andwealthattheverytopwillcontinue
2Advani,Hughson,etal.,2023Figure1showsthatpeoplewithmorethan£10minincomepay25%effectivetaxrates.
3Theprojectedcurrentbudgetdeficitin2026accordingtotheOfficeofBudgetResponsibility(OBR)is£33.9bn. Wefocusonthe
currentbudgetdeficit,ratherthanpublicsectornetborrowing,givenitsuseintheUK’sfiscalrules.
4SeeIHTM47001oftheInheritanceTaxManual.
4

Figure1:Wealthoftop300residenthouseholdstoGDP
Note:Wealth-to-GDPratiosoftop300residenthouseholds(roughlythetop0.001%ofthepopulation)intheUKfromThe
SundayTimesRichList.ThedataonlyincludesUKtaxresidentsontherichlistandsplitsfamilywealthintohouseholds
assetoutinthedataappendix.Dataisfrom(Tippet,2026).
topullaway.Assumingthetrendsofthepastdecade,inadecade’stimethewealthofthetop300households
willreach22%ofGDP.5Undera2%wealthtax,theirwealthtoGDPwouldstillrisebutto17.5%.
It is difficult to justify a system in which some of the wealthiest households can face lower average tax
ratesthanmanyordinaryworkersintheUK.6Capitalgainstaxandinheritancetaxreformwouldhelpreduce
thisunfairnessandshouldbepursued. Yetneithercanfullyaddresstheproblem,becausethewealthofthe
super-richisheldinassetsthatcanbeaccumulatedfordecadesandborrowedagainstwithoutevertriggering
a taxable event. This proposal tackles this directly by taxing wealth itself, rather than waiting for income,
gainsorinheritancestoberealised.
ThequestionisnotwhetherawealthtaxcansolveeveryfiscalchallengefacingtheUK.Itcannot. The
questioniswhetherataxsystemcanremainfairandsustainablewhenextremewealthistaxedmorelightly
thanwork.
Section3setsoutthetaxdesign.Section4givesabriefoverviewofthedataandmethodsforsimulatingthe
taxandsection5presentstheresults. Section6discussespotentialcriticismsandresponsestotheproposal.
Adetaileddataandmethodologicalappendixthatcanbefoundinsection7.
3 Tax design
This report outlines a proposal for a 2% minimum annual tax on the total wealth of households with more
than£100millioninnetwealth. Undertheproposal,householdsabovethe£100millionthresholdwouldbe
requiredtopayaminimumeffectivetaxrateof2%oftheirtotalwealtheachyear,withpersonalincometaxes
already paid credited against this liability. For example, if a household with £200 million in wealth already
paystheequivalentof0.2%ofitswealthinpersonalincometaxes(throughtaxesonsalaries,dividendsand
capitalgains),itwouldpayanadditional1.8%ofitstotalwealthundertheminimumtax.
Theacademicliteratureestimatesthathouseholdswithmorethan£100millioninwealthcurrentlypay
onlyaround0.1–0.2%oftheirwealtheachyearintax(Zucman,2024).7 Thisreportshowsthataminimumtax
5Thelast10yearshasincludedbothperiodsofrisingandfallingwealthatthetop.
6ThisinequityisalsofoundinFrance(Bachetal.,2025),theUSA(Balkiretal.,2025)andtheNetherlands(Bruiletal.,2025).
7Datalinkingthesuper-richtoactualincometaxespaidisnotyetavailablefortheUK,sothisdatacomesfromFrance,theUSAand
5

rateof2%wouldbesufficienttobringtheeffectivetaxratesofthesuper-richintolinewiththosefacedbythe
restofsociety. Anadditionaladvantageoftheproposalisthatitdoesnotpenalisehouseholdsthatalready
payhighlevelsoftax: householdswhoseexistingincometaxpaymentsalreadyexceedtheequivalentof2%
oftheirwealthwouldpaynoadditionaltax,whilethosepayinglesswouldpayonlythedifference.
Thehouseholdistheappropriatetaxunit,aswealthattheverytopisoftenheldcollectivelywithinfamilies
andahousehold-basedapproachreducesopportunitiestoavoidthetaxthroughfragmentingwealth.Thetax
baseshouldbebroad,coveringallformsofnetwealth-includingprivatebusinesses,financialassets,property,
trusts,pensionwealth,land,art,luxuryassets,overseasholdings,charitableassetsoverwhichtheownerstill
hascontrol-toensureequaltreatmentacrosstaxpayersandminimiseavoidanceopportunities.
Toreduceincentivesfortax-motivatedmigration,householdswouldstillbeliableforthewealthtaxupto
10yearsiftheydecidetomovetheirresidencystatus.Thiswouldensurethatindividualswhohaveaccumu-
latedwealthwhileresidentintheUKcannotavoidtaxationsimplybyrelocatingbeforeassetsaresold.Such
taxesarealreadyusedinanumberofcountriesandhelpprotecttheintegrityofthetaxbasewhilelimiting
avoidanceopportunities(SeeDirectorate-GeneralforTaxationandCustomsUnion(EuropeanCommission)
etal.,2026forarecentreviewoftheliteratureonexittaxes),inadditiontohavingprecedentinrecentchanges
toUKinheritancetaxlaw.
A£100millionthresholdischosenprimarilyfortworeasons.First,itisaroundthe£100millionthreshold
thataveragetaxratespaidbythesuper-richtendtodeclinesubstantially(Zucman,2024). Second,ahigher
thresholdavoidsmanyofthevaluationandcomplianceproblemsthataffectedhistoricalwealthtaxesbecause
HMRCcanconcentrateresourcesonaverysmallnumberoftaxpayers.Thesuccessofawealthtaxdependsin
partonitsabilitytobeannouncedandimplementedquickly,limitingopportunitiesforpre-emptiveavoidance
vialeaks. Byrestrictingthetaxtofewerthan1,000households,HMRCcandevoteresourcestoidentifying,
valuing and auditing taxpayers, making rapid implementation feasible. A high threshold therefore reduces
administrativecomplexity, strengthensenforcementandminimisesopportunitiesforbehaviouralresponses
before the tax takes effect. It differs to previous estimates of UK wealth taxes which use lower thresholds
(Tippetetal.,2024;Advani,Chamberlain,etal.,2020;Tippet,2025b;Tippet,2025a).
Taxingaveragewealthinthiswayinevitablycreatesthresholdeffects. Forexample,ahouseholdwhose
wealthincreasesfrom£99millionto£101millionwouldbecomeliablefora2%taxonitsentire£101million
ofwealth. Consequently,despiteaccumulatinganadditional£2millioninwealth,itsafter-taxwealthcould
belowerthanbeforecrossingthethreshold.
However, evidence from Zucman (2024) suggests that these threshold effects are likely to be less pro-
nounced in practice. Households close to the £100 million threshold typically already pay relatively high
amountsoftaxthroughexistingincomeandcapitaltaxescomparedwithhouseholdsfurtherupthewealth
distribution.Whiletheaverageeffectivetaxrateacrosstheultra-wealthyisaround0.2%ofwealth,thismasks
substantialheterogeneity: thelowesteffectivetax ratesaregenerallyobserved amongbillionaires, whereas
centi-millionairesoftenfaceconsiderablyhighereffectiverates.Underaminimumaveragewealthtax,house-
holdswouldonlyberequiredtopayenoughadditionaltaxtobringtheireffectivetaxrateuptothe2%mini-
mum.Asaresult,manyhouseholdsnearthethresholdwouldfaceonlyarelativelysmalltop-up,substantially
reducingthesizeofthediscontinuityatthe£100millioncutoff.
4 Data and Methods
ThisreportusespaneldatafromTheSundayTimesRichlist (STRL),constructedbyTippet(2026). Adetailed
overviewofthedataandthesemethodsareoutlinedinthedataappendix7.
Only entries on the rich list that are likely to be tax residents of the UK are included. Entries are split
theNetherlands.WewelcomeresearcherstoconductasimilarexerciseintheUKandforHMRCtoallowthedataaccessandlinkagesto
dothis.
6

intohouseholds,basedonthenumberofindividualsandfamiliesnamedontherichlist.Weassumeseparate
households for all individuals that are not couples, and an additional 2 households whenever the wealth is
shared between a family, given that each family is likely to have 2 children on average.8 For example, the
richest observation 2026 was “Sanjay and Dheeraj Hinduja and family” with £38bn in wealth. We split this
wealthequallybetween4differenthouseholds: oneforeachbrother(SanjayandDheeraj)andtwomorefor
theadditionalfamily.
In2026, thepooresthouseholdontherichlisthasanestimatednetwealthof£340million. Toestimate
thenumberofhouseholdswithwealthabove£100million,wefitaParetodistributiontotheobservedupper
tailofthe2026RichListandextrapolatebelowtheRichListthreshold.Thisproceduresuggeststhatthereare
approximately946householdswithwealthexceeding£100millionand1710above£50.
Thisestimateisslightlylowerbutinthesameordersofmagnitudewithalternativesources. HMRCfind
that2500individualshavewealthabove£100mand5000withwealthabove£50m. Giventhatthereare2.3
peopleperhouseholdintheUK,thisworksoutatjustover1086and2171householdsrespectively(Davies,
2025,p.14).
Weassumethatallhouseholdsalreadypay0.2%oftheirwealthinincometaxes. Anadditional1.8%tax
ontheirtotalwealthisapplied,andallrevenuesarefromthisadditional1.8%tax.
Revenues are estimated over a 10 year period from 2026 to 2036. In all revenue estimates, we assume
that10%ofthetaxrevenuesarelostduetoavoidanceandevasionfollowingSaezetal.(2026). Theappendix
presentsalternativeestimatesusingdifferentbehaviouralelasticitiesandtaxdesigns.
5 Results: Revenues and Impact on Wealth Concentration
Therearethreekeyresults.
First,aminimum2%averagewealthtaxontotalwealthofhouseholdswithmorethan£100millionwould
raise£10.41billionin2026afterbehaviouralresponses(and£11.57bningrossrevenues). AsshowninTable
1, this is equivalent to 0.33% of GDP and 0.80% of total public sector receipts. In 2026, £10.41 billion would
reducethecurrentbudgetdeficitbyalmostathird,from£33.9billionto£23.9billion.
Second, the wealth tax would continue to generate increasing revenues over time. Assuming that the
wealthofthesuper-richcontinuestogrowalongitsaveragegrowthperyearoverthelastdecade(6.5%)and
thatGDPfollowstheprojectionsoftheOfficeforBudgetResponsibility,annualrevenuesincreasefrom0.33%
of GDP to 0.39% of GDP throughout the next decade. By 2036, annual revenues would reach £20 billion,
equivalentto0.39%ofGDPand0.87%oftotalgovernmentrevenues.
Figure2showstheprojectedimpactofthetaxonthewealthoftherichest300householdsrelativetoGDP.9
In2026,thewealthofthesehouseholdsisjustabove16%ofGDP.Withoutawealthtax,thiswouldriseto22%
ofGDPby2026.Withthetax,themechanicaleffectofpayingthetaxslowsdownthisrapidaccumulationof
wealthatthetop,leavingthewealth-to-GDPratioatjustabove17.5%by2036.Inotherwords,evenwitha2%
minimumaveragewealthtax,thewealthofthesuper-richwouldgrowrelativetothesizeoftheeconomy.
Finally,Figure3showshowtheserevenuesin2026arebrokendownbysector. Over28%oftherevenues
areraisedfromwealthprimarilyheldinthefinancialandinvestmentsector,18%fromtheretail,restaurant,
13%fromtherealestatesector,10%fromindustryandmanufacturing,8%fromtechnologyandICT,6%from
shipping and media, and roughly 4% from the rest (aristocratic estates, energy, mining and commodities,
diversified).
8Section7.2.6intheappendixshowsthattherevenueestimatesarerobusttochangingthisassumptionto+3or+4families.Themain
headlineresultsdonotsubstantiallychange.
9Therichest300householdsmakeupthetop0.001%ofthepopulation.Wepresenthistoricaltimeserieswithjustthetop300house-
holds,ratherthanthefull1000householdsimpactedbythetax,duetodatalimitationsinpreviousversionsoftheSundayTimesRich
List.
7

Table 1: Projected revenues from a 2% minimum wealth tax on total wealth on houesholds with more than
£100million,assumingrealisedrevenuesare10%lowerduetobehaviouralresponses.
Year Grossrevenue(£bn) Revenue10%reduction(£bn) Revenue(%GDP) Revenue(%govrev)
| 2026 | 11.57 | 10.41 | 0.33 | 0.80 |
| ---- | ----- | ----- | ---- | ---- |
| 2027 | 12.19 | 10.97 | 0.33 | 0.80 |
| 2028 | 12.86 | 11.58 | 0.34 | 0.81 |
| 2029 | 13.54 | 12.18 | 0.35 | 0.82 |
| 2030 | 14.26 | 12.84 | 0.35 | 0.83 |
| 2031 | 15.04 | 13.53 | 0.36 | 0.84 |
| 2032 | 15.87 | 14.28 | 0.37 | 0.84 |
| 2033 | 16.74 | 15.07 | 0.37 | 0.85 |
| 2034 | 17.64 | 15.88 | 0.38 | 0.86 |
| 2035 | 18.58 | 16.73 | 0.39 | 0.87 |
| 2036 | 19.56 | 17.61 | 0.39 | 0.87 |
Figure2:Wealthoftop300residenthouseholdstoGDP(£bncurrent)
Note: Wealth-to-GDPratiosoftop300residenthouseholdsintheUKwithandwithouta2%minimumaveragetaxon
householdswithmorethan£100minnetwealth.Thetaxremainsliablefor10yearsevenifthesuper-richmoretheirtax
residencyabroad.Weassumea10%avoidancerate,giventhatthistaxwouldbeveryhardtoavoidintheshortrun.
8

Figure3:Revenuesbysector
Note: Revenues of minimum average 2% wealth tax on total wealth of households with more than £100m by different
sectors.
Overalltherevenueestimatesappearrobusttoarangeofalternativeassumptions.Threesensitivitytests
areconducted,withfullresultsarepresentedinAppendix7.3.1.
First,ratherthanestimatingaminimumaveragetax, wealsoestimatetherevenueofa2%marginaltax
onallwealthabove£100million.In2026,thiswouldraise£9.86bnassuminga10%avoidancerate.
6 Addressing the questions of a wealth tax
6.1 Pastfailures
Critics often point to the decline in the number of European wealth taxes since the 1990s as proof that
wealth taxes do not work. However, most historical wealth taxes were fundamentally different from the
proposaloutlinedhere.Theytypicallyhadrelativelylowthresholds,coveredlargesectionsofthepopulation,
and/orcontainedextensiveexemptionsforparticularassets,inparticularprivatebusinessassets(Perret,2020;
Directorate-GeneralforTaxationandCustomsUnion(EuropeanCommission)etal.,2026).Theseexemptions
created avoidance opportunities, reduced revenues, and generated political opposition from taxpayers who
feltunfairlytreated.
Thelessonsfromtheseexperiencesareclear.Wealthtaxesworkbestwhentheyfocusontheverywealth-
iest households, apply to a broad asset base, and are supported by strong administrative enforcement. The
question is not whether past wealth taxes were perfect, but whether we can learn from their shortcomings
anddesignabettersystem.Ataxrestrictedtoonlythosewithmorethan£100millionincludeslessthan1000
households,meaningprivatebusinessassetsdonotneedtobeexemptedandopportunitiesforavoidingthe
taxcanbeprevented.
9

6.2 Administrativecostsanddifficulties
Administrative costs areone of the most commonobjections to wealth taxes. However, these costs depend
criticallyonthethresholdchosen. Ataxaffectingmillionsofhouseholdswouldrequiresubstantialadminis-
trativeresources.Ataxaffectingonlythosewithwealthabove£100millionwouldnot.
The UK already operates sophisticated systems for administering taxes on income, capital gains, inher-
itance and corporate profits. HMRC has already started to enhance its understanding of billionaire wealth.
Fromautumn2026,followingtherecommendationsoftheCommitteeofPublicAccountsin2024-25,HMRC
willprovideassurancethatallbillionairesintheUKwithataxfootprintareassignedaCustomerCompliance
Manager(CCM)-seniortaxprofessionalswhoprovideextrascrutinyofindividualswithcomplextaxaffairs.10
It is not just the households above the threshold that would need to be audited but all households near
the threshold. We suggest that any household with more than £50m in wealth should be checked. HMRC
findsthatthiswouldbe5000individuals(orjustover2100households)(Davies,2025,p.14).Itcurrentlycosts
HMRC£2,500toauditeachreturn(Advani,Chamberlain,etal.,2020).Evensupposingthatforthesuper-rich
thesecostswereincreasedbyafactorof10duetothecomplexityoftheirtaxaffairs,thecoststoauditingall
householdsabove£50mwouldbe£52.5m(2100x£25,000),or0.5%oftherevenuesofthetax.Evensupposing
afurther£50minfixedcostswouldmeanthatadministrationcostsremainlessthan1%oftotalrevenues.
6.3 TaxAvoidance
Therearethreeprincipalwaysinwhichwealthyhouseholdscouldattempttoreducetheirpaymentsinthe
shortrununderanannualwealthtax:changingtaxresidency,fragmentingwealthacrossmultiplehouseholds,
andconcealingassetsthroughtrustsorotheroffshorestructures. Noneofthesewouldbeparticularlyviable
underthecurrentproposal.
To reduce migration responses, the proposal would include a ten-year post-emigration liability period,
underwhichhouseholdswithmorethan£100millioninwealthwouldremainliablefortheminimumtaxfor
uptotenyearsafterleavingtheUnitedKingdom,withcreditsavailableforanyequivalentwealthtaxespaid
overseas.11 Aswithanymajortaxreform,thetimingoftheannouncementisimportant.Speculationaboutthe
introductionofthepolicycouldencouragesomehouseholdstochangetheirtaxresidencebeforeitcomesinto
force.Giventherelativelysmallnumberofhouseholdsaffected,theproposalshouldthereforebeannounced
withimmediateeffectandwithoutadvancenotice.LiabilityshouldbedeterminedbasedonUKtaxresidence
onthedateoftheannouncement(orimmediatelybeforehand), consistentwiththeapproachrecommended
bytheUKWealthTaxCommission. Becausefewerthan1,000householdswouldfallwithinthescopeofthe
tax,implementingandenforcingthepolicyoverashorttimescalewouldbeadministrativelyfeasible.
Given the high threshold, fragmentation may occur to bring households at the threshold below £100m.
Wealthmaybetransferredacrossrelativesorfriendsinordertoreducetaxablewealthbelowthethreshold.
Forthisreason,followingChamberlain(2020),weusethehouseholdratherthantheindividualasthetaxunit
to prevent fragmentation between spouses and children still living in the family home. Fragmentation also
becomeslesseffectivefurtherupthewealthdistributionandthereforecannotrealisticallybeusedtoavoidall
taxes.Itwouldrequireownerstogiveawayamajorityoftheirfortunestoavoida2%wealthtax.Moreover,as
wetaxtotalwealth,splittingwealthfurtherupthedistributionwouldstillbeliableunlessitissplitsomany
timesthateachhouseholdhaslessthan£100m.
The scope for offshore evasion is also limited by the small number of taxpayers affected. The objective
is not to assume zero avoidance, but to design a system in which avoidance is costly, difficult and highly
visible.Becausethetaxappliesonlytohouseholdswithmorethan£100millioninwealth,HMRCcanconcen-
trateenforcementresourcesonarelativelysmallnumberoftaxpayers. Internationalinformationexchange
10SeeBalataetal.(2026)foranoverviewofrecommendationsonhowtobuildadministrativesystemstotaxwealth.
11Asveryfewcountriescurrentlyhaveeffectivewaysoftaxingthesuper-richinrealitythesewouldbenegligibleforthetimebeing
andwethereforedonotmodelthem.
10

agreements,beneficialownershipregistersandstrengthenedanti-avoidancemeasureshavealsosubstantially
reducedopportunitiestoconcealwealthoffshore.
Inthelongrun(20–30years),awealthtaxmayinfluencesaving,governmentandinvestmentdecisions,
leading to changes in the accumulation of wealth. In the short run, however, there is no clear economic
mechanismthroughwhichexistingwealthwouldsimplydisappear.
6.4 Valuation
Allassetsshouldbevaluedaccordingtotheiropenmarketvalue:thepricetheywouldreasonablybeexpected
toachieveinanarm’s-lengthtransaction.Openmarketvaluationisalreadyusedextensivelythroughoutthe
UKtaxsystem,includingforinheritancetaxandcapitalgainstax.Acommonconcernisthatprivatebusiness
assets,whichconstitutealargeshareofwealthatthetopofthedistribution,aretoodifficulttovalueonan
annualbasis.
Concernsaboutvaluationareoftenoverstated. AsSaezetal.(2019)argue, valuationdifficultiesarepri-
marilyanadministrativechallengeratherthanafundamentalobstacletowealthtaxation. Ataxapplyingto
fewerthan1000householdsallowsHMRCtodevotespecialistexpertisetocomplexcasesandtorequireaddi-
tionalreportingwherenecessary. HMRCalreadycollectextensiveinformationonfinancialassets,property
ownershipandbusinessinterestsandarealreadyconstructingcomprehensivewealthassessmentsformost
taxpayers(Davies,2025).AsSaezetal.(2019)note,governmentscanalsocreatemechanismsthathelpreveal
marketvalueswhenrequired,forexamplebyallowingtaxpayerstosettleliabilitiesusingsharesinprivately
heldbusinessesiftheydisputethegovernment’svaluation.
6.5 BusinessInnovation
Acommoncriticismofwealthtaxesisthattheydiscourageentrepreneurshipandinnovation(Neidle,2025).
Start-ups often generate little or no profit in their early years and involve substantial risk. Because wealth
taxesimposeahighereffectivetaxrateonlow-returnassetsthanonhigh-returnassets12, theymayreduce
incentivestoundertakeriskyinvestmentsandcreatesuccessfulnewbusinesses(Hebousetal.,2024;Mirrlees
etal.,2011,p.19).
Forawealthtaxbeginningat£100millioninnetwealth,concernsregardingbusinessinnovationarelikely
tobelimited.AsSaezetal.(2019)argue,policiesaimedatencouraginginnovationshouldfocusonyoungand
not-yet-wealthy individuals. The key determinants of entrepreneurship are access to finance (Holtz-Eakin
etal.,1994),exposuretoinnovation(Belletal.,2019),skills(Guvenenetal.,2023)andprofitableopportunities,
ratherthantheprospectofpayingawealthtaxafterbecomingoneoftherichesthouseholdsinthecountry.
A tax that only applies once an individual has accumulated more than £100 million in wealth is therefore
unlikelytomateriallyaffectthedecisiontostartabusiness.Evenprogressiveincometaxes,whichstartmuch
lowerdownthedistribution,havebeenshowntohaveamixedimpactonrisktaking(Gentryetal.(2005)find
negativeeffectswhileCullenetal.(2007)findpositiveones).
A high-threshold wealth tax may actually increase economic dynamism. The tax does not affect new
entrants but instead falls on individuals who have already accumulated exceptionally large fortunes, who
tendtospendalargeamountoftheirincomesfightingcompetitionfromnewcomers. Bymodestlyreducing
theadvantagesenjoyedbyincumbentwealthholders,itmayimproveopportunitiesfornewentrepreneursto
compete(Saezetal.,2019).Similarly,recenttheoreticalworkbyGuvenenetal.(2023)showsthatawealthtax
canimprovetheallocationofcapitalbyencouragingitsmovementfromlessproductivetomoreproductive
entrepreneurs.Inthisuse-it-or-lose-itframework,thehighereffectivetaxburdenonlow-returnassetsisnot
necessarilyadistortion,butmayhelpdirectresourcestowardsmoreinnovativeandproductiveuses.
12Becausethetaxisleviedonthestockofwealthratherthanthereturngeneratedbythatwealth,thesametaxliabilityapplieswhether
anassetgeneratesareturnof2%,10%ornoreturnatall.A2%wealthtaxthereforerepresentsamuchlargershareofprofitsforlow-return
businessesthanforhigh-returnbusinesses.
11

6.6 CapitalStock
A separate concern is that a wealth tax may reduce the aggregate stock of productive capital available to
the economy. Several mechanisms have been proposed. Wealthy business owners may increase dividend
paymentsinordertofinancetheirtaxliabilities,reducingretainedearningsavailableforinvestment(Johnsen
etal.,2014;Fuestetal.,2018;Barrosoetal.,2023).Householdsmayalsoincreaseconsumptionorshiftwealth
towardshard-to-valueassetssuchasart,jewellery,vintagecarsoryachts,reducinginvestmentinproductive
activities(Neidle,2025).
However, theseargumentsrelyontheassumptionthatreducingthewealthoftheveryrichnecessarily
reduces the economy’s capital stock. As Saez et al. (2019) emphasise, a distinction must be made between
privatewealthandproductivecapital.Thevalueofprivatewealthcanincreasebecauseofhigherassetprices,
monopolypower,intellectualpropertyrights,rentextractionandothervaluationeffects,evenwhentheun-
derlyingstockofproductivecapitalremainsunchanged. Areductioninthewealthoftheveryrichtherefore
does not necessarily imply a reduction in the quantity of productive capital available to the economy. This
distinction may be particularly important in economies where a growing share of wealth reflects economic
rentsratherthanproductiveinvestment. AsBottaetal.(2021)argue,risingwealthconcentrationcanbeas-
sociatedwithincreasingrentextractionandmarketpowerratherthanhigherratesofproductiveinvestment.
Areductioninextremewealthconcentrationthereforeneednotreduceproductivecapacityandcanactually
increasegrowth.Nearlyhalfofallrevenuesfromthistaxwouldbefromrealestate,landandfinance(Tippet,
2026).
Moreover, wealth tax revenues remain within the economy rather than disappearing. Revenues can be
used to finance public investment, support innovation, reduce borrowing or fund other growth-enhancing
expenditures, leading to overall increases in growth (Onaran et al., 2023). Similarly, if wealthy households
reduce their holdings of particular assets, those assets remain available to be purchased by other domestic
orforeigninvestors. Theproductiveassetdoesnotdisappearandsolongastheassetisprofitable,itwillbe
boughtbyotheractorsinthemarket. Thewealthtaxsimplytargetsthehighconcentrationofthatassetin
onehousehold.
Theconcernregardingshiftsintohard-to-valueassetsmayalsobelessimportantwhenthethresholdis
set at £100 million. The practical scope for shifting hundreds of millions of pounds away from productive
investmentsintoart, jewelleryorothercollectiblesislimited, particularlygiventheauditingresourcesthat
HMRCcoulduseforeachtaxunitasdiscussed.
Theexistingempiricalliteraturegenerallyfindslimitedeffectsofwealthtaxesoninvestmentandeconomic
growth(Seim,2017;Bru¨lhartetal.,2022;Dura´n-Cabre´etal.,2019;Bjørnebyetal.,2023).OnestudyonNorway
evenfindspositivelaboursupplyeffects,ashouseholdsincreaseworkeffortinresponsetolowerwealth(Ring,
2025). However,manyhistoricalwealthtaxescontainedextensiveexemptionsandavoidanceopportunities,
makingitdifficulttodrawstrongconclusionsfrompastexperience(Neidle,2025).
6.7 ForeignOwnership
ThedesignproposedinthisreportfollowstherecommendationsoftheWealthTaxCommissionbyapplying
thetaxtoUKlandandpropertyownedbynon-residents,whilenotextendingthetaxtomostotherUKassets
heldbyforeigners. Thisreflectsapracticaldistinction. Landandpropertyareimmobileandalreadysubject
toarangeoftaxesirrespectiveoftheowner’sresidence.ExtendingthewealthtaxtoforeignownershipofUK
businessesandfinancialassetswouldraisemoresignificantconcernsregardinginternationalcompetitiveness
andinvestment.
Acommoncriticismofthisapproachhoweveristhattheymayplacedomesticinvestorsatadisadvantage
relativetoforeigninvestors(ibid.). SupposeaUKresidentwithwealthabove£100millionwishestoacquire
a UK business. Because they are subject to the wealth tax, the after-tax return from owning the asset may
12

belowerthanforanotherwiseidenticalforeigninvestorwhoisnotliableforthetax. Overtime,thiscould
increaseforeignownershipofUKassets.
However, the importance of this effect should not be overstated. A wealth tax is explicitly designed to
slow the accumulation of extreme wealth among a small number of households. The fact that UK centi-
millionairesmayownasmallershareofUKassetsovertimedoesnotnecessarilymeanthatforeignerswill
buythoseassets.Potentialbuyerscouldalsoincludethemuchlargerpoolofunaffecteddomesticinvestorsand
institutionswhodonothave£100minwealth,suchasentrepreneurs,households,pensionfunds,insurance
companies,listedcompaniesorprivateequityfunds.Solongasthoseassetsremainprofitable,theseinvestors
wouldbeinterestedinbuyingthem.
6.8 OtherTaxRevenues
Oneconcernisthatawealthtaxmayreducerevenuesfromothertaxesifwealthyhouseholdsaltertheirbe-
haviour.SomebehaviouralresponsesremovewealthfromtheUKtaxbasealtogether,suchasconcealingassets
offshore,migratingtoanothercountry,oraccumulatinglesswealthinthefirstplace.Fragmentingwealth,by
contrast,doesnotreducethestockofwealthitself;itsimplyredistributesownershipacrosshouseholds.
Zucman(2024)estimatesthattheglobaleffectivetaxrateonbillionairewealthisapproximately0.2%as
afractionofwealth. Ifallofthewealthlostthroughbehaviouralresponsesin2026wereremovedfromthe
UKtaxbase,taxablewealthwouldfallbyaround10%,equivalenttoapproximately£64billion.Applyinga0.2
percenteffectivetaxrateimpliesareductioninrevenuesfromothertaxesofaround£128millionperyear.
Thisisequivalenttolessthan1.5%ofthe£10billionraisedbythewealthtaxin2026andthereforehasonly
amodesteffectontheoverallrevenueestimates.
13

7 Appendix
7.1 Data
This report uses panel data from The Sunday Times Rich list (STRL), constructed by Tippet (2026). We first
discusssomekeyfeaturesoftherichlistdatabeforemovingontothemethodsusedinthereport.
7.1.1 TheTaxUnit
OneproblemwithSTRL,andrichlistsingeneral,isthattheydonotuseaconsistentunitofanalysis. Some
entries refer to single named individuals, others to named couples, multiple named individuals, and many
entriesincludefamilies.
Inthisreport,wedistinguishbetweenentries,families,householdsandindividuals. Entries(orobserva-
tions) refer to the units recorded in the rich list. An entry may represent a single individual, a couple, or a
wider family group. Families refer specifically to entries where the rich list indicates that wealth is shared
acrossabroaderfamilystructure,typicallybyincluding“family”intheentrydescription.Householdsarethe
taxunitusedinthisstudyandrefertogroupsofindividualslivingatthesameaddress. Individualsreferto
distinctpersons. BecausetheRichListisnotconstructedusinghouseholdsastheunitofobservation,akey
stepintheanalysisisconvertingfamily-levelwealthintohousehold-levelwealth.
To restructure this into households, we split each entry in STRL into households using the following
rules. Iftheobservationisasinglenamedindividualoracouple,weassume1household. Ifanobservation
containsmultiplenamedindividualswhoarenotacouple(suchasbrothers,orbusinesspartners),weassume
ahouseholdforeachnamedindividual. Ifanobservationalsoincludesthewordfamily,weassumeanextra
2householdsforeachfamily,giventhatfamiliestendtohave2childenandthatintheUKthereareroughly
1.46householdsperfamily(29millionhouseholdsand19.9millionfamiliesaccordingtotheONS).
Forexample,therichestobservationinthe2026STRLwas“SanjayandDheerajHindujaandfamily”with
£38bninwealth. Wesplitthiswealthequallybetween4differenthouseholds: oneforeachbrother(Sanjay
andDheeraj)andtwomorefortheadditionalfamily. Ontheotherhand,“SirChristopherNolanandDame
Emma Thomas” with £370m are just assigned to one household, as they are a couple and the wealth is not
denotedassharedacrossawiderfamily.
7.1.2 Residents
AnotherproblemwiththeSTRListhatitdoesnothaveacleardefinitionofwhoisincludedinthelist. The
magazine states that it includes people who are not British citizens so long as they either live and work in
Britain,aremarriedtoBritons,havestronglinkswithBritainorBritishassetsorhavebackedBritishpolitical
parties, institutionsorcharities. Britishcitizensabroadarealsoincluded. Theyremovepeoplewhoarenot
Britishcitizensandhavemovedaway.
Toprovidesomeclarityontherichlist,wederiveanimputedvariableforwhetherafamilyontherichlist
islikelytobeataxresidentintheUK.ThefirststeptakestheanalysisfromAdvaniandTarrant(2022)who
linkindividualsontherichlistin2020toCompaniesHousedata. Wetakethisinformation,kindlyprovided
bytheauthors, toidentifytheresidencystatusofthe1000observationsofthosewhoareontherichlistin
2020. Toconstructanindicatorfortheremainingobservations,thepaperusesindividualbiographiesinthe
STRL alongside other sources to estimate tax residency (such as Forbes, Wikipedia and media articles). We
takeaconservativeapproachfortheseremainingobservations,assumingthatanindividualisataxresident
ofanothercountryif: (i)theyareaforeignnational; (ii)thereisinformationthattheyliveforasignificant
amount of time in a foreign country; (iii) the Forbes global rich list identifies their residency as not in the
UK. While this classification will over-estimate the number of non-UK tax residents on the list, given the
international mobility of the super-rich, it is better to be cautious when assuming that the super-rich with
14

connectionstotheUKmayalsohavetaxresidencystatushere. Allestimatesareconductedontheresident
data.Table8providesanoverviewoftherawdata.WedroptheMonarchgivenmeasurementproblemswith
identifyingtheirwealth.
7.1.3 Imputationofmissingwealthvariables
Somefamiliesdropoffthelistin2021and2022duetothechangeinthesizeofthemagazine. In2020there
were1000familiesontherichlist.Thisdropsto250for2021and2022beforegoingbackupto350in2023.We
linearlyimputeanyonewhodropsoffduringthisperiodbutwhoreappearsin2023orafter.Thisisimportant
fordeterminingthegrowthratesofwealthacrosswealthbins,althoughitwillnotimpactthelevelofwealth
in2026ortheParetoextrapolation.Table9providesanoverviewoftheresidentdatawiththeimputation.
7.2 Method
7.2.1 ParetoExtrapolation:theory
In2026,therichlistonlyincludestherichest350individualsorfamilies,287ofwhicharetaxresidentsofthe
UK.Theminimumwealthontherichlist(bothfortherawandresidentdata)was£340m.Inordertosimulate
therevenueofawealthtaxonwealthabove£100m,weneedtoimputethewealthdistributionbelow£340m.
Understandingthispartofthedistributionisparticularlyhardtopindownasitisnotcoveredbyeitherrich
listdataorsurveydata,suchastheWealthandAssetsSurvey.
Toprovideanestimateofthispartofthedistribution,wefitaParetodistributiontotheobservedrichlist,
whichweextrapolatefurtherdownthedistribution.13 ThekeyassumptionisthattheParetoshapecontinues
belowthethreshold. Thesetupisasfollows. LetN(w)denotethenumberoffamilieswithwealthgreater
thanorequaltow.UndertheParetoassumption,
N(w)=Aw−α (1)
whereα>0istheParetocoefficientandAisascaleparameter.
SupposethattheRichListobservesN familieswithwealthaboveathresholdw .Then
wmin min
N =Aw−α (2)
wmin min
Rearranginggives
A=N wα (3)
wmin min
SubstitutingintoEquation(1)yields
(cid:16)w (cid:17)α
N(w)=N min . (4)
wmin w
Thisequationallowsthenumberoffamiliesaboveanywealththresholdw < w tobeestimatedfrom
min
theobservedRichListthreshold.
TheParetocoefficientisestimatedfromtheobservedwealthdistributionusingtherank-sizerelationship.
Takinglogsofequation4gives:
log(N(w))=log(N )+log(w )−αlog(w) (5)
wmin min
Whichcanbeestimatedas:
13WedonotlinksurveydataonrichlistdataandinterpolatethemissingobservationsfollowingthemethodbyVermeulen(2018)as
theUKWealthandAssetsSurveydatadoesnotcoverthisperiodandhasbeencriticisedforitslargenon-responseandlackofcoverage
ofbusinessassetsatthetop.
15

Table2:Householdsandwealthaboveselectedwealththresholdsin2026.
Threshold(£m) Households Totalwealth(£bn)
50 1710 695.9
100 946 642.5
250 444 566.2
1000 129 417.5
log(R )=C−αlog(W )+ε (6)
i i i
whereR denotestherankoffamilyiandW denoteswealth. TherankofR issimplythenumberof
i i i
families above that given wealth level N(W ). The estimated coefficient αˆ is then used to extrapolate the
i
uppertailbelowtheRichListthreshold.
However,asiswellknownintheliterature,thisequationhasabiasthatcanbecorrectedbysubtracting
0.5fromtherank(Gabaixetal.,2011).Sothefinalequationtobeestimatedis
log(R −0.5)=C−αlog(W )+ε (7)
i i i
7.2.2 ParetoExtrapolation:applicationto2026data
WeperformtheParetoextrapolationontheresidentrichlistentrydatafor2026,i.e. beforewesplitentries
intohouseholds. Thereasonforthisisthefollowing. Supposewehavefamilywith£100mthatissplitinto
fourhouseholdsof£20m. Thehouseholddatasetwillcontainsomehouseholdswith£20m,butthesedonot
representallhouseholdsthatcouldhave£20minthepopulation-onlythosethatcomefromsplittingthedata.
Ifwesplitentriesintohouseholdsfirst,wecannotestimatetheactualnumberoffamilieswithwealthgreater
thanagivenwealthlevel-whichisnecessaryfortheParetoadjustment.
We estimate the Pareto coefficient α using only the entries below the top 50. As there are 287 resident
entriesinthe2026richlist,theestimationisonthedatasetbetweenranks50and287. Thereasonweignore
the top 50 entries is that the Pareto distribution does not hold for the very richest observations, as can be
seeninFigure4. TheestimatedParetocoefficientis0.91. Usingequation4weestimatethatthereare1638
observationswithmorethan£50mand873observationswithmorethan£100m.14
Fromthiswegenerateasyntheticobservationsabove£50mbutbeforetheobserveddataset.Eventhough
the wealth tax only covers households above £100m, we create synthetic observations down to £50m given
thatweneedtosimulatewealthbelowthethresholdovertime,aswealthgrowthwillcausesomefamilieto
enterthetaxbase.
Lastly, we convert this dataset into households. We do this using the method set-out above. For the
simulated households, we assume that the same structure of the observed data for 2026 is applied to the
synthetic data: 49% are kept as 1 household, 9% as 2 households, 35% as 3 households, 5% as 4 households,
1%as5households,andlessthan0.3%as6households.Fromthiswefind946householdswithwealthabove
£100m and 1710 with wealth above £50m as can be seen in Table 2. This estimate is slightly lower but in
thesameordersofmagnitudewithalternativesources. HMRCfindthat2500individualshavewealthabove
£100mand5000withwealthabove£50m.Giventhatthereare2.3peopleperhouseholdintheUK,thisworks
outatjustover1086and2171householdsrespectively(Davies,2025,p.14).
14In2026,ifwmin =£340mandthatthenumberoffamilieswhosewealthatorabovethisthresholdisNwmin =288,withaPareto
coefficientof0.91,thentheimpliednumberoffamilieswithwealthabove£100millionis
(cid:18)340(cid:19)0.9069
N(100)=288 =873 (8)
100
16

Figure4:ParetoFit:UK2026RichListResidentEntries
Note: We fit the Pareto to UK rich list resident entries for 2026 between ranks 50 and 287. We do not use the top 50
observations,astherelationshipbetweenlogrankandlogwealthisnotlinearforthetoppartofthedistribution. The
estimatedParetocoefficientis0.91.
ApracticalissuewhenworkingwithSTRListhatwealthisoftenreportedinroundedamounts,meaning
that many families have identical recorded wealth. To avoid imposing an arbitrary ordering on these tied
observations, ranks are calculated using average ranks. For example, if three families occupy positions 3,
4 and 5 with identical wealth, each is assigned a rank of 4. If multiple families share the threshold wealth,
allareincludedintheextrapolation. ThisensuresthatboththeestimationoftheParetocoefficientandthe
extrapolationitselfarerobusttotheextensiveroundingpresentinthedata.
7.2.3 ParetoExtrapolation:validationwith2015and2020data
Giventheuncertaintieswithextrapolation,weconductavalidationexerciseusingthe2015and2020richlist
data,asthe2015and2020richlistdatacontainsmanymoreobservationsthanthe2026data.
To conduct the validation exercise, we repeat exactly the same set up the 2026 estimation, estimating
theParetocoefficientonjustranks50-287,toseehowwellourParetoextrapolationcomparestotheactual
2015 and 2020 data for ranks before 287. Figure 5 shows that the Pareto extrapolation perfectly matches
theobservationsbelowrank287. In2020,thereare673observationswithwealthabove£120m15. ThePareto
extrapolationpredictsexactly672.892observations.In2015,thereare518observationswithmorethan£120m
inwealth.Wepredictthatthereare498,whichgivesa4%error.GivenhowcloseourParetofitistotheactual
richlistdata,thishelpstojustifyourassumptionthattheParetodistributionholdsforthedatajustbelowthe
287thrankinthe2026richlist.
7.2.4 Simulationswithoutawealthtax
Wesimulatethetrajectoryofwealthover10yearsfrom2026to2036usingthefollowingsteps.
15Wetake£150masthesecondlastobservedwealthlevelinthe2020richlist. Usingthelastwealthlevel(£120m)meanswecannot
compareexactlytherichlistwiththeextrapolation,astheremaybehouseholdswith£120mwhoarenotintherichlistastheydrop
belowthe1000thrank
17

(a)2020 (b)2015
Figure5:ParetoValidationwith2020and2015data
Note:WefittheParetotoUKrichlistresidententriesfor2015and2020betweenranks50and287.Wedonotusethetop
50observations,astherelationshipbetweenlogrankandlogwealthisnotlinearforthetoppartofthedistribution.The
estimatedParetoextrapolationiscomparedtotheactualdatabelowrank287.
First, weestimateaverageannualgrowthratefortheaggregatewealthofthetop181residentobserva-
tionsonSTRLbetween2016and2026. Weusethetop181observationsastheminimumnumberofresident
observationsoverthisperiodwas181in2021and2022andwewantaconsistentnumberoftime,ascanbe
seeninTable10.Thisgivesanaveragegrowthrateof6.48%peryear.
Second, we take the combination of the observed and the synthetic data for 2026 as the starting point.
Thiscombineddatasethas3263householdsintotal,asitincludeshouseholdsabove£50m. Everyhousehold
is assigned the 6.48% annual growth rate for the next 10 years. We do not assume any other changes such
as people entering or exiting due to relocation or death. Figure 6 shows the aggregate wealth of the top
300residenthouseholdsfrom1989to2026,withthesimulationupto2036. In2026,thetop300households
had £522bn in wealth. By 2036, it would have increased to £800bn under these trends. We use the top 300
householdsasthisisaconsistentnumberofhouseholdswecanusefrom1989to2026givenchangesinthe
richlist,ascanbeseeninfigure11.
ForGDPandpublicsectorgovernmentreceipts(whichwecallgovernmentrevenues), wetakenominal
datafromtheOfficeforBudgetResponsibility(OBR).TheOBRprovidesa5yearpredictionofnominalGDP
andgovernmentrevenuesfrom2026to2030.Toextrapolatethisto2036,weassumetheaveragegrowthrate
overthe2026-2030periodforbothseries,ascanbeseeninFigure8andFigure7.
Throughoutthisexerciseweusenominalwealthlevelsforallgrowthratesandseries. Theperiodfrom
2016-2026 contains periods of high and low inflation. The assumption over the next 10 years is that there
willbeasimiliarperiodofpotentiallyhighinflationaryepisodes,whichgivengeopoliticalshocks(suchasUS
attackonIran)andclimatebreakdown,isreasonable.
7.2.5 Simulationswithawealthtax
Thewealthtaxismodelledasa1.8%annualtaxonthetotalwealthofallhouseholdsthathavemorethane
£100 million in net wealth. Aggregate revenues in each year are obtained by summing liabilities across all
households.
Weassumethatallhouseholdsalreadypay0.2%oftheirwealthinincometaxes.Wethereforeonlyapply
a1.8%additionaltaxtomeetthe2%minimumtax.
Theestimatethatthesuper-richpayaround0.2%oftheirwealthintaxisbasedonevidencefromFrance,
the United States and the Netherlands, as comparable estimates for the United Kingdom are not currently
18

available.ThisestimateislikelytoexceedtheeffectivetaxratesimpliedbytheSundayTimesTaxListbecause
thelatterincludescorporationtaxespaidbycompaniesandmaynotfullycapturetheuseofholdingcompanies
andotherstructuresthatreducepersonalincometaxliabilities. Atpresent,itisnotpossibletoestimatethe
effectivetaxratesoftheUK’ssuper-richusingpubliclyavailabledataalone. Doingsowouldrequirelinking
richlistdatawithadministrativetaxrecords.WewouldthereforewelcomesuchanexerciseintheUK.
Thesimulationassumesthat10%oftherevenuesarelosttotaxavoidance. Giventhenatureofthistax,
itisnotclearhowthesuper-richwouldavoidorevadepayingintheshort-run. However,weassumea10%
reductioneachyearasaconservativeestimate,asdiscussedabove.
7.2.6 Sensitivity:changingnumberofhouseholdsperfamily
Inthebaselineresults,familywealthisdividedacross3households(anadditional2).Toassessthesensitivity
oftheresultstothisassumption,weconsideralternativescenariosinwhichfamilywealthisdividedacross
four and five additional households. These scenarios increase the number of households in the simulated
populationandthereforereducethewealthheldbyeachindividualhousehold.
Table 3 presents the resulting revenue estimates with the baseline behavioural effects. The results are
robusttoalternativeassumptionsregardinghouseholdformation. Inthecasethatfamiliesaresplitbetween
fivehouseholds,thegrossrevenuesgeneratedin2026declinefrom£11.57to£11.10bn. By2036,thedecline
isfrom£19.56inthebaselinecaseto£19.12whenfamilyissplitbetweenfivehouseholds. Thissuggeststhat
themainfindingsarenotdrivenbytheparticularassumptionsusedtoconvertfamilywealthintohousehold
wealth. The reason why splitting family wealth further does not have much of an impact on revenues is
because total wealth is taxed, and therefore splitting say a billionaire into extra multi-millionaires does not
impactthetaxrevenues.
7.2.7 Sensitivity:modelingfragmentation
Akeyuncertaintyinmodellingthebehaviouralresponsetoawealthtaxistheextenttowhichhouseholds
may fragment wealth across family members in order to reduce their tax liability. The existing empirical
literatureprovideslittleevidenceonhowhouseholdswithwealthabove£100millionrespondtoawealthtax,
aspreviouswealthtaxesgenerallyappliedatmuchlowerthresholdsandoftencontainedextensiveexemptions
forthesuper-rich.
Tounderstandhowfragmentationimpactstaxrevenues,weconsideraseriesofalternativescenariosin
whichallhouseholdsareassumedtosplittheirwealthequallyacrossadditionalhouseholds.
Table3:Annualrevenuesfromthe2%minimumaveragetaxunderalternativeassumptionsforsplittingfamily
wealthintoseparatehouseholds(£bn).
| Year Baseline:family+2 |       | Family+3 | Family+4 |
| ---------------------- | ----- | -------- | -------- |
| 2026                   | 11.57 | 11.36    | 11.20    |
| 2027                   | 12.19 | 11.97    | 11.81    |
| 2028                   | 12.86 | 12.63    | 12.47    |
| 2029                   | 13.54 | 13.31    | 13.15    |
| 2030                   | 14.26 | 14.05    | 13.88    |
| 2031                   | 15.04 | 14.79    | 14.62    |
| 2032                   | 15.87 | 15.60    | 15.40    |
| 2033                   | 16.74 | 16.50    | 16.26    |
| 2034                   | 17.64 | 17.40    | 17.16    |
| 2035                   | 18.58 | 18.34    | 18.08    |
| 2036                   | 19.56 | 19.33    | 19.12    |
19

Table4: Annualrevenuesfromthe2%minimumaveragetaxunderalternativehousehold-fragmentationas-
sumptions(£bn).
|     | Year | Baseline |       | 3households | 5households |     |
| --- | ---- | -------- | ----- | ----------- | ----------- | --- |
|     | 2026 |          | 11.57 | 9.84        | 9.03        |     |
|     | 2027 |          | 12.19 | 10.41       | 9.51        |     |
|     | 2028 |          | 12.86 | 10.99       | 9.97        |     |
|     | 2029 |          | 13.54 | 11.67       | 10.59       |     |
|     | 2030 |          | 14.26 | 12.36       | 11.22       |     |
|     | 2031 |          | 15.04 | 13.08       | 11.90       |     |
|     | 2032 |          | 15.87 | 13.77       | 12.60       |     |
|     | 2033 |          | 16.74 | 14.49       | 13.31       |     |
|     | 2034 |          | 17.64 | 15.29       | 14.09       |     |
|     | 2035 |          | 18.58 | 16.17       | 15.02       |     |
|     | 2036 |          | 19.56 | 17.08       | 15.84       |     |
Table5:Sensitivityofrevenuesfromthe2%minimumaveragetaxtothehouseholdwealththreshold.
| Threshold | Households |      | Eligiblewealth(£bn) |        | Additionalrevenue(£bn) |       |
| --------- | ---------- | ---- | ------------------- | ------ | ---------------------- | ----- |
| £50m      |            | 1710 |                     | 695.88 |                        | 12.53 |
| £100m     |            | 946  |                     | 642.54 |                        | 11.57 |
| £250m     |            | 444  |                     | 566.15 |                        | 10.19 |
Table 4 presents the resulting revenues when every household is divided into 3 and 5 households. The
upperendofthesescenariosaredeliberatelyextreme. Theyassumethatallhouseholdsarebothwillingand
able to find 4 additional households to give away the vast majority of their wealth to, regardless of family
structure, control considerations, inheritance plans or legal constraints. However we include them to see
whatextremelevelsoffragmentationdoestorevenues.
Incolumn2weshowthecasewhereeachhouseholdsissplitintothree.Thegrossrevenuesin2026decline
from£11.57to£9.84.Whenhouseholdsaresplitinto5,thisreducesto£9.03.
Theresultssuggestthatfragmentationonlypartiallyerodesrevenuesandisnotlikelytoreducerevenues.
Moreover, in practice, it seems unlikely that all wealthy households would be willing to divide their assets
across large numbers of separate households simply to avoid a 2 % annual tax. Fragmentation involves a
genuine transfer of ownership and control rather than a purely paper transaction. While some degree of
fragmentationwilloccur,revenuesarestillmaintained.
7.2.8 Sensitivity:changingthresholds
Table5showshowthenumberofaffectedhouseholdsandtherevenuesraisedvarywiththewealthtaxthresh-
old. Asexpected,loweringthethresholdincreasesboththenumberofhouseholdsliableforthetaxandthe
revenues generated, while raising the threshold has the opposite effect. A threshold of £100 million strikes
a balance between revenue generation and administrative feasibility. At this level, the tax applies to fewer
than1,000householdswhilestillraisingapproximately£10billionperyear.Usingthelowerthresholdof£50
would only raise revenues to £12.53 billion but would over double the number of households to be admin-
istered. Higherthresholdsof£250mwouldfurthersimplifyadministrationbutreducerevenuesto£10.19bn.
The results therefore suggest that a £100 million threshold captures a large share of extreme wealth while
remainingfocusedonaverysmallgroupofhouseholds.
20

Table 6: Annual additional revenues from a 2% minimum average tax under alternative assumptions about
existingtaxespaidbyhouseholdswithwealthabove£100million(£bn).
Year Existingtax:0.1% Existingtax:0.2% Existingtax:0.3% Existingtax:0.5%
| 2026 | 12.21 | 11.57 | 10.92 | 9.64  |
| ---- | ----- | ----- | ----- | ----- |
| 2027 | 12.86 | 12.19 | 11.53 | 10.19 |
| 2028 | 13.55 | 12.86 | 12.17 | 10.78 |
| 2029 | 14.25 | 13.54 | 12.82 | 11.38 |
| 2030 | 15.00 | 14.26 | 13.52 | 12.03 |
| 2031 | 15.80 | 15.04 | 14.27 | 12.72 |
| 2032 | 16.65 | 15.87 | 15.08 | 13.46 |
| 2033 | 17.55 | 16.74 | 15.92 | 14.24 |
| 2034 | 18.48 | 17.64 | 16.79 | 15.05 |
| 2035 | 19.45 | 18.58 | 17.71 | 15.90 |
| 2036 | 20.45 | 19.56 | 18.66 | 16.78 |
7.2.9 Sensitivity:changing0.2%existingaveragetaxrate
In our baseline assumption we assume that centi-millionaires and billionaires pay 0.2% of their wealth in
existingincometaxes. Howdoesthischangewhenweadjustthisassumption? Table6presentstheresults.
Lookingatjustthe2026revenuesestimations,thegrossrevenuesincreaseto£12.21bnwhentheexistingtax
ratedeclinesto0.1%.Inthecasethatweassumethatbillionairespay0.3%oftheirwealthincurrenttaxes,the
revenuesdeclinesto£10.92. Giventhattheinternationalevidencesuggeststherangeisfrom0.1to0.3, the
revenuesremainrobusttotherangeoftheseassumptions.
7.3 AdditionalTablesandFigures
21

Figure6:Aggregatewealthoftop300residenthouseholds(£bncurrent)
Note: Aggregatewealthoftop300residenthouseholdsintheUKwithandwithouta2%wealthtaxonallhouseholdnet
wealthabove£100m.Tomodelbehaviouralresponses,weassumethat7%ofwealthislostinthefirstyearandaremaining
7%islostoverthenext10years. AdvaniandTarrant,2020arguesthatfortheUKa2%wealthtaxwouldreducewealth
by14%inthelongrun.Anexittaxisimposedtostopinternationalmigration.
22

Figure7:NominalGDP(£bncurrent)
DataisfromtheOfficeforBudgetResponsibility(OBR).OBRprovidesforecastfor2026-2030. Weextrapolatethis
Note:
forecastfor2031-2036usingthegrowthratesfromthe2026-2030forecastperiod.
7.3.1 Sensitivity:2%marginalwealthtaxabove£100million
Lastly,weestimatetherevenuesthatwouldbegeneratedfroma2%annualtaxonhouseholdnetwealthabove
£100million. Inthisscenarioallwealthupto£100mwouldbeexempt,andallhouseholdwealthabovethis
wouldbetaxedat2%.
AscanbeseeninTable7a2%wealthtaxonhouseholdswithwealthabove£100millionwouldraise£9.86
billionin2026afterthe10%reductionforbehaviouralresponses. AsshowninTable1, thisisequivalentto
0.32% of GDP and 0.76% of total public sector receipts. This is only a £1bn less that the baseline minimum
wealthtaxproposal.Thereasonforthedifferenceisduetotheexemptfirst£100mforallhouseholds.
Table7: Projectedrevenuesfroma2%marginalwealthtaxonwealthabove£100million,assumingrealised
revenuesare10%lowerduetobehaviouralresponses.
Year Grossrevenue(£bn) Revenue10%reduction(£bn) Revenue(%GDP) Revenue(%govrev)
| 2026 | 10.96 | 9.86  | 0.31 | 0.76 |
| ---- | ----- | ----- | ---- | ---- |
| 2027 | 11.56 | 10.41 | 0.32 | 0.76 |
| 2028 | 12.20 | 10.98 | 0.32 | 0.77 |
| 2029 | 12.87 | 11.58 | 0.33 | 0.78 |
| 2030 | 13.58 | 12.22 | 0.34 | 0.79 |
| 2031 | 14.32 | 12.89 | 0.34 | 0.80 |
| 2032 | 15.11 | 13.60 | 0.35 | 0.80 |
| 2033 | 15.95 | 14.35 | 0.36 | 0.81 |
| 2034 | 16.82 | 15.14 | 0.36 | 0.82 |
| 2035 | 17.75 | 15.98 | 0.37 | 0.83 |
| 2036 | 18.73 | 16.85 | 0.38 | 0.84 |
23

Figure8:NominalGovernmentRevenues(£bncurrent)
Note:Dataonpublicsectorcurrentreceipts,whichwecallgovernmentrevenues,isfromtheOfficeforBudgetResponsi-
bility(OBR).OBRprovidesforecastfor2026-2030.Weextrapolatethisforecastfor2031-2036usingthegrowthratesfrom
the2026-2030forecastperiod.
24

Table8:SummarystatisticsfortherawSundayTimesRichListdataset.
| year observations | totalwealth | minimumwealth | billionaires |
| ----------------- | ----------- | ------------- | ------------ |
| 1989 199          | 36898       | 30            | 10           |
| 1990 199          | 41741       | 50            | 10           |
| 1991 199          | 39958       | 50            | 9            |
| 1992 299          | 43750       | 23            | 7            |
| 1993 399          | 49112       | 20            | 8            |
| 1994 499          | 61557       | 20            | 8            |
| 1995 499          | 54574       | 25            | 4            |
| 1996 499          | 70152       | 35            | 10           |
| 1997 987          | 98408       | 15            | 16           |
| 1998 999          | 108275      | 20            | 16           |
| 1999 999          | 114579      | 21            | 17           |
| 2000 999          | 145689      | 30            | 26           |
| 2001 999          | 157469      | 35            | 22           |
| 2002 999          | 159429      | 35            | 21           |
| 2003 999          | 155575      | 30            | 21           |
| 2004 999          | 202172      | 40            | 30           |
| 2005 999          | 249518      | 50            | 40           |
| 2006 999          | 300647      | 60            | 54           |
| 2007 999          | 359711      | 70            | 68           |
| 2008 999          | 412461      | 70            | 74           |
| 2009 999          | 257998      | 55            | 43           |
| 2010 999          | 335381      | 63            | 53           |
| 2011 999          | 395476      | 70            | 73           |
| 2012 999          | 413990      | 70            | 77           |
| 2013 999          | 449133      | 75            | 88           |
| 2014 999          | 522519      | 85            | 105          |
| 2015 999          | 546788      | 100           | 117          |
| 2016 999          | 575760      | 103           | 120          |
| 2017 999          | 657770      | 110           | 134          |
| 2018 999          | 723154      | 115           | 145          |
| 2019 999          | 775685      | 100           | 150          |
| 2020 999          | 742263      | 120           | 147          |
| 2021 250          | 658089      | 613           | 171          |
| 2022 250          | 710723      | 650           | 177          |
| 2023 349          | 795869      | 350           | 171          |
| 2024 349          | 794823      | 350           | 165          |
| 2025 349          | 772207      | 350           | 156          |
| 2026 349          | 783357      | 340           | 157          |
25

Table9:SummarystatisticsfortheresidentSundayTimesRichListdataset.
| year observations | totalwealth | minimumwealth | billionaires |     |
| ----------------- | ----------- | ------------- | ------------ | --- |
| 1989              | 181         | 32483         | 30           | 8   |
| 1990              | 173         | 34839         | 50           | 7   |
| 1991              | 171         | 32527         | 50           | 7   |
| 1992              | 257         | 36451         | 23           | 6   |
| 1993              | 341         | 41836         | 20           | 7   |
| 1994              | 447         | 52917         | 20           | 7   |
| 1995              | 444         | 48155         | 25           | 4   |
| 1996              | 436         | 58741         | 35           | 9   |
| 1997              | 618         | 72800         | 15           | 13  |
| 1998              | 680         | 81706         | 20           | 13  |
| 1999              | 682         | 83225         | 21           | 12  |
| 2000              | 697         | 109777        | 30           | 18  |
| 2001              | 721         | 118847        | 35           | 16  |
| 2002              | 724         | 121903        | 35           | 15  |
| 2003              | 747         | 116689        | 30           | 14  |
| 2004              | 751         | 139862        | 40           | 18  |
| 2005              | 757         | 171705        | 50           | 23  |
| 2006              | 757         | 210110        | 60           | 34  |
| 2007              | 752         | 252839        | 70           | 45  |
| 2008              | 756         | 277067        | 70           | 43  |
| 2009              | 785         | 179483        | 55           | 24  |
| 2010              | 814         | 230854        | 63           | 27  |
| 2011              | 811         | 265922        | 70           | 43  |
| 2012              | 796         | 277913        | 70           | 44  |
| 2013              | 813         | 304260        | 75           | 53  |
| 2014              | 804         | 356574        | 85           | 66  |
| 2015              | 803         | 385165        | 100          | 78  |
| 2016              | 810         | 403098        | 103          | 77  |
| 2017              | 815         | 457809        | 110          | 84  |
| 2018              | 821         | 505036        | 115          | 90  |
| 2019              | 824         | 546059        | 100          | 97  |
| 2020              | 833         | 529414        | 120          | 99  |
| 2021              | 308         | 482177        | 175          | 113 |
| 2022              | 310         | 553046        | 225          | 121 |
| 2023              | 325         | 597051        | 260          | 123 |
| 2024              | 316         | 609035        | 290          | 121 |
| 2025              | 301         | 592011        | 320          | 116 |
| 2026              | 287         | 582273        | 340          | 115 |
26

Table10: SummarystatisticsforUK-residentdynastiesintheSundayTimesRichListusingobservedwealth
only.
| Year Observations | Totalwealth(£m) | Minimumwealth(£m) | Billionaires |     |
| ----------------- | --------------- | ----------------- | ------------ | --- |
| 1989              | 181             | 32483             | 30           | 8   |
| 1990              | 173             | 34839             | 50           | 7   |
| 1991              | 172             | 32602             | 50           | 7   |
| 1992              | 260             | 36906             | 23           | 6   |
| 1993              | 344             | 42202             | 20           | 7   |
| 1994              | 449             | 53077             | 20           | 7   |
| 1995              | 446             | 48278             | 25           | 4   |
| 1996              | 439             | 58932             | 35           | 9   |
| 1997              | 622             | 73214             | 15           | 13  |
| 1998              | 684             | 82176             | 20           | 13  |
| 1999              | 686             | 83684             | 21           | 12  |
| 2000              | 703             | 110484            | 30           | 18  |
| 2001              | 726             | 119510            | 35           | 16  |
| 2002              | 731             | 122782            | 35           | 15  |
| 2003              | 752             | 117472            | 30           | 14  |
| 2004              | 757             | 141097            | 40           | 18  |
| 2005              | 761             | 172873            | 50           | 23  |
| 2006              | 760             | 211560            | 60           | 34  |
| 2007              | 756             | 254613            | 70           | 45  |
| 2008              | 759             | 278736            | 70           | 43  |
| 2009              | 788             | 180708            | 55           | 24  |
| 2010              | 817             | 232395            | 63           | 27  |
| 2011              | 814             | 267732            | 70           | 43  |
| 2012              | 800             | 280353            | 70           | 45  |
| 2013              | 817             | 306780            | 75           | 54  |
| 2014              | 808             | 359767            | 85           | 68  |
| 2015              | 807             | 388648            | 100          | 80  |
| 2016              | 814             | 406638            | 103          | 79  |
| 2017              | 818             | 461559            | 110          | 86  |
| 2018              | 824             | 509063            | 115          | 92  |
| 2019              | 827             | 550431            | 100          | 99  |
| 2020              | 836             | 535170            | 120          | 101 |
| 2021              | 181             | 437924            | 613          | 115 |
| 2022              | 181             | 501398            | 650          | 121 |
| 2023              | 280             | 584621            | 350          | 124 |
| 2024              | 284             | 601303            | 353          | 121 |
| 2025              | 285             | 591073            | 350          | 117 |
| 2026              | 288             | 587018            | 340          | 116 |
27

Table11:SummarystatisticsfortheresidenthouseholdSundayTimesRichListdataset.
| year observations | totalwealth |        | minimumwealth | billionaires |     |
| ----------------- | ----------- | ------ | ------------- | ------------ | --- |
| 1989              | 321         | 32483  |               | 10           | 4   |
| 1990              | 325         | 34839  |               | 12           | 4   |
| 1991              | 329         | 32527  |               | 12           | 2   |
| 1992              | 463         | 36451  |               | 8            | 4   |
| 1993              | 619         | 41836  |               | 7            | 7   |
| 1994              | 809         | 52917  |               | 7            | 4   |
| 1995              | 824         | 48155  |               | 8            | 3   |
| 1996              | 839         | 58741  |               | 9            | 5   |
| 1997              | 1115        | 72770  |               | 5            | 5   |
| 1998              | 1291        | 81706  |               | 5            | 7   |
| 1999              | 1296        | 83225  |               | 6            | 7   |
| 2000              | 1321        | 109777 |               | 8            | 6   |
| 2001              | 1359        | 118847 |               | 9            | 8   |
| 2002              | 1408        | 121903 |               | 10           | 10  |
| 2003              | 1471        | 116689 |               | 6            | 6   |
| 2004              | 1498        | 139862 |               | 7            | 11  |
| 2005              | 1472        | 171705 |               | 8            | 15  |
| 2006              | 1483        | 210110 |               | 15           | 18  |
| 2007              | 1455        | 252839 |               | 19           | 33  |
| 2008              | 1449        | 277067 |               | 21           | 34  |
| 2009              | 1497        | 178749 |               | 18           | 13  |
| 2010              | 1565        | 230120 |               | 11           | 14  |
| 2011              | 1549        | 265188 |               | 18           | 36  |
| 2012              | 1526        | 277173 |               | 18           | 35  |
| 2013              | 1552        | 303520 |               | 19           | 46  |
| 2014              | 1540        | 355834 |               | 21           | 70  |
| 2015              | 1559        | 384425 |               | 25           | 84  |
| 2016              | 1589        | 402358 |               | 26           | 81  |
| 2017              | 1604        | 457069 |               | 22           | 96  |
| 2018              | 1611        | 504296 |               | 27           | 110 |
| 2019              | 1625        | 545329 |               | 26           | 121 |
| 2020              | 1656        | 528684 |               | 26           | 118 |
| 2021              | 644         | 481447 |               | 40           | 124 |
| 2022              | 637         | 552316 |               | 48           | 133 |
| 2023              | 669         | 596321 |               | 55           | 143 |
| 2024              | 639         | 608305 |               | 62           | 140 |
| 2025              | 605         | 591281 |               | 70           | 133 |
| 2026              | 578         | 582273 |               | 77           | 129 |
28

Table12:Sectoralcomposition(percentofobservations)ofthe2020and2026SundayTimesRichLists.
| Sector                       | Top350(2020) | Bottom650(2020) | Top350(2026) |
| ---------------------------- | ------------ | --------------- | ------------ |
| Realestate                   | 20.6         | 19.3            | 20.1         |
| Finance/investments          | 19.1         | 15.6            | 17.8         |
| Retail/restaurant/consumer   | 18.9         | 21.3            | 19.2         |
| Technology                   | 12.0         | 10.3            | 10.9         |
| Media                        | 7.4          | 10.6            | 11.2         |
| Diversified/other            | 5.4          | 10.2            | 5.7          |
| Energy                       | 5.4          | 4.0             | 4.0          |
| Shipping/transport/logistics | 5.1          | 4.3             | 5.4          |
| Industry/Manufacturing       | 3.1          | 1.1             | 2.0          |
| Land                         | 2.6          | 2.3             | 2.3          |
|                              | 0.3          | 1.1             | 1.4          |
29

References
Advani,Arun,EmmaChamberlain,andAndySummers(2020).“FinalReport:AWealthTaxfortheUK”.In:
WealthTaxCommissionEvidencePaper,p.126.
Advani, Arun, Helen Hughson, and Andy Summers (Sept. 1, 2023). “How much tax do the rich really pay?
EvidencefromtheUK”.In:OxfordReviewofEconomicPolicy39.3,pp.406–437.issn:0266-903X.doi:
10.
.url: (visitedon06/10/2026).
1093/oxrep/grad032 https://doi.org/10.1093/oxrep/grad032
Advani, Arun and Hannah Tarrant (Oct. 27, 2020). “Behavioural responses to a wealth tax”. In: Wealth Tax
Commission Evidence Paper. doi: 10.47445/105 . url: https://www.wealthandpolicy.com/wp/
(visitedon08/24/2021).
105.html
— (2022).OfficialstatisticsunderestimatewealthinequalityinBritain.LSEBritishPoliticsandPolicy.
Bach,Laurentetal.(Sept.2025).“DoBillionairesPayTaxes?”In:AMSEWorkingPapers.Number:2532.url:
(visitedon06/16/2026).
https://ideas.repec.org//p/aim/wpaimx/2532.html
Balata, Fernanda and Hollie Wright (Jan. 30, 2026). Taxing Invisible Wealth: Fixing an Outdated Tax System
intheAgeofExtremeWealth.NewEconomicsFoundation.url:
https://new-economicsf.files.
(visitedon
svdcdn.com/production/files/Taxing-invisible-wealth briefing NEF v2.pdf
07/14/2026).
Balkir,AkcanS.etal.(Aug.2025).HowMuchTaxDoUSBillionairesPay?EvidencefromAdministrativeData.
doi: .url: (visitedon06/16/2026).
10.3386/w34170 https://www.nber.org/papers/w34170
Barroso,Rau´l,DonaldN’Gatta,andGaizkaOrmazabal(Sept.1,2023).“IndividualWealthTaxesandCorporate
Payouts”.In:TheAccountingReview 98.5,pp.31–60.issn:0001-4826.doi:
10.2308/TAR-2021-0475
.
url: (visitedon06/15/2026).
https://doi.org/10.2308/TAR-2021-0475
Bell,Alexetal.(May1,2019).“WhoBecomesanInventorinAmerica?TheImportanceofExposuretoInno-
vation”.In:TheQuarterlyJournalofEconomics 134.2,pp.647–713.issn:0033-5533.doi:
10.1093/qje/
.url: (visitedon06/16/2026).
qjy028 https://doi.org/10.1093/qje/qjy028
Bjørneby,Marie,SimenMarkussen,andKnutRøed(2023).“Animperfectwealthtaxandemploymentinclosely
heldfirms”.In:Economica90.358. eprint:https://onlinelibrary.wiley.com/doi/pdf/10.1111/ecca.12456,pp.557–
583.issn:1468-0335.doi: .url:
10.1111/ecca.12456 https://onlinelibrary.wiley.com/doi/
(visitedon06/15/2026).
abs/10.1111/ecca.12456
Botta,Albertoetal.(Mar.1,2021).“Inequalityandfinanceinarenteconomy”.In:JournalofEconomicBehavior
&Organization183,pp.998–1029.issn:0167-2681.doi:
10.1016/j.jebo.2019.02.013
.url:
https:
(visitedon06/15/2026).
//www.sciencedirect.com/science/article/pii/S0167268119300447
Bruil,Arjanetal.(2025).“InequalityandRedistributionintheNetherlands”.In:CPBDiscussionPaper.Number:
436.url: (visitedon06/16/2026).
https://ideas.repec.org//p/cpb/discus/436.html
Bru¨lhart,Mariusetal.(Nov.2022).“BehavioralResponsestoWealthTaxes:EvidencefromSwitzerland”.In:
American Economic Journal: Economic Policy 14.4, pp. 111–150. issn: 1945-7731. doi: 10.1257/pol.
.url: (visitedon
20200258 https://www.aeaweb.org/articles?id=10.1257/pol.20200258
06/15/2026).
Chamberlain,Emma(Oct.27,2020).“Definingthetaxbase:designissues”.In:WealthTaxCommissionEvidence
Paper.doi:
10.47445/108
.url:
https://www.wealthandpolicy.com/wp/108.html
(visitedon
08/24/2021).
Cullen,JulieBerryandRogerH.Gordon(Aug.1,2007).“Taxesandentrepreneurialrisk-taking:Theoryand
evidencefortheU.S.”In:JournalofPublicEconomics91.7,pp.1479–1505.issn:0047-2727.doi:
10.1016/
. url:
j.jpubeco.2006.12.001 https://www.sciencedirect.com/science/article/pii/
(visitedon06/16/2026).
S004727270600168X
30

Davies,Gareth(2025).Collectingtherighttaxfromwealthyindividuals.ReportbytheComptrollerandAuditor
General. UK: National Audit Office. url:
http://nao.org.uk/wp-content/uploads/2025/05/
.
collecting-the-right-tax-from-wealthy-individuals.pdf
Directorate-GeneralforTaxationandCustomsUnion(EuropeanCommission)etal.(2026).Wealthtaxation,
including net wealth, capital and exit taxes. Publications Office of the European Union. isbn: 978-92-68-
38938-6.url: (visitedon06/12/2026).
https://data.europa.eu/doi/10.2778/0817231
Dura´n-Cabre´, Jose´ Mar´ıa, Alejandro Esteller-More´, and Mariona Mas-Montserrat (2019). “Behavioural re-
sponsestothe(re)introductionofwealthtaxes.EvidencefromSpain”.In:WorkingPapers.Number:2019/04.
url: (visitedon06/15/2026).
https://ideas.repec.org//p/ieb/wpaper/doc2019-04.html
Fuest, Clemens et al. (2018). “The Economic Effects of a Wealth Tax in Germany”. In: ifo DICE Report 16.2,
pp.22–26.url: (visited
https://ideas.repec.org//a/ces/ifodic/v16y2018i02p22-26.html
on06/14/2026).
Gabaix,XavierandRustamIbragimov(Jan.1,2011).“Rank 1/2:ASimpleWaytoImprovetheOLSEstimation
ofTailExponents”.In:JournalofBusiness&EconomicStatistics29.1. eprint:https://doi.org/10.1198/jbes.2009.06157,
pp. 24–39. issn: 0735-0015. doi: . url:
10.1198/jbes.2009.06157 https://doi.org/10.1198/
(visitedon03/10/2021).
jbes.2009.06157
Gentry,WilliamM.andR.GlennHubbard(Jan.2005).“”SuccessTaxes,”EntrepreneurialEntry,andInnova-
tion”.In:InnovationPolicyandtheEconomy5,pp.87–108.doi:
10.1086/ipe.5.25056172
.url:
https:
(visitedon06/16/2026).
//www.journals.uchicago.edu/doi/abs/10.1086/ipe.5.25056172
Guvenen,Fatihetal.(Apr.3,2023).“UseItorLoseIt:EfficiencyandRedistributionalEffectsofWealthTaxa-
tion”.In:TheQuarterlyJournalofEconomics138.2,pp.835–894.issn:0033-5533,1531-4650.doi:
10.1093/
.url: (visitedon
qje/qjac047 https://academic.oup.com/qje/article/138/2/835/6979843
06/15/2026).
Hebous,Shafik,AlexanderDKlemm,andGeertenMichielse(2024).HowtoTaxWealth.IMFHowtoNotes001.
IMF,p.39.doi: .url:
https://doi.org/10.5089/9798400266881.061 https://www.imf.org/
en/publications/imf-how-to-notes/issues/2024/03/08/how-to-tax-wealth-544948
(visitedon06/14/2026).
Holtz-Eakin, Douglas, David Joulfaian, and Harvey Rosen (1994). “Sticking It Out: Entrepreneurial Survival
andLiquidityConstraints”.In:JournalofPoliticalEconomy102.1,pp.53–75.doi:
10.1086/261921
.url:
(visitedon
https://EconPapers.repec.org/RePEc:ucp:jpolec:v:102:y:1994:i:1:p:53-75
06/16/2026).
Johnsen,ThoreandTerjeLensberg(2014).“ANoteontheCostofCollectingWealthTaxes”.In:SSRNElectronic
Journal. issn: 1556-5068. doi:
10.2139/ssrn.2512663
. url:
http://www.ssrn.com/abstract=
(visitedon06/14/2026).
2512663
Mirrlees,Jamesetal.(2011).“TheMirrleesReview:ConclusionsandRecommendationsforReform”.In:Fis-
calStudies32.3. eprint:https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1475-5890.2011.00140.x,pp.331–
359.issn:1475-5890.doi: .url:
10.1111/j.1475-5890.2011.00140.x https://onlinelibrary.
(visitedon06/15/2026).
wiley.com/doi/abs/10.1111/j.1475-5890.2011.00140.x
Neidle, Dan (July 22, 2025). UK wealth tax: high risk and anti-growth. Tax Policy Associates. url: https:
(visitedon06/15/2026).
//taxpolicy.org.uk/2025/07/22/uk-wealth-tax-anti-growth/
Onaran,O¨zlem,CemOyvat,andEurydiceFotopoulou(July1,2023).“Canwealthtaxationfundpublicinvest-
mentinacaringandsustainableeconomy?ThecaseoftheUK”.In:CambridgeJournalofEconomics47.4,
pp.703–724.issn:0309-166X.doi: .url:
10.1093/cje/bead026 https://doi.org/10.1093/cje/
(visitedon06/15/2026).
bead026
Perret, Sarah (2020). “Why did other wealth taxes fail? Is this time different?” In: Wealth Tax Commission
EvidencePaper,p.32.
31

Ring, Marius A K (Oct. 1, 2025). “Wealth Taxation and Household Saving: Evidence from Assessment Dis-
continuities in Norway”. In: The Review of Economic Studies 92.5, pp. 3375–3402. issn: 0034-6527. doi:
. url: (visited on
10.1093/restud/rdae100 https://doi.org/10.1093/restud/rdae100
06/14/2026).
Saez,EmmanuelandGabrielZucman(2019).“ProgressiveWealthTaxation”.In:BrookingsPapersonEconomic
Activity 2019.2, pp. 437–533. issn: 1533-4465. doi: 10.1353/eca.2019.0017 . url: https://muse.
(visitedon08/30/2021).
jhu.edu/article/764710
— (Mar.2,2026).AnalysisofSenatorSanders’ProposalforanAnnual5%WealthTaxonBillionaires.Prepared
forSenatorBernieSanders.UniversityofCalifornia,Berkeley.url:
https://www.sanders.senate.
(visitedon07/14/2026).
gov/wp-content/uploads/saez-zucman-sanders2026wealthtax.pdf
Seim,David(Nov.2017).“BehavioralResponsestoWealthTaxes:EvidencefromSweden”.In:AmericanEco-
nomic Journal: Economic Policy 9.4, pp. 395–421. issn: 1945-7731. doi: 10.1257/pol.20150290 . url:
(visitedon06/15/2026).
https://www.aeaweb.org/articles?id=10.1257/pol.20150290
Tippet, Ben (2025a). National Renewal Tax. Greenpeace. url: https://www.greenpeace.org.uk/wp-
.
content/uploads/2024/10/Greenpeace-National-Renewal-Tax-Report.pdf
— (2025b).SpecialReportontheSundayTimesRichList:TheMissingBillions—PatrioticMillionairesUK.Pa-
trioticMillionaires.url:
https://patrioticmillionaires.uk/latest-news/special-report-
(visitedon06/16/2026).
on-the-sunday-times-rich-list-the-missing-billions
— (2026). “Using Rich Lists to Study the Super-Rich and Top Wealth Inequality: Insights from the UK”. In:
WorkingPaper.url:
https://www.bentippet.com/rich-list
(visitedon06/16/2026).
Tippet,Ben,RafaelWildauer,andO¨zlemOnaran(2024).“Thecaseforaprogressiveannualwealthtaxinthe
UKupdated”.In:url: .
https://gala.gre.ac.uk/id/eprint/47322/
Vermeulen,Philip(June2018).“HowFatistheTopTailoftheWealthDistribution?”In:ReviewofIncomeand
Wealth64.2,pp.357–387.issn:00346586.doi:
10.1111/roiw.12279
.url:
http://doi.wiley.com/
(visitedon03/10/2021).
10.1111/roiw.12279
Zucman,Gabriel(2024).Ablueprintforacoordinatedminimumeffectivetaxationstandardforultra-high-net-
worth individuals. Commissioned by the Brazilian G20 presidency. International Tax Observatory. url:
.
https://taxobservatory.world//www-site/uploads/2024/06/report-g20.pdf
32
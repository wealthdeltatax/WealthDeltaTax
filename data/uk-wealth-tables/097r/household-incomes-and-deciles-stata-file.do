
*** EXAMPLE DO-FILE TO CREATE HOUSEHOLD INCOME VARIABLES AND INCOME DECILES FOR 2024 AND MARCH 2025 NMG DATA ***

// This do-file creates variables for household income and household income deciles for the 2024 and March 2025 data in the "BoE NMG household survey data - 2011 - March 2025.xlsx" spreadsheet. It also includes an example on how to append the wave-by-wave data to create a time series of household incomes reported in the data. 

// The household income variable is based on individuals' incomes reported in each household. The code first creates the annual reported income of the main respondent, then the income of the second earner, followed by the income of the remaining household members. These measures are then combined into an annual household income measure.

// The code combines point responses (where respondents have provided a numerical response to the question) with band responses (where respondents have responded with "don't know" or "prefer not to say" to the numerical question). The banded question is then asked as a follow-up question to the numerical question. For the band responses, the mid-point of the band is imputed to obtain a numerical value for the respective band. 


* 2024
clear
set more off

* Import data
import excel "enter file path here", sheet("2024") firstrow

* Create a year and month variable to create a time series of the data
gen year = 2024
gen month = 9 
gen date = ym(year, month)
format date %tm 

* Annual income for 2024
//Create income variables for type 2 income question
tab qincomev2_1_1

//Recode band question for main respondent
recode qincomev2_1_1 (19=-8) (18=-7) // recode don't know to -7 and prefer not to state to -8
recode qincomev2_1_1 .=-10 // recode missing data as -10
la var qincomev2_1_1 "annual individual income for type 2s" // label variable
la define qincomev2_1_1 -7 "don't know" -8 "prefer not to state" -10 "missing" 1 "none"/*
*/ 2 "<£2,500" /*
*/ 3 "£2,500-£4,499" /*
*/ 4 "£4,500-£6,499" 5 "£6,500-£7,499" /*
*/ 6 "£7,500-£9,499" 7 "£9,500-£11,499" /*
*/ 8 "£11,500-£13,499" 9 "£13,500-£15,499" /*
*/ 10 "£15,500-£17,499" 11 "£17,500-£24,999" /*
*/ 12 "£25,000-£34,999" 13 "£35,000-£44,999" /*
*/ 14 "£45,000-£54,999" 15 "£55,000-£74,999" 16 "£75,000-£99,999" 17 ">=£100,000", replace 
la val qincomev2_1_1 qincomev2_1_1
tab qincomev2_1_1

//Create mid-point variable for main respondent (convert banded responses into numerical values corresponding to mid-points of bands)
gen qincomev2_1_1_a=.
replace qincomev2_1_1_a=0 if qincomev2_1_1==1
replace qincomev2_1_1_a=1250 if qincomev2_1_1==2
replace qincomev2_1_1_a=3500 if qincomev2_1_1==3
replace qincomev2_1_1_a=5500 if qincomev2_1_1==4
replace qincomev2_1_1_a=7000 if qincomev2_1_1==5
replace qincomev2_1_1_a=8500 if qincomev2_1_1==6
replace qincomev2_1_1_a=10500 if qincomev2_1_1==7
replace qincomev2_1_1_a=12500 if qincomev2_1_1==8
replace qincomev2_1_1_a=14500 if qincomev2_1_1==9
replace qincomev2_1_1_a=16500 if qincomev2_1_1==10
replace qincomev2_1_1_a=21250 if qincomev2_1_1==11
replace qincomev2_1_1_a=30000 if qincomev2_1_1==12
replace qincomev2_1_1_a=40000 if qincomev2_1_1==13
replace qincomev2_1_1_a=50000 if qincomev2_1_1==14
replace qincomev2_1_1_a=65000 if qincomev2_1_1==15
replace qincomev2_1_1_a=87500 if qincomev2_1_1==16
replace qincomev2_1_1_a=125000 if qincomev2_1_1==17
replace qincomev2_1_1_a=-7 if qincomev2_1_1==-7
replace qincomev2_1_1_a=-8 if qincomev2_1_1==-8
recode qincomev2_1_1_a .=-10

//Label mid-point variable for main respondent 
la var qincomev2_1_1_a "annual individual income for type 2s (mid-points)"
la define qincomev2_1_1_a -7 "don't know" -8 "prefer not to state" -10 "missing"
la val qincomev2_1_1_a qincomev2_1_1_a

//Recode continuous income question for main respondent
rename qincomefreev2_n_1 qincomev2_1_1_c
replace qincomev2_1_1_c=0 if qincomev2_1_1_c<0
replace qincomev2_1_1_c=-7 if qincomefreev2_dk_1==1
replace qincomev2_1_1_c=-8 if qincomefreev2_ps_1==1
label var qincomev2_1_1_c "continuous individual income variable for type 2s"
la define qincomev2_1_1_c -7 "don't know" -8 "refused"
la val qincomev2_1_1_c qincomev2_1_1_c

//Continuous income series using main respondents' income when given and mid-point of income range otherwise (combines continuous responses and mid-points of banded responses)
gen qincomev2_1_1_m=qincomev2_1_1_c
replace qincomev2_1_1_m=0 if qincomev2_1_1==1 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=1250 if qincomev2_1_1==2 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=3500 if qincomev2_1_1==3 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=5500 if qincomev2_1_1==4 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=7000 if qincomev2_1_1==5 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=8500 if qincomev2_1_1==6 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=10500 if qincomev2_1_1==7 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=12500 if qincomev2_1_1==8 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=14500 if qincomev2_1_1==9 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=16500 if qincomev2_1_1==10 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=21250 if qincomev2_1_1==11 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=30000 if qincomev2_1_1==12 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=40000 if qincomev2_1_1==13 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=50000 if qincomev2_1_1==14 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=65000 if qincomev2_1_1==15 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=87500 if qincomev2_1_1==16 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=125000 if qincomev2_1_1==17 & qincomev2_1_1_m<0

label var qincomev2_1_1_m "continuous individual income variable for type 2s, everyone" // label continuous variable for main respondent
la define qincomev2_1_1_m -7 "don't know" -8 "refused"
la val qincomev2_1_1_m qincomev2_1_1_m
sum qincomev2_1_1_m 


//Recode income band question for partner/2nd earner
recode qincomev2_1_2 (19=-8) (18=-7) // recode don't know to -7 and prefer not to state to -8
recode qincomev2_1_2 .=-10 // recode missing data as -10
la var qincomev2_1_2 "annual partner income for type 2s" // label variable
la define qincomev2_1_2 -7 "don't know" -8 "prefer not to state" -10 "not applicable" 1 "none"/*
*/ 2 "<£2,500" /*
*/ 3 "£2,500-£4,499" /*
*/ 4 "£4,500-£6,499" 5 "£6,500-£7,499" /*
*/ 6 "£7,500-£9,499" 7 "£9,500-£11,499" /*
*/ 8 "£11,500-£13,499" 9 "£13,500-£15,499" /*
*/ 10 "£15,500-£17,499" 11 "£17,500-£24,999" /*
*/ 12 "£25,000-£34,999" 13 "£35,000-£44,999" /*
*/ 14 "£45,000-£54,999" 15 "£55,000-£74,999" 16 "£75,000-£99,999" 17 ">=£100,000", replace 
la val qincomev2_1_2 qincomev2_1_2
tab qincomev2_1_2 

//Create mid-point income variable for partner/2nd earner (convert banded responses into numerical values corresponding to mid-points of bands)
gen qincomev2_1_2_a=.
replace qincomev2_1_2_a=0 if qincomev2_1_2==1
replace qincomev2_1_2_a=1250 if qincomev2_1_2==2
replace qincomev2_1_2_a=3500 if qincomev2_1_2==3
replace qincomev2_1_2_a=5500 if qincomev2_1_2==4
replace qincomev2_1_2_a=7000 if qincomev2_1_2==5
replace qincomev2_1_2_a=8500 if qincomev2_1_2==6
replace qincomev2_1_2_a=10500 if qincomev2_1_2==7
replace qincomev2_1_2_a=12500 if qincomev2_1_2==8
replace qincomev2_1_2_a=14500 if qincomev2_1_2==9
replace qincomev2_1_2_a=16500 if qincomev2_1_2==10
replace qincomev2_1_2_a=21250 if qincomev2_1_2==11
replace qincomev2_1_2_a=30000 if qincomev2_1_2==12
replace qincomev2_1_2_a=40000 if qincomev2_1_2==13
replace qincomev2_1_2_a=50000 if qincomev2_1_2==14
replace qincomev2_1_2_a=65000 if qincomev2_1_2==15
replace qincomev2_1_2_a=87500 if qincomev2_1_2==16
replace qincomev2_1_2_a=125000 if qincomev2_1_2==17

replace qincomev2_1_2_a=-7 if qincomev2_1_2==-7
replace qincomev2_1_2_a=-8 if qincomev2_1_2==-8
recode qincomev2_1_2_a .=-10
la var qincomev2_1_2_a "annual partner income for type 2s (mid-points)"
la define qincomev2_1_2_a -7 "don't know" -8 "prefer not to state" -10 "missing"
la val qincomev2_1_2_a qincomev2_1_2_a

//Recode continuous income question for partner/2nd earner
rename qincomefreev2_n_2 qincomev2_1_2_c
replace qincomev2_1_2_c=0 if qincomev2_1_2_c<0
replace qincomev2_1_2_c=-7 if qincomefreev2_dk_2==1
replace qincomev2_1_2_c=-8 if qincomefreev2_ps_2==1
label var qincomev2_1_2_c "continuous partner income variable for type 2s"
la define qincomev2_1_2_c -7 "don't know" -8 "refused"
la val qincomev2_1_2_c qincomev2_1_2_c
sum qincomev2_1_2_c

//Continuous income series using partner/2nd earner income when given and mid-point of income range otherwise (combines continuous responses and mid-points of banded responses)
gen qincomev2_1_2_m=qincomev2_1_2_c
replace qincomev2_1_2_m=0 if qincomev2_1_2==1 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=1250 if qincomev2_1_2==2 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=3500 if qincomev2_1_2==3 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=5500 if qincomev2_1_2==4 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=7000 if qincomev2_1_2==5 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=8500 if qincomev2_1_2==6 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=10500 if qincomev2_1_2==7 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=12500 if qincomev2_1_2==8 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=14500 if qincomev2_1_2==9 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=16500 if qincomev2_1_2==10 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=21250 if qincomev2_1_2==11 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=30000 if qincomev2_1_2==12 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=40000 if qincomev2_1_2==13 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=50000 if qincomev2_1_2==14 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=65000 if qincomev2_1_2==15 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=87500 if qincomev2_1_2==16 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=125000 if qincomev2_1_2==17 & qincomev2_1_2_m<0

label var qincomev2_1_2_m "continuous partner income variable for type 2s, everyone"
la define qincomev2_1_2_m -7 "don't know" -8 "refused"
la val qincomev2_1_2_m qincomev2_1_2_m
sum qincomev2_1_2_m


//Recode income band question for other earners
recode qincomev2_1_3 (19=-8) (18=-7) // recode don't know to -7 and prefer not to state to -8
recode qincomev2_1_3 .=-10 // recode missing data as -10
la var qincomev2_1_3 "annual other income for type 2s" // label variable
la define qincomev2_1_3 -7 "don't know" -8 "prefer not to state" -10 "missing" 1 "none"/*
*/ 2 "<£2,500" /*
*/ 3 "£2,500-£4,499" /*
*/ 4 "£4,500-£6,499" 5 "£6,500-£7,499" /*
*/ 6 "£7,500-£9,499" 7 "£9,500-£11,499" /*
*/ 8 "£11,500-£13,499" 9 "£13,500-£15,499" /*
*/ 10 "£15,500-£17,499" 11 "£17,500-£24,999" /*
*/ 12 "£25,000-£34,999" 13 "£35,000-£44,999" /*
*/ 14 "£45,000-£54,999" 15 "£55,000-£74,999" 16 "£75,000-£99,999" 17 ">=£100,000",replace 
la val qincomev2_1_3 qincomev2_1_3
tab qincomev2_1_3

//Create income mid-point variable for other earners (convert banded responses into numerical values corresponding to mid-points of bands)
gen qincomev2_1_3_a=.
replace qincomev2_1_3_a=0 if qincomev2_1_3==1
replace qincomev2_1_3_a=1250 if qincomev2_1_3==2
replace qincomev2_1_3_a=3500 if qincomev2_1_3==3
replace qincomev2_1_3_a=5500 if qincomev2_1_3==4
replace qincomev2_1_3_a=7000 if qincomev2_1_3==5
replace qincomev2_1_3_a=8500 if qincomev2_1_3==6
replace qincomev2_1_3_a=10500 if qincomev2_1_3==7
replace qincomev2_1_3_a=12500 if qincomev2_1_3==8
replace qincomev2_1_3_a=14500 if qincomev2_1_3==9
replace qincomev2_1_3_a=16500 if qincomev2_1_3==10
replace qincomev2_1_3_a=21250 if qincomev2_1_3==11
replace qincomev2_1_3_a=30000 if qincomev2_1_3==12
replace qincomev2_1_3_a=40000 if qincomev2_1_3==13
replace qincomev2_1_3_a=50000 if qincomev2_1_3==14
replace qincomev2_1_3_a=65000 if qincomev2_1_3==15
replace qincomev2_1_3_a=87500 if qincomev2_1_3==16
replace qincomev2_1_3_a=125000 if qincomev2_1_3==17
replace qincomev2_1_3_a=-7 if qincomev2_1_3==-7
replace qincomev2_1_3_a=-8 if qincomev2_1_3==-8
recode qincomev2_1_3_a .=-10
la var qincomev2_1_3_a "annual other income for type 2s (mid-points)"
la define qincomev2_1_3_a -7 "don't know" -8 "prefer not to state" -10 "missing"
la val qincomev2_1_3_a qincomev2_1_3_a

//Recode continuous income question for other earners
rename qincomefreev2_n_3 qincomev2_1_3_c
replace qincomev2_1_3_c=0 if qincomev2_1_3_c<0
replace qincomev2_1_3_c=-7 if qincomefreev2_dk_3==1
replace qincomev2_1_3_c=-8 if qincomefreev2_ps_3==1
label var qincomev2_1_3_c "continuous other income variable for type 2s"
la define qincomev2_1_3_c -7 "don't know" -8 "refused"
la val qincomev2_1_3_c qincomev2_1_3_c
sum qincomev2_1_3_c
kdensity qincomev2_1_3_c if qincomev2_1_3_c>0

//Continuous income series using other earners when given and mid-point of income range otherwise (combines continuous responses and mid-points of banded responses)
gen qincomev2_1_3_m=qincomev2_1_3_c
replace qincomev2_1_3_m=0 if qincomev2_1_3==1 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=1250 if qincomev2_1_3==2 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=3500 if qincomev2_1_3==3 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=5500 if qincomev2_1_3==4 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=7000 if qincomev2_1_3==5 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=8500 if qincomev2_1_3==6 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=10500 if qincomev2_1_3==7 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=12500 if qincomev2_1_3==8 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=14500 if qincomev2_1_3==9 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=16500 if qincomev2_1_3==10 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=21250 if qincomev2_1_3==11 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=30000 if qincomev2_1_3==12 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=40000 if qincomev2_1_3==13 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=50000 if qincomev2_1_3==14 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=65000 if qincomev2_1_3==15 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=87500 if qincomev2_1_3==16 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=125000 if qincomev2_1_3==17 & qincomev2_1_3_m<0

label var qincomev2_1_3_m "continuous other income variable for type 2s, everyone"
la define qincomev2_1_3_m -7 "don't know" -8 "refused"
la val qincomev2_1_3_m qincomev2_1_3_m

sum qincomev2_1_3_m
kdensity qincomev2_1_3_m if qincomev2_1_3_m>0


//Combine income from different individuals into household income 
gen q2dum=1 if (qincomev2_1_1_m>=0 & qincomev2_1_1_m!=.) & (qincomev2_1_2_m>=0) & (qincomev2_1_3_m>=0) 

egen fihhyr2v2_m=rowtotal(qincomev2_1_1_m qincomev2_1_2_m qincomev2_1_3_m) if q2dum==1
replace fihhyr2v2_m=-7 if qincomev2_1_1_m==-7|qincomev2_1_2_m==-7|qincomev2_1_3_m==-7
replace fihhyr2v2_m=-8 if qincomev2_1_1_m==-8|qincomev2_1_2_m==-8|qincomev2_1_3_m==-8
replace fihhyr2v2_m=-10 if qincomev2_1_1_m==-10|qincomev2_1_2_m==-10|qincomev2_1_3_m==-10
la define fihhyr2v2_m -7 "don't know" -8 "refused" -10 "missing" 
la val fihhyr2v2_m fihhyr2v2_m
label var fihhyr2v2_m "continuous income variable for type 2s, household"


//Create continuous income variable across all question types
capture drop randomgen /*Note randomgen was used to indicate which type of income question a respondent received*/
gen randomgen=2
label var randomgen "type of income question asked"
gen fihhyr2_m=fihhyr2v2_m if randomgen==2
la define fihhyr2_m -7 "don't know" -8 "refused" -10 "missing" 
la val fihhyr2_m fihhyr2_m
label var fihhyr2_m "continuous income variable for all types, household"



* Income deciles
* Define income deciles for all households (percentiles are defined based on the distribution of household income by survey wave/year)
bysort date: egen adhhy10=pctile(fihhyr2_m) if fihhyr2_m>=0, p(10)
bysort date: egen adhhy20=pctile(fihhyr2_m) if fihhyr2_m>=0, p(20)
bysort date: egen adhhy30=pctile(fihhyr2_m) if fihhyr2_m>=0, p(30)
bysort date: egen adhhy40=pctile(fihhyr2_m) if fihhyr2_m>=0, p(40)
bysort date: egen adhhy50=pctile(fihhyr2_m) if fihhyr2_m>=0, p(50)
bysort date: egen adhhy60=pctile(fihhyr2_m) if fihhyr2_m>=0, p(60)
bysort date: egen adhhy70=pctile(fihhyr2_m) if fihhyr2_m>=0, p(70)
bysort date: egen adhhy80=pctile(fihhyr2_m) if fihhyr2_m>=0, p(80)
bysort date: egen adhhy90=pctile(fihhyr2_m) if fihhyr2_m>=0, p(90)

gen ahhincome_decile=1 if fihhyr2_m<adhhy10 & fihhyr2_m>=0 // generate numerical household income decile variable, where 1 indicates the lowest household income decile, and 10 the highest household income decile
replace ahhincome_decile=2 if fihhyr2_m>=adhhy10 & fihhyr2_m<adhhy20 
replace ahhincome_decile=3 if fihhyr2_m>=adhhy20 & fihhyr2_m<adhhy30 
replace ahhincome_decile=4 if fihhyr2_m>=adhhy30 & fihhyr2_m<adhhy40 
replace ahhincome_decile=5 if fihhyr2_m>=adhhy40 & fihhyr2_m<adhhy50 
replace ahhincome_decile=6 if fihhyr2_m>=adhhy50 & fihhyr2_m<adhhy60 
replace ahhincome_decile=7 if fihhyr2_m>=adhhy60 & fihhyr2_m<adhhy70 
replace ahhincome_decile=8 if fihhyr2_m>=adhhy70 & fihhyr2_m<adhhy80 
replace ahhincome_decile=9 if fihhyr2_m>=adhhy80 & fihhyr2_m<adhhy90 
replace ahhincome_decile=10 if fihhyr2_m>=adhhy90 & fihhyr2_m<. 


// Save Stata file for 2024
save "[enter file path and name here, 2024].dta", replace // save 2024 data


* March 2025
// The example below for March 2025 is the same as for 2024, except that the survey wave is different - the main reason for this is to illustrate how to append different survey waves and create a time series of household income.

clear
set more off

* Import data
import excel "enter file path here", sheet("March 2025") firstrow

gen year = 2025
gen month = 3
gen date = ym(year, month)
format date %tm 

* Annual income for March 2025
//Create income variable for type 2s 
tab qincomev2_1_1

//Recode band question for main respondent
recode qincomev2_1_1 (19=-8) (18=-7)
recode qincomev2_1_1 .=-10
la var qincomev2_1_1 "annual individual income for type 2s"
la define qincomev2_1_1 -7 "don't know" -8 "prefer not to state" -10 "missing" 1 "none"/*
*/ 2 "<£2,500" /*
*/ 3 "£2,500-£4,499" /*
*/ 4 "£4,500-£6,499" 5 "£6,500-£7,499" /*
*/ 6 "£7,500-£9,499" 7 "£9,500-£11,499" /*
*/ 8 "£11,500-£13,499" 9 "£13,500-£15,499" /*
*/ 10 "£15,500-£17,499" 11 "£17,500-£24,999" /*
*/ 12 "£25,000-£34,999" 13 "£35,000-£44,999" /*
*/ 14 "£45,000-£54,999" 15 "£55,000-£74,999" 16 "£75,000-£99,999" 17 ">=£100,000", replace 
la val qincomev2_1_1 qincomev2_1_1
tab qincomev2_1_1

//Create mid-point variable for main respondent 
gen qincomev2_1_1_a=.
replace qincomev2_1_1_a=0 if qincomev2_1_1==1
replace qincomev2_1_1_a=1250 if qincomev2_1_1==2
replace qincomev2_1_1_a=3500 if qincomev2_1_1==3
replace qincomev2_1_1_a=5500 if qincomev2_1_1==4
replace qincomev2_1_1_a=7000 if qincomev2_1_1==5
replace qincomev2_1_1_a=8500 if qincomev2_1_1==6
replace qincomev2_1_1_a=10500 if qincomev2_1_1==7
replace qincomev2_1_1_a=12500 if qincomev2_1_1==8
replace qincomev2_1_1_a=14500 if qincomev2_1_1==9
replace qincomev2_1_1_a=16500 if qincomev2_1_1==10
replace qincomev2_1_1_a=21250 if qincomev2_1_1==11
replace qincomev2_1_1_a=30000 if qincomev2_1_1==12
replace qincomev2_1_1_a=40000 if qincomev2_1_1==13
replace qincomev2_1_1_a=50000 if qincomev2_1_1==14
replace qincomev2_1_1_a=65000 if qincomev2_1_1==15
replace qincomev2_1_1_a=87500 if qincomev2_1_1==16
replace qincomev2_1_1_a=125000 if qincomev2_1_1==17
replace qincomev2_1_1_a=-7 if qincomev2_1_1==-7
replace qincomev2_1_1_a=-8 if qincomev2_1_1==-8
recode qincomev2_1_1_a .=-10

//Label mid-point variable for main respondent 
la var qincomev2_1_1_a "annual individual income for type 2s (mid-points)"
la define qincomev2_1_1_a -7 "don't know" -8 "prefer not to state" -10 "missing"
la val qincomev2_1_1_a qincomev2_1_1_a

//Recode continuous income question for main respondent
rename qincomefreev2_n_1 qincomev2_1_1_c
replace qincomev2_1_1_c=0 if qincomev2_1_1_c<0
replace qincomev2_1_1_c=-7 if qincomefreev2_dk_1==1
replace qincomev2_1_1_c=-8 if qincomefreev2_ps_1==1
label var qincomev2_1_1_c "continuous individual income variable for type 2s"
la define qincomev2_1_1_c -7 "don't know" -8 "refused"
la val qincomev2_1_1_c qincomev2_1_1_c

//Continuous income series using main respondents' income when given and mid-point of income range otherwise
gen qincomev2_1_1_m=qincomev2_1_1_c
replace qincomev2_1_1_m=0 if qincomev2_1_1==1 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=1250 if qincomev2_1_1==2 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=3500 if qincomev2_1_1==3 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=5500 if qincomev2_1_1==4 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=7000 if qincomev2_1_1==5 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=8500 if qincomev2_1_1==6 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=10500 if qincomev2_1_1==7 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=12500 if qincomev2_1_1==8 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=14500 if qincomev2_1_1==9 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=16500 if qincomev2_1_1==10 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=21250 if qincomev2_1_1==11 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=30000 if qincomev2_1_1==12 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=40000 if qincomev2_1_1==13 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=50000 if qincomev2_1_1==14 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=65000 if qincomev2_1_1==15 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=87500 if qincomev2_1_1==16 & qincomev2_1_1_m<0
replace qincomev2_1_1_m=125000 if qincomev2_1_1==17 & qincomev2_1_1_m<0

label var qincomev2_1_1_m "continuous individual income variable for type 2s, everyone"
la define qincomev2_1_1_m -7 "don't know" -8 "refused"
la val qincomev2_1_1_m qincomev2_1_1_m
sum qincomev2_1_1_m


//Recode income band question for partner/2nd earner
recode qincomev2_1_2 (19=-8) (18=-7)
recode qincomev2_1_2 .=-10
la var qincomev2_1_2 "annual partner income for type 2s"
la define qincomev2_1_2 -7 "don't know" -8 "prefer not to state" -10 "not applicable" 1 "none"/*
*/ 2 "<£2,500" /*
*/ 3 "£2,500-£4,499" /*
*/ 4 "£4,500-£6,499" 5 "£6,500-£7,499" /*
*/ 6 "£7,500-£9,499" 7 "£9,500-£11,499" /*
*/ 8 "£11,500-£13,499" 9 "£13,500-£15,499" /*
*/ 10 "£15,500-£17,499" 11 "£17,500-£24,999" /*
*/ 12 "£25,000-£34,999" 13 "£35,000-£44,999" /*
*/ 14 "£45,000-£54,999" 15 "£55,000-£74,999" 16 "£75,000-£99,999" 17 ">=£100,000", replace 
la val qincomev2_1_2 qincomev2_1_2
tab qincomev2_1_2 

//Create mid-point income variable for partner/2nd earner
gen qincomev2_1_2_a=.
replace qincomev2_1_2_a=0 if qincomev2_1_2==1
replace qincomev2_1_2_a=1250 if qincomev2_1_2==2
replace qincomev2_1_2_a=3500 if qincomev2_1_2==3
replace qincomev2_1_2_a=5500 if qincomev2_1_2==4
replace qincomev2_1_2_a=7000 if qincomev2_1_2==5
replace qincomev2_1_2_a=8500 if qincomev2_1_2==6
replace qincomev2_1_2_a=10500 if qincomev2_1_2==7
replace qincomev2_1_2_a=12500 if qincomev2_1_2==8
replace qincomev2_1_2_a=14500 if qincomev2_1_2==9
replace qincomev2_1_2_a=16500 if qincomev2_1_2==10
replace qincomev2_1_2_a=21250 if qincomev2_1_2==11
replace qincomev2_1_2_a=30000 if qincomev2_1_2==12
replace qincomev2_1_2_a=40000 if qincomev2_1_2==13
replace qincomev2_1_2_a=50000 if qincomev2_1_2==14
replace qincomev2_1_2_a=65000 if qincomev2_1_2==15
replace qincomev2_1_2_a=87500 if qincomev2_1_2==16
replace qincomev2_1_2_a=125000 if qincomev2_1_2==17

replace qincomev2_1_2_a=-7 if qincomev2_1_2==-7
replace qincomev2_1_2_a=-8 if qincomev2_1_2==-8
recode qincomev2_1_2_a .=-10
la var qincomev2_1_2_a "annual partner income for type 2s (mid-points)"
la define qincomev2_1_2_a -7 "don't know" -8 "prefer not to state" -10 "missing"
la val qincomev2_1_2_a qincomev2_1_2_a

//Recode continuous income question for partner/2nd earner
rename qincomefreev2_n_2 qincomev2_1_2_c
replace qincomev2_1_2_c=0 if qincomev2_1_2_c<0
replace qincomev2_1_2_c=-7 if qincomefreev2_dk_2==1
replace qincomev2_1_2_c=-8 if qincomefreev2_ps_2==1
label var qincomev2_1_2_c "continuous partner income variable for type 2s"
la define qincomev2_1_2_c -7 "don't know" -8 "refused"
la val qincomev2_1_2_c qincomev2_1_2_c
sum qincomev2_1_2_c

//Continuous income series using partner/2nd earner income when given and mid-point of income range otherwise
gen qincomev2_1_2_m=qincomev2_1_2_c
replace qincomev2_1_2_m=0 if qincomev2_1_2==1 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=1250 if qincomev2_1_2==2 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=3500 if qincomev2_1_2==3 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=5500 if qincomev2_1_2==4 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=7000 if qincomev2_1_2==5 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=8500 if qincomev2_1_2==6 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=10500 if qincomev2_1_2==7 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=12500 if qincomev2_1_2==8 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=14500 if qincomev2_1_2==9 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=16500 if qincomev2_1_2==10 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=21250 if qincomev2_1_2==11 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=30000 if qincomev2_1_2==12 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=40000 if qincomev2_1_2==13 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=50000 if qincomev2_1_2==14 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=65000 if qincomev2_1_2==15 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=87500 if qincomev2_1_2==16 & qincomev2_1_2_m<0
replace qincomev2_1_2_m=125000 if qincomev2_1_2==17 & qincomev2_1_2_m<0

label var qincomev2_1_2_m "continuous partner income variable for type 2s, everyone"
la define qincomev2_1_2_m -7 "don't know" -8 "refused"
la val qincomev2_1_2_m qincomev2_1_2_m
sum qincomev2_1_2_m


//Recode income band question for other earners
recode qincomev2_1_3 (19=-8) (18=-7)
recode qincomev2_1_3 .=-10
la var qincomev2_1_3 "annual other income for type 2s"
la define qincomev2_1_3 -7 "don't know" -8 "prefer not to state" -10 "missing" 1 "none"/*
*/ 2 "<£2,500" /*
*/ 3 "£2,500-£4,499" /*
*/ 4 "£4,500-£6,499" 5 "£6,500-£7,499" /*
*/ 6 "£7,500-£9,499" 7 "£9,500-£11,499" /*
*/ 8 "£11,500-£13,499" 9 "£13,500-£15,499" /*
*/ 10 "£15,500-£17,499" 11 "£17,500-£24,999" /*
*/ 12 "£25,000-£34,999" 13 "£35,000-£44,999" /*
*/ 14 "£45,000-£54,999" 15 "£55,000-£74,999" 16 "£75,000-£99,999" 17 ">=£100,000",replace 
la val qincomev2_1_3 qincomev2_1_3
tab qincomev2_1_3

//Create income mid-point variable for other earners
gen qincomev2_1_3_a=.
replace qincomev2_1_3_a=0 if qincomev2_1_3==1
replace qincomev2_1_3_a=1250 if qincomev2_1_3==2
replace qincomev2_1_3_a=3500 if qincomev2_1_3==3
replace qincomev2_1_3_a=5500 if qincomev2_1_3==4
replace qincomev2_1_3_a=7000 if qincomev2_1_3==5
replace qincomev2_1_3_a=8500 if qincomev2_1_3==6
replace qincomev2_1_3_a=10500 if qincomev2_1_3==7
replace qincomev2_1_3_a=12500 if qincomev2_1_3==8
replace qincomev2_1_3_a=14500 if qincomev2_1_3==9
replace qincomev2_1_3_a=16500 if qincomev2_1_3==10
replace qincomev2_1_3_a=21250 if qincomev2_1_3==11
replace qincomev2_1_3_a=30000 if qincomev2_1_3==12
replace qincomev2_1_3_a=40000 if qincomev2_1_3==13
replace qincomev2_1_3_a=50000 if qincomev2_1_3==14
replace qincomev2_1_3_a=65000 if qincomev2_1_3==15
replace qincomev2_1_3_a=87500 if qincomev2_1_3==16
replace qincomev2_1_3_a=125000 if qincomev2_1_3==17
replace qincomev2_1_3_a=-7 if qincomev2_1_3==-7
replace qincomev2_1_3_a=-8 if qincomev2_1_3==-8
recode qincomev2_1_3_a .=-10
la var qincomev2_1_3_a "annual other income for type 2s (mid-points)"
la define qincomev2_1_3_a -7 "don't know" -8 "prefer not to state" -10 "missing"
la val qincomev2_1_3_a qincomev2_1_3_a

//Recode continuous income question for other earners
rename qincomefreev2_n_3 qincomev2_1_3_c
replace qincomev2_1_3_c=0 if qincomev2_1_3_c<0
replace qincomev2_1_3_c=-7 if qincomefreev2_dk_3==1
replace qincomev2_1_3_c=-8 if qincomefreev2_ps_3==1
label var qincomev2_1_3_c "continuous other income variable for type 2s"
la define qincomev2_1_3_c -7 "don't know" -8 "refused"
la val qincomev2_1_3_c qincomev2_1_3_c
sum qincomev2_1_3_c
kdensity qincomev2_1_3_c if qincomev2_1_3_c>0

//Continuous income series using other earners when given and mid-point of income range otherwise
gen qincomev2_1_3_m=qincomev2_1_3_c
replace qincomev2_1_3_m=0 if qincomev2_1_3==1 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=1250 if qincomev2_1_3==2 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=3500 if qincomev2_1_3==3 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=5500 if qincomev2_1_3==4 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=7000 if qincomev2_1_3==5 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=8500 if qincomev2_1_3==6 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=10500 if qincomev2_1_3==7 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=12500 if qincomev2_1_3==8 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=14500 if qincomev2_1_3==9 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=16500 if qincomev2_1_3==10 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=21250 if qincomev2_1_3==11 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=30000 if qincomev2_1_3==12 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=40000 if qincomev2_1_3==13 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=50000 if qincomev2_1_3==14 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=65000 if qincomev2_1_3==15 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=87500 if qincomev2_1_3==16 & qincomev2_1_3_m<0
replace qincomev2_1_3_m=125000 if qincomev2_1_3==17 & qincomev2_1_3_m<0

label var qincomev2_1_3_m "continuous other income variable for type 2s, everyone"
la define qincomev2_1_3_m -7 "don't know" -8 "refused"
la val qincomev2_1_3_m qincomev2_1_3_m

sum qincomev2_1_3_m
kdensity qincomev2_1_3_m if qincomev2_1_3_m>0


//Combine income from different individuals into household income
gen q2dum=1 if (qincomev2_1_1_m>=0 & qincomev2_1_1_m!=.) & (qincomev2_1_2_m>=0) & (qincomev2_1_3_m>=0) 

egen fihhyr2v2_m=rowtotal(qincomev2_1_1_m qincomev2_1_2_m qincomev2_1_3_m) if q2dum==1
replace fihhyr2v2_m=-7 if qincomev2_1_1_m==-7|qincomev2_1_2_m==-7|qincomev2_1_3_m==-7
replace fihhyr2v2_m=-8 if qincomev2_1_1_m==-8|qincomev2_1_2_m==-8|qincomev2_1_3_m==-8
replace fihhyr2v2_m=-10 if qincomev2_1_1_m==-10|qincomev2_1_2_m==-10|qincomev2_1_3_m==-10
la define fihhyr2v2_m -7 "don't know" -8 "refused" -10 "missing" 
la val fihhyr2v2_m fihhyr2v2_m
label var fihhyr2v2_m "continuous income variable for type 2s, household"


//Create continuous income variable across all question types
capture drop randomgen /*Note randomgen was used to indicate which type of income question a respondent received */
gen randomgen=2
label var randomgen "type of income question asked"
gen fihhyr2_m=fihhyr2v2_m if randomgen==2
la define fihhyr2_m -7 "don't know" -8 "refused" -10 "missing" 
la val fihhyr2_m fihhyr2_m
label var fihhyr2_m "continuous income variable for all types, household"



* Income deciles
* Define income deciles for all households (percentiles are defined based on the distribution of household income by survey wave/year)
bysort date: egen adhhy10=pctile(fihhyr2_m) if fihhyr2_m>=0, p(10)
bysort date: egen adhhy20=pctile(fihhyr2_m) if fihhyr2_m>=0, p(20)
bysort date: egen adhhy30=pctile(fihhyr2_m) if fihhyr2_m>=0, p(30)
bysort date: egen adhhy40=pctile(fihhyr2_m) if fihhyr2_m>=0, p(40)
bysort date: egen adhhy50=pctile(fihhyr2_m) if fihhyr2_m>=0, p(50)
bysort date: egen adhhy60=pctile(fihhyr2_m) if fihhyr2_m>=0, p(60)
bysort date: egen adhhy70=pctile(fihhyr2_m) if fihhyr2_m>=0, p(70)
bysort date: egen adhhy80=pctile(fihhyr2_m) if fihhyr2_m>=0, p(80)
bysort date: egen adhhy90=pctile(fihhyr2_m) if fihhyr2_m>=0, p(90)

gen ahhincome_decile=1 if fihhyr2_m<adhhy10 & fihhyr2_m>=0 // generate numerical household income decile variable, where 1 indicates the lowest household income decile, and 10 the highest household income decile
replace ahhincome_decile=2 if fihhyr2_m>=adhhy10 & fihhyr2_m<adhhy20 
replace ahhincome_decile=3 if fihhyr2_m>=adhhy20 & fihhyr2_m<adhhy30 
replace ahhincome_decile=4 if fihhyr2_m>=adhhy30 & fihhyr2_m<adhhy40 
replace ahhincome_decile=5 if fihhyr2_m>=adhhy40 & fihhyr2_m<adhhy50 
replace ahhincome_decile=6 if fihhyr2_m>=adhhy50 & fihhyr2_m<adhhy60 
replace ahhincome_decile=7 if fihhyr2_m>=adhhy60 & fihhyr2_m<adhhy70 
replace ahhincome_decile=8 if fihhyr2_m>=adhhy70 & fihhyr2_m<adhhy80 
replace ahhincome_decile=9 if fihhyr2_m>=adhhy80 & fihhyr2_m<adhhy90 
replace ahhincome_decile=10 if fihhyr2_m>=adhhy90 & fihhyr2_m<. 


// Save Stata file
save "[enter file path and name here, March 2025].dta", replace // save March 2025 data

// Append files from different waves/years
append using "[enter file path and name here, 2024.dta" // append the March 2025 file using the previously saved file containing 2024 data from line 315

save "[enter file path and name here, 2024-2025].dta", replace // save the combined data file with 2024 and March 2025 data






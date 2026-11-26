> **Reading copy** of `literature/wp-2017-241-fuest-peichl-siegloch-corporate-taxes.pdf` (2.7 MB, 86 pages). Route: markitdown; tool: markitdown 0.1.7; converted 2026-11-26.
> Generated, not edited. Quote numbers from the source file, not from this text.

ifo
241
2017
WORKING
September 2017
PA PERS
Do Higher Corporate Taxes
Reduce Wages?
Micro Evidence from Germany
Clemens Fuest, Andreas Peichl, Sebastian Siegloch

Impressum:
ifo Working Papers
Publisher and distributor: ifo Institute – Leibniz Institute for Economic Research at the
University of Munich
Poschingerstr. 5, 81679 Munich, Germany
Telephone +49(0)89 9224 0, Telefax +49(0)89 985369, email ifo@ifo.de
www.cesifo-group.de
An electronic version of the paper may be downloaded from the ifo website:
www.cesifo-group.de

ifo Working Paper No. 241
Do Higher Corporate Taxes Reduce Wages?
∗
Micro Evidence from Germany
Clemens Fuest Andreas Peichl Sebastian Siegloch
First version: July 2011. This version: September 22, 2017
Abstract
This paper estimates the incidence of corporate taxes on wages using a 20-year
panelofGermanmunicipalitiesexploiting6,800taxchangesforidentification. Using
event study designs and differences-in-differences models, we find that workers bear
about half of the total tax burden. Administrative linked employer-employee data
allow us to estimate heterogeneous firm and worker effects. Our findings highlight
the importance of labor market institutions and profit-shifting opportunities for the
incidence of corporate taxes on wages. Moreover, we show that low-skilled, young
and female employees bear a larger share of the tax burden. This has important
distributive implications.
JEL Classification: H2, H7, J3
Keywords: business taxation, incidence, administrative data, local taxation
∗Fuest: ifo Institute, University of Munich and CESifo (fuest@ifo.de); Peichl: ifo Institute, Uni-
versity of Munich, CESifo, IZA and ZEW (peichl@ifo.de); Siegloch: University of Mannheim, IZA,
ZEWandCESifo(siegloch@uni-mannheim.de). WewouldliketothankHilaryHoynes, theeditor, and
four anonymous referees for their helpful comments. We are indebted to J. Angrist, W. Arulampalam,
A. Auerbach, D. Autor, R. Blundell, D. Card, R. Chetty, M. Devereux, P. Doerrenberg, D. Duncan,
A.Finkelstein,G.Friebel,J.Hermle,J.Hines,H.Kleven,G.Maffini,A.Oswald,M.Overesch,T.Piketty,
J. Poterba, E. Saez, J. C. Su´arez Serrato, J. Voget, D. Yagan, O. Zidar, as well as numerous conference
and seminar participants for valuable comments and suggestions on earlier versions (sometimes circulat-
ing as “Do Employees Bear the Burden of Corporate Taxation? A Micro Level Approach Using Linked
Employer-Employee Data”). We are also thankful to Stefan Bender, J¨org Heining, Dana Mu¨ller and the
whole team of the research data center (FDZ) of the IAB for their continuous support throughout the
project(FDZ259). PeichlgratefullyacknowledgesfinancialsupportbyDeutscheForschungsgemeinschaft
(DFG, PE 1675/3-1). The authors declare that they have no relevant or material financial interests that
relate to the research described in this paper which is forthcoming in the American Economic Review.

1 Introduction
Theincidenceofcorporatetaxationisakeyissueintaxpolicydebates. Thedistributionof
the tax burden between labor and capital has important implications for the progressivity
of the tax system. According to surveys, most people think that capital owners bear the
burden of corporate taxation.1 Business lobbyists, in contrast, argue that the tax reduces
investment so that labor productivity and wages decline, which means that workers bear
the tax burden. Most economists take a middle ground and think that the tax burden
is shared between labor and capital. Yet, even among researchers in the field, there is
substantial disagreement about how much of the burden is shifted to workers.2 The main
reason is that credible empirical evidence on the causal effect of corporate taxes on wages
is scarce. In this paper, we revisit the question of how corporate taxes affect wages.
We exploit the specific institutional setting of the German local business tax (LBT)
to identify the corporate tax incidence on wages. The German setting is well-suited for
several reasons. First, there is substantial tax variation at the local level. From 1993
to 2012, on average about 10% of all municipalities adjusted their LBT rates annually,
resulting in 17,999 tax changes in 10,001 municipalities between 1993 and 2012. Second,
municipalities can only change the LBT rate. The tax base definition and rules about
which types of firms are liable to the tax are determined at the federal level.3 More-
over, municipal autonomy in setting tax rates allows us to treat municipalities as many
small open economies within the highly integrated German national economy – with high
mobility of capital, labor and goods across municipal borders. In this setting, general
equilibrium effects on interest rates or consumer prices, which may complicate measuring
the incidence of the tax on workers, are likely to be of minor importance.
Our analysis combines administrative panel data on the universe of German mu-
nicipalities with administrative linked employer-employee micro data from social security
records. In this data, we observe firms in 3,522 municipalities, leaving us with 6,802 tax
changes for identification. We use non-parametric event study designs to show that wages
decrease significantly after tax increases. At the same time, they do not react in the
periods prior to a tax reform. In addition, we use the event study set-up to show that
tax reforms are not driven by local business cycles. These flat pre-trends support our
identifying assumption and the causal interpretation of our estimates.
1See, e.g., Sheffrin (1994) and various Gallup polls: http://www.gallup.com/poll/1714/taxes.aspx.
2 For example, public economists surveyed by Fuchs, Krueger and Poterba (1998) respond on average
that 40% of the corporate tax incidence is on capital, leaving a substantial share of the burden for labor
(and land owners or consumers). However, one quarter of the surveyed economists believed that the
capital share is below 20%, while another quarter believed the share to be 65% or higher.
3 Kawano and Slemrod (2016) compare a large number of reforms of nationwide corporate taxes and
show that tax rate changes are usually combined with changes in the tax base as well.
1

We then estimate differences-in-differences (DiD) models to quantify the magnitude
of the wage response. Averaging over all firms liable to the LBT, we find that workers
bear approximately 51% of the total tax burden.4 Our findings are robust to the inclusion
of a comprehensive set of flexible non-parametric local controls at different aggregation
levels, suggesting that potentially relevant omitted variables such as local shocks are not
driving the results. Finally, we estimate various heterogeneous firm and worker effects
and discuss the results with regard to different (labor market) theories.
Wecontributetotheliteratureinseveralways. Weprovidenewestimatesofthecor-
porate tax incidence on wages by exploiting the compelling German institutional setting.
So far, credible empirical evidence on the incidence of corporate taxes has been scarce
because sufficient and exogenous variation in corporate tax rates is lacking in previous
studies. While cross-country research designs (such as Hassett and Mathur, 2006; Felix,
2007; Desai, Foley and Hines, 2007; Clausing, 2013; Az´emar and Hubbard, 2015) need to
defend their (implicit or explicit) common trend assumptions, single-country designs can
establish a valid control group more easily. Most existing single-country studies (see, e.g.,
Dwenger, Rattenhuber and Steiner, 2011; Arulampalam, Devereux and Maffini, 2012; Liu
and Altshuler, 2013), however, have to rely on variation in the tax burden that is not
solely driven by policy reforms but also by firms’ choices. For instance, differences in tax
burdens across industries or across regions due to formula apportionment may depend
directly on sales and investment activities, which may be endogenous to tax rates. The
contribution of our paper is to exploit substantial within-country variation in statutory
municipal tax rates. In a recent contribution, Su´arez Serrato and Zidar (2016) estimate
the incidence of U.S. state-level corporate taxes using a spatial equilibrium framework
exploiting regional variation in tax rates and apportionment rules.5 The German setting
has the advantage to offer substantially larger variation in terms of both number and size
of tax rate changes.
Furthermore, we go beyond a cleanly identified average effect of corporate taxes on
wages and analyze the economic factors driving these changes. We estimate heteroge-
neous firm effects and discuss the results in light of different labor market theories and
tax incidence mechanisms. The German labor market, with its variety of wage-setting in-
stitutions, is particularly useful for this exercise. Exploiting the rich administrative linked
employer-employee data, we find that labor market institutions matter for the incidence
4 We observe only very few nominal wage decreases in the data but rather smaller wage increases
leading to lower future wage levels in the treated municipalities.
5 Felix and Hines (2009) also use U.S. state tax variation but rely on cross-sectional data. Bauer,
KastenandSiemers(2012)alsoinvestigatetheGermanLBTbutwithoutusinglinkedemployer-employee
data. Moreover, as in an earlier version of this paper (Fuest, Peichl and Siegloch, 2011), they have to
average tax rates at the county level (consisting of 28 municipalities on average) which leads to biased
results.
2

of corporate taxes on wages. In particular and in line with Felix and Hines (2009) and
Arulampalam, Devereux and Maffini (2012), collective bargaining agreements play a key
role: If wages are set via collective bargaining at the firm level, wage responses are larger
than in cases where wages are set at the sector level or without collective bargaining.
Overall, our results suggest that the higher the rents to be shared between firms and
workers, the higher the pass-through on wages. For instance, wages are more sensitive
to tax changes in more profitable firms. However, we find that wage effects are close
to zero for very large firms, foreign-owned firms and for firms that operate in multiple
jurisdictions. This can be explained by better profit-shifting capabilities of these firms.
In general, the interaction of labor market institutions, avoidance opportunities and tax
rates has received little attention in the literature on the incidence of corporate taxes,
both theoretically and empirically. Our heterogeneous firm effects show that such inter-
actions affect wage responses. This has implications beyond the German setting. While
labor market institutions differ internationally, most countries exhibit a mixture of union-
ized and non-unionized firms or sectors, so that the heterogeneous effects we find in our
setting are likely to be relevant in many other countries as well. This is also true for the
differences between firm types, in particular the finding that higher taxes do not seem to
reduce wages in firms with profit-shifting opportunities.
Last,weaddtothedistributionaldebateabouttheburdenofcorporatetaxation. By
estimating the tax incidence for heterogeneous worker groups we show that higher taxes
reduce wages most for the low-skilled, women, and young workers. Both the average
pass-through on wages of 51% and the heterogeneous worker effects are important for tax
policy because they qualify the widespread view that the corporate income tax is highly
progressive. In a back-of-the-envelope calculation based on Piketty and Saez (2007), we
show that the estimated progressivity of the overall tax systems in both Germany and
the U.S. would decrease by 25-40% if we account for our incidence estimates.
Our analysis focuses on the corporate tax incidence on workers and therefore on
the causal wage response to corporate tax changes. We do not investigate the impact
on input factors, production levels, firm entry or exit. Studying these other margins is
important to understand the overall efficiency costs of corporate taxes. Such an analysis
would, however, be complicated by data (linkage) limitations and is beyond the scope of
this paper.
The rest of this paper is structured as follows. In Section 2, we describe the in-
stitutional setting of business taxation in Germany and introduce the datasets used in
the empirical analysis. The empirical model is presented in Section 3. In Section 4, we
presentourmainestimatesofthecorporatetaxincidenceonwages. Section5providesev-
idence on heterogeneous worker and firm effects which we discuss with respect to different
3

theoretical models and mechanisms. Section 6 concludes.
2 Institutional background and data
Weestimatetheincidenceofcorporatetaxesonwagesbyexploitingtheparticularfeatures
of the German business tax system. We describe this system in Subsection 2.1, with a
special emphasis on the local business tax (LBT, Gewerbesteuer). In Subsection 2.2,
we document the cross-sectional and time variation of the LBT. In Subsection 2.3, we
introduce the administrative linked employer-employee data set, while Subsection 2.4
contains the definition of our estimation sample and descriptive statistics.
2.1 Business taxation in Germany
There are three taxes on business profits in Germany: the municipal LBT as well as
the corporate income tax (CIT, K¨orperschaftsteuer) and the personal income tax (PIT,
Einkommensteuer) which are both set by the federal government. In the following, we
describe the LBT, while the CIT and PIT are described in Appendix B.1.
The LBT applies to both corporate and non-corporate firms, but most firms in
the agricultural and public sector are not liable.6 The tax base of the LBT is basically
operatingprofits. Thecostofdebtfinancingisdeductible, withsomelimitations7, andthe
cost of equity financing is not. Taxable profits of firms with establishments in more than
one municipality are divided between municipalities according to formula apportionment
based on the payroll share. Importantly, the local government can change the tax rate
but neither the tax base nor the liability criteria. Both are set at the federal level.
The tax rate, τ , consists of two components: the basic rate (Steuermesszahl),
LBT
tfed , which is set at the federal level, and a local scaling factor (Hebesatz), θmun, which
LBT LBT
is set at the municipal level. Each year, the municipal council votes on next year’s θmun
LBT
– even if it remains unchanged. The total LBT rate is given by τ = tfed ·θmun. From
LBT LBT LBT
1993 to 2007, tfed was 5.0% and decreased to 3.5% in 2008. For example, for the median
LBT
θmun of 3.9, τ was 19.5% before 2008. In the empirical analysis, we rely on variation
LBT LBT
in τ induced by changes in θmun (described next).
LBT LBT
6 To be precise, paragraphs 2 and 3 of the LBT law (Gewerbesteuergesetz) regulate which firms are
exempt from the LBT. The main criteria are interactions of legal form and industry. Moreover, certain
professions such as accountants, lawyers, journalists or physicians are exempt.
7 A special feature of the LBT is that 25% of interest costs are added to the tax base. Another
peculiarity is that until 2007, the LBT itself was deductible as an expense.
4

2.2 Municipal data and tax rate variation
We use administrative statistics provided by the Statistical Offices of the 16 German fed-
eral states (Statistische Landesaemter) on the fiscal situation of all 11,441 municipalities.
Most importantly, the dataset contains information on θmun, but also on population, mu-
LBT
nicipal spending and revenues. In addition, we observe county (Kreis) level GDP as well
as unemployment rates compiled by the German federal employment agency.
We combined and harmonized the annual state-specific datasets and constructed
a panel on the universe of all municipalities from 1993 to 2012. In the administrative
wage data (see Section 2.3), we can identify municipalities according to their boundaries
as of 2010. Due to mergers, various municipal borders predominantly in East Germany
changed prior to 2010. As we cannot assign the exact LBT rate for affected jurisdictions,
we exclude all municipalities that underwent a municipal merger between 1993 and 2010
from our baseline sample. This concerns 47% of East German and 0.6% of West German
municipalities.8 Overall, there are 10,001 non-merged municipalities in Germany.
Figure 1 visualizes the substantial cross-sectional and time variation in LBT rates.
The left panel of the figure shows the cross-sectional variation in τ for the year 2003,
LBT
the mid-year of our sample.9 Appendix Table C.1 provides measures of the distribution of
θmun over time. The right panel of Figure 1 illustrates this time variation by showing the
LBT
numberofchangesinθmun permunicipalityduringtheperiod1993–2012(AppendixTable
LBT
C.2showsthecorrespondingnumbers). Overall, 19%ofthenon-mergedmunicipalitiesdid
not change θmun during the 20-year period. More than half of the jurisdictions changed it
LBT
once or twice, and only 7.5% experienced 4 or more changes. In total, we observe 17,999
tax rate changes in 10,001 non-merged municipalities.
8 East German municipalities were rather small after reunification in 1990 and were subsequently
merged (sometimes several times) to bigger jurisdictions. As a sensitivity check, we impute tax rates for
merged municipalities by using weighted averages. See Appendix C for a more detailed discussion of the
jurisdictional changes and Figure C.1 showing the tax rate variation including merged municipalities.
9 Thecross-sectionalvariationrevealssomeregionalclustering: forinstance,scalingfactorsarehigher
in the state of North Rhine Westphalia. This is partly due to particularities of that state’s fiscal equal-
ization scheme. Empirically, we account for such differences by including “state × year’ fixed effects.
5

Figure 1: Cross-sectional and time variation in local tax rates
Source: Statistical Offices of the Laender. Maps: GeoBasis-DE / BKG 2015. Notes: This figure shows
the cross-sectional and time variation in municipal scaling factors of the German LBT. The left graph
plots the cross-sectional variation in LBT rates (in %) induced by different scaling factors for 2003 (the
mid-yearofoursample). Therightgraphindicatesthenumberofscalingfactorchangespermunicipality
between 1993 and 2012. White areas are municipalities that underwent a change of boundaries due to
a merger; which are dropped from the baseline sample (see Appendix Figure C.1 for the same graphs
including the dropped municipalities). Jurisdictional boundaries are as of December 31, 2010.
2.3 Linked employer-employee data
Wecombinethemunicipaldatapresentedintheprevioussubsectionwithlinkedemployer-
employee data (LIAB) provided by the Institute of Employment Research (IAB). The
LIAB combines administrative worker data with firm-level data (Alda, Bender and Gart-
ner, 2005).
The firm component of the LIAB is the IAB Establishment Panel (Ko¨lling, 2000),
which is a 1% stratified random sample of all German establishments. The term estab-
lishment refers to the fact that the observational unit is the individual plant, not the
firm. The employer data covers establishments with at least one worker subject to social
insurance contributions and contains about 15,000 establishments. We extract the fol-
lowing variables: number of employees, industry, union status (sector- or firm-level wage
bargaining or no collective agreement), self-rated profitability10, firm structure (single vs.
10 The survey question asks for a self-assessment of the profit situation. We construct a three-point
scale (high, medium, low) for profitability with well-balanced support over the three categories.
6

multi-plant firms), and residence (domestic or foreign) of the owner.
In addition to the establishment-level information, the dataset contains information
on all employees in the sampled establishments. This includes between 1.6 and 2.0 million
workers (corresponding to about 6% of all workers) per year. The employee data is taken
from the administrative employment register of the German Federal Employment Agency
(Bundesagentur fu¨r Arbeit) covering all employees paying social security contributions
(Bender, Haas and Klose, 2000). While civil servants, self-employed individuals and
students are not observed in the social security data, the dataset covers more than 80% of
all employed persons in Germany. The employee information is recorded on June 30th of
each year and includes information on wages, age, gender, occupation, employment type
(full-time or part-time employment) and skill.
Importantly, wages are right-censored at the ceiling for social security contributions
(63,400 euros in 2008 for Western Germany). Up to 13% of the observations are censored
(see Appendix Table C.4 for the distribution of censored workers across firms). Note
that the censoring does not affect our baseline results at the firm-level since we use the
median wage in the establishment as our left-hand-side variable. At the individual level,
we opt for a conservative approach and assign censored individuals the cap, leading to an
underestimation of the wage effect.
2.4 Sample definition and descriptive statistics
We select a ten-year panel of the administrative wage data spanning the years 1999 to
2008 for our analysis. This choice yields a sufficient number of years before and after tax
changes, which are necessary to set up the event study design with a window running
from four years prior to five years after the reform, implying that we need tax data from
1993 (the first year available to us) until 2012 (see Section 3 for details on the empirical
model). Furthermore, ending in 2008 avoids potential wage effects of the Great Recession.
As discussed in Section 2.2, we focus on the 10,001 municipalities that did not
change jurisdictional borders between 1993 and 2012. In the LIAB data, we observe
firms in 3,522 of those non-merged municipalities. This leaves us with 6,802 tax changes
to identify the effect of corporate taxes on wages. Figure 2 shows the distribution of
these changes. The left panel shows all non-merged municipalities, while the panel on the
right-hand side is based on the non-merged municipalities represented in our estimation
sample. The figure shows that tax rate variation in both samples is very similar. In both
samples, 93% of the tax changes are increases (see, also, Tables C.2 and C.3, for more
details on the (similarity of the) tax rate variation).11 The mean increase of τ is 0.9
LBT
11 Given the international trend towards lower corporate tax rates this seems surprising. Yet, both
7

percentage points (or 5%) and the 75th percentile of the tax increase distribution is equal
to 1.1 percentage points (6%). We are therefore able to exploit many and fairly large tax
reforms for identification.12
|     | all municipalities (N=10,001) |     |     | LIAB municipalities (N=3,522) |     |
| --- | ----------------------------- | --- | --- | ----------------------------- | --- |
| 8.  |                               |     | 8.  |                               |     |
avg increase: .9 pp avg increase: .9 pp
p75 increase: 1.1 pp p75 increase: 1.1 pp
| 6.      |                            |                 | 6.                |                            |     |
| ------- | -------------------------- | --------------- | ----------------- | -------------------------- | --- |
| ytisneD |                            |                 | ytisneD           |                            |     |
| 4.      |                            |                 | 4.                |                            |     |
| 2.      |                            |                 | 2.                |                            |     |
| 0       |                            |                 | 0                 |                            |     |
| -5      | 0                          |                 | 5 -5              | 0                          | 5   |
|         | Size of tax change (in pp) |                 |                   | Size of tax change (in pp) |     |
|         | Figure                     | 2: Distribution | of local business | tax changes                |     |
Source: Statistical Offices of the Laender. Notes: The histogram shows the distribution of changes
in the LBT rate induced by changes of the municipal scaling factor from 1993 to 2012 in non-merged
municipalities. In the left panel, the sample consists of all 17,999 tax rate changes in the 10,001 non-
merged municipalities, while in the right panel it is constrained to the 6,802 tax changes in those 3,522
non-mergedmunicipalitiesrepresentedinthelinkedemployer-employeedata(LIAB).Inbothhistograms,
we omit 0.1% of the observations with absolute changes larger than 5 percentage points for illustrative
purposes. The average LBT rate in the full (LIAB) sample is 16.0% (18.7%).
Our estimation sample consist of all firms in non-merged municipalities observed in
the LIAB data and their corresponding workers. We exclude the few firms that changed
their incorporation status during the observation period from the baseline since such a
change simultaneously affects the LBT tax base, the applicable business tax at the federal
level (see Appendix B.1) and potentially other firm characteristics such as firm scale or
collective bargaining agreements. We also focus on firms with more than three workers to
be able to calculate meaningful and reliable wage measures at the firm level. We check the
the federal CIT rate and the top PIT rate decreased in Germany over the period 1993–2012 so that the
overall business tax rate declined as well (see Appendix B.1 for more details). Thus, a rise in the LBT
rates in a municipality over time has to be seen as leading to a slower decrease in the overall tax burden
for firms in these municipalities compared to firms in jurisdictions with constant local tax rates.
12 Forinstance,Su´arezSerratoandZidar(2016)exploitabout100corporatetaxchangesofU.S.states
with an average change (over 10 years) of 1% (and about 20% of changes larger than 2%). Part of their
variationstemsfromtaxbasedifferencesforexampleduetodifferentapportionmentrules. Su´arezSerrato
and Zidar (2017) document that tax base rules explain more of the U.S. state corporate tax variation
than tax rates do.
8

sensitivity of our results with respect to these sample selection choices below. Appendix
Tables C.5 and C.6 present descriptive statistics of our establishment and worker level
sample in non-merged municipalities.13 Table C.5 shows that the average median firm
wage is 2,733 euros per month. The average θmun is 3.85, and the average τ is 18.7%.
LBT LBT
The average (median) establishment has 265 (53) employees. 64% of the establishments
are liable to the LBT. Our baseline estimates presented below will be based on the sample
of liable firms, while we use the sample of non-liable firms for a sensitivity check.
Moreover, the descriptive statistics reveal that 62% of the establishments are single-
plant firms. More than half of the firms have sector-level bargaining agreements in place,
while about a third have no collective bargaining agreement. The descriptive statistics
of the individual worker sample (see Table C.6) place greater weight on larger firms with
more employees. As larger firms pay higher wages, we see that the median wage in
the individual level sample increases to 3,363 euros per month. In terms of individual
characteristics, the table shows that the average worker in our sample is 41 years old.
The share of males is 72%. 14% of the individuals are high-skilled, while about as many
are low-skilled.14 81% of the individuals have never earned a wage higher than the social
security contribution ceiling in our sample.
3 Empirical strategy
3.1 Research design and identification
We use different empirical models to estimate the causal effect of LBT changes on wages.
Our baseline outcome variable is the log median real full-time wage in firm f, located in
municipality m, which is part of commuting zone (CZ) c and state s, in year t, wp50 .15
f(m,c,s),t
We choose the median as the baseline on the firm level to account for the top-coding of
wages at the ceiling for social security contributions (see the discussion in Section 2.3).
We start our analysis using an event study design, which formally reads:
5
(cid:88)
lnwp50 = γ Dj +µ +µ +ψ +ε . (1)
f,t j m,t f m s,t f,t
j=−4
The independent variables of interest are a set of dummies Dj indicating an event
m,t
13 In the baseline, we only consider full-time workers. We also looked at the effects on part-time wages
but found no significant differences (see below).
14 We differentiate between three skill groups: high-skilled workers who have obtained a col-
lege/university degree; medium-skilled who have completed either vocational training or the highest
high school diploma (Abitur); low-skilled who have completed neither of the two.
15 Inordertoeasenotation, weonlyincludetheindexofthelowestgeographicallevelinthefollowing.
9

happening j periods away. Following Simon (2016), we estimate different specifications,
where events are either (i) any LBT increase, (ii) large tax increases, or (iii) tax decreases.
Large increases are defined as any tax hike greater than or equal to the 75th percentile
of the tax increase distribution. There are two potential advantages of focusing on large
increases. First,wagesmightnotrespondtosmalltaxratechanges, e.g.duetoadjustment
costs. Second, we limit the number of events per firm and reduce the likelihood that other
tax events happened within the event window (Simon, 2016). As an additional sensitivity
check, we estimate the model on a restricted sample of tax changes that have no other
changes in the event window. We set a baseline event window, running from 4 years prior
to a tax change to 5 years after.16 In addition, we include firm, (µ ), and municipal, (µ ),
|     |     |     |     |     |     |     |     |     | f   |     | m   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
fixed effects.17 To account for regional shocks, our baseline specification includes “state
| × year” | fixed | effects | (ψ  | ). The | error | term is | denoted | by ε | .   |     |     |
| ------- | ----- | ------- | --- | ------ | ----- | ------- | ------- | ---- | --- | --- | --- |
|         |       |         |     | s,t    |       |         |         | f,t  |     |     |     |
The event study specification uses dummy variables to capture tax rate changes. In
order to account for different magnitudes of tax changes, we follow Su´arez Serrato and
| Zidar | (2016) | and | estimate | the | following | distributed |     | lag model: |     |     |     |
| ----- | ------ | --- | -------- | --- | --------- | ----------- | --- | ---------- | --- | --- | --- |
5
(cid:88)
|     | lnwp50 | −lnwp50 |       | =   | β [ln(1−τ |       | )−ln(1−τ |         | )]+ψ | +ε  | . (2) |
| --- | ------ | ------- | ----- | --- | --------- | ----- | -------- | ------- | ---- | --- | ----- |
|     |        |         |       |     | j         | m,t−j |          | m,t−1−j |      | s,t | f,t   |
|     |        | f,t     | f,t−1 |     |           |       |          |         |      |     |       |
j=−4
We regress the annual change in log wages on the change in the log net-of-business-tax
ˆ
rate. The estimated coefficients β measure the effect of leads and lags of a tax rate
j
change on the annual real wage growth. Time invariant factors are differenced out. We
use the estimates of the model to calculate the cumulative effect of a tax change.
In both models (1) and (2), identification is achieved within firms and municipalities
over time, and we thus estimate variants of a DiD model with fixed effects. Identifica-
tion of causal effects in such models requires common trends pre-treatment – that is, no
statistically significant wage responses preceding a tax reform. While we use specifica-
tions (1) and (2) mainly to establish flat pre-trends, we use the following generalized DiD
model to estimate the average effect of a change in the LBT rate on wages relative to the
pre-treatment period, which we then use to calculate the tax incidence:
|     |     |     | lnwp50 | =   | δln(1−τ | )+µ | +µ  | +ψ    | +ε , |     | (3) |
| --- | --- | --- | ------ | --- | ------- | --- | --- | ----- | ---- | --- | --- |
|     |     |     |        | f,t |         | m,t | f   | m s,t | f,t  |     |     |
16 Weexperimentedwithdifferentleadsandlags,butresultsarerobusttotheeventwindowdefinition.
As commonly done, we bin up event dummies at the endpoints of the event window (i.e., j = −4 and
j = 5). Hence, the dummy D5 accounts for all reforms occurring five or more years ago (McCrary,
m,t
2007). This is necessary as we have a balanced panel in terms of years (1993-2012), but reform years
differ across municipalities, which yields an unbalanced panel in event time. Because of this, we do not
| plot | the endpoint | estimates |     | in the event | study | graphs. |     |     |     |     |     |
| ---- | ------------ | --------- | --- | ------------ | ----- | ------- | --- | --- | --- | --- | --- |
17 Firm and municipal fixed effects are highly collinear as only very few firms move between munici-
| palities | in the | data. |     |     |     |     |     |     |     |     |     |
| -------- | ------ | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
10

where δ measures the percent change in wages induced by a one percent increase in the
net-of-tax rate.
Givenflatpre-trends,ourresearchdesignwouldstillbeinvalidiflocalshockssystem-
atically affected tax rates and wages. We provide three further checks to assess whether
such potential local shocks are likely to bias our estimates. First, we run event study de-
signsasspecifiedinequation(1)usingGDP,unemployment, aswellasmunicipalrevenues
and spending as outcome variables. Significant pre-treatment trends for these outcomes
wouldhintatlocalshocksandcastdoubtonouridentifyingassumption. Aswillbeshown
in Section 4, there are no local shocks to the business cycle prior to a tax change. Second,
we further test the sensitivity of the empirical models with respect to local shocks. While
our baseline specifications include “state × year” fixed effects, which non-parametrically
account for local shocks at the state level, we can control for shocks at different levels of
aggregation. We estimate a simpler model using only year fixed effects and a more com-
plex model with “commuting zone × year” fixed effects (there are 258 CZ in Germany).
If confounding local labor market shocks were important, estimates should vary across
different specifications since they should be picked up at least partly by “CZ × year” fixed
effects. Third, besides these non-parametric specifications, we directly account for local
time-varying confounders by additionally controlling for (lagged) GDP, unemployment,
population, and municipal spending. As will be shown below, our results are robust to
these tests for omitted confounders.
Heterogeneous effects. In order to test for heterogeneous effects, we interact the
local tax rates in the DiD models with firm or worker characteristics. Some of these
characteristics such as wage setting institutions are potentially endogenous to the tax
rate. For this reason, we fix the characteristics to the values of 1997, i.e., two years
prior to our first panel observation. Heterogeneous firm effects are estimated at the firm
level, and worker effects at the individual level. In terms of controls, the models include
municipal, firm, “state × year” fixed effects (cf. model (3)) and additionally “firm/worker
type × year” fixed effects. On the worker level, the outcome variable is the log individual
wage, and we additionaly include worker fixed effects.
Inference. In our baseline approach, we cluster standard errors at the municipal level,
i.e. the level of our identifying variation. Given the well-known problems of biased stan-
dard errors in differences-in-differences models (Bertrand, Duflo and Mullainathan, 2004),
we conduct two tests to assess the sensitivity of our estimates: First, we aggregate the
data to the municipal level, finding similar results. Second, we follow the suggestions by
Angrist and Pischke (2009) to “pass the buck up one level” and cluster standard errors
11

on a higher level of aggregation, which in our case is the county or the commuting zone.
As will be shown below, standard errors of estimates are hardly affected.
| 3.2 Measuring |     | the | tax | incidence |     |     |
| ------------- | --- | --- | --- | --------- | --- | --- |
The DID estimate from equation (3) measures the elasticity of the wage rate with respect
|     |     |     | ˆ   | dw (1−τ). |     |     |
| --- | --- | --- | --- | --------- | --- | --- |
to the net-of-business tax rate, δ = We can use this estimate to calculate the
|     |     |     |     | d(1−τ) w |     |     |
| --- | --- | --- | --- | -------- | --- | --- |
incidence of corporate taxes on wages as the share of the total business tax burden falling
on workers. We do so by relating the welfare change of workers induced by a marginal
change in the net-of-tax rate to the sum of the welfare changes of workers and firm owners
| (see Su´arez | Serrato | and Zidar, | 2016). |     |     |     |
| ------------ | ------- | ---------- | ------ | --- | --- | --- |
Assume that worker i in municipality c maximizes utility U(C,L) over consumption
C and leisure L, subject to the budget constraint C = w(1−t)L, where t is the personal
income tax rate and L the quantity of labor.18 The indirect utility function can be written
as V((1 − t)w) and the change in worker utility induced by a change in the wage rate
is given by dV = L(1 − t)dw. A representative firm j faces a corporate tax rate τ and
maximizes profits, Π = (1−τ)[F(K,L)−wL]−(1−ατ)rK, over capital K and labor L.
The tax base T is given by T = F(K,L)−wL−αrK, where α is the share of deductible
capital costs. By the envelope theorem, the change in welfare for firm owners is given
by dΠ = −dτT −dwL(1−τ). The share of workers in the overall burden of a marginal
|     |     |     |     | dV  |     | ˆ   |
| --- | --- | --- | --- | --- | --- | --- |
change in the corporate tax rate is given by Iw = . Plugging in our estimate of δ
dV+dΠ
and rearranging, the share of workers in the tax burden can be written as:
ˆ
wLδ(1−t)
|     |     |     | Iw = |     | .   | (4) |
| --- | --- | --- | ---- | --- | --- | --- |
ˆ
|     |     |     |     | (1−τ)T −wLδ(t−τ) |     |     |
| --- | --- | --- | --- | ---------------- | --- | --- |
Equation (4) measures the incidence of corporate taxation on wages. As in Sua´rez Serrato
and Zidar (2016), the wage elasticity with respect to the net of tax rate is a sufficient
statistic to calculate marginal welfare changes of both workers and firms.19 It would
also be interesting to look at responses in input factors or output. This would allow us to
calculatetheexcessburdenofthecorporateincometax. However,giventhatthenecessary
information is either incomplete (output) or not available (capital) in our administrative
wage data (see Section 2.3) and given that linking another dataset to our data is not
possible, addressing these questions is beyond the scope of this paper.
18 We omit indices for readability. For notational simplicity, we assume quasilinear preferences and
| normalize | the marginal | utility | of income | to unity. |     |     |
| --------- | ------------ | ------- | --------- | --------- | --- | --- |
19
This approach relies on simplifying assumptions. In particular, all agents are price takers, that is,
imperfect competition in input and output markets is not taken into account, and the measure abstracts
| from heterogeneity | of  | firms and | workers. |     |     |     |
| ------------------ | --- | --------- | -------- | --- | --- | --- |
12

4 Baseline results
We start our analysis of the wage effects of the LBT by plotting the event study estimates
from equation (1) in Panel A of Figure 3 for three different specifications: any increase,
large increases, and any decrease. Given the 0-1-event dummy definition, we exclude
tax decreases (increases) from the sample used to estimate the effect of tax increases
(decreases).20 We find a negative and significant effect of business tax increases on real
wages. We hardly observe any decline in nominal wages in our data but find slower wage
growth in affected firms over time, leading to lower levels in the future. Reassuringly,
wage effects become stronger when focusing on the 25% largest tax increases. Estimates
for tax decreases (which are relatively rare - cf. Figure 2) are noisy and inconclusive. The
point estimates hint at a slight yet insignificant pre-trend. In the sensitivity checks below,
we show that municipalities with tax decreases are not driving our results.
In order to exploit the different sizes of tax changes, we plot the cumulative effects
of the distributed lag model (equation (2)) in Panel B of Figure 3. The higher the net-of-
tax rate increase, the higher the wage growth. Hence, the results of the event study are
confirmed as a tax increase implies a decrease in the net-of-tax rate. Including four leads
of the change in the log net-of-tax rate, we again find a flat pre-trend. The model plotted
in Panel B is estimated on the same sample of municipalities to allow for comparisons to
Panel A. Appendix Figure D.3 shows a similar pattern when including all municipalities.
A remaining concern in our setting is that tax rates might respond to local business
cycle shocks, which could also affect wages. We can test directly for violations of the
identifyingassumptionsbyusinglocaleconomicoutcomesasleft-hand-sidevariablesinthe
event study design. Figure 4 shows the results for GDP and unemployment. Investigating
the pre-treatment periods, we find flat pre-trends for our specifications using (large) tax
increases.21 We find similar patterns when looking at municipal revenues and spending
(see Appendix Figure D.5). For tax decreases, we find again pre-trends for GDP but not
unemployment (see Appendix Figure D.4).
20 We also estimated the model on other sample definitions: (i) no restriction, (ii) zero decreases and
only one increase in event window, (iii) zero decreases and only one increase in the sample. Appendix
Figure D.1 shows that those kinds of sample restrictions are not driving our results.
21 This is in line with previous evidence for the German LBT (Foremny and Riedel, 2014) as well as
for income tax reforms in Europe (Castanheira, Nicod`eme and Profeta, 2012), which suggests that tax
changes are typically triggered by political factors, not shocks on economic variables.
13

|     |     |     | Panel |     | A: Event | study | model |     |
| --- | --- | --- | ----- | --- | -------- | ----- | ----- | --- |
4
)1-=t doirep mrofer-erp ot evitaler(
2
segaw laer goL
0
-2
-4
|     |     |     | -3    | -2        | -1             | 0         | 1         | 2 3 4     |
| --- | --- | --- | ----- | --------- | -------------- | --------- | --------- | --------- |
|     |     |     |       | Increases |                | Large Inc |           | Decreases |
|     |     |     | Panel |           | B: Distributed |           | lag model |           |
2
)tceffe evitalumuc( htworg egaw laeR
1.5
1
.5 0
-.5
|     |     | -5  | -4  | -3     | -2 -1       | 0    | 1 2     | 3 4 5 |
| --- | --- | --- | --- | ------ | ----------- | ---- | ------- | ----- |
|     |     |     |     |        | Lead/Lag    |      | Lag     |       |
|     |     |     |     | Figure | 3: Baseline | wage | effects |       |
Source: LIABandStatisticalOfficesoftheLaender. Notes: PanelAplotseventstudyestimates(γˆ j ,j ∈
[−3,4]) and corresponding 95% confidence bands of different specifications of equation (1). Dependent
variable is the log median firm wage (observed on 30 June for each year). Event variables are dummies
equaltooneforataxincrease,alargetaxincrease(greaterthanorequaltothe75thpercentileofthetax
increasedistribution),orataxdecrease(seelegend). Theestimationsamplecomprisesallestablishments
liable to the LBT in non-merged municipalities. In specifications with tax increase (decrease) dummies,
we exclude all municipalities that experienced a tax decrease (increase) during the observation period.
(βˆ
Panel B plots distributed lag model estimates j ,j ∈ [−4,5]) and corresponding 95% confidence bands
of different specifications of equation (2). Dependent variable is the yearly change in the log median firm
wage. Depending on the specification, main regressors are lags or leads and leads of the yearly change
in the net-of-local-business-tax rate (see legend). Note that a tax increase in the event study design
in Panel A implies a decrease in the net-of-tax rate in Panel B. The estimation sample comprises all
establishments liable to the LBT in non-merged municipalities that did not experience a tax decrease
during the observation period. In both panels, the tax change occurred for the treatment group on 1
Januaryineventyeart=0,asindicatedbytheverticalredline. Allregressionmodelsincludemunicipal,
firm and “state × year” fixed effects. Standard errors are clustered at the municipal level. Estimates are
| reported | in Tables D.10 | and | D.13. |     |     |     |     |     |
| -------- | -------------- | --- | ----- | --- | --- | --- | --- | --- |
14

|     |     |     | Panel | A:  | GDP |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
.5 )1-=t doirep mrofer-erp ot evitaler(
0
.c.p PDG goL
-.5
-1
|     |     | -3    | -2  | -1           | 0         | 1   | 2         | 3   | 4   |
| --- | --- | ----- | --- | ------------ | --------- | --- | --------- | --- | --- |
|     |     |       |     |              | Increases |     | Large Inc |     |     |
|     |     | Panel | B:  | Unemployment |           |     |           |     |     |
3
)1-=t doirep mrofer-erp ot evitaler(
2
etar tnemyolpmenu goL
1
0
-1
-2
|     |     |        | -3       | -2    | -1      | 0         | 1              | 2         | 3 4     |
| --- | --- | ------ | -------- | ----- | ------- | --------- | -------------- | --------- | ------- |
|     |     |        |          |       |         | Increases |                | Large Inc |         |
|     |     | Figure | 4: Event | study | graphs: |           | local business | cycle     | effects |
Source: Statistical Offices of the Laender. Notes: The graph plots event study estimates (γˆ ,j ∈[−3,4])
j
and corresponding 95% confidence bands of different specifications of equation (1). Dependent variables
arelogcountyGDPpercapita(PanelA)andunemploymentrate(PanelB).Eventvariablesaredummies
equal to one for a tax increase or a large tax increase (greater than or equal to the 75th percentile of the
tax increase distribution, see legend). The tax change occurred for the treatment group on 1 January in
eventyeart=0, asindicatedbytheverticalredline. Allregressionmodelsincludemunicipaland“state
× year” fixed effects. The estimation sample comprises all non-merged municipalities from the LIAB
data that did not experience a tax decrease during the observation period. Standard errors are clustered
at the municipal level. For corresponding event study graphs including tax decrease specifications, see
| Figure D.4. | Estimates | are | reported | in Tables | D.15 | and | D.16, respectively. |     |     |
| ----------- | --------- | --- | -------- | --------- | ---- | --- | ------------------- | --- | --- |
15

While we use the graphical representation of the event study and distributed lag
specifications mainly to establish flat pre-trends, we use the DiD model given by equation
(3) to estimate the average effect of a change in the LBT on wages. The baseline elasticity
for liable firms is provided in column (1) of Table 1. A one percent decline in the net-of-
tax rate (reflecting an increase in the tax rate) reduces wages by 0.39 percent. Applying
formula (4), we can calculate the share of the tax burden borne by workers as a measure
of tax incidence. We find that 51% of the corporate tax burden is passed onto workers.
Table 1: Differences-in-differences estimates: baseline wage effects
|                |      | (1)      | (2)     | (3)     | (4)      | (5)      | (6)      |
| -------------- | ---- | -------- | ------- | ------- | -------- | -------- | -------- |
| Log net-of-LBT | rate | 0.388    | 0.229   | 0.386   | 0.396    | 0.343    | 0.399    |
|                |      | (0.127)  | (0.110) | (0.127) | (0.128)  | (0.164)  | (0.118)  |
| Incidence (Iw) |      | 0.505    | 0.288   | 0.502   | 0.516    | 0.442    | 0.520    |
|                |      | (0.170)  | (0.140) | (0.170) | (0.172)  | (0.217)  | (0.159)  |
|                |      | (cid:88) |         |         | (cid:88) | (cid:88) | (cid:88) |
| State × year   | FE   |          |         |         |          |          |          |
(cid:88)
Year FE
(cid:88)
| CZ × year FE |     |     |     |     |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- | --- |
(cid:88)
| Municipal controls | t−2 |     |     |     |     |     |     |
| ------------------ | --- | --- | --- | --- | --- | --- | --- |
(cid:88)
| Firm controls | t−2 |     |     |     |     |     |     |
| ------------- | --- | --- | --- | --- | --- | --- | --- |
(cid:88)
Worker shares
| Observations |     | 44,654 | 44,654 | 44,654 | 44,654 | 25,241 | 44,654 |
| ------------ | --- | ------ | ------ | ------ | ------ | ------ | ------ |
Source: LIAB and Statistical Offices of the Laender. Notes: This table presents the DiD estimates, δˆ,
of regression model (3) at the firm level. Coefficients measure the wage elasticity with respect to the
net-of-local-business-tax rate. The incidence effect Iw is measured according to formula (4) as the share
of the total tax burden borne by workers. All regression models include municipal and firm fixed effects.
Additional control variables and fixed effects (year, “state × year” or “commuting zone (CZ) × year”)
vary depending on the specification (as indicated at the bottom of the table). The estimation sample
is restricted to all establishments liable to the LBT in non-merged municipalities. Standard errors are
clustered at the municipal level. Corresponding standard errors for the incidence measure are obtained
using the Delta method. Our preferred (baseline) specification is shown in column (1).
Sensitivity checks. We run a set of sensitivity checks testing whether our estimates
are driven by modeling choices. We start with further tests of the robustness of our
estimates with respect to unobserved local shocks. The baseline specification includes
“state × year” fixed effects to non-parametrically account for shocks at the state level.
We estimate various specifications where we vary the set of control variables, replacing
“state × year” with more aggregated year fixed effects or more disaggregated “commuting
zone (CZ) × year” fixed effects. We also estimate specifications where we add local
controls (GDP, unemployment, spending, population) and firm controls (employment) to
16

the model, capturing the local business cycle.22 If local shocks were important, estimates
should vary across different specifications. Yet, the results reported in Table 1 are robust.
In particular, estimates are unchanged when moving from the baseline to the very rich
specification with CZ-year fixed effects.
While our baseline results are estimated at the firm level, we also estimated the DiD
model at the municipal and individual level (cf. Appendix Table D.1). While estimates
are a bit noisier on the municipal level due to smaller numbers of observations, point
estimates are reassuringly similar at all three levels of aggregation.
In our baseline specification, the dependent variable is the median wage in the firm.
We chose this measure toaccount forthe right-censoringof the data, which would bias our
estimates toward zero.23 Nevertheless, we conduct several additional checks to assess the
implications of this choice. First, we check that results are not driven by the composition
of the workforce and hence by a change in the median worker. Specification (6) in Table
1 shows that estimates are hardly affected when controlling for various worker shares
(age, gender, skill, occupation and employment type) at the firm level. This is confirmed
by a second test where we estimate the DiD model using the different worker shares as
dependent variables. Results are shown in Appendix Table D.2 and reveal that the worker
composition does not react to changes in the tax rate. Estimates are insignificant and/or
very small. Third, and in line with the predicted bias toward zero, specification (3) of
Table D.3 shows that the wage effect increases when controlling for the share of never-
censored workers at the firm level. Similarly, we find that wage effects are stronger for
firms with fewer censored workers. Last, we estimate the DiD model at the worker level
and exclude all individuals who at least once earned a wage above the contribution ceiling
during the observation period. Again, we find that estimates increase when excluding
censored workers (see column (7) of Table D.6 as well as Table D.8).24
We also test the sensitivity with respect to sample restrictions (cf. Appendix Table
D.5). Our DiD baseline sample comprises firms liable to the LBT in municipalities that
22All control variables are in logs and lagged by two periods to reduce endogeneity issues; results are
similar when using contemporaneous variables.
23 Ifallworkersearnedabovethecontributionceiling,wewouldnotbeabletoobserveanywagechange
in the data and hence estimate a zero wage effect. However, in our data, the median worker in almost
all firms earns a wage below the cap for social security contributions (see Table C.4). We also estimated
model(3)usingdifferentwagemeasuresasleft-handsidevariables(cf.AppendixTableD.4). Whenusing
the mean wage on the firm level (instead of the median), we find smaller yet still significant wage effects.
Moreover, we find that wages for the top 25% of workers across firms respond less. We discuss potential
distributional implications in more detail below.
24 Imputing censored wages would be another option used in the literature (Dustmann, Ludsteck and
Schoenberg,2009;Card,HeiningandKline,2013). Whilethisissensiblewhenanalyzingwageinequality,
it is problematic in our setting since the LBT rate would have to be included in both the selection
equation and the second stage equation.
17

never merged with other municipalities and never experienced a tax decrease during the
observation period. We find smaller but still significant effects when adding tax-exempt
firms to the baseline sample (see also the discussion in Section 5.2). Likewise, estimates
decrease when adding the merged municipalities to the sample. In column (4) of Table
D.5, werestrictthesampletomunicipalitieswithoutataxdecreaseduringtheobservation
period to rule out that those decreases are driving the results. DiD estimates increase
slightly, which suggests that potential endogeneity would bias our estimates downward.
In columns (5) and (6), we add firms that switched their incorporation status and firms
with less than four workers to the estimation sample (cf. Section 2.4). In both cases, the
wage elasticity increases a bit. In 2008, the basic federal rate of the LBT was reduced
from 5 to 3.5% and deductibility of the tax payment itself was abolished (see Section 2.1).
Results are robust to dropping this year from the sample (column 7).
Finally, we show that standard errors hardly change when clustering at higher ag-
gregation levels than municipalities such as counties or commuting zones (see Appendix
Table D.7). These findings are in line with the results that we get when estimating the
model on different levels of aggregation (Table D.1).
5 Theoretical mechanisms and heterogeneous effects
We have established that workers on average bear half of the corporate tax burden. In
this section, we analyze the economic forces driving this effect. We start with a brief
discussion of different theoretical models of corporate tax incidence and the wage effects
theypredict(seeAppendixAforthefulltheoreticalanalysis). Inasecondstep, weexploit
the rich firm and worker level information in our data to investigate the predictions of
the different theories.
5.1 Theoretical predictions
In his seminal paper on corporate tax incidence, Harberger (1962) considers a closed
economy with a corporate and a non-corporate sector. In his setting, the burden of
corporate taxes is borne entirely by capital. The subsequent literature has emphasized
the importance of international capital mobility. In open economies, higher corporate
taxes reduce domestic investment, and wages decline.25
In this paper, we study the effects of a local business tax. In this setting labor is
25 See, e.g., Bradford (1978); Kotlikoff and Summers (1987). In these models, the share of the (source-
based) corporate tax burden borne by domestic immobile factors increases as the size of the economy
relative to the rest of the world decreases. See Auerbach (2006), Harberger (2006) and Gravelle (2013)
for surveys of the literature.
18

arguably more mobile across jurisdictional borders than internationally. In the polar case
of perfect worker mobility, local corporate tax changes should not affect wages because
they are determined in the national labor market.26 Yet, even at the local level, mobility
is likely to be imperfect, and it may differ across workers.
Even with perfect worker mobility, Tiebout (1956)-type models would predict neg-
ative wage responses to local corporate tax increases because migration decisions may
depend on local public services. If the additional revenue raised is spent on local public
services, workers may accept lower local wages. An implication of the Tiebout model is
that wages would also decline in tax-exempt firms if the local tax rate increases.
The models discussed so far are based on the assumption of competitive product and
labor markets. If products (or consumers) are costlessly mobile across jurisdictions, firms
cannot shift the burden onto their customers. This implies that other shifting channels
must be more relevant. Given that we look at a local tax, we expect the pass-through
on consumer prices to be of second order. Nevertheless, the incidence on wages might be
higher for industries that produce more tradable goods.
Relaxing the assumption of perfectly competitive labor markets, we show in Ap-
pendix A that most models with labor market frictions also predict that higher corporate
taxes reduce wages. The mechanisms at work are, however, different, and the magnitude
of the effects depends on wage setting institutions. We will briefly discuss the key insights
from these models in the following paragraphs.
In collective bargaining models, workers receive a share of the surplus generated by
the firm. If higher corporate taxes reduce this surplus, workers bear part of the burden.27
The level at which employers and unions bargain over wages is important. Local taxes
can be expected to have the strongest impact on wages if bargaining is at the firm level,
and the firm operates in one jurisdiction only. If wages are set at the sector level, the
impact of a tax change in one jurisdiction will decrease with the number of jurisdictions
where the sector is present. Similarly, if a firm operates plants in multiple jurisdictions,
a tax change in one may not matter much – even if wages are set at the firm level.
Fair wage models (Akerlof and Yellen, 1990; Amiti and Davis, 2010) also imply
that higher corporate taxes reduce wages. In some variants, wages are directly related to
after tax profits. In other efficiency wage models, such as shirking models (Solow, 1979;
Shapiro and Stiglitz, 1984), the optimal wage trades off higher output against the cost of
26Alongthesamelines,astandardassumptionisthatoutputpricesaredeterminedinnationalmarkets
for goods and services so that the tax burden cannot be shifted onto consumers.
27 Therentaccruingtotheworkersdeclines,buthowthisistranslatedintochangesinemploymentand
wages is theoretically ambiguous. If employment is constant or increases, wages decline unambiguously.
However, it is theoretically possible that employment declines by so much that wages increase although
the overall rent accruing to workers falls.
19

wages.28
higher If wage setting in tax-exempt firms considers wages in taxable firms as
a reference for fairness, the prediction would be that wages in tax-exempt firms are also
| affected by | tax changes. |     |     |     |     |
| ----------- | ------------ | --- | --- | --- | --- |
In monopsonistic labor markets where firms have wage setting power, higher cor-
porate taxes also reduce wages. The magnitude of the effect depends on the degree of
market power. Firms with a lot of market power will pay lower wages. This implies little
room for wages to fall in response to higher corporate taxes and consequently smaller
| wage effects | in firms dominating | the local labor | market. |     |     |
| ------------ | ------------------- | --------------- | ------- | --- | --- |
Another factor that may affect the incidence of corporate taxes is income shifting to
avoid taxes. Large, multi-plant and in particular foreign-owned firms can avoid taxes by
shifting profits across jurisdictions or even abroad. If this is relevant, we should observe
| smaller effects | of tax changes | for these firms. |     |     |     |
| --------------- | -------------- | ---------------- | --- | --- | --- |
Table 2: Wage effects of a local corporate tax under different theoretical models
| Model | Main | mechanism | Predicted wage | effect | Empirical |
| ----- | ---- | --------- | -------------- | ------ | --------- |
findings
Harberger-typemodel Mobilityofproduction Largerwageeffectforlessmobileworkers (cid:88)
| w/openeconomy | factorsdeterminesincidence |     |     |     |     |
| ------------- | -------------------------- | --- | --- | --- | --- |
Tieboutsorting Taxrevenuesincreasepublic Wageeffectssmallerconditional –
|     | goodquality,whichleadsto     |     | onfuturemunicipalspending           |     |     |
| --- | ---------------------------- | --- | ----------------------------------- | --- | --- |
|     | compensatingwagedifferential |     | Wagesinnon-liablefirmsshoulddecline |     | –   |
(cid:88)
Additionalpass-through Ifalternativepass-through Wageeffectshigherinsectors
opportunities opportunitiesexist,wagechannel thatproducemoretradablegoods
becomeslessimportant
(cid:88)
Collectivebargaining Taxreducesrenttobesplit NegativewageeffectforplantswithCBA
betweenfirmsandworkers,
|     | reducingwagesc.p. | Overalleffect | Smallerwageeffectforplantswith |     |     |
| --- | ----------------- | ------------- | ------------------------------ | --- | --- |
(cid:88)
|     | dependsonemploymentresponse.      |     | sector-levelCBAcomparedtoplants |     |     |
| --- | --------------------------------- | --- | ------------------------------- | --- | --- |
|     | Sector-levelbargainingdilutesrent |     | withfirm-levelCBA               |     |     |
effectoflocal taxifsectorpresent
inmanyjurisdictions
Fair/efficiencywages Wagedependsonprofits Strongerwagedeclineinmoreprofitablefirms (cid:88)
|     | and/orreferencewages |     | Wagesinnon-liablefirmsshoulddecline |     | –   |
| --- | -------------------- | --- | ----------------------------------- | --- | --- |
(cid:88)
Monopsonypower Firmswithmarketpowerpay Effectssmallerinfirmswithhigher
|     | lowerwagesgivenlittleroom |     | regionallabormarketpower |     |     |
| --- | ------------------------- | --- | ------------------------ | --- | --- |
forshiftingofcorporatetaxburden
(cid:88)
Incomeshifting Firmsmayshiftprofitsto Smallereffectformulti-establishmentfirms
|     | differentjurisdictionorabroad |     | Smallereffectforforeign-ownedfirms |     | (cid:88) |
| --- | ----------------------------- | --- | ---------------------------------- | --- | -------- |
28
Here, higher corporate taxes decrease investment and therefore reduce the marginal productivity
gainfromawageincrease. Consequently, wagesfallwhencorporatetaxesincrease. Asimilarmechanism
isatplayindirectedsearchmodels,wherehigherwagesaffectedproductivitythroughbetterworker-firm
| matches (Acemoglu | and Shimer, | 1999). |     |     |     |
| ----------------- | ----------- | ------ | --- | --- | --- |
20

In Table 2, we summarize the different theoretical mechanisms and the predicted
wage effects. We can shed light on the relevance of these theories by testing their main
assumptions and mechanisms using the rich linked employer-employee data. The last
column of Table 2 provides a preview of our empirical findings.
5.2 Empirical tests
Inthissubsection, weinvestigatetheempiricalrelevanceofthedifferenttheoriesdiscussed
in the preceding section. As different mechanisms may be at play simultaneously, it is
difficult (if not impossible) to single out specific channels empirically.29 Nonetheless, the
rich linked employer-employee data allows us to zoom in on central implications of the
different theories and test their relevance, assuming that other characteristics are given.
We test the different theoretical predictions by interacting the net-of-tax rate from the
DiD model (3) with pre-determined indicators for specific firm or worker types.
Firm-level heterogeneity. Thefirm-levelresultsarepresentedinTable3. Westartby
testing whether tax-exempt firms also respond to tax rate changes.30 We find a negative
but insignificant point estimate for tax-exempt firms.31 This result suggests that Tiebout
sorting mechanisms do not play a major role in the German context. In line with this
assertion, we find that estimates do not change when we include current and future
municipal spending as additional control variables (see column (3) of Table D.3). Instead,
the negative point estimate suggests that the higher tax burden on other firms might give
tax-exempt firms a competitive advantage, boosting their wages.
Next, we test for differences by industry. Empirically, we find larger and significant
effects only for manufacturing and construction sector firms. One explanation for the
difference to trade and service sector firms could be that the latter are able to shift part
oftheburdentotheircustomersastheirproductsandservicesareonaveragelesstradable
than manufacturing goods.
Next, we investigate the interaction of tax rates and different wage-setting institu-
29 For instance, a large multi-plant firm might be more profitable than others. Consequently, it may
be able to shift income abroad. At the same time, wages may be set via collective bargaining at the firm
level. In order to isolate and test a specific theory, e.g., union bargaining, we would need exogenous (and
exclusive) variation in the bargaining status of the firm.
30Intheabsenceofanyspill-overs,wecouldestimateatriple-differencemodel. Theresultingtreatment
effect, which would equal the difference between the two DiD estimates for liable and non-liable firms,
would be larger.
31 When considering all firms, column (2) of Table D.3 shows that the average worker in Germany
bears 22% of the LBT instead of 51% in liable firms. This is confirmed when estimating the event study
design for liable vs. non-liable firms (see Appendix Figure D.2).
21

tions.32 We start by estimating heterogeneous effects by collective bargaining agreement
(CBA) of the firm. We group firms into three categories: firms with (i) a sector-level
CBA; (ii) a firm-level CBA; (iii) no CBA. Overall, we find larger wage effects for firms
under collective bargaining. In line with the theoretical predictions, we find that the inci-
dence effects for firm-level bargaining are stronger than for sector-level CBA. We also find
wage responses for firms without CBA but they are smaller and not significant. Another
striking empirical pattern is that effects are increasing in firm profitability. This is in line
with collective bargaining models, but also many other labor market theories, where rents
are split between firms and workers, for instance fair wage models.
When stratifying the results by firm size, we find that the wage effect is driven by
small and medium sized firms, which account for more than 95% of all firms in Germany
(andemployabouttwo-thirdsoftheworkers). Takingacloserlook, wealsofindsignificant
wageeffectsforlargerandprofitablemanufacturingfirmswithupto500employees. These
firms (the so-called “Mittelstand”) are often considered to be the backbone of the German
economy, with many ’hidden champions’ (Simon, 2009). Our results suggest that workers
in these companies are more affected by local corporate tax changes than employees of
very large firms. One reason for this finding may be local wage setting power of larger
firms,assuggestedbymonoposonymodels. WheninteractingtheLBTratewithadummy
indicating the size of the firm relative to the local labor market, we indeed find that wages
in relatively small firms react more strongly.
Other potential explanations for the insignificant wage effect in large firms include
more tax avoidance opportunities or a presence in multiple jurisdictions. Table 3 shows
significant wage effects only for single-plant firms, while establishments in multi-plant
firms show no wage response. For those firms, tax changes in one jurisdiction might not
be relevant enough to influence wages. Another explanation is that multi-plant firms can
shift profits to other jurisdictions (nationally and/or internationally). In line with this
reasoning, we also find a zero (to be precise, a negative but insignificant) wage effect if a
plant has a foreign owner.33 This supports the theoretical prediction that profit-shifting
opportunities dampen effects of local tax changes on wages.
32 See Appendix B.2 for a brief discussion of labor market institutions in Germany.
33 Neither the effect for single-plant firms nor for German-owned firms is driven by firm size.
22

Table 3: Differences-in-differences estimates: wage effects by firm type
Stratified by ... Effect of log net-of-LBT rate by firm type N
| Liability      |         | Liable  | Non-liable |         |         | 69,249 |
| -------------- | ------- | ------- | ---------- | ------- | ------- | ------ |
|                |         | 0.388   | −0.178     |         |         |        |
|                |         | (0.127) | (0.154)    |         |         |        |
| Sector         |         | Manuf.  | Const.     | Trade   | Serv.   | 44,654 |
|                |         | 0.556   | 0.452      | 0.151   | 0.383   |        |
|                |         | (0.155) | (0.248)    | (0.276) | (0.253) |        |
| Collect.-Barg. | agreem. | Firm    | Sector     | None    |         | 44,654 |
|                |         | 0.731   | 0.418      | 0.292   |         |        |
|                |         | (0.351) | (0.127)    | (0.239) |         |        |
| Profitability  |         | High    | Medium     | Low     |         | 43,622 |
|                |         | 0.565   | 0.330      | 0.210   |         |        |
|                |         | (0.214) | (0.187)    | (0.200) |         |        |
Firm size (# workers) Below 10 10 to 99 100 to 499 Above 500 44,654
|                |                       | 1.241        | 0.311       | 0.064   | −0.212  |        |
| -------------- | --------------------- | ------------ | ----------- | ------- | ------- | ------ |
|                |                       | (0.520)      | (0.157)     | (0.159) | (0.210) |        |
| Size rel.      | to local labor market | Small        | Medium      | Large   |         | 44,654 |
| (market        | power)                | 0.652        | 0.481       | 0.456   |         |        |
|                |                       | (0.310)      | (0.206)     | (0.169) |         |        |
| Firm structure |                       | Single-plant | Multi-plant |         |         | 44,226 |
|                |                       | 0.426∗∗∗     | 0.223       |         |         |        |
|                |                       | (0.160)      | (0.162)     |         |         |        |
| Ownership      |                       | German       | Foreign     |         |         | 44,654 |
0.449∗∗∗
−0.293
|     |     | (0.141) | (0.298) |     |     |     |
| --- | --- | ------- | ------- | --- | --- | --- |
δˆ
Source: LIAB and Statistical Offices of the Laender. Notes: This table presents the DiD estimates
of regression model (3) for different types of firms as indicated in the table. The heterogeneous effects
are estimated by interacting the LBT rate with dummy variables for different firms types. Coefficients
measure the wage elasticity with respect to the net-of-local-business-tax rate. All specifications include
firm and municipal fixed effects, as well as “state × year” and “firm type × year” fixed effects. The
estimation sample comprises all establishments liable to the LBT in non-merged municipalities.
23

Worker heterogeneity. We test for worker heterogeneity by estimating model (3)
at the individual level. Baseline estimates are similar to results at the firm level and
robust to including various control sets (cf. Table D.6).34 Heterogeneous worker effects
are summarized in Table 4.
In our first test, we look at the effect by skill. While effects are similar for medium-
and low-skilled workers, we find no wage effect for high-skilled individuals, even if we
exclude workers affected by censoring (see Appendix Table D.8). A potential reason
for this difference is that high-skilled workers are usually more mobile than low-skilled
individuals in Germany (Haas, 2000). An alternative explanation would be that the wage
setting process differs across skill levels.35
Mobility effects are also a potential explanation for our heterogeneous effects by
gender, where we find larger wage effects for women. In Germany, women are often the
secondaryearnerinacouple. Thisreducestheirmobility. Wecheckthatgendereffectsare
not driven by differences in industry, occupation, or different work contracts in terms of
working hours. In general, wage effects do not change when including part-time workers;
see column (8) of Table D.6. When differentiating by broad occupation group, we find a
stronger effect for blue-collar workers, in line with the results by industry shown above.
Similarly, when stratifying by age, the effect is significantly higher for younger workers.
Our results for heterogeneous types of workers are particularly important for the
distributional implications of corporate taxation. We confirm other empirical studies
that corporate taxes are not entirely borne by capital, finding that half of the burden
is shifted onto wage earners. In addition, more vulnerable worker groups are affected
more strongly by changes in corporate tax rates. Both findings reduce the progressivity
of business taxes and consequently of the overall tax system.
We assess the implications of our findings for tax progressivity in a back-of-the-
envelope calculation. Our starting point is the study on the progressivity of the US
tax system by Piketty and Saez (2007). They calculate effective average (personal plus
corporate) income tax rates across the income distribution, and measure the progressivity
of the tax system by comparing the average tax rate of the top 10% or top 1% to the
average tax rate of the bottom 90%. Importantly, they assume that corporate taxes fall
34 Unlike the analysis at the firm-level, for which we used the median wage as our left-hand-side
variable, the observed wage at the individual level might be censored as discussed above. We address
this issue by estimating each interaction model for the full sample of all workers and for a subsample
excluding individuals who have been above the contribution ceiling at least once. As above, we find that
wage effects increase when restricting the sample to never censored workers (see Appendix Table D.8).
35 More bargaining power of skilled workers is not a sufficient explanation for the observation that
wages of this group do not fall in response to higher taxes. Groups with high bargaining power can be
expected to capture a high share of the firm’s profit ex ante, so that they should suffer larger losses than
groups with less bargaining power if corporate taxes increase.
24

Table 4: Differences-in-differences estimates: wage effects by worker type
|     | Stratified | by ... | Effect of   | log net-of-LBT | rate by worker | type | N         |
| --- | ---------- | ------ | ----------- | -------------- | -------------- | ---- | --------- |
|     | Skill      |        | High        | Medium         | Low            |      | 9,295,488 |
|     |            |        | 0.013       | 0.357          | 0.377          |      |           |
|     |            |        | (0.120)     | (0.115)        | (0.168)        |      |           |
|     | Gender     |        | Female      | Male           |                |      | 9,295,488 |
|     |            |        | 0.530       | 0.325          |                |      |           |
|     |            |        | (0.129)     | (0.119)        |                |      |           |
|     | Occupation |        | Blue-collar | White-collar   |                |      | 9,295,442 |
|     |            |        | 0.363       | 0.250          |                |      |           |
|     |            |        | (0.132)     | (0.104)        |                |      |           |
|     | Age        |        | Young       | Medium         | Old            |      | 9,295,488 |
|     |            |        | 0.507       | 0.317          | 0.329          |      |           |
|     |            |        | (0.127)     | (0.111)        | (0.106)        |      |           |
δˆof
Source: LIAB and Statistical Offices of the Laender. Notes: This table presents the DiD estimates
regression model (3) with the log individual wage as dependent variables for different worker types as
indicatedinthetable. TheheterogeneouseffectsareestimatedbyinteractingtheLBTratewithdummy
variablesfordifferentfirmstypes. Coefficientsmeasurethewageelasticitywithrespecttothenet-of-local-
business-tax rate. All specifications include worker, firm and municipal fixed effects, as well as “state ×
year” and “worker type × year” fixed effects. The estimation sample comprises all establishments liable
to the LBT in non-merged municipalities. Standard errors are clustered at the municipal level.
entirely on capital income. We take their data and estimates as a benchmark for the US
and use comparable data compiled by Bach, Beznoska and Steiner (2016) for Germany.
We then compute two counterfactuals where 50% (or 100%) of corporate taxes fall on
D.9.36
wages. Calculations are reported in Appendix Table The ratio between the total
effective average tax rate of the top 1% and the bottom 90% decreases substantially from
2.9to2.2ifhalfofthecorporatetaxburdenisbornebylabor, orto1.9ifthefullcorporate
tax burden is shifted onto wages. We find similar relative changes of progressivity for the
German tax system (decreasing from 6.1 to 4.6 and 3.7). Overall, our calculations imply
thattheprogressivityofthe overalltaxsystem inbothcountrieswoulddeclinebybetween
| 25 and 40% | if we account |     | for our incidence | estimates. |     |     |     |
| ---------- | ------------- | --- | ----------------- | ---------- | --- | --- | --- |
6 Conclusions
In this paper, we exploit the compelling institutional setting of the German local business
tax to analyze the incidence of corporate taxes on wages. We combine administrative
informationfrom1993to2012ontheuniverseofmunicipalitieswithadministrativelinked
employer-employee data to estimate the causal effect of corporate taxation on wages.
| 36 Further | details are | explained | in the | notes to Appendix | Table D.9. |     |     |
| ---------- | ----------- | --------- | ------ | ----------------- | ---------- | --- | --- |
25

Averaging over firms liable to the LBT, workers bear about 51% of the total tax burden.
This finding is similar to other studies analyzing the corporate tax incidence on wages
(Arulampalam, Devereux and Maffini, 2012; Liu and Altshuler, 2013; Su´arez Serrato and
Zidar, 2016).
Our results thus confirm the view that labor bears a substantial share of the cor-
porate tax burden. Importantly, our results are obtained by exploiting variation at the
local level. Corporate taxes levied at the subnational level exist in many countries, and
our results are likely to be relevant in these countries as well. At the same time, it is
important to discuss how our findings are related to settings with state-level or national
corporate taxes. Two differences are important. On the one hand, labor is likely to be
more mobile at the local level, which attenuates the incidence on wages. On the other
hand, focusing on tax changes at the municipal level implies that changes of prices other
than wages, in particular output prices and prices of intermediate goods, are probably
much smaller than in the case of national corporate tax changes. This would imply that
wage effects of local tax changes are larger.
Going beyond the average wage effect, our analysis shows that incidence estimates
differ considerably across firms and individuals. First, we do not find effects for firms that
are not liable to the LBT. Second, our findings suggest that labor market institutions play
a key role for the incidence of corporate taxes on wages. If there is rent sharing in the
labor market, due to collective bargaining, for instance, wage responses are larger. Third,
wage effects are close to zero for firms that operate in multiple jurisdictions, large firms
and foreign-owned firms. This may be explained by profit-shifting opportunities available
to these firms. Clearly, the heterogeneous results are correlations and should be seen as a
first step toward understanding the underlying mechanisms of the incidence of corporate
taxation on wages. For a more rigorous test of competing theories, additional exogenous
variation in labor market institutions and other firm characteristics would be necessary.
The heterogeneous worker analysis reveals stronger wage effects for low-skilled work-
ers, women and young workers. High-skilled employees are not affected at all. This chal-
lenges the widespread view that the corporate income tax is highly progressive. In fact,
our estimates imply that the shifting of part of the corporate tax burden onto wages
reduces the overall progressivity of the tax systems both in Germany and the U.S. by 25
to 40% compared to a hypothetical situation where no shifting occurs.
An important limitation of our analysis is that we focus on wage effects and do not
investigate the impact of tax changes on quantities of input factors, on output or on entry
and exit of firms. These potential responses are important for the efficiency costs of taxes.
Another limitation is that we do not consider the impact on land rents. These are issues
for future research.
26

References
Acemoglu, Daron, and Robert Shimer. 1999. “Efficient Unemployment Insurance.”
| Journal | of Political | Economy, | 107(5): 893–928. |     |
| ------- | ------------ | -------- | ---------------- | --- |
Akerlof, G.A. 1982. “Labor Contracts as Partial Gift Exchange.” Quarterly Journal of
| Economics, | 97: 543–569. |     |     |     |
| ---------- | ------------ | --- | --- | --- |
Akerlof, George A., and Janet L. Yellen. 1990. “The Fair Wage-Effort Hypothesis
and Unemployment.” The Quarterly Journal of Economics, 105(2): 255–283.
Alda, Holger, Stefan Bender, and Hermann Gartner. 2005. “European Data
Watch: The Linked Employer-Employee Dataset Created from the IAB Establishment
Panel and the Process-Produced data of the IAB (LIAB).” Schmollers Jahrbuch: Jour-
| nal of Applied | Social | Science | Studies, 125(2): | 327–336. |
| -------------- | ------ | ------- | ---------------- | -------- |
Amiti, Mary, and Donald R. Davis. 2010. “Trade, Firms, and Wages: Theory and
| Evidence.” | Review | of Economic | Studies, | 79(1): 1–36. |
| ---------- | ------ | ----------- | -------- | ------------ |
Angrist, Joshua D., and J¨orn-Steffen Pischke.2009.Mostly Harmless Econometrics.
| Princeton, | New Jersey:Princeton |     | University | Press. |
| ---------- | -------------------- | --- | ---------- | ------ |
Arulampalam, Wiji, Michael P. Devereux, and Giorgia Maffini. 2012. “The
Direct Incidence of Corporate Income Tax on Wages.” European Economc Review,
56(6): 1038–1054.
Auerbach, Alan J. 2006. “Who Bears the Corporate Tax? A Review of What We
Know.” Tax Policy and the Economy, Volume 20, 1–40. The MIT Press.
Az´emar, C´eline, and R. Glenn Hubbard. 2015. “Country characteristics and the
incidence of capital income taxation on wages: An empirical assessment.” Canadian
| Journal | of Economics, | 48(5): | 1762–1802. |     |
| ------- | ------------- | ------ | ---------- | --- |
Bach, Stefan, Martin Beznoska, and Viktor Steiner. 2016. “Who Bears the Tax
Burden in Germany? Tax Structure Slightly Progressive.” DIW Economic Bulletin,
51/52: 601–608.
Ballentine, J. Gregory.1978.“TheIncidenceofaCorporationIncomeTaxinaGrowing
| Economy.” | Journal | of Political | Economy, | 86(5): 863–875. |
| --------- | ------- | ------------ | -------- | --------------- |
Barth, Erling, and Josef Zweimu¨ller.1995.“RelativeWagesunderDecentralizedand
Corporatist Bargaining Systems.” Scandinavian Journal of Economics, 97(3): 369–384.
27

Bauer, Thomas K., Tanja Kasten, and Lars Siemers. 2012. “Business Taxation
and Wages: Evidence from Individual Panel Data.” IZA Discussion Paper No. 6717.
Bender, Stefan, Anette Haas, and Christoph Klose. 2000. “The IAB Employment
Subsample1975-1995.”Schmollers Jahrbuch: Journal of Applied Social Science Studies,
120(4): 649–662.
Bertrand, Marianne, Esther Duflo, and Sendhil Mullainathan. 2004. “How Much
Should we Trust Difference-in-Difference Estimates?” Quarterly Journal of Economics,
119(1): 249–275.
Boeri, Tito. 2014. “Two-Tier Bargaining.” IZA Discussion Paper No. 8358.
Bradford, David F. 1978. “Factor prices may be constant but factor returns are not.”
Economics Letters, 1(3): 199–203.
Card, David, J¨org Heining, and Patrick Kline. 2013. “Workplace Heterogeneity
and the Rise of West German Wage Inequality.” The Quarterly Journal of Economics,
128(3): 967–1015.
Castanheira, Micael, Ga¨etan Nicod`eme, and Paola Profeta. 2012. “On the po-
litical economics of tax reforms: survey and empirical assessment.” International Tax
and Public Finance, 19(4): 598–624.
Clausing, Kimberly A. 2013. “Who pays the corporate tax in a global economy?”
National Tax Journal, 66(1): 151–184.
Desai, Mihir A., C. Fritz Foley, and James R. Hines. 2007. “Labor and Capital
Shares of the Corporate Tax Burden: International Evidence.” mimeo, presented at the
International Tax Policy Forum and Urban-Brookings Tax Policy Center conference on
Who Pays the Corporate Tax in an Open Economy?, 18 December, 2007.
Diamond, P. A., and J. Mirrlees. 1971a. “Optimal Taxation and Public Production
I: Production Efficiency.” American Economic Review, 61(1): 8–27.
Diamond, P. A., and J. Mirrlees. 1971b. “Optimal Taxation and Public Production
II: Tax Rules.” American Economic Review, 61(3): 261–278.
Du Caju, P., E. Gautier, D. Momferatou, and M. Ward-Warmedinger. 2008.
“Institutional Features of Wage Bargaining in 23 European Countries, the US and
Japan.” ECB Working Paper Series No 974.
28

Dustmann, Christian, Bernd Fitzenberger, Uta Scho¨nberg, and Alexandra
Spitz-Oehner. 2014. “From Sick Man of Europe to Economic Superstar: Germany’s
Resurgent Economy.” Journal of Economic Perspectives, 28(1): 167–188.
Dustmann, Christian, Johannes Ludsteck, and Uta Schoenberg. 2009. “Revisit-
ing the German Wage Structure.” Quarterly Journal of Economics, 124(2): 843–881.
Dwenger, Nadja, Pia Rattenhuber, and Viktor Steiner. 2011. “Sharing the Bur-
den: Empirical Evidence of Corporate Tax Incidence.” Preprint of the Max Planck
Institute for Tax Law and Public Finance 2011-14.
Egger, Hartmut, and Udo Kreickemeier. 2012. “Fairness, trade, and inequality.”
Journal of International Economics, 86(2): 184–196.
Ellguth, Peter, Hans-Dieter Gerner, and Jens Stegmaier.2012.“WageBargaining
inGermany–theRoleofWorksCouncilsandOpeningClauses.”IAB Discussion Paper
05/2012.
Feldstein, Martin. 1974. “Incidence of a Capital Income Tax in a Growing Economy
with Variable Savings Rates.” The Review of Economic Studies, 41(4): 505–513.
Felix, R. Alison. 2007. “Passing the Burden: Corporate Tax Incidence in Open
Economies.” Federal Reserve Bank of Kansas City Regional Research Working Paper
07-01.
Felix, R. Alison, and James R. Hines. 2009. “Corporate Taxes and Union Wages in
the United States.” NBER Working Paper No. 15263.
Foremny, Dirk, and Nadine Riedel. 2014. “Business Taxes and the Electoral Cycle.”
Journal of Public Economics, 115: 48–61.
Fuchs, Victor R., Ala B. Krueger, and James M. Poterba. 1998. “Economists’
Views about Parameters, Values, and Policies: Survey Results in Labor and Public
Economics.” Journal of Economic Literature, 36(3): 1387–1425.
Fuest, Clemens, Andreas Peichl, and Sebastian Siegloch. 2011. “Do Employ-
ees Bear the Burden of Corporate Taxation? A Micro Level Approach Using Linked
Employer-Employee Data.” Presented at the 67th Annual Congress of the International
Institute of Public Finance in Ann Arbor.
Fuest, Clemens, Andreas Peichl, and Sebastian Siegloch. 2013. “Do Higher Cor-
porate Taxes Reduce Wages? Micro Evidence from Germany.” IZA Discussion Paper
No. 7390.
29

Gravelle, Jennifer C. 2013. “Corporate Tax Incidence: Review of General Equilibirum
Estimates and Analysis.” National Tax Journal, 66(1): 185–214.
Haas, Anette. 2000. “Regionale Mobilit¨at gestiegen.” IAB Kurzbericht, 4.
Harberger, Arnold C. 1962. “The Incidence of the Corporation Income Tax.” Journal
| of Political | Economy, | 70(3): | 215–240. |     |
| ------------ | -------- | ------ | -------- | --- |
Harberger, Arnold C. 1995. “The ABCs of Corporate Tax Incidence: Insights into the
Open-Economy Case.” In Tax Policy and Economic Growth: Proceedings of a Sym-
posium sponsored by the American Council for Capital Formation. 51–73. Washing-
| ton:ACCF | Center | for Policy | Research. |     |
| -------- | ------ | ---------- | --------- | --- |
Harberger, Arnold C.2006.“CorporateTaxIncidence: ReflectionsonWhatIsKnown,
Unknonw and Unknowable.” In Fundamental Tax Reforms: Issues, Choices, and Impli-
cations. , ed. John W. Diamond and George R. Zodrow, 283–308. Cambridge, MA:MIT
Press.
Hassett, Kevin A., and Aparna Mathur. 2006. “Taxes and Wages.” AEI Working
| Paper No. | 128. |     |     |     |
| --------- | ---- | --- | --- | --- |
Kawano, Laura, and Joel Slemrod. 2016. “How do corporate tax bases change when
corporate tax rates change? With implications for the tax rate elasticity of corporate
tax revenues.” International Tax and Public Finance, 23(3): 401–433.
Ko¨lling, Arnd. 2000. “The IAB-Establishment Panel.” Schmollers Jahrbuch: Journal
| of Applied | Social Science | Studies, | 120(2): | 291–300. |
| ---------- | -------------- | -------- | ------- | -------- |
Kotlikoff, Laurence J., and Lawrence H. Summers. 1987. “Tax Incidence.” In
Handbook of Public Economics. Vol. 2, , ed. Alan J. Auerbach and Martin Feldstein,
| 1043–1092. | Amsterdam:Elsevier. |     |     |     |
| ---------- | ------------------- | --- | --- | --- |
Liu, Li, and Rosanne Altshuler. 2013. “Measuring the Burden of the Corporate
Income Tax under Imperfect Competition.” National Tax Journal, 66(1): 215–237.
McCrary, Justin. 2007. “The Effect of Court-Ordered Hiring Quotas on the Composi-
tion and Quality of Police.” The Amercian Economic Review, 97(1): 318–353.
McDonald, Ian M., and Robert E. Solow. 1981. “Wage Bargaining and Employ-
| ment.”      | The America | Economic | Review,   | 71(5): 896–908. |
| ----------- | ----------- | -------- | --------- | --------------- |
| NCSL. 2009. | “State,     | Federal  | and Local | Taxes.”         |
http://www.ncsl.org/documents/
fiscal/statefederalandlocaltaxes.pdf.
30

OECD. 2015. “Tax on corporate profits (indicator).” doi: 10.1787/d30cc412-en.
Oswald, Andrew J. 1993. “Efficient contracts are on the labour demand curve: Theory
| and facts.” |     | Labour | Economics, | 1(1): | 85–113. |     |
| ----------- | --- | ------ | ---------- | ----- | ------- | --- |
Piketty, Thomas, and Emmanuel Saez. 2007. “How Progressive is the U.S. Fed-
eral Tax System? A Historical and International Perspective.” Journal of Economic
| Perspectives, |     | 21(1): | 3–24. |     |     |     |
| ------------- | --- | ------ | ----- | --- | --- | --- |
Ratti, Ronald A., and Parthasarathi Shome. 1977. “On a General Equilibrium
Model of the Incidence of the Corporation Tax under Uncertainty.” Journal of Public
| Economics, |     | 8(2): | 233–238. |     |     |     |
| ---------- | --- | ----- | -------- | --- | --- | --- |
Rogerson, Richard, Robert Shimer, and Randall Wright. 2005. “Search-Theoretic
Models of the Labor Market: A Survey.” Journal of Economic Literature, 43(4): 959–
988.
Shapiro, C., and J. Stiglitz. 1984. “Equilibrium Unemployment as a Worker Discipline
| Device.” | The | American | Economic |     | Review, 74(3): | 433–444. |
| -------- | --- | -------- | -------- | --- | -------------- | -------- |
Sheffrin, Steven M. 1994. “Tax Progressivity and Income Inequality.” , ed. Joel Slem-
rod, Chapter Perceptions of Fairness in the Crucible of Tax Policy, 309–334. Cambridge
| University | Press. |     |     |     |     |     |
| ---------- | ------ | --- | --- | --- | --- | --- |
Shoven, John B. 1976. “The Incidence and Efficiency Effects of Taxes on Income from
| Capital.” | Journal |     | of Political | Economy, | 84(6): | 1261–1283. |
| --------- | ------- | --- | ------------ | -------- | ------ | ---------- |
Simon, David. 2016. “Does Early Life Exposure to Cigarette Smoke Permanently Harm
Childhood Welfare? Evidence from Cigarette Tax.” American Economic Journal: Ap-
| plied Economics, |     |     | 8(4): 128–159. |     |     |     |
| ---------------- | --- | --- | -------------- | --- | --- | --- |
Simon, Hermann. 2009. Hidden Champions of the Twenty-First Century: The Success
| Strategies | of  | Unknown | World | Market | Leaders. | Berlin:Springer. |
| ---------- | --- | ------- | ----- | ------ | -------- | ---------------- |
Solow, Robert M. 1979. “Another possible source of wage stickiness.” Journal of
| Macroeconomics, |     |     | 1(1): 79–82. |     |     |     |
| --------------- | --- | --- | ------------ | --- | --- | --- |
Su´arez Serrato, Juan Carlos, and Owen M. Zidar. 2017. “The Structure of State
Corporate Taxation and its Impact on State Tax Revenues and Economic Activity.”
| National | Bureau |     | of Economic | Research | Working | Paper 23653. |
| -------- | ------ | --- | ----------- | -------- | ------- | ------------ |
Su´arez Serrato, Juan Carlos, and Owen Zidar. 2016. “Who Benefits from State
Corporate Tax Cuts? A Local Labor Markets Approach with Heterogeneous Firms.”
| The Amercian |     | Economic | Review, | 106(9): | 2582–2624. |     |
| ------------ | --- | -------- | ------- | ------- | ---------- | --- |
31

Tiebout, C. M. 1956. “A Pure Theory of Local Expenditure.” Journal of Political
Economy, 64: 416–424.
32

Appendices for online publication only
A The theory of corporate tax incidence
The theoretical literature has produced various models of corporate tax incidence. These
models lead to different predictions, depending on the assumptions made about factor
and output markets, wage-setting institutions, the structure of the tax system and be-
havioral reactions to tax changes. In the seminal paper by Harberger (1962), the economy
is closed, labor markets are competitive and capital is in fixed supply. At least for plau-
sible parameter values, the corporate tax burden is almost fully borne by capital.37 The
subsequent literature has emphasized the importance of international capital mobility in
open economies (Diamond and Mirrlees, 1971a,b; Bradford, 1978; Kotlikoff and Summers,
1987; Harberger, 1995).38 In these models, the share of the (source-based) corporate tax
burden bore by domestic immobile factors increases as the size of the economy relative to
the rest of the world decreases. In the case of a small open economy that faces a perfectly
elastic supply of capital, the burden of the corporate tax is fully borne by factors other
than capital. If profits of a firm are the result of location specific rents, the tax will partly
fall on these rents. By contrast, if rents are firm specific and firms are mobile, the tax
burden will be fully shifted to owners of immobile factors like land or labor.39
However, complete immobility of labor is a strong assumption, in particular when
considering corporate taxes at the sub-national level. Another restrictive assumption
of standard models is that labor markets are competitive. Relatively little attention
has been paid to the role of wage-setting institutions and labor market frictions in the
context of corporate taxation, two exceptions the studies by Felix and Hines (2009) and
Arulampalam, Devereux and Maffini (2012).
In this Appendix, we discuss the implications of various wage-setting models for the
impact of corporate tax changes on wages. As will be explained further below, the model
will be varied slightly to incorporate different assumptions about wage setting and two
aspects of the tax system relating to formula apportionment and income shifting.
Consider an economy which consists of n jurisdictions. There is a large number of
37 Feldstein (1974) and Ballentine (1978) study tax incidence in models with endogenous savings and
find that part of the tax burden is shifted to labor.
38 Other important extensions of the canonical Harberger model focus on the sectoral composition
(Shoven,1976), savingsbehavior(Feldstein,1974;Bradford,1978)andthepresenceofuncertaintyinthe
economy (Ratti and Shome, 1977).
39 From a global perspective, a tax increase in one jurisdiction reduces the income of immobile factors
in that jurisdiction but increases the income of immobile factors and reduces capital income in the rest
of the world. In principle, the burden of corporate taxes may also fall on suppliers or on customers,
provided input and output prices are not pinned down by international markets.
33

firms in the economy. To ease notation we normalize the number of firms per jurisdiction
to unity. Firms use the following factors of production: capital (K) and labor of two
skill levels. Labor of skill type k, k = h,l, is denoted by Lk.40 We will consider different
production technologies. In the base version of the model we consider a concave produc-
F(K,Lh,Ll),
tion function which is assumed to exhibit declining returns to scale. One
interpretation is that there is an implicit fourth factor, which may be interpreted as a
location-specific rent. While capital and both types of labor are mobile across municipal
| borders, |     | firms | are immobile, |     | due to | the location-specific |     | rent. |     |     |     |     |
| -------- | --- | ----- | ------------- | --- | ------ | --------------------- | --- | ----- | --- | --- | --- | --- |
The after-tax profit of firm i located in jurisdiction j , j = 1...n, is given by
|     |     | P   | = p F | (K ,Lh,Ll)(1−τ |     | )− (cid:80) wkLk(1−τ |     | )−(1−ατ |     | )r K |     | (5) |
| --- | --- | --- | ----- | -------------- | --- | -------------------- | --- | ------- | --- | ---- | --- | --- |
|     |     | ij  | i     | i i            |     | j                    |     | j       |     | j i  | i   |     |
|     |     |     |       |                | i i | k i                  | i   |         |     |      |     |     |
wk
where p is the output price, r is the non-tax cost of capital and is the wage labor
|     | i   |     |     |     | i   |     |     |     |     | i   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
of skill type k. In some variants of the model, labor markets may not clear. In these
cases, we assume that unemployed workers of skill type k receive unemployment benefits
denoted by wk. The tax rate on corporate profits in jurisdiction j is denoted by τ .
j
The variable α, with 0 ≤ α ≤ 1, is a tax base parameter representing the share
of the capital cost which can be deducted from the tax base. This parameter is the
same in all jurisdictions. A cash-flow tax would imply α = 1, that is full deductibility
of all costs. Most existing corporate tax systems are more restrictive, however. Costs
of debt financing are usually deductible while costs of equity financing are not and loss
offset is typically restricted. These properties of the corporate tax base are important for
theoretical predictions about the incidence of the tax, as will be shown below.
In the following we drop the index j for firm variables to ease notation. Total
differentiation of the profit equation and using the standard first order conditions for
| profit-maximization |         |     | yields |      |             |          |           |     |      |       |     |     |
| ------------------- | ------- | --- | ------ | ---- | ----------- | -------- | --------- | --- | ---- | ----- | --- | --- |
|                     |         |     |        |      | ,Lh,Ll)(1−τ | (cid:80) |           |     |      |       |     |     |
|                     | dP =−dτ |     | T +dp  | F (K |             | )−       | dwkLk(1−τ |     | )−dr | (1−ατ | )K  | (6) |
|                     | i       | j   | i      | i i  | i i i       | j k      | i         | i   | j    | i     | j i |     |
(cid:80)
where T = p F (K ,Lh,Ll)− wkLk−αr K is the profit tax base. Equation (6) shows
|     | i   | i   | i i | i i | k i | i i i |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
that a tax increase may lead to lower profits for firm owners, higher output prices charged
to customers, a decline in wages received by workers, lower income for capital owners or
a combination of these effects. It is also possible that some of these groups lose while
others gain.
The distribution of the tax burden depends on how the model is closed, that is,
40
To keep the notation simple we abstract from other input factors like land, energy or other interme-
diate goods. Clearly, the prices of these goods could also be affected by corporate tax changes and the
suppliers might bear part of the corporate tax burden. Corporate tax changes could also be capitalized
in house prices.
34

on the assumed overall structure of the economy, in particular the supply and demand
elasticitiesinfactormarketsandthewage-settinginstitutions. Inthefollowing, wediscuss
the corporate tax incidence on wages under different assumptions about the labor market
regime. As a benchmark, we start with the case of competitive labor markets. We then
turn to models with wage bargaining, fair wage models, models where wages affect worker
productivity and monopsonistic labor markets. In all of the following cases, we assume
that output markets are perfectly competitive and normalize the price p of the output
good to equal 1.
| A.1 Competitive labor | markets |     |     |     |
| --------------------- | ------- | --- | --- | --- |
Assume that input markets are perfectly competitive, so that factor prices will adjust to
equate demand and supply. Factor demand functions are given by the firm’s first order
conditions
|     | ∂F (K ,Lh,Ll) | (1−ατ | )   |     |
| --- | ------------- | ----- | --- | --- |
|     | i i           | i i = | i r | (7) |
|     | ∂K            | (1−τ  | )   |     |
|     | i             |       | i   |     |
and
| ∂F  | (K ,Lh,Ll) |     |     |     |
| --- | ---------- | --- | --- | --- |
i i
|     | i   | i = wk, | k = h,l. | (8) |
| --- | --- | ------- | -------- | --- |
|     | ∂Lk | i       |          |     |
i
Equations (7) and (8) implicitly define the factor demand functions
| KD(wh,wl,R | ) and | LkD(wh,wl,R | ) k = h,l |     |
| ---------- | ----- | ----------- | --------- | --- |
|            | i     |             | i         |     |
| i i        | i     | i           | i i       |     |
r1−ατi
where R = is the tax inclusive cost of capital. While the interest rate r is assumed
i 1−τi
to be independent of capital demand in jurisdiction j, wage rates are determined by
equating labor demand and labor supply. Labor supply is derived from worker utility
maximization. Denote the utility of a worker of skill type k by Uk(Ck,Lk). Ck is the
i i i i
Ck wk(1 t)Lk
worker’s consumption and her budget constraint is given by = − where t
i i i
is the personal income tax rate. Standard utility maximization leads to a labor supply
function which can be expressed as LkS(wk),k = h,l.41. Standard comparative static
i
analysis of the labor market equilibrium conditions LkD(wh,wl,R ) = LkS(wk),k = h,l
i i i i
yields expressions for the impact of a tax rate change on the skill-specific wage. Consider
41 Fornotationalconvenienceweexpressthelaborsupplyfunctionasafunctionofthewageratebefore
income taxation
35

| for example |     | the effect | on  | wages  | of       | skill      | type | h:  |     |                  |     |            |     |
| ----------- | --- | ---------- | --- | ------ | -------- | ---------- | ---- | --- | --- | ---------------- | --- | ---------- | --- |
|             |     | dwh        |     | LhDLlD | (cid:18) |            |      |     |     | (cid:19)(cid:18) |     | (cid:19)   |     |
|             |     |            |     |        |          |            | 1−α  |     |     |                  | 1   |            |     |
|             |     |            | i = | i      | i        | ε          |      |     |     | ε                |     |            |     |
|             |     |            |     |        |          | lR         |      |     |     |                  | hh  |            |     |
|             |     | dτ         |     | ϕ      |          | (1−α)(1−ατ |      |     | )   |                  | wh  |            |     |
|             |     |            | i   |        |          |            |      |     | i   |                  | i   |            |     |
|             |     |            |     | LhDLlD | (cid:18) |            | 1−α  |     |     | (cid:19)(cid:18) |     | 1 (cid:19) |     |
|             |     |            | −   | i      | i        | ε          |      |     |     | (ε               | −µ  | )          | (9) |
|             |     |            |     |        |          | hR         |      |     |     |                  | ll  | l wh       |     |
|             |     |            |     | ϕ      |          | (1−α)(1−ατ |      |     | )   |                  |     |            |     |
|             |     |            |     |        |          |            |      |     | i   |                  |     | i          |     |
where ϕ is a positive parameter (the determinant of the matrix of coefficients). Parameter
ε is the labor demand elasticity of skill group s with respect to wage changes of skill type
st
|     |     |     |     | ∂Ls D(w | h,w l,Ri) |     | t   |     |     |     |     |     |     |
| --- | --- | --- | --- | ------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
t and is defined as ε = i i i w i , s,t = h,l. The labor supply elasticity
|     |     |     | st  |     | t   | Ls  | D(w h,w | l,Ri) |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ----- | --- | --- | --- | --- | --- |
∂w i
|          |      |            |     |     |       |       | i i     | i   |        |     |     |     |     |
| -------- | ---- | ---------- | --- | --- | ----- | ----- | ------- | --- | ------ | --- | --- | --- | --- |
| of skill | type | k is given | by  | µ   | = ∂Lk | S(wk) | wk      | , k | = h,l. |     |     |     |     |
|          |      |            |     | k   |       | i     |         |     |        |     |     |     |     |
|          |      |            |     |     |       | ∂wk   | LkS(wk) |     |        |     |     |     |     |
i
Equation (9) shows that, in general, the impact of a tax change on the wage depends
on demand and supply elasticities in the labor market. However, if the corporate tax is
a cash-flow tax (α = 1), a change in the corporate tax rate will be neutral for factor
demand and, hence, will leave wages unchanged. As a result, the corporate tax is a lump
| sum tax | and | the tax | burden |     | falls | entirely | on  | profits: |     |     |     |     |     |
| ------- | --- | ------- | ------ | --- | ----- | -------- | --- | -------- | --- | --- | --- | --- | --- |
|         | ∂P  |         |        |     |       |          | 2   |          |     |     |     |     |     |
i = −[p F (K ,L1,L2)− (cid:80) wkLk −αrK ] < 0, ∂w k = 0 k = 1,2.
|          |     |        | i i | i   |     |     |     |     | i   |     | i   |     |     |
| -------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|          | ∂τ  |        |     |     | i i |     | i   | i   |     |     | ∂τi |     |     |
|          |     | i      |     |     |     | k=1 |     |     |     |     |     |     |     |
| This may | be  | stated | as  |     |     |     |     |     |     |     |     |     |     |
Result 1: Competitive labor markets: Theimpactofataxchangeonwagesdepends
on the demand and supply elasticities in the labor market. If all costs are perfectly
deductible, the burden of the corporate income tax is fully borne by firm owners. Then a
| tax rate | change | does | not | affect | the | wage | rate. |     |     |     |     |     |     |
| -------- | ------ | ---- | --- | ------ | --- | ---- | ----- | --- | --- | --- | --- | --- | --- |
Interestingly, the cash-flow tax result also carries over to various (but not all) stan-
dard models of imperfect labor markets, as we will show below. Most real world corporate
tax systems deviate from the polar case of a profit tax with perfect cost deductibility,
though. Accordingly, models of tax incidence in the literature typically consider settings
where either capital or labor costs are less than fully deductible.
| A.2 | Wage | bargaining |     |     |     |     |     |     |     |     |     |     |     |
| --- | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Various labor market theories assume that wages are set via bargaining between firms
and their employees. Bargaining models imply that firm owners and employees share a
surplus generated by the firm. If corporate taxes reduce this surplus, it is straightforward
to expect that employees share part of the loss through lower wages. The magnitude
of these wage effects depends on the level where bargaining takes place. We consider
| individual | and | collective |     | (firm | and | sector-level) |     | bargaining. |     |     |     |     |     |
| ---------- | --- | ---------- | --- | ----- | --- | ------------- | --- | ----------- | --- | --- | --- | --- | --- |
36

| A.2.1 | Individual |     | wage | bargaining |     |     |     |     |     |
| ----- | ---------- | --- | ---- | ---------- | --- | --- | --- | --- | --- |
Assume that the wage is set via bargaining between the firm and the employee. The
most widely used labor market model where this happens is the job search model, where
firms and individual employees bargain over a matching rent (see Rogerson, Shimer and
| Wright, | 2005, | for a | survey). |     |     |     |     |     |     |
| ------- | ----- | ----- | -------- | --- | --- | --- | --- | --- | --- |
Let the output a worker of type k in firm i be given by Qk(Kk). The additional
i i
profit the firm earns is PIB = Qk(Kk)(1−τ )−wk(1−τ )−(1−ατ )rKk. The variable
|     |     |     | i   |     | i i | i   | i i | i i |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Kk
is the capital the firm invests to equip the worker. The outcome of the bargaining
i
| process | is given | by  |     |     |     |     |     |     |     |
| ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
wk∗
= argmaxΩ
|     |     |     |     |     | i   |     | i   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
wk
i
where
|     |     |     |     | βkln(wk | −wk)+(1−βk)lnPIB. |     |     |     |     |
| --- | --- | --- | --- | ------- | ----------------- | --- | --- | --- | --- |
Ω =
|     |     |     |     | i i | i   |     | i i |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
βk
The variable ∈ (0,1) stands for the relative bargaining power of the employee. The
i
| first order | conditions |     | of the     | bargaining | problem    |     | yield   |      |      |
| ----------- | ---------- | --- | ---------- | ---------- | ---------- | --- | ------- | ---- | ---- |
|             |            |     |            |            | Qk(Kk)(1−τ |     | )−(1−ατ | )rKk |      |
|             |            |     |            |            |            |     | i       | i    |      |
|             |            | wk∗ | = (1−βk)wk |            | +βk        | i i |         | i .  | (10) |
|             |            | i   |            | i          | i          |     |         |      |      |
|             |            |     |            |            |            |     | (1−τ )  |      |      |
i
| The effect | of  | a change | in the | corporate | tax     | rate     | on the wage is |     |      |
| ---------- | --- | -------- | ------ | --------- | ------- | -------- | -------------- | --- | ---- |
|            |     |          |        | ∂wk∗      |         | (1−α)rKk |                |     |      |
|            |     |          |        |           | i = −βk |          | i ≤ 0.         |     | (11) |
i
|     |     |     |     | ∂τ  |     | (1−τ | )2  |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
|     |     |     |     |     | i   |      | i   |     |     |
A higher corporate tax reduces the wage unless capital costs are fully deductible. Since
the employee’s share of the surplus generated by the firm is increasing in the employee’s
bargaining power, it is plausible that she also bears a larger loss if her bargaining power
| is higher. | This | may | be stated | as  |     |     |     |     |     |
| ---------- | ---- | --- | --------- | --- | --- | --- | --- | --- | --- |
Result 2: Individual wage bargaining: If capital costs are less than fully deductible,
| an increase | in  | the local | corporate |     | tax rate | reduces | the wage. |     |     |
| ----------- | --- | --------- | --------- | --- | -------- | ------- | --------- | --- | --- |
This wage change increases with the bargaining power of the employee. If the
employee receives a large part of the surplus generated by the firm, she also bears a large
| loss if | the surplus | declines |     | due to | taxation. |     |     |     |     |
| ------- | ----------- | -------- | --- | ------ | --------- | --- | --- | --- | --- |
37

| A.2.2 | Collective | bargaining |     |     |     |     |
| ----- | ---------- | ---------- | --- | --- | --- | --- |
Assume that trade union represent workers. We consider two cases: The first case is firm-
level bargaining, where firm-level unions bargain with individual firms. The second case
is sector-level bargaining, where sector-level unions bargain with sector-level employer
organizations.
Firm-level bargaining. Denote the wage for a worker of skill type k employed by a
firm located in jurisdiction i by wk = wk+sk , where sk is the wage premium generated by
|     |     |     | i   | i i | i   |     |
| --- | --- | --- | --- | --- | --- | --- |
bargaining at the firm-level. The bargaining model we use for the firm-level is a standard
efficient bargaining model (McDonald and Solow, 1981), where unions and firms bargain
|     |     | sk, |     | Lk. |     |     |
| --- | --- | --- | --- | --- | --- | --- |
over the wage premium, and employment Each skill type is represented by one
|     |     |     | i   |     | i   |     |
| --- | --- | --- | --- | --- | --- | --- |
trade union and each firm negotiates with the two unions simultaneously (Barth and
Zweimu¨ller, 1995). The objective function of the trade union representing the workers of
| skill type | k in firm | i is given | by   |            |         |     |
| ---------- | --------- | ---------- | ---- | ---------- | ------- | --- |
|            |           |            | Zk = | Lk(wk −wk) | = Lksk. |     |
|            |           |            | i    | i i        | i i     |     |
In case of disagreement, the rent of the union Zk and the firm’s profit PFB are equal
i i
to zero. After wages and employment levels are determined, firms set K to maximize
i
profits:
,Lh,Ll)
∂F(K
|     |     |     |     | i i | i = R | (12) |
| --- | --- | --- | --- | --- | ----- | ---- |
i
∂K
i
| where | R denotes | the cost | of capital: |     |     |     |
| ----- | --------- | -------- | ----------- | --- | --- | --- |
i
|     |     |     |     | (1−ατ | )   |     |
| --- | --- | --- | --- | ----- | --- | --- |
i
|     |     |     | R   | = r | .   |     |
| --- | --- | --- | --- | --- | --- | --- |
i
|     |     |     |     | (1−τ | )   |     |
| --- | --- | --- | --- | ---- | --- | --- |
i
| The outcome | of the | bargaining | process | is given   | by  |     |
| ----------- | ------ | ---------- | ------- | ---------- | --- | --- |
|             |        |            | sk∗,Lk∗ | = argmaxΩk |     |     |
|             |        |            | i       | i          | i   |     |
sk,Lk
i i
where
|     |     |     | Ωk = βklnZk | +(1−βk)lnPFB. |     |     |
| --- | --- | --- | ----------- | ------------- | --- | --- |
|     |     |     | i i         | i             | i i |     |
βk
The variable ∈ (0,1) stands for relative bargaining power of the skill type k union in
i
firm i. The first order conditions of the bargaining problem yield
38

|     |     |     |     |       | (1−βj)βk       | ΠFB |     |     |        |             |     |      |
| --- | --- | --- | --- | ----- | -------------- | --- | --- | --- | ------ | ----------- | --- | ---- |
|     |     |     |     | sk∗ = | i              | i   | i   | k,j | = h,l, | k (cid:54)= | j   | (13) |
|     |     |     |     | i     | (1−βkβj)Lk(1−τ |     |     |     |        |             |     |      |
)
|     |     |     |     |     | i   | i i | i   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
where
(cid:80)
|     |            |     | ΠFB = | F(K ,Lh,Ll)(1−τ |      | )−      |     | wkLk(1−τ |        | )−(1−ατ | )rK . |      |
| --- | ---------- | --- | ----- | --------------- | ---- | ------- | --- | -------- | ------ | ------- | ----- | ---- |
|     |            |     | i     | i               | i i  | i       | k   | i        | i      |         | i i   |      |
| For | employment |     | we    | find            |      |         |     |          |        |         |       |      |
|     |            |     |       |                 | ∂F(K | ,Lh,Ll) |     |          |        |         |       |      |
|     |            |     |       |                 |      | i i     | i   | wk       |        |         |       |      |
|     |            |     |       |                 |      |         | =   | k        | = h,l. |         |       | (14) |
∂Lk
i
sk∗
The wage premium is equal to a share of the surplus per employee generated by the
i
firm. The size of this share is increasing in the relative bargaining power of the skill group
and decreasing in the bargaining power of the other group of employees. Employment
is set so that the marginal productivity of labor is equal to the skill-specific reservation
| wage. | Differentiating |     |     | (13) | yields    |      |      |          |     |       |     |      |
| ----- | --------------- | --- | --- | ---- | --------- | ---- | ---- | -------- | --- | ----- | --- | ---- |
|       |                 |     |     | dsk∗ |           | dLk  |      |          |     |       |     |      |
|       |                 |     |     |      | i Lk +sk∗ | i    | = −β | ((1−α)rK |     | ) ≤ 0 |     | (15) |
|       |                 |     |     |      |           |      |      | 0        |     | i     |     |      |
|       |                 |     |     | dτ   | i         | i dτ |      |          |     |       |     |      |
|       |                 |     |     |      | i         | i    |      |          |     |       |     |      |
where
(1−βj)βk
|     |     |     |     |     | β = |     | i   | i   | > 0. |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
0 (1−βkβj)(1−τ
)2
|     |     |     |     |     |     |     | i i | i   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The left-hand side of (15) is equal to the change in the rent accruing to the workers
of skill type k employed by firm i. This rent unambiguously declines because of the
tax change. Whether the wage rate declines depends on how employment changes in
response to the tax change. Equations (12) and (14) implicitly define the factor demand
functions K (wk,wj,τ ,..),Lk(wk,wj,τ ,..). Standard comparative static analysis shows
|     |     |     | i   | i   |     | i   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
i
thattheimpact ofataxchangeon demand forlaborof typek maybepositive ornegative,
depending on whether the different production factors are complements or substitutes.
| The | effect | on  | wages | is therefore | also | ambiguous. |     |     |     |     |     |     |
| --- | ------ | --- | ----- | ------------ | ---- | ---------- | --- | --- | --- | --- | --- | --- |
|     | This   | may | be    | summarized   | as:  |            |     |     |     |     |     |     |
Result 3: Firm-level bargaining: If capital costs are less than fully deductible, an
increase in the local corporate tax rate reduces the rent of each skill group. The effect on
the wage rate is ambiguous and depends on potential changes in employment.
This result is similar to that of individual bargaining. Higher taxes reduce the rent
that can be shared between the firm and its employees. For given levels of employment,
wages unambiguously decline in response to a tax increase. In the literature, this effect
39

has been referred to as the “direct effect” of a corporate tax change on wages in firms
where wages are set via collective bargaining (Arulampalam, Devereux and Maffini, 2012;
Fuest,PeichlandSiegloch,2013). Takingintoaccountchangesinemploymentmaychange
the wage effect (“indirect effect”). If the number of employees declines in response to a
tax increase, the rent generated by the company is shared among a smaller number of
employees and the overall wage effect can be positive or negative.
Sector-level bargaining. We now assume that bargaining takes place at the sector-
level. To ease notation we normalize the number of sectors in the unionized part of the
labor market to unity. This implies that there are n firms in the sector. An employer
organization bargains with sector-level unions over the sector wide wage. We continue
to assume that each skill group is represented by its own trade union. The employer
organization has the objective of maximizing aggregate profits of the firms in the sector.
Following the seniority model proposed by Oswald (1993), we assume that each union
wishestomaximizethepremiumoverthereservationwagefortheskillgroupitrepresents,
which is given by vk = wk−wk. For given wages, firms set profit-maximizing employment.
The outcome of the sector-level bargaining process is given by
vk∗ = argmaxΩSk
i
vk
where
m
ΩSk = γklnvk +(1−γk)ln (cid:80) PSB.
i i
i=1
The variable γk ∈ (0,1) stands for the relative bargaining power of the sector-level skill
type k union. Rearranging the first order condition of the bargaining problem yields
n
(cid:80) ΠSB
i
vk∗ = γ i=1 k,j = h,l, k (cid:54)= j (16)
0 n
(cid:80) Lk(1−τ )
i i
i=1
where
(1−γj)γk
γ = > 0.
0 (1−γjγk)
The sector wide wage premium is equal to a share of the average surplus per worker
generated by the firms in the sector. Employment and investment decisions are now given
by
40

∂F(K ,Lh,Ll)
i i i = wk k = h,l (17)
∂Lk
i
and
∂F(K ,Lh,Ll)
i i i = R .
i
∂K
i
We now analyze the effect of a corporate tax change in jurisdiction m , m ∈ (1,...,n), on
vk∗. Total differentiation of equation (16) yields
(cid:20) (cid:21)
n n n n
Lk dτ − (cid:80) dLk(1−τ ) (cid:80) ΠSB + (cid:80) dΠFB (cid:80) Lk(1−τ )
m m i i i i i i
dvk∗ = γ i=1 i=1 i=1 i=1 k,j = h,l, k (cid:54)= j
0 (cid:20)
n
(cid:21)2
(cid:80) Lk(1−τ )
i i
i=1
(18)
where
n
(cid:80) dΠFB =− (cid:2) F(K ,Lh ,Ll )− (cid:80) wkLk −αrK (cid:3) dτ
i m m m k i i m
i=1
(cid:18) (cid:19)
n n
+ vh∗ (cid:80) dLh(1−τ )+vl∗ (cid:80) dLl(1−τ ) .
i i i i
i=1 i=1
In general, the impact of a tax change on the wage is ambiguous.
The wage effect converges to zero if the firm in the jurisdiction where the tax change
occurs is small, relative to the sector as a whole. The conditions for the wage effect to
be negligible dvk∗ → 0, which implies dLk = 0 for all i (cid:54)= m,k = h,l follow from (18) and
i
are given by
(cid:104) (cid:105)
Lk m − ∂τm ∂ ( L 1− k m τm) → 0, F(K m ,Lh m ,Ll m )− (cid:80) k wkLk m −αrK m → 0. (19)
n n
(cid:80) Lk(1−τ ) (cid:80) Lk(1−τ )
i i i i
i=1 i=1
The effect is thus negligible if employment (including the tax induced change in em-
ployment) as well as the tax base in jurisdiction m are small, relative to the number of
employees in the sector as a whole, weighted with the tax factors (1−τ ).
i
This may be summarized as
Result 4: Sector-level bargaining: If capital costs are less than fully deductible, an
increase in the tax rate may increase or decrease wages. The wage effect converges to
zero if the activity of the sector in the jurisdiction where the tax change occurs is small,
41

| relative | to the rest | of the sector. |     |     |     |     |     |     |     |
| -------- | ----------- | -------------- | --- | --- | --- | --- | --- | --- | --- |
Result 4 suggests that local tax changes will have a smaller or negligible effect on
wages if wage bargaining takes place at the sector level, rather than the firm level, because
jurisdictions.42
| the sector | will usually | include | many |     |     |     |     |     |     |
| ---------- | ------------ | ------- | ---- | --- | --- | --- | --- | --- | --- |
| A.3        | Fair wage    | models  |      |     |     |     |     |     |     |
In fair wage models (Akerlof, 1982) the wage is usually assumed to be a function of i)
wage43
wages of other employees of the same firm, ii) an external reference and iii) profits
of the firm (Amiti and Davis, 2010; Egger and Kreickemeier, 2012).
Consider a firm i with two types of workers. Assume that the fair wage for type
|     |     |     |     |     |     | wkf | fk(wk,w−k,P |     | wk  |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- |
k workers employed by firm i is given by the function = ), where
|     |     |     |     |     |     |     | i   | i i i i | i   |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- |
are unemployment benefits, w−k are wages of the other skill group in the firm and profits
i
| PFW are | given by |     |     |     |     |     |     |     |     |
| ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
i
(cid:80)
|     | PFW = | F (K ,Lh,Ll)(1−τ |     | )−  | wkLk(1−τ |     | )−(1−ατ | )rK . |     |
| --- | ----- | ---------------- | --- | --- | -------- | --- | ------- | ----- | --- |
|     | i     | i i i            | i   | i   | i        | i   | i       | i i   |     |
k
We assume that the fair wage function has the following standard properties:
|     |     |     |     | ∂fk | ∂fk ∂fk |     |     |     |      |
| --- | --- | --- | --- | --- | ------- | --- | --- | --- | ---- |
|     |     |     |     | i   | i       | i   |     |     |      |
|     |     |     |     | ,   | ,       | >   | 0,  |     | (20) |
|     |     |     |     | ∂wk | ∂w−k ∂P |     |     |     |      |
i
|     |     |     |     | i   | i   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∂fk ∂fk
|     |     |     | i   | − i | L (1−τ | ) > | 0,  |     | (21) |
| --- | --- | --- | --- | --- | ------ | --- | --- | --- | ---- |
|     |     |     |     |     | −k     | i   |     |     |      |
∂w−k ∂P
i
i
∂f−k
∂fk
|     |     |     |     | 1−  | i        | i > | 0.  |     | (22) |
| --- | --- | --- | --- | --- | -------- | --- | --- | --- | ---- |
|     |     |     |     |     | ∂w−k ∂wk |     |     |     |      |
|     |     |     |     |     | i        | i   |     |     |      |
The fair wage is increasing in unemployment benefits wk, in the wage of the other
i
skill group employed by the firm and in the firm’s profits. Equation (21) implies that
the fair wage for skill group k increases if the wage of the other skill group −k increases.
This does not follow directly from the first derivatives, as an increase in the wage of the
other skill group reduces profits. The effect on profits reduces the fair wage. Equation
(22) implies that an increase in any of the reservation wages raises the fair wages of both
groups.
42 Some labor markets are characterized by two tier bargaining, where sector-level bargaining sets a
minimum wage and wage premiums on top of the minimum wage are negotiated at the firm-level (Boeri,
2014). In such a setting, one would expect local tax changes to have a more significant impact on local
| wages than | in the case | of pure sector-level |     | wage bargaining. |     |     |     |     |     |
| ---------- | ----------- | -------------------- | --- | ---------------- | --- | --- | --- | --- | --- |
43 We assume that the reference wage, which can be the average wage level paid in other firms, a
statutory minimum wage or a transfer to the unemployed, is given. It may of course be the case that the
reference wage is affected by local tax changes. This would not alter the result that higher taxes lead to
| lower wages | and vice | versa. |     |     |     |     |     |     |     |
| ----------- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- |
42

In equilibrium, the firm pays fair wages to both types of employees and sets factor
inputs to maximize after-tax profits. Optimal factor inputs are given by the standard
marginal productivity conditions. Equilibrium wages are given by
|     |     |     |     |     | wk∗ | = fk(wk,w−k∗,P∗) |     |     | k = | h,l. |     |     | (23) |
| --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | ---- | --- | --- | ---- |
|     |     |     |     |     | i   | i                | i i | i   |     |      |     |     |      |
Equation (23) implicitly defines the equilibrium wage rates wh∗ and wl∗ as functions
|     |     |     |     |     |     |     |     |     |     | i   |     | i   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
of, among other things, the corporate tax rate τ . Standard comparative static analysis
i
| shows | that | the | effect | of  | a change | in τ | on wages | is  | given | by  |     |     |     |
| ----- | ---- | --- | ------ | --- | -------- | ---- | -------- | --- | ----- | --- | --- | --- | --- |
i
|     |     | ∂wkf∗ |     |     | (cid:20) |      |      |      |     |          | (cid:21) |     |     |
| --- | --- | ----- | --- | --- | -------- | ---- | ---- | ---- | --- | -------- | -------- | --- | --- |
|     |     |       |     | T   |          | ∂f−k |      | ∂fk  |     | ∂fk      |          |     |     |
|     |     |       | i = | − i | 1+       | i L  | (1−τ | )+   | i − | i L (1−τ | )        | < 0 |     |
|     |     |       |     |     |          |      | k i  |      |     | −k       | i        |     |     |
|     |     | ∂τ    |     | ξ   |          | ∂P   |      | ∂w−k |     | ∂P       |          |     |     |
|     |     |       | i   |     |          | i    |      |      |     | i        |          |     |     |
i
where
(cid:80)
|     |     |            |     |      | T = | F (K ,Lh,Ll)− |     |     | wkLk −αrK |     |     |     |     |
| --- | --- | ---------- | --- | ---- | --- | ------------- | --- | --- | --------- | --- | --- | --- | --- |
|     |     |            |     |      | i   | i i           | i i | k   | i i       | i   |     |     |     |
|     | is  | the profit | tax | base | and |               |     |     |           |     |     |     |     |
∂f−k
∂fk
|     |     | ξ = | 1−  | i    | i   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | ∂w−k | ∂wk |     |     |     |     |     |     |     |     |
i
i
|     |     |     | (cid:18) |       | ∂f−k |         | ∂f−k |      |     | (cid:19)   |     |      |     |
| --- | --- | --- | -------- | ----- | ---- | ------- | ---- | ---- | --- | ---------- | --- | ---- | --- |
|     |     |     | ∂fk      |       |      |         |      |      | ∂fk |            |     |      |     |
|     |     | +   |          | i (Lk | +    | i L−k)+ | i    | (L−k | +   | i Lk) (1−τ | )   | > 0. |     |
i
|     |      |     | ∂P  | i          | ∂wk | i   | ∂P  | i   | ∂w−k | i   |     |     |     |
| --- | ---- | --- | --- | ---------- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
|     |      |     |     | i          |     | i   | i   |     |      | i   |     |     |     |
|     | This | may | be  | summarized |     | as  |     |     |      |     |     |     |     |
Result 5: Fair wage model: An increase in the local corporate tax rate reduces the
| wages | of  | all skill | groups. |     |     |     |     |     |     |     |     |     |     |
| ----- | --- | --------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The intuition behind Result 5 is that if higher corporate taxes reduce after-tax
profits, fairness considerations would suggest that employees will bear part of this burden
and vice versa. This effect is independent of whether or not wage and capital costs are
fully deductible from the tax base. The neutrality property of cash-flow taxes does not
hold here because wage fairness is assumed to depend directly on after-tax profits.
| A.4 |     | Models |     | where | wages |     | affect | labor | productivity |     |     |     |     |
| --- | --- | ------ | --- | ----- | ----- | --- | ------ | ----- | ------------ | --- | --- | --- | --- |
Some labor market models emphasize that firms may want to raise wages because higher
wages lead to higher labor productivity and, hence, higher output. These models include
efficiencywagemodels, wherehigherwagesleadtomoreeffortorlowerworkerfluctuation,
and models of directed job search, where higher wages lead to better matches between
43

firms.44
| workers | and |     |     |     |     |     |     |     |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Following Acemoglu and Shimer (1999), we assume that output is uncertain and
depends on the quality of firm worker matches.45 There is only one type of labor. If a
firm offers a higher wage, more workers will apply for the job and the chances of a good
match increase, given the wages offered by other firms. With probability ρ (w ,q) the
i i
additional output produced by filling a vacancy i in a firm located in jurisdiction j equals
Q (K ) , with probability 1− ρ (w ,q) it is equal to zero. The wages paid by other firms
| i i |     |     |     |     | i   | i   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
as well as other factors which may be relevant for the likelihood of success are summarized
by the vector q. The function ρ (w ,q) has the following properties:46
|     |     |     |     |     | i   | i   |     |       |     |     |     |      |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ---- |
|     |     |     |     |     | ∂ρ  | ∂2ρ |     | ∂2ρ   |     |     |     |      |
|     |     |     |     |     | i   |     | i   |       | i   |     |     |      |
|     |     |     |     |     | >   | 0,  | <   | 0,    | =   | 0.  |     | (24) |
|     |     |     |     |     | ∂w  | ∂w  | 2   | ∂wk∂q |     |     |     |      |
|     |     |     |     |     | i   |     | i   |       |     |     |     |      |
i
| Expected | profits |     | are now | given   | by  |       |     |      |         |     |       |      |
| -------- | ------- | --- | ------- | ------- | --- | ----- | --- | ---- | ------- | --- | ----- | ---- |
|          |         | Pe  | = ρ     | (w ,q)Q | (K  | )(1−τ | )−w | (1−τ | )−(1−ατ |     | )rK . | (25) |
|          |         |     |         | i i     | i   | i     | j   | i    | j       |     | j i   |      |
i
The first order conditions for the optimal wage and optimal investment are given by
∂ρ
i
|     |     |     |     |     | Q    | (K )(1−τ |     | )−(1−τ | )   | = 0 |     | (26) |
| --- | --- | --- | --- | --- | ---- | -------- | --- | ------ | --- | --- | --- | ---- |
|     |     |     |     |     | ∂w i | i        | j   |        | j   |     |     |      |
i
and
|     |     |     |     | ρ (w | ,q)Q(cid:48)(K | )(1−τ |     | )−(1−ατ |     | )r = 0. |     | (27) |
| --- | --- | --- | --- | ---- | -------------- | ----- | --- | ------- | --- | ------- | --- | ---- |
|     |     |     |     | i    | i              | i i   |     | j       |     | j       |     |      |
Equations (26) and (27) imply that we can write the equilibrium wage rate as a
w∗ w∗(τ
function = ,φ,α,r). Standard comparative static analysis leads to
|     | i   | i   | i   |     |       |     |          |               |        |          |     |      |
| --- | --- | --- | --- | --- | ----- | --- | -------- | ------------- | ------ | -------- | --- | ---- |
|     |     |     |     | ∂w∗ |       |     | (cid:20) |               |        | (cid:21) |     |      |
|     |     |     |     |     |       | −r  | ∂ρ       |               |        |          |     |      |
|     |     |     |     | i = |       |     |          | i Q(cid:48)(K | )(1−α) | ≤        | 0   | (28) |
|     |     |     |     |     |       |     |          | i             | i      |          |     |      |
|     |     |     |     | ∂τ  | ∆(1−τ | )2  | ∂w       |               |        |          |     |      |
|     |     |     |     | j   |       | j   |          | i             |        |          |     |      |
44 The key difference to the fair wage model discussed in the preceding section is that the latter
emphasizes the direct link between the profits of a firm and the wage that is perceived to be fair. No
such direct link exists here. However, fair wage models may also be considered as models where wages
affect labor productivity because wages deemed as unfair would reduce worker effort or increase costly
fluctuation.
45 The results would be similar in an efficiency wage model following Solow (1979) with continuous
effort. Inshirkingmodelswithdiscreteeffort(suchasShapiroandStiglitz,1984), wewouldnotexpecta
directeffectonwages(forgivenemployment)butonlyanindirecteffectthroughchangesinunemployment
| rates and | hence | the | shirking | constraint. |     |     |     |     |     |     |     |     |
| --------- | ----- | --- | -------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
46 The assumption that all cross derivatives are equal to zero is made to simplify the exposition, it is
| not necessary |     | for the | results. |     |     |     |     |     |     |     |     |     |
| ------------- | --- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
44

where
|     |     |     |     |                           |     | ∂2ρ |     |       | (cid:20) ∂ρ | (cid:21)2 |      |     |     |
| --- | --- | --- | --- | ------------------------- | --- | --- | --- | ----- | ----------- | --------- | ---- | --- | --- |
|     |     |     |     |                           |     |     | i   |       | i           |           |      |     |     |
|     |     | ∆   | = ρ | (w ,q)Q(cid:48)(cid:48)(K |     | )   | Q   | (K )− | Q(cid:48)(K | )         | > 0. |     |     |
|     |     |     | i   | i                         | i   | i   | i   | i     |             | i i       |      |     |     |
|     |     |     |     |                           |     | ∂w  | 2   |       | ∂w          |           |      |     |     |
|     |     |     |     |                           |     |     | i   |       | i           |           |      |     |     |
Notethat∆ > 0followsfromthesecondorderconditionsforprofitmaximization. A
higher corporate tax rate thus reduces the wage if there is limited deductibility of capital
| costs. | This | may be | summarized |     | as  |     |     |     |     |     |     |     |     |
| ------ | ---- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Result 6: Models where wages affect productivity: If capital costs are less than fully
deductible, an increase in the local corporate tax rate reduces wages.
The optimal wage trades off higher output against the cost of higher wages. The
increase in output achieved through a wage increase is higher, the higher the capital stock
of the firm. In the presence of imperfect deductibility of capital costs, investment declines
when the tax rate increases. Therefore the firm’s marginal productivity gain from a wage
increase falls. As a result, it is optimal for the firm to adjust its wage policy towards
| lower | wages         | and a | lower | quality | of  | worker | firm | matches. |     |     |     |     |     |
| ----- | ------------- | ----- | ----- | ------- | --- | ------ | ---- | -------- | --- | --- | --- | --- | --- |
| A.5   | Monopsonistic |       |       | labor   |     | market |      |          |     |     |     |     |     |
Consider a firm facing the labor supply function by Ls = Ls(w), Ls(cid:48)(w) > 0. Output is
produced using a standard, strictly concave production technology F(K ,L ) with com-
i i
∂2F(Ki,Ls(wi))
plementarity between labor and capital: > 0 . Profits are given by
∂Ki∂Li
|           | PM(K  | ,w         | ) = F(K | ,Ls(w          |        | ))(1−τ       | )−w             | Ls(w | )(1−τ | )−(1−ατ |     | )rK   |      |
| --------- | ----- | ---------- | ------- | -------------- | ------ | ------------ | --------------- | ---- | ----- | ------- | --- | ----- | ---- |
|           | i     | i          | i       | i              |        | i            | j               | i    | i     | j       |     | i i   |      |
| The first | order | conditions |         | for            | profit | maximization |                 | are  |       |         |     |       |      |
|           |       | ∂F(K ,Ls(w |         | ))             |        |              |                 |      |       |         |     |       |      |
|           |       | i          |         | i Ls(cid:48)(w |        |              | )−(Ls(cid:48)(w |      | +Ls(w |         |     |       |      |
|           |       |            |         |                | )(1−τ  |              |                 |      | )w    | ))(1−τ  |     | ) = 0 | (29) |
|           |       | ∂L         |         |                | i      |              | j               | i    | i     | i       |     | j     |      |
i
|     |     |     |     |     |     | ∂F(K | ,Ls(w | ))  |      |         |     |        |      |
| --- | --- | --- | --- | --- | --- | ---- | ----- | --- | ---- | ------- | --- | ------ | ---- |
|     |     |     |     |     |     |      | i     | i   |      |         |     |        |      |
|     |     |     |     |     |     |      |       |     | (1−τ | )−(1−ατ |     | )r = 0 | (30) |
|     |     |     |     |     |     |      |       |     | j    |         | j   |        |      |
∂K
i
Equations (29) and (30) implicitly define the profit-maximizing wage rate w∗ and
i
the capital stock set by the monopsonist, as functions of the tax corporate rate. Standard
| comparative |     | static | analysis | leads | to               |     |       |              |        |          |     |     |     |
| ----------- | --- | ------ | -------- | ----- | ---------------- | --- | ----- | ------------ | ------ | -------- | --- | --- | --- |
|             |     |        | ∂w∗      |       | 1 (cid:20) ∂2F(K |     | ,Ls(w | ))           |        | (cid:21) |     |     |     |
|             |     |        |          |       |                  |     | i     | i            |        |          |     |     |     |
|             |     |        | i        | = −   |                  |     |       | Ls(cid:48)(w | )(1−α) | <        | 0.  |     |     |
i
|       |            |       | ∂τ     |            | Γ          | ∂K    | ∂L  |          |        |      |           |     |     |
| ----- | ---------- | ----- | ------ | ---------- | ---------- | ----- | --- | -------- | ------ | ---- | --------- | --- | --- |
|       |            |       | j      |            |            |       | i i |          |        |      |           |     |     |
| where | the second | order |        | conditions |            | imply |     |          |        |      |           |     |     |
|       |            |       |        |            |            |       |     | (cid:20) |        |      | (cid:21)2 |     |     |
|       |            |       | ∂2PM(K |            | ,w )∂2PM(K |       | ,w  | )        | ∂2PM(K | ,w ) |           |     |     |
|       |            |       | i      | i          | i          | i     | i   | i        | i      | i i  |           |     |     |
|       |            | Γ =   |        |            |            |       |     | −        |        |      | >         | 0.  |     |
|       |            |       |        | ∂K2        |            | ∂w2   |     |          | ∂K     | ∂w   |           |     |     |
|       |            |       |        | i          |            |       | i   |          |        | i i  |           |     |     |
45

|     | This | implies |     |     |     |     |     |     |     |     |
| --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
Result 7: Monopsonistic labor market: If capital costs are less than fully deductible, an
| increase |     | in the | local corporate |     | tax | rate reduces | wages. |     |     |     |
| -------- | --- | ------ | --------------- | --- | --- | ------------ | ------ | --- | --- | --- |
A higher corporate tax rate reduces investment so that the marginal productivity
of labor falls. As a result, firms employ less labor. In a monopsonistic labor market this
| implies | a          | lower | wage.47 |     |     |     |     |     |     |     |
| ------- | ---------- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- |
| A.6     | Extensions |       |         |     |     |     |     |     |     |     |
In this subsection, we consider two extensions of the model that are both related to
particular aspects of corporate taxation. The first extension takes into account that firms
may operate in more than one jurisdiction. Many countries use formula apportionment
to allocate corporate profits to different jurisdictions for taxation purposes. The second
extension is to allow for tax avoidance through different types of income shifting.
A.6.1 Firms operating in multiple jurisdictions with formula apportionment
Consider a company with plants in two jurisdictions, 1 and 2. As a first step, we assume
that there is just one type of labor.48 Employment (capital) in jurisdiction j is denoted
by L (K ),j = 1,2. The wage rate is the same in both plants. After-tax profits of the
|         | j   | j     |     |      |          |        |      |            |         |     |
| ------- | --- | ----- | --- | ---- | -------- | ------ | ---- | ---------- | ------- | --- |
| company |     | are   |     |      |          |        |      |            |         |     |
|         | PFA | = F(K | ,K  | L    | ,L )(1−τ | )−(1−τ | )w[L | +L ]−(1−ατ | )r[K +K | ]   |
|         | i   |       | 1   | 2, 1 | 2        | i      | i 1  | 2          | i 1     | 2   |
Assume that the tax apportionment formula is based on payroll as the only appor-
tionment factor.49 Given that there is a uniform wage rate in the two plants, the profit
| tax | rate | is given | by  |     |     |       |         |     |     |      |
| --- | ---- | -------- | --- | --- | --- | ----- | ------- | --- | --- | ---- |
|     |      |          |     |     |     | τ L   | +τ L    |     |     |      |
|     |      |          |     |     |     | τ = 1 | 1 2 2 . |     |     | (31) |
i
|     |     |     |     |     |     | L   | +L  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1 2
The effect of a tax rate change in one jurisdiction on the firm’s effective profit tax
| rate | τ, given | the | level | of employment, |     | is   |       |     |     |     |
| ---- | -------- | --- | ----- | -------------- | --- | ---- | ----- | --- | --- | --- |
|      |          |     |       |                |     | ∂τ L |       |     |     |     |
|      |          |     |       |                |     | i j  |       |     |     |     |
|      |          |     |       |                |     | =    | , j = | 1,2 |     |     |
|      |          |     |       |                | ∂τ  | L +L |       |     |     |     |
|      |          |     |       |                |     | j 1  | 2     |     |     |     |
47 This result holds in models of monopsonistic wage setting with constant labor supply elasticities. If
this assumption is relaxed, the result on tax shifting is theoretically ambiguous.
48
|     | The case | for | two skill | types | is discussed | below. |     |     |     |     |
| --- | -------- | --- | --------- | ----- | ------------ | ------ | --- | --- | --- | --- |
49 This is the case for the LBT in Germany. In the US, apportionment for state taxes is based on
| payroll, | sales, | and | assets, | see Su´arez | Serrato | and Zidar | (2016). |     |     |     |
| -------- | ------ | --- | ------- | ----------- | ------- | --------- | ------- | --- | --- | --- |
46

| where | τ   | is the | tax rate | of  | jurisdiction |     | j.  |     |     |     |     |
| ----- | --- | ------ | -------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
j
Assume that wages are set via collective bargaining which takes place at the firm-
level, not at the plant-level, and that wages paid to workers of a given skill group are the
same in the two plants. The objective function of the skill type k union is now given by
|     |     |         |     | ZFA |            |       |         |          | )sFA. |     |     |
| --- | --- | ------- | --- | --- | ---------- | ----- | ------- | -------- | ----- | --- | --- |
|     |     |         |     |     | =          | (L +L | )(w−w)  | =        | (L +L |     |     |
|     |     |         |     |     |            | 1     | 2       |          | 1 2   |     |     |
|     | The | outcome | of  | the | bargaining |       | process | is given | by    |     |     |
|     |     |         |     |     | sFA∗,L∗,L∗ |       |         |          | ΩFA   |     |     |
|     |     |         |     |     |            |       | =       | arg max  |       |     |     |
|     |     |         |     |     |            |       | 1 2     |          |       |     |     |
sFA,L1,L2
where
|     |     |     |     |     | ΩFA | =   | λlnZFA | +(1−λ)lnPFA. |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------------ | --- | --- | --- |
|     |     |     |     |     |     |     | i      |              | i   |     |     |
The variable λ ∈ (0,1) stands for the relative bargaining power of the union. The
| first | order | condition |     | for the | wage | rate | yields |     |     |     |     |
| ----- | ----- | --------- | --- | ------- | ---- | ---- | ------ | --- | --- | --- | --- |
ΠFA
|     |     |     |     |     |     | sFA∗ | = λ | i        |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | -------- | --- | --- | --- |
|     |     |     |     |     |     |      | [(L | +L )(1−τ | )]  |     |     |
|     |     |     |     |     |     |      | 1   | 2        | i   |     |     |
where
|     | ΠFA | = F(K | ,K  | L   | ,L )(1−τ |     | )−(1−τ | )w[L | +L ]−(1−ατ | )r[K +K | ].  |
| --- | --- | ----- | --- | --- | -------- | --- | ------ | ---- | ---------- | ------- | --- |
|     |     | i     | 1   | 2,  | 1 2      |     | i      | i    | 1 2        | i 1     | 2   |
For given levels of employment, the change in the wage premium caused by a change
| in  | the tax | rate     | is given | by  |       |      |          |        |      |     |     |
| --- | ------- | -------- | -------- | --- | ----- | ---- | -------- | ------ | ---- | --- | --- |
|     |         |          |          |     | ∂sFA∗ |      | (1−α)r(K | +K     | )L   |     |     |
|     |         |          |          |     |       |      |          | 1      | 2 j  |     |     |
|     |         |          |          |     |       | = −λ |          |        | ≤ 0. |     |     |
|     |         |          |          |     | ∂τ    |      | (L +L    | )2(1−τ | )2   |     |     |
|     |         |          |          |     | j     |      | 1        | 2      | j    |     |     |
|     | This    | implies: |          |     |       |      |          |        |      |     |     |
Result 8: Formula apportionment and firm-level bargaining: In firms with plants in
many jurisdictions and homogeneous labor, where corporate taxation is based on formula
apportionment, wages are set via collective bargaining at the firm-level, and capital costs
are less than fully deductible, an increase in the corporate tax rate in one jurisdiction
decreases wages in the entire firm. If employment in the jurisdiction that changes the tax
rate is small, relative to employment in the firm as a whole, the tax effect is also small.
Consider next the case of two skill types, k = h,l. After-tax profits of the company
are now
47

|      |         |           |                  |     |        |     | (cid:16) |                   | (cid:17)  |         |         |     |
| ---- | ------- | --------- | ---------------- | --- | ------ | --- | -------- | ----------------- | --------- | ------- | ------- | --- |
| PFA  |         |           | Lh,Ll,Lh,Ll)(1−τ |     |        |     |          | (cid:80) (cid:80) |           |         |         |     |
|      | k = F(K | ,K        |                  |     |        |     | )−       |                   | wkLk (1−τ | )−(1−ατ | )r[K +K | ]   |
| i    |         | 1         | 2,               | 1 1 | 2 2    |     | i        | j k               | j         | i       | i 1     | 2   |
| with | obvious | notation. |                  | The | profit | tax | rate is  | given             | by        |         |         |     |
(cid:80) (cid:80)
τ wkLk
|     |     |     |     |     |     |     | j        | k j           | j   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------- | --- | --- | --- | --- |
|     |     |     |     |     |     | τ = |          |               | .   |     |     |     |
|     |     |     |     |     |     | i   | (cid:80) | (cid:80) wkLk |     |     |     |     |
|     |     |     |     |     |     |     | j        | k             | j   |     |     |     |
For given employment, the effect of a tax rate change in one jurisdiction on the firm’s
| effective | profit |     | tax rate | τ is |     |     |     |     |     |     |     |     |
| --------- | ------ | --- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
i
|     |     |     |     |     |     |     | (cid:80) | wkLk |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---- | --- | --- | --- | --- |
∂τ
|     |     |     |     |     |     | i   | =        | k j      | .   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | (cid:80) | (cid:80) |     |     |     |     |
|     |     |     |     |     |     | ∂τ  |          | wkLk     |     |     |     |     |
|     |     |     |     |     |     | j   |          |          | j   |     |     |     |
|     |     |     |     |     |     |     |          | j k      |     |     |     |     |
The effect of a wage change for workers of skill type h on the effective profit tax rate
is:
|     |     |     |     |     |     |         | (cid:20) | Lh Lh(cid:21) |        |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | -------- | ------------- | ------ | --- | --- | --- |
|     |     |     |     |     | ∂τ  |         |          |               |        | 1   |     |     |
|     |     |     |     |     | i   | = [τ −τ | ]        | 1 −           | 2 LlLl |     |     |     |
|     |     |     |     |     |     | 1       | 2        |               |        |     |     |     |
|     |     |     |     |     | ∂wh |         |          | Ll Ll         | 1 2σ   |     |     |     |
|     |     |     |     |     |     |         |          | 1             | 2      |     |     |     |
where
|     |     |     |     | (cid:20) |     |     |     | (cid:21)2 |     |     |     |     |
| --- | --- | --- | --- | -------- | --- | --- | --- | --------- | --- | --- | --- | --- |
whLh +wlLl
|     |     |     |     | σ = | 1+   | 1     |     | 1 [whLh | +wlLl]2 | > 0. |     |     |
| --- | --- | --- | --- | --- | ---- | ----- | --- | ------- | ------- | ---- | --- | --- |
|     |     |     |     |     | whLh | +wlLl |     |         | 2       | 2    |     |     |
|     |     |     |     |     |      | 2     |     | 2       |         |      |     |     |
Assume, for instance, that municipality 1 has a higher tax rate than municipality
2. The effect of an increase in the wage of the high skilled wh on the tax burden will
depend on whether this increases the payroll share of the high tax municipality, or that
of the low tax municipality. If the share of high skilled is higher in jurisdiction 1, so that
| (cid:104) | (cid:105) |     |     |     |     |     |     |     |     |     |     |     |
| --------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Lh Lh
1 − 2 > 0, the tax rate τ will increase, and vice versa. The effect of a wage change
| Ll  | Ll  |     |     |     | i   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 1 2 |     |     |     |     |     |     |     |     |     |     |     |
on the profit tax rate a firm effectively pays is therefore generally ambiguous.
Once again assuming firm-level collective bargaining and homogeneous wages for a
skill group across plants, the objective function of the skill type k union is now given by
|     |     |         |     | ZFAk           | (Lk           | +Lk)(wk |     | −wk)     | (Lk +Lk)sFAk. |     |     |     |
| --- | --- | ------- | --- | -------------- | ------------- | ------- | --- | -------- | ------------- | --- | --- | --- |
|     |     |         |     |                | =             |         |     | =        |               |     |     |     |
|     |     |         |     |                |               | 1 2     | 1   |          | 1             | 2   |     |     |
|     | The | outcome | of  | the bargaining |               | process |     | is given | by            |     |     |     |
|     |     |         |     |                | sFAk∗,Lk∗,Lk∗ |         | =   | arg max  | ΩFAk          |     |     |     |
|     |     |         |     |                |               | 1       | 2   |          |               |     |     |     |
sk,Lk,Lk
1 2
48

where
|     |     | ΩFAk λklnZFAk | +(1−λk)lnPFAt. |     |     |     |
| --- | --- | ------------- | -------------- | --- | --- | --- |
=
|     |     |     | i   | i   |     |     |
| --- | --- | --- | --- | --- | --- | --- |
λk
As above, the variable ∈ (0,1) stands for relative bargaining power of the skill
| type k union. | The first order | condition | for the wage | rate yields |     |     |
| ------------- | --------------- | --------- | ------------ | ----------- | --- | --- |
|               |                 | λk        | PFAt         |             |     |     |
sFAk∗
|     | =   |            |          | , k | = h,l | (32) |
| --- | --- | ---------- | -------- | --- | ----- | ---- |
|     |     | (1−λk)[(Lk | +Lk)(1−τ |     |       |      |
)−Φk]
|     |     |     | 1 2 | i w |     |     |
| --- | --- | --- | --- | --- | --- | --- |
where
|     |     |     | ∂PFA ∂τ  |     |     |     |
| --- | --- | --- | -------- | --- | --- | --- |
|     |     |     | Φk i     | i   |     |     |
|     |     |     | =        | .   |     |     |
|     |     |     | w ∂τ ∂wk |     |     |     |
i
Thekeydifferencebetweenthiscaseandthatwithhomogeneouslaboristhatawage
change now affects the effective tax rate. It thus influences the outcome of union-firm
bargaining. For instance, if a higher wage increases the effective tax rate, which implies
Φ < 0, the wage premium achieved by the union will be smaller, other things equal, and
wk
vice versa. Equation (32) implicitly defines the two firm-specific wage premiums emerging
from the bargaining process as functions of the type sFAk∗ = sFAk∗(τ ,τ ,T,Lk∗,Lk∗...).
|     |     |     |     |     | i j i | j   |
| --- | --- | --- | --- | --- | ----- | --- |
Differentiating (32) shows that the change in the local corporate tax rate on wages is, in
| general, ambiguous. |          |     |     |     |     |     |
| ------------------- | -------- | --- | --- | --- | --- | --- |
| A.6.2 Income        | shifting |     |     |     |     |     |
Income shifting to avoid taxes may occur in different forms. Multinational firms can use
debt financing or transfer pricing to shift profits across national borders. Income shifting
may also occur between different tax bases within a country. For instance, firm owners
may shift income between the corporate and the personal income tax base by changing
wages paid to family members. We discuss the two cases in turn.
International income shifting. Assume that the firm’s profits are given by
(cid:80)
PS = p F (K ,Lh,Ll)(1−τ )− wkLk(1−τ )−(1−α τ )r K +θ S −c(S ). (33)
| ij i | i i i i | j   | i i j | j j i | i ij i | i   |
| ---- | ------- | --- | ----- | ----- | ------ | --- |
k
The variable S is income shifted from the profit tax base to the personal income tax base
i
of the firm owners, which may be positive or negative, θ is the tax benefit per unit of
ij
income shifted and c(S ) is a convex shifting cost function.50 Profit maximization factor
i
50 Here we assume that profit shifting is carried out by changing the wages of firm owners working in
the firm or family members of the firm owner. This implies that s would be reported as wage income.
i
Another way of shifting income is to provide capital in the form of debt, rather than equity. Many
countries have introduced anti-tax-avoidance legislation, which limits income shifting. We therefore take
49

input decisions lead to the usual marginal productivity conditions, and optimal income
shifting implies c(cid:48)(S ) = θ so that the profit-maximizing amount of shifted income S∗
|     |     |     | i   | ij  |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
i
can be expressed as a function of the tax benefit S∗ = S∗(θ ), with S∗(cid:48) > 0. Consider
|     |     |     |     |     |     |     |     |     | i i | ij  | i   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
first the case of a multinational company which is able to shift income abroad. If the firm
can do so, for instance, through a foreign subsidiary charging a fully deductible cost to
the domestic parent company, the tax advantage from income shifting is given by θ =
ij
τ −τ , where τ is the foreign profit tax rate. Assume that wages in the multinational
| j f |     | f   |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
firm are determined by firm-level bargaining. In this case, the wage premium generated
| by union | firm | bargaining |     | is given | by  |     |     |     |     |     |     |     |
| -------- | ---- | ---------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
(1−βj)βk
ΠS
|     |     |     | zk∗ |                | i   | i   | i   |     |        |     |             |      |
| --- | --- | --- | --- | -------------- | --- | --- | --- | --- | ------ | --- | ----------- | ---- |
|     |     |     | =   |                |     |     |     | k,j | = h,l, | k   | (cid:54)= j | (34) |
|     |     |     | i   | (1−βkβj)Lk(1−τ |     |     | )   |     |        |     |             |      |
|     |     |     |     |                |     | i   | i   |     |        |     |             |      |
i i
where
(cid:80)
ΠS = F(K ,Lh,Ll)(1−τ )− wkLk(1−τ )−(1−ατ )rK +(τ −τ )S −c(S ).
| i               |     | i i | i    | i      |     | k   | i    | i    |      | i i | j f i | i   |
| --------------- | --- | --- | ---- | ------ | --- | --- | ---- | ---- | ---- | --- | ----- | --- |
| Differentiating |     |     | (34) | yields |     |     |      |      |      |     |       |     |
|                 |     |     |      |        |     |     | dzk∗ |      |      | dLk |       |     |
|                 |     |     |      |        |     |     |      | i Lk | +zk∗ | i   |       |     |
=
|     |     |     |             |     |     |     |      | dτ    | i i | dτ      |     |      |
| --- | --- | --- | ----------- | --- | --- | --- | ---- | ----- | --- | ------- | --- | ---- |
|     |     |     |             |     |     |     |      | i     |     | i       |     |      |
|     |     |     | −βS[(1−α)rK |     |     | −(S | (1−τ | )−c(S |     | ))] ≤ 0 |     | (35) |
|     |     |     |             | 0   |     | i   | i    | f     |     | i       |     |      |
where
(1−βj)βk
|     |     | βS  |     |              |     | i i |     |     |        |     |              |     |
| --- | --- | --- | --- | ------------ | --- | --- | --- | --- | ------ | --- | ------------ | --- |
|     |     |     | =   |              |     |     | > 0 | k,j | = h,l, | k   | (cid:54)= j. |     |
|     |     |     | 0   | (1−βkβj)(1−τ |     |     | )2  |     |        |     |              |     |
i
|     |     |     |     |     | i i |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The right-hand side of (35) is increasing in S (given that S = S∗), which implies
|     |     |     |     |     |     |     |     | i   |     |     | i i |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
that the decline in the rent accruing to labor is smaller, the higher the equilibrium level
| of income | shifting. |     | This | yields |     |     |     |     |     |     |     |     |
| --------- | --------- | --- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
Result 9 International income shifting: If firms engage in international income
shifting and wages are set by firm-level bargaining, the decline in the rent accruing to
laborcausedbyahighercorporatetaxdecreasesastheequilibriumlevelofincomeshifting
increases.
National income shifting. Wenowconsiderthepossibilityofdomesticincomeshifting
between the profit tax base and wage income. In this case the tax advantage from income
shifting is given by θ = φ τ −t , where t is the marginal tax rate on wage income of
|     |     |     | ij  | j j | pi  |     | pi  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
into account costs of income shifting. This can be interpreted as the cost of hiring tax consultants or the
cost of concealing income shifting. For notational simplicity we assume that shifting costs are not tax
deductible.
50

the relevant employee. This is relevant in settings where the wages of some employees are
effectively profit distributions, so that wage bargaining plays no role for them. Assume
that the wages paid in the absence of incentives for income shifting, that is for equal
taxes on profits and labor income, would be given by the function wkS(τ ,...). Then the
i j
observed change in the wages paid out by the firm would equal (cid:80) dw i kS Lk + dSi. While
k dτj i dτj
’true’ wages are likely to decline in response to higher taxes, albeit by less than they
would in the absence of income-shifting possibilities, we now have the additional effect
that the income-shifting effect dSi > 0 increases reported wages. Thus if income shifting
dτj
is important, we would expect observed wages to decline less, or even increase, in response
to higher corporate taxes. This may be summarized as
Result 10 National income shifting: If firms shift income between the profit tax
base and the labor income tax base, a higher corporate tax rate will lead to a smaller
declineinreportedwagesthanintheabsenceofincomeshifting. Wagesmayevenincrease.
Unfortunately, we cannot test this mechanism directly with our data because we do
not know whether there are employees who are members of the owner family.
51

B Institutional background
B.1 German business taxes
In 2007, profit taxes accounted for about 6.2% of total tax revenue (including social se-
curity) in Germany (OECD, 2015).51 In terms of tax revenues, the LBT is the most
important profit tax, accounting for about 60–70% of total profit tax revenues from cor-
porate firms. Overall, the share of profit tax revenues from local taxes is relatively high
in Germany compared with other countries. In the US, for instance, state and local
corporate taxes together account only for about 20% of total corporate taxes (NCSL,
2009). In addition, the LBT is the most important source of financing at the disposal of
municipalities, generating roughly three quarters of municipal tax revenue.
AsmentionedinSection2,therearetwootherprofittaxesinGermany,thecorporate
income tax (CIT), which applies to corporations, and the personal income tax (PIT),
which applies to non-corporate firms. We discuss the most important features of these
two taxes in turn.
Corporate income tax. The rate of the nationwide corporate income tax, τ , has
CIT
undergone several changes in recent years. Until 2000, a split rate imputation system
existed in Germany, where retained profits were subject to a tax rate of 45% in 1998 and
40% in 1999 and 2000. Distributed profits were taxed at a rate of 30% from 1998 to 2000.
As of 2001, retained and distributed profits were taxed equally at 25% (26.5% in 2003).
In 2008, τ was lowered to 15%. In all years, a so-called solidarity surcharge (to finance
CIT
the costs of reunification), soli, of 5.5% of the corporate tax rate was added.
There are two steps to calculating the total statutory tax rate for corporate firms.
First, LBT and CT rates are added. Second, the deduction of the LBT payments from
the tax base has to be taken into account. The statutory tax rate for corporate firms,
τcorp, from 1998 to 2007, is τcorp = τCIT·(1+soli)+tf L e B d T ·θ L m B u T n . Since 2008, the denominator of
1+tfed ·θmun
LBT LBT
the equation is equal to 1, as the LBT can no longer be deducted from the tax base.
Personal income tax. Non-corporate firms (Personengesellschaften) are subject to
the progressive personal income tax (on operating profits assigned to the proprietor).
Non-corporate firms have an LBT allowance of 24,500 euros and a reduced tfed for small
LBT
non-corporate firms prior to 2008: for every 12,000 euros exceeding the allowance of
51 This is below the OECD average of about 10.6% (US: 10.8%, UK: 9.4%). Part of this relatively low
share of profit taxes is due to the rather high share of social insurance contributions (SIC) in Germany.
If SIC are excluded, the share in total taxes is about 11.5%. A high share of unincorporated firms in
Germany is a second factor. These firms pay PIT, in addition to the LBT, and the OECD does not
classify PIT as profit taxes.
52

24,500 euros, tfed was raised by one percentage point so that the full basic federal rate
LBT
of 5.0% had to be paid only for taxable income exceeding 72,500 euros. The tax rate for
a non-corporate firms τnon−corp from 1998 to 2007, is τnon−corp = τPIT·(1+soli)+tf L e B d T ·θ L m B u T n .
1+tfed ×1.8
LBT
The denominator of the equation shows that a fixed share of the LBT liabilities can be
deducted from the personal income tax base. This share amounted to tfed ·1.8·Y from
LBT
2001 to 2007 and tfed ·3.8·Y from 2008 onwards.
LBT
B.2 German labor market institutions
Traditionally, German labor unions have been very influential.52 Collective bargaining
agreements (CBAs) at the sector-level are the most important mechanism for wage de-
termination. Nevertheless, there has been a significant decline in bargaining coverage. In
West (East) Germany, CBA coverage decreased from 76% (63%) in 1998 to 65% (51%) in
2009. The share of workers covered by sectoral agreements fell from 68% (52%) to 56%
(38%) (Ellguth, Gerner and Stegmaier, 2012).53 In addition to sector-level CBA, some
firms have firm-level agreements, while other firms are not covered by a CBA and rely on
individual contracts with each employee.
The average duration of a CBA increased from 12 months in 1991 to 22 months in
2011. Usually, negotiations take place in the first half of a year. Firms may pay wages
above those negotiated in CBAs. Except for a few industries, there was no legal minimum
wage in Germany during our period of analysis. However, the social security and welfare
system provides an implicit minimum wage and CBAs ensure that wages are above that
level.
52 SeeDustmannetal.(2014)foranoverviewandanalysisofthedevelopmentofGermanlabormarket
institutions during our period of investigation.
53 Coverageratesvarybyindustry: collectivebargainingisslightlyaboveaverageinthemanufacturing
sector,whilethehighestcoverageisinthepublicsectorandthelowestinICT,agricultureandrestaurant
industries. Overall,unioncoverageratesinGermanyarelowerthaninotherEuropeancountries–except
the UK and some Eastern European countries – but higher than in the US (Du Caju et al., 2008).
53

C Descriptive Statistics
Jurisdictional changes Analogously to Figure 1, Figure C.1 shows the cross-sectional
andtime variationin LBTratesfor the fullsampleof municipalities, includingmunicipali-
tiesthatunderwentajurisdictionalchange. Therightpanelclearlyshowsthatthenumber
of tax changes for these merged municipalities is relatively high. However, the variation in
tax rates is artificial and related to the way we impute tax rates. As described in Section
2.2, the wage data contains geographical information for the jurisdictional boundaries
as of December 31, 2010. In order to match the tax data, we have to bring it to the
same boundaries. This generates artificial variation in tax rates, as we need to calculate
population weighted average tax rates for those merged jurisdictions.
Consequently, we find a large number of (small) tax changes for East German mu-
nicipalities. Table C.3 shows that on average 12.4% of the municipalities change their
tax rate per year. Among the merged municipalities, however, the share is 33% (with
a much smaller average change). Given this measurement error in tax rate changes, we
focus on non-merged municipalities in our baseline analysis (and check whether results
for merged and non-merged municipalities differ). Due to this restriction, we are left with
about 10,000 municipalities and 18,000 tax changes for identification (instead of 11,441
municipalities with about 27,000 partly artificial tax changes).
54

Figure C.1: Cross-sectional and time variation in local tax rates
Source: StatisticalOfficesoftheLaender. Maps: GeoBasis-DE/BKG2015. Notes: Thisfigureshowsthe
cross-sectional and time variation in municipal scaling factors of the German LBT. This figure includes
both non-merged and merged municipalities. The left graph depicts the cross-sectional variation in LBT
rates (in %) induced by different scaling factors for 2003 (the mid-year of our sample). The right graph
indicates the number of scaling factor changes per municipality between 1993 and 2012. Jurisdictional
boundaries are as of December 31, 2010.
55

|     | Table   | C.1: Municipal |      | scaling factors, | 1993-2012 |
| --- | ------- | -------------- | ---- | ---------------- | --------- |
|     |         | mean           | min  | p5 p50           | p95 max   |
|     | 1993    | 3.12           | 2.00 | 2.50 3.10        | 3.70 7.37 |
|     | 1994    | 3.15           | 2.00 | 2.59 3.13        | 3.72 5.15 |
|     | 1995    | 3.17           | 2.00 | 2.60 3.20        | 3.80 5.15 |
|     | 1996    | 3.19           | 2.00 | 2.70 3.20        | 3.80 5.15 |
|     | 1997    | 3.21           | 2.00 | 2.70 3.20        | 3.80 5.15 |
|     | 1998    | 3.22           | 2.00 | 2.74 3.20        | 3.80 9.00 |
|     | 1999    | 3.23           | 2.00 | 2.75 3.20        | 3.80 9.00 |
|     | 2000    | 3.24           | 2.00 | 2.75 3.20        | 3.80 9.00 |
|     | 2001    | 3.26           | 2.00 | 2.75 3.27        | 3.80 9.00 |
|     | 2002    | 3.27           | 2.00 | 2.80 3.30        | 3.85 9.00 |
|     | 2003    | 3.29           | 2.00 | 2.80 3.30        | 4.00 9.00 |
|     | 2004    | 3.31           | 2.00 | 2.80 3.30        | 4.00 9.00 |
|     | 2005    | 3.33           | 2.00 | 2.85 3.30        | 4.00 9.00 |
|     | 2006    | 3.34           | 2.00 | 2.90 3.30        | 4.00 9.00 |
|     | 2007    | 3.34           | 2.00 | 2.90 3.30        | 4.00 9.00 |
|     | 2008    | 3.35           | 2.00 | 2.90 3.30        | 4.00 9.00 |
|     | 2009    | 3.36           | 2.00 | 2.90 3.35        | 4.00 9.00 |
|     | 2010    | 3.38           | 2.00 | 3.00 3.40        | 4.00 9.00 |
|     | 2011    | 3.44           | 2.00 | 3.00 3.50        | 4.00 9.00 |
|     | 2012    | 3.47           | 2.00 | 3.00 3.50        | 4.03 9.00 |
|     | Average | 3.28           | 2.00 | 2.80 3.30        | 3.95 9.00 |
Source: Statistical Offices of the Laender. Notes: The table provides descrip-
tive statistics on the municipal scaling factors for all non-merged municipalities
| (N=10001) | in Germany | over time. |     |     |     |
| --------- | ---------- | ---------- | --- | --- | --- |
56

Table C.2: Municipal scaling factors changes per municipality, 1993-2012
|         |                | any                | increase       |                  | large increases |       |
| ------- | -------------- | ------------------ | -------------- | ---------------- | --------------- | ----- |
| changes | municipalities |                    | in             | % municipalities |                 | in %  |
|         |                | all municipalities |                | (N=11,441)       |                 |       |
| 0       |                | 2041               | 17.80          |                  | 6969            | 60.90 |
| 1       |                | 3218               | 28.10          |                  | 3583            | 31.30 |
| 2       |                | 3091               | 27.00          |                  | 784             | 6.90  |
| 3       |                | 1667               | 14.60          |                  | 95              | 0.80  |
| 4       |                | 720                |                | 6.30             | 9               | 0.10  |
| 5+      |                | 704                |                | 6.20             | 1               | 0.00  |
|         | all non-merged |                    | municipalities |                  | (N=10,001)      |       |
| 0       |                | 1902               | 19.00          |                  | 6358            | 63.60 |
| 1       |                | 3025               | 30.20          |                  | 3012            | 30.10 |
| 2       |                | 2862               | 28.60          |                  | 566             | 5.70  |
| 3       |                | 1465               | 14.60          |                  | 58              | 0.60  |
| 4       |                | 536                |                | 5.40             | 6               | 0.10  |
| 5+      |                | 211                |                | 2.10             | 1               | 0.00  |
|         | non-merged     | municipalities     |                | in               | LIAB (N=3,522)  |       |
| 0       |                | 672                | 19.08          |                  | 2290            | 65.02 |
| 1       |                | 1018               | 28.90          |                  | 993             | 28.19 |
| 2       |                | 914                | 25.95          |                  | 213             | 6.05  |
| 3       |                | 541                | 15.36          |                  | 22              | 0.62  |
| 4+      |                | 377                | 10.70          |                  | 4               | 0.11  |
|         | all            | merged             | municipalities |                  | (N=1,440)       |       |
| 0       |                | 139                |                | 9.70             | 611             | 42.40 |
| 1       |                | 193                | 13.40          |                  | 571             | 39.70 |
| 2       |                | 229                | 15.90          |                  | 218             | 15.10 |
| 3       |                | 202                | 14.00          |                  | 37              | 2.60  |
| 4       |                | 184                | 12.80          |                  | 3               | 0.20  |
| 5+      |                | 493                | 34.20          |                  | 0               | 0.00  |
Source: StatisticalOfficesoftheLaender. Notes: Thetablesummarizesthenumber
oftaxincreasesandlargetaxincreasesforall,non-mergedandmergedmunicipalities
from 1993 to 2012. Large increases are defined as the top 25% of the tax increase
distribution, that is an increase of the business tax rate of 1.1 percentage points or
more.
57

Table C.3: Time variation in municipal scaling factors, 1993–2012
| municip.     | with a(n)       | ...             |       | ... | change |        |       | ... increase |          | ...        | decrease |
| ------------ | --------------- | --------------- | ----- | --- | ------ | ------ | ----- | ------------ | -------- | ---------- | -------- |
|              |                 |                 | share |     | mean   | change | share | mean         | increase | share mean | decrease |
| all municip. |                 |                 | 12.2  |     | 0.15   |        | 10.3  |              | 0.20     | 1.9        | -0.14    |
| non-merged   | municip.        | (all)           |       | 9.4 | 0.19   |        | 8.8   |              | 0.22     | 0.6        | -0.30    |
| non-merged   | municip.        | (LIAB)          | 10.2  |     | 0.17   |        | 9.4   |              | 0.21     | 0.8        | -0.26    |
| merged       | municip.        |                 | 31.9  |     | 0.07   |        | 20.6  |              | 0.15     | 11.3       | -0.08    |
| by year      | (all non-merged | municipalities) |       |     |        |        |       |              |          |            |          |
| 1994         |                 |                 | 10.9  |     | 0.18   |        | 10.0  |              | 0.23     | 0.9        | -0.45    |
| 1995         |                 |                 | 15.5  |     | 0.19   |        | 14.9  |              | 0.22     | 0.6        | -0.40    |
| 1996         |                 |                 | 11.2  |     | 0.16   |        | 10.7  |              | 0.19     | 0.5        | -0.37    |
| 1997         |                 |                 |       | 8.5 | 0.17   |        | 8.0   |              | 0.21     | 0.5        | -0.41    |
| 1998         |                 |                 |       | 8.7 | 0.18   |        | 8.2   |              | 0.21     | 0.5        | -0.32    |
| 1999         |                 |                 |       | 4.2 | 0.13   |        | 3.6   |              | 0.20     | 0.6        | -0.31    |
| 2000         |                 |                 |       | 8.7 | 0.13   |        | 7.8   |              | 0.17     | 0.8        | -0.23    |
| 2001         |                 |                 | 12.8  |     | 0.14   |        | 11.7  |              | 0.18     | 1.1        | -0.23    |
| 2002         |                 |                 |       | 8.3 | 0.17   |        | 7.8   |              | 0.20     | 0.4        | -0.35    |
| 2003         |                 |                 |       | 9.6 | 0.19   |        | 9.2   |              | 0.21     | 0.4        | -0.28    |
| 2004         |                 |                 |       | 8.4 | 0.19   |        | 8.1   |              | 0.21     | 0.3        | -0.30    |
| 2005         |                 |                 | 11.5  |     | 0.17   |        | 11.0  |              | 0.19     | 0.5        | -0.27    |
| 2006         |                 |                 |       | 8.3 | 0.13   |        | 7.4   |              | 0.18     | 0.9        | -0.28    |
| 2007         |                 |                 |       | 4.0 | 0.10   |        | 3.2   |              | 0.19     | 0.8        | -0.26    |
| 2008         |                 |                 |       | 4.0 | 0.18   |        | 3.2   |              | 0.28     | 0.8        | -0.26    |
| 2009         |                 |                 |       | 4.2 | 0.18   |        | 3.4   |              | 0.27     | 0.8        | -0.20    |
| 2010         |                 |                 |       | 8.8 | 0.27   |        | 8.4   |              | 0.29     | 0.4        | -0.22    |
| 2011         |                 |                 | 18.4  |     | 0.28   |        | 18.1  |              | 0.29     | 0.3        | -0.21    |
| 2012         |                 |                 | 12.8  |     | 0.25   |        | 12.5  |              | 0.27     | 0.3        | -0.30    |
Source: Statistical Offices of the Laender. Notes: The top part of the table sum-
marizes the frequency, signs, and sizes of municipal scaling factor changes for all
municipalities (N=11441), non-merged municipalities (N=10001), and merged mu-
nicipalities (N=1440). The bottom part of the table shows the frequency, sign and
size of municipal scaling factor changes for non-merged municipalities over time.
Table C.4: Percentiles of the share of non-wage-censored workers across firms
|     |         | p1   | p5   | p10  | p25  | p50  | p75 | p90 | p95 p99 | obs      |     |
| --- | ------- | ---- | ---- | ---- | ---- | ---- | --- | --- | ------- | -------- | --- |
|     | manuf.  | 0.38 | 0.68 | 0.78 | 0.89 | 0.96 | 1   | 1   | 1       | 1 23,137 |     |
|     | service | 0.32 | 0.59 | 0.73 | 0.88 | 0.98 | 1   | 1   | 1       | 1 21,490 |     |
|     | total   | 0.36 | 0.63 | 0.75 | 0.89 | 0.97 | 1   | 1   | 1       | 1 44,627 |     |
Source: LIAB.Notes: Thistableshowsthedistributionoftheshareofnon-wage-censoredworkersacross
firms in different sectors. Workers are defined as wage-censored if they earned more than the social
security contributions earnings ceilings at least once in the sample. In this table, manufacturing includes
| construction | and services | include | trade. |     |     |     |     |     |     |     |     |
| ------------ | ------------ | ------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
58

Table C.5: Descriptive statistics, plant sample, non-merged municipalities, 1999-2008
|                         |                   |                | mean p50       | sd      |
| ----------------------- | ----------------- | -------------- | -------------- | ------- |
| Wage                    |                   |                | 2,733 2,717    | 877     |
| Local scaling           | factor            |                | 3.85 3.90      | 0.52    |
| LBT rate                | (in %)            |                | 18.65 19.00    | 3.09    |
| Municipal               | spending          | (in millions)  | 2,648 110      | 6,155   |
| Municipal               | population        |                | 436,255 49,856 | 904,957 |
| District                | unemployment      | rate           | 0.12 0.10      | 0.05    |
| District                | GDP (in millions) |                | 18,977 6,758   | 28,198  |
| Share: West             | German            | municipalities | 0.80 1.00      | 0.40    |
| Number                  | of employees      |                | 265 53         | 1,136   |
| Share: Liable           | plants            |                | 0.64 1.00      | 0.48    |
| Share: Sector           | level             | bargaining     | 0.56 1.00      | 0.50    |
| Share: Firm             | level bargaining  |                | 0.08 0.00      | 0.28    |
| Share: No               | collective        | bargaining     | 0.36 0.00      | 0.48    |
| Share: Manufacturing    |                   |                | 0.26 0.00      | 0.44    |
| Share: Construction     |                   |                | 0.08 0.00      | 0.26    |
| Share: Trade            |                   |                | 0.11 0.00      | 0.32    |
| Share: Services         |                   |                | 0.23 0.00      | 0.42    |
| Share: Public/Utilities |                   |                | 0.32 0.00      | 0.45    |
| Share: High             | profitability     |                | 0.37 0.00      | 0.48    |
| Share: Medium           | profitability     |                | 0.34 0.00      | 0.47    |
| Share: Low              | profitability     |                | 0.29 0.00      | 0.46    |
| Share: Single           | plant             | firms          | 0.62 1.00      | 0.49    |
| Share: German           | owner             |                | 0.94 1.00      | 0.24    |
Source: LIAB and Statistical Offices of the Laender. Notes: Total number of plant-
year observations: 69,249. Number of plants: 21,253. All monetary variables in
2008 euros.
59

Table C.6: Descriptive statistics, worker sample, non-merged municipalities, 1999-2008
|                     |                        | mean p50        | sd      |
| ------------------- | ---------------------- | --------------- | ------- |
| Wage                |                        | 3,491 3,363     | 1,092   |
| Local scaling       | factor                 | 4.00 4.10       | 0.53    |
| LBT rate            | (in %)                 | 19.50 19.50     | 3.85    |
| Municipal           | spending (in millions) | 2,605 334       | 5,667   |
| Municipal           | population             | 470,429 120,136 | 833,344 |
| District            | unemployment rate      | 0.11 0.10       | 0.04    |
| District            | GDP (in millions)      | 22,233 9,211    | 28,541  |
| Share: West         | German municipalities  | 0.88 1.00       | 0.32    |
| Number              | of employees           | 5,802 1,138     | 10,345  |
| Share: Liable       | firms                  | 0.73 1.00       | 0.44    |
| Age                 |                        | 41 42           | 10      |
| Share: Male         |                        | 0.72 1.00       | 0.45    |
| Share: High-skilled |                        | 0.14 0.00       | 0.34    |
| Share: Medium       | skilled                | 0.71 1.00       | 0.45    |
| Share: Blue         | collar                 | 0.53 1.00       | 0.50    |
| Share: Never        | censored individuals   | 0.81 1.00       | 0.39    |
Source: LIABandStatisticalOfficesoftheLaender. Notes: Numberofperson-year
observations: 12,673,576. Number of individuals: 4,091,932. All monetary variables
in 2008 euros.
60

D Additional Results
2
0
-2
-4
-6
segaw
laer
goL
)1-=t
doirep
mrofer-erp
ot
evitaler(
-3 -2 -1 0 1 2 3 4
no restriction 0 drops in sample (base)
0 drops, 1 hike in window 0 drops, 1 hike in sample
Figure D.1: Event study graphs: wage effects by event window cut
Source: LIAB and Statistical Offices of the Laender. Notes: The graph plots event study estimates
(γˆ ,j ∈ [−3,4]) and corresponding 95% confidence bands of different specifications of equation (1). De-
j
pendent variable is the log median firm wage (observed on 30 June for each year). Event dummies are
equaltoonefortaxincreasesgreaterthanorequaltothe75thpercentileofthetaxincreasedistribution.
The tax change occurred for the treatment group on 1 January in event year t = 0, as indicated by the
verticalredline. Allregressionmodelsincludemunicipal, firmand“state×year”fixedeffects. Theesti-
mation sample comprises all establishments liable to the LBT in non-merged municipalities. Depending
on the specification, we additionally restrict the sample to municipalities without a tax decrease during
the observation period, not more than one increase in the event window, and/or only one tax increase in
thewholeobservationperiod(seelegend). Standarderrorsareclusteredatthemunicipallevel. Estimates
are reported in Table D.11.
61

4
2
0
-2
-4
segaw
laer
goL
)1-=t
doirep
mrofer-erp
ot
evitaler(
-3 -2 -1 0 1 2 3 4
All firms Liable Non Liable
Figure D.2: Event study graphs: wage effects by firm liability
Source: LIAB and Statistical Offices of the Laender. Notes: The graph plots event study estimates
(γˆ ,j ∈ [−3,4]) and corresponding 95% confidence bands of different specifications of equation (1).
j
Dependent variable is the log median firm wage (observed on 30 June for each year). Event dummies are
equaltoonefortaxincreasesgreaterthanorequaltothe75thpercentileofthetaxincreasedistribution.
The tax change occurred for the treatment group on 1 January in event year t = 0, as indicated by the
vertical red line. All regression models include municipal, firm and “state × year” fixed effects. The
estimation sample comprises all establishments in non-merged municipalities that did not experienced a
tax decrease during the observation period. Depending on the specification, we additionally restrict the
sample to firms that are liable to or exempt from the LBT (see legend). Standard errors are clustered at
the municipal level. Estimates are reported in Table D.12.
62

2
1.5
1
.5 0
-.5
)tceffe
evitalumuc(
htworg
egaw
laeR
-5 -4 -3 -2 -1 0 1 2 3 4 5
no restriction 0 decreases in sample (base)
Figure D.3: Distributed lag model estimates: wage effects by event window cut
Source: LIAB and Statistical Offices of the Laender. Notes: The graph plots distributed lag model
estimates (βˆ ,j ∈[−4,5]) and corresponding 95% confidence bands of different specifications of equation
j
(2). Dependent variable is the yearly change in the log median firm wage (observed on 30 June for
each year). Main regressors are leads and lags of the yearly change in the net-of-local-business-tax
rate. All regression models include municipal, firm and “state × year” fixed effects. The estimation
sample comprises all establishments liable to the LBT in non-merged municipalities. Depending on the
specification, we additionally restrict the sample to municipalities without a tax decrease during the
observation period, not more than one increase in the event window, and/or only one tax increase in the
whole observation period (see legend). Standard errors are clustered at the municipal level. Estimates
are reported in Table D.14.
63

Panel A: GDP
4
2
0
-2
-4
.c.p
PDG
goL
)1-=t
doirep
mrofer-erp
ot
evitaler(
-3 -2 -1 0 1 2 3 4
Increases Large Inc Decreases
Panel B: Unemployment
8
6
4
2
0
-2
etar
tnemyolpmenu
goL
)1-=t
doirep
mrofer-erp
ot
evitaler(
-3 -2 -1 0 1 2 3 4
Increases Large Inc Decreases
Figure D.4: Event study graphs: local business cycle effects including tax decreases
Source: Statistical Offices of the Laender. Notes: The graph plots event study estimates (γˆ ,j ∈[−3,4])
j
and corresponding 95% confidence bands of different specifications of equation (1). Dependent variables
arelogcountyGDPpercapita(PanelA)andunemploymentrate(PanelB).Eventvariablesaredummies
equaltooneforataxincrease,alargetaxincrease(greaterthanorequaltothe75thpercentileofthetax
increasedistribution),orataxdecrease(seelegend). Thetaxchangeoccurredforthetreatmentgroupon
1Januaryineventyeart=0,asindicatedbytheverticalredline. Allregressionmodelsincludemunicipal
and “state × year” fixed effects. In specifications with tax increase (decrease) dummies, we exclude all
municipalities that experienced a tax decrease (increase) during the observation period. Standard errors
are clustered at the municipal level. Estimates are reported in Tables D.15 and D.16, respectively.
64

Panel A: Revenues
20
10
0
-10
-20
seunever
goL
)1-=t
doirep
mrofer-erp
ot
evitaler(
-3 -2 -1 0 1 2 3 4
Increases Large Inc Decreases
Panel B: Spending
20
10
0
-10
-20
gnidneps
goL
)1-=t
doirep
mrofer-erp
ot
evitaler(
-3 -2 -1 0 1 2 3 4
Increases Large Inc Decreases
Panel C: Fiscal surplus
4
2
0
-2
-4
-6
sulprus
lacsiF
)1-=t
doirep
mrofer-erp
ot
evitaler(
-3 -2 -1 0 1 2 3 4
Increases Large Inc Decreases
Figure D.5: Event study graphs: municipal fiscal budget variables
Source: Statistical Offices of the Laender. Notes: The graph plots event study estimates (γˆ ,j ∈[−3,4])
j
and corresponding 95% confidence bands of different specifications of equation (1). Dependent variables
are log municipal revenues per capita (Panel A), log municipal spending per capita (Panel B), and
municipal fiscal surplus, i.e. revenues – spending, per capita (Panel C). Event variables are dummies
equal to one for a tax increase or a large tax increase (greater than or equal to the 75th percentile of the
tax increase distribution, see legend). The tax change occurred for the treatment group on 1 January
in event year t = 0, as indicated by the vertical red line. All regression models include municipal and
“state × year” fixed effects. We exclude all municipalities that experienced a tax decrease during the
observationperiod. Standarderrorsareclusteredatthemunicipallevel. EstimatesarereportedinTables
D.17, D.18, and D.19 respectively.
65

Table D.1: Differences-in-differences estimates: wage effects at different levels of aggre-
gation
|     |             |            |       | (1)        | (2)     |              | (3) |     |
| --- | ----------- | ---------- | ----- | ---------- | ------- | ------------ | --- | --- |
|     | Aggregation |            | level | worker     | firm    | municipality |     |     |
|     | Log         | net-of-LBT |       | rate 0.374 | 0.388   | 0.416        |     |     |
|     |             |            |       | (0.114)    | (0.127) | (0.252)      |     |     |
|     | N           |            |       | 9,295,488  | 44,654  | 15,433       |     |     |
Source: LIAB and Statistical Offices of the Laender. Notes: This table presents the DiD estimates δˆ
of regression model (3), estimated on different levels of aggregation as indicated at the top of the table.
Dependent variable at the worker levels is the log individual wage, at the municipal level the log mean
municipal wage. Coefficients measure the wage elasticity with respect to the net-of-local-business-tax
rate. All specifications include municipal fixed effects, as well as “state × year” fixed effects. The model
at the firm level additionally includes firm fixed effects, at the individual firm and worker fixed effects
are added. The estimation sample comprises ([workers in] establishments in) non-merged municipalities.
Standarderrorsareclusteredatthemunicipallevel. Standarderrorsareclusteredatthemunicipallevel.
Specification (2) replicates the baseline estimate, presented in column (1) of Table 1.
Table D.2: Differences-in-differences estimates: effects on worker composition
|     |     |     | (1) | (2) | (3) | (4) | (5) | (6) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Dependent var. ln share ln share ln share ln share ln share ln mean
|                |      | high-skilled |       | med-skilled | male    | full-time | blue-collar | age     |
| -------------- | ---- | ------------ | ----- | ----------- | ------- | --------- | ----------- | ------- |
| Log net-of-LBT | rate |              | 0.054 | −0.161      | 0.001   | −0.139    | 0.425       | −0.108  |
|                |      | (0.648)      |       | (0.224)     | (0.176) | (0.170)   | (0.309)     | (0.062) |
| N              |      | 22,978       |       | 44,289      | 43,446  | 44,654    | 40,115      | 44,654  |
Source: LIAB and Statistical Offices of the Laender. Notes: This table presents the DiD estimates δˆof
regression model (3). Instead of the log wage, the dependent variables are log worker shares at the firm
level, and the log mean worker age as indicated at the top of the table. Coefficients measure the wage
elasticity with respect to the net-of-local-business-tax rate. All specifications include firm and municipal
fixed effects, as well as “state × year” fixed effects. The estimation sample comprises all establishments
liable to the LBT in non-merged municipalities. Standard errors are clustered at the municipal level.
66

Table D.3: Differences-in-differences estimates: robustness of wage effects to other con-
trols
(1) (2) (3)
Log net-of-LBT rate 0.388 0.436 0.476
(0.127) (0.138) (0.131)
Future muni. spending (cid:88)
Share never-censored (cid:88)
N 44,654 40,558 44,654
Source: LIAB and Statistical Offices of the Laender. Notes: This table presents the DiD estimates δˆ of
regressionmodel(3). Coefficientsmeasurethewageelasticitywithrespecttothenet-of-local-business-taxrate.
All specifications include firm and municipal fixed effects, as well as “state × year” fixed effects. In addition,
control variables are added as indicated at the bottom of the table: (i) current and future (lead 1 and 2)
municipal spending, (ii) the share of workers in the firm that are never wage-censored during the observation
period. The estimation sample comprises all establishments liable to the LBT in non-merged municipalities.
Standard errors are clustered at the municipal level. Specification replicates the baseline estimate, presented
in column (1) of Table 1.
Table D.4: Differences-in-differences estimates at firm level: robustness to other depen-
dent variables
(1) (2) (3) (4)
Log net-of-LBT rate 0.388 0.220 0.317 0.152
(0.127) (0.104) (0.136) (0.166)
Dep. var: log firm wage P50 Mean P25 P75
N 44,654 44,654 44,654 44,654
Source: LIAB and Statistical Offices of the Laender. Notes: This table presents the DiD estimates δˆ of
regression model (3). The dependent variable are specific measures (median, mean, p25, p75) of the firm wage
(in logs), as indicated at the top of the table. Coefficients measure the wage elasticity with respect to the net-
of-local-business-tax rate. All specifications include firm and municipal fixed effects, as well as “state × year”
fixedeffects.TheestimationsamplecomprisesallestablishmentsliabletotheLBTinnon-mergedmunicipalities.
Standarderrorsareclusteredatthemunicipallevel. Specification(1)replicatesthebaselineestimate,presented
in column (1) of Table 1.
67

Table D.5: Differences-in-differences estimates: robustness of wage effects to different
estimation samples
|     | (1) | (2) | (3) |     | (4) | (5) |     | (6) | (7) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Log net-of-LBT rate 0.388 0.185 0.188 0.409 0.406 0.408 0.367
|     | (0.127) | (0.097) | (0.102) | (0.146) |     | (0.122) |     | (0.151) | (0.143) |
| --- | ------- | ------- | ------- | ------- | --- | ------- | --- | ------- | ------- |
Municipalities Non-merged Non-merged All Non-merged Non-merged Non-merged Non-merged
| Firms          | Liable | All    | Liable | Liable |       | Liable    |     | Liable    | Liable |
| -------------- | ------ | ------ | ------ | ------ | ----- | --------- | --- | --------- | ------ |
| Years          | 99-08  | 99-08  | 99-08  | 99-08  |       | 99-08     |     | 99-08     | 99-07  |
| Add. condition |        |        |        | 0      | drops | + incorp. |     | + firms < |        |
|                |        |        |        |        |       | changers  |     | 4 workers |        |
| N              | 44,654 | 69,249 | 58,062 | 36,828 |       | 49,886    |     | 56,066    | 39,975 |
δˆ
Source: LIAB and Statistical Offices of the Laender. Notes: This table presents the DiD estimates of
regressionmodel(3). Coefficientsmeasurethewageelasticitywithrespecttothenet-of-local-business-taxrate.
Allspecificationsincludefirmandmunicipalfixedeffects,aswellas“state×year”fixedeffects. Theestimation
sample varies across specifications as indicated at the bottom of the table. Standard errors are clustered at the
municipal level. Specification (1) replicates the baseline estimate, presented in column (1) of Table 1.
Table D.6: Differences-in-differences estimates: wage effects at individual level
|     | (1) | (2) | (3) | (4) | (5) | (6) |     | (7) (8) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- |
Log net-of-LBT rate 0.374 0.347 0.353 0.414 0.298 0.361 0.468 0.367
|         | (0.114) | (0.087) | (0.104) (0.116) |     | (0.173) | (0.114) | (0.144)  | (0.116) |     |
| ------- | ------- | ------- | --------------- | --- | ------- | ------- | -------- | ------- | --- |
| Workers | ft      | ft      | ft              | ft  | ft      | ft      | non-cens | ft+pt   |     |
State × year FE (cid:88) (cid:88) (cid:88) (cid:88) (cid:88) (cid:88)
| Year FE      |     | (cid:88) |          |     |     |     |     |     |     |
| ------------ | --- | -------- | -------- | --- | --- | --- | --- | --- | --- |
| CZ × year FE |     |          | (cid:88) |     |     |     |     |     |     |
(cid:88)
| Municipal controls | t−2 |     |     |     |     |     |     |     |     |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:88)
| Firm controls t−2      |     |     |     |     |     |          |     |     |     |
| ---------------------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
| Worker characteristics |     |     |     |     |     | (cid:88) |     |     |     |
N (in million) 9.295 9.295 9.295 9.295 6.430 9.295 7.275 10.091
Source: LIAB and Statistical Offices of the Laender. Notes: This table presents the DiD estimates δˆof
regression model (3) with the log individual wage as dependent variable. Coefficients measure the wage
elasticity with respect to the net-of-local-business-tax rate. All regression models include municipal,
firm and worker fixed effects. Additional control variables and fixed effects (year, “state × year” or
“commuting zone (CZ) × year”) vary depending on the specification (as indicated at the bottom of
the table). For specifications (1) to (6), the estimation sample comprises all full-time (ft) workers in
establishments liable to the LBT in non-merged municipalities. In model (7), the sample is restricted to
workers whose wages have never been right-censored at the ceiling for social security contributions. In
specification (8), part-time workers are added to the full-time worker sample.
68

Table D.7: Differences-in-differences estimates: robustness of wage effects with respect
to clustering
|                |          | (1)     | (2)       | (3)     | (4)     | (5)     | (6)     |
| -------------- | -------- | ------- | --------- | ------- | ------- | ------- | ------- |
| Log net-of-LBT | rate     | 0.388   | 0.388     | 0.388   | 0.388   | 0.388   | 0.388   |
|                |          | (0.127) | (0.091)   | (0.129) | (0.131) | (0.119) | (0.129) |
| N              |          | 44,654  | 44,654    | 44,654  | 44,654  | 44,654  | 44,654  |
| Clustering     | at level | of muni | muni×year | county  | CZ      | state   | firm    |
| Clusters       |          | 2,820   | 14,610    | 394     | 253     | 16      | 14,221  |
δˆof
Source: LIAB and Statistical Offices of the Laender. Notes: This table presents the DiD estimates
regressionmodel(3). Coefficientsmeasurewagetheelasticitywithrespecttothenet-of-local-business-tax
rate. Allspecificationsincludefirmandmunicipalfixedeffects,aswellas“state×year”fixedeffects. The
estimationsamplecomprisesallestablishmentsliabletotheLBTinnon-mergedmunicipalities. Standard
errorsareclusteredatdifferentlevelsasindicatedatthebottomofthetable. Ourpreferredspecification
is shown in column (1), where standard errors are clustered at the municipal level.
69

Table D.8: Differences-in-differences estimates: wage effects by worker type, robustness
with respect to censoring
Stratified by ... Effect of the log net-of-LBT rate by worker type N
| Skill             | High        | Medium       | Low      |           |
| ----------------- | ----------- | ------------ | -------- | --------- |
| All workers       | 0.013       | 0.357        | 0.377    | 9,295,488 |
|                   | (0.120)     | (0.115)      | (0.168)  |           |
| Not wage-censored | 0.011       | 0.431        | 0.428    | 7,275,134 |
|                   | (0.230)     | (0.139)      | (0.192)  |           |
| Gender            | Female      | Male         |          |           |
| All workers       | 0.530       | 0.325        |          | 9,295,488 |
|                   | (0.129)     | (0.119)      |          |           |
| Not wage-censored | 0.583       | 0.429        |          | 7,275,134 |
|                   | (0.140)     | (0.153)      |          |           |
| Occupation        | Blue-collar | White-collar |          |           |
| All workers       | 0.363       | 0.250        |          | 9,295,422 |
|                   | (0.132)     | (0.104)      |          |           |
| Not wage-censored | 0.424       | 0.333        |          | 7,275,090 |
|                   | (0.161)     | (0.128)      |          |           |
| Age               | Young       | Medium       | Old      |           |
| All workers       | 0.507∗∗∗    | 0.317∗∗∗     | 0.329∗∗∗ | 9,295,488 |
|                   | (0.127)     | (0.111)      | (0.106)  |           |
| Not wage-censored | 0.526       | 0.370        | 0.401    | 7,275,134 |
|                   | (0.151)     | (0.136)      | (0.124)  |           |
Source: LIAB and Statistical Offices of the Laender. Notes: This table presents the DiD estimates δˆof
regression model (3) with the log individual wage as dependent variables for different worker types as
indicatedinthetable. TheheterogeneouseffectsareestimatedbyinteractingtheLBTratewithdummy
variables for different firms types. Coefficients measure the wage elasticity with respect to the net-of-
local-business-tax rate. All specifications include worker, firm and municipal fixed effects, as well as
“state × year” and “firm type × year” fixed effects. The estimation sample comprises all establishments
liable to the LBT in non-merged municipalities. Standard errors are clustered at the municipal level.
70

TableD.9: Effectofincidenceassumptionsonaveragetaxratesacrossincomedistribution
|     | Groups     |                   | PIT  | CIT      | Total           | Ratio | PIT CIT    | Total Ratio   |
| --- | ---------- | ----------------- | ---- | -------- | --------------- | ----- | ---------- | ------------- |
|     |            |                   |      | US       | (2004)          |       | Germany    | (2015)        |
|     | Population | average           | 11.5 | 2.3      | 13.7            |       | 12.3 2.0   | 14.4          |
|     | Panel      | A: Piketty-Saez   |      | Baseline | (CIT incidence: |       | 0% wages,  | 100% capital) |
|     | P0-90      |                   | 5.4  | 1.5      | 7.0             |       | 5.5 0.2    | 5.7           |
|     | P90-100    |                   | 14.7 | 2.3      | 16.9            | 1.4   | 21.8 2.7   | 24.6 4.3      |
|     | P99-100    |                   | 22.7 | 4.0      | 26.8            | 2.9   | 27.4 7.4   | 34.8 6.1      |
|     | Panel      | B: Counterfactual |      | 1 (CIT   | incidence:      | 50%   | wages, 50% | capital)      |
|     | P0-90      |                   | 5.4  | 2.4      | 7.8             |       | 5.5 1.2    | 6.7           |
|     | P90-100    |                   | 14.7 | 1.1      | 15.8            | 1.0   | 21.8 1.4   | 23.2 3.5      |
|     | P99-100    |                   | 22.7 | 2.0      | 24.8            | 2.2   | 27.4 3.7   | 31.1 4.6      |
|     | Panel      | C: Counterfactual |      | 2 (CIT   | incidence:      | 100%  | wages,     | 0% capital)   |
|     | P0-90      |                   | 5.4  | 2.5      | 7.9             |       | 5.5 2.0    | 7.5           |
|     | P90-100    |                   | 14.7 | 0.0      | 14.7            | 0.8   | 21.8 0.0   | 21.8 2.9      |
|     | P99-100    |                   | 22.7 | 0.0      | 22.7            | 1.9   | 27.4 0.0   | 27.4 3.7      |
Source: Own calculations based on Piketty and Saez (2007) for the US-2004 and Bach, Beznoska and
Steiner (2016) for Germany-2015. Notes: This table shows the average income tax rates for the bottom
90%, top 10% and top 1% of the market income distribution. The total tax rates are decomposed into
personal and corporate income tax rates (PIT and CIT). The CIT for Germany includes the LBT. The
“ratio” column reports the ratio of the top tax rate (top 10% or top 1%) to the tax rate for the bottom
90% as a measure of progressivity. Panel A reports tax rates under the incidence assumption of Piketty
and Saez (2007), i.e. the full corporate tax incidence being on capital income. Panels B and C report
two counterfactuals with 50% (100%) of the incidence on wages. Note that formula (4) calculates the
shareofthetaxburdenbornebyworkersintermsofwelfare–asdiscussedinSection3.2. Giventhatthe
back-of-the-envelope calculation reported in this table is meant for illustrative purposes only, we assume
here for simplicity reasons that 50% (100%) of the effective tax burden is shifted onto workers. In both
counterfactuals,thewageincidenceisonlyaffectingwagesofworkersinthethebottom90%(inlinewith
| the heterogeneous | effects | that we | find). |     |     |     |     |     |
| ----------------- | ------- | ------- | ------ | --- | --- | --- | --- | --- |
71

| Table | D.10: Event   | study estimates: | baseline  | wage      | effects |
| ----- | ------------- | ---------------- | --------- | --------- | ------- |
|       |               | (1)              | (2)       | (3)       |         |
|       | Specification | Increases        | Large Inc | Decreases |         |
|       | F4            | 0.559            | -0.435    | 0.231     |         |
|       |               | (0.352)          | (0.816)   | (1.110)   |         |
|       | F3            | 0.423            | -0.282    | 0.697     |         |
|       |               | (0.305)          | (0.776)   | (1.220)   |         |
|       | F2            | 0.069            | -0.448    | 0.916     |         |
|       |               | (0.228)          | (0.667)   | (0.876)   |         |
|       | L0            | -0.073           | -0.736    | 1.370     |         |
|       |               | (0.206)          | (0.580)   | (0.724)   |         |
|       | L1            | -0.226           | -0.952    | 0.279     |         |
|       |               | (0.281)          | (0.582)   | (0.907)   |         |
|       | L2            | -0.622           | -2.140    | 0.490     |         |
|       |               | (0.309)          | (0.817)   | (0.799)   |         |
|       | L3            | -0.576           | -2.640    | 0.674     |         |
|       |               | (0.318)          | (0.957)   | (0.710)   |         |
|       | L4            | -0.450           | -2.630    | -0.574    |         |
|       |               | (0.359)          | (0.923)   | (1.030)   |         |
|       | L5            | -0.899           | -3.100    | 0.729     |         |
|       |               | (0.349)          | (1.030)   | (0.659)   |         |
|       | N             | 36,826           | 36,826    | 6,001     |         |
Source: LIAB and Statistical Offices of the Laender. Notes: The table shows the
event study estimates plotted in Panel A of Figure 3. Please refer to figure note for
further information.
72

Table D.11: Event study estimates: wage effects by event window cut
|               | (1)     | (2)         | (3)     | (4)         |
| ------------- | ------- | ----------- | ------- | ----------- |
| Specification | no res. | 0D in S 0D, | 1H in W | 0D, 1H in S |
| F4            | 0.566   | -0.435      | -0.644  | -0.807      |
|               | (0.935) | (0.816)     | (0.839) | (0.851)     |
| F3            | 0.077   | -0.282      | -0.481  | -0.582      |
|               | (0.851) | (0.776)     | (0.799) | (0.824)     |
| F2            | -0.459  | -0.448      | -0.590  | -0.400      |
|               | (0.703) | (0.667)     | (0.709) | (0.708)     |
| L0            | -0.700  | -0.736      | -0.798  | -0.786      |
|               | (0.583) | (0.580)     | (0.592) | (0.634)     |
| L1            | -1.090  | -0.952      | -1.030  | -0.843      |
|               | (0.762) | (0.582)     | (0.604) | (0.635)     |
| L2            | -1.340  | -2.140      | -2.200  | -2.180      |
|               | (0.787) | (0.817)     | (0.832) | (0.890)     |
| L3            | -1.940  | -2.640      | -2.710  | -2.790      |
|               | (0.879) | (0.957)     | (0.968) | (1.020)     |
| L4            | -1.700  | -2.630      | -2.670  | -2.670      |
|               | (0.880) | (0.923)     | (0.943) | (0.989)     |
| L5            | -2.030  | -3.100      | -3.280  | -3.330      |
|               | (0.976) | (1.030)     | (1.070) | (1.130)     |
| N             | 44,630  | 36,826      | 36,086  | 33,554      |
Source: LIAB and Statistical Offices of the Laender. Notes: The table shows the
event study estimates plotted in Figure D.1. Please refer to figure note for further
information.
73

Table D.12: Event study estimates: wage effects by firm liability
|               | (1) (2)          | (3)        |
| ------------- | ---------------- | ---------- |
| Specification | All firms Liable | Non Liable |
| F4            | -0.771 -0.435    | -1.040     |
|               | (0.812) (0.816)  | (1.530)    |
| F3            | -0.651 -0.282    | -0.985     |
|               | (0.731) (0.776)  | (1.290)    |
| F2            | -0.505 -0.448    | -0.595     |
|               | (0.600) (0.667)  | (1.190)    |
| L0            | -0.479 -0.736    | 0.294      |
|               | (0.436) (0.580)  | (0.588)    |
| L1            | -0.590 -0.952    | 0.369      |
|               | (0.476) (0.582)  | (0.777)    |
| L2            | -1.470 -2.140    | 0.119      |
|               | (0.627) (0.817)  | (0.882)    |
| L3            | -1.640 -2.640    | 0.157      |
|               | (0.703) (0.957)  | (1.060)    |
| L4            | -1.310 -2.630    | 0.789      |
|               | (0.743) (0.923)  | (1.060)    |
| L5            | -1.460 -3.100    | 1.400      |
|               | (0.790) (1.030)  | (1.240)    |
| N             | 57,032 36,826    | 20,206     |
Source: LIAB and Statistical Offices of the Laender. Notes: The table shows the
event study estimates plotted in Figure D.2. Please refer to figure note for further
information.
74

Table D.13: Distributed lag model estimates: baseline wage effects
|     |     |               | (1)      | (2) |
| --- | --- | ------------- | -------- | --- |
|     |     | Specification | Lead/Lag | Lag |
|     |     | F4            | 0.104    |     |
(0.119)
|     |     | F3  | -0.026 |     |
| --- | --- | --- | ------ | --- |
(0.128)
|     |     | F2  | -0.023 |     |
| --- | --- | --- | ------ | --- |
(0.109)
|     |     | F1  | 0.064 |     |
| --- | --- | --- | ----- | --- |
(0.117)
|     |     | L0  | 0.236   | 0.237   |
| --- | --- | --- | ------- | ------- |
|     |     |     | (0.115) | (0.115) |
|     |     | L1  | 0.109   | 0.111   |
|     |     |     | (0.152) | (0.152) |
|     |     | L2  | 0.333   | 0.327   |
|     |     |     | (0.158) | (0.158) |
|     |     | L3  | 0.019   | 0.013   |
|     |     |     | (0.152) | (0.151) |
|     |     | L4  | 0.097   | 0.104   |
|     |     |     | (0.151) | (0.151) |
|     |     | L5  | 0.188   | 0.186   |
|     |     |     | (0.126) | (0.126) |
|     |     | N   | 24,626  | 24,626  |
Source: LIAB and Statistical Offices of the Laender. Notes: The table shows the
estimates of the distributed lag model whose cumulative effects are plotted in Panel
| B of Figure | 3. Please | refer to figure | note for further | information. |
| ----------- | --------- | --------------- | ---------------- | ------------ |
75

Table D.14: Distributed lag model estimates: wage effects by event window cut
|     |     |               | (1)     | (2)     |
| --- | --- | ------------- | ------- | ------- |
|     |     | Specification | no res. | 0D in S |
|     |     | F4            | 0.014   | 0.104   |
|     |     |               | (0.092) | (0.119) |
|     |     | F3            | 0.132   | -0.026  |
|     |     |               | (0.103) | (0.128) |
|     |     | F2            | 0.023   | -0.023  |
|     |     |               | (0.093) | (0.109) |
|     |     | F1            | -0.034  | 0.064   |
|     |     |               | (0.110) | (0.117) |
|     |     | L0            | 0.206   | 0.236   |
|     |     |               | (0.101) | (0.115) |
|     |     | L1            | 0.074   | 0.109   |
|     |     |               | (0.109) | (0.152) |
|     |     | L2            | 0.214   | 0.333   |
|     |     |               | (0.115) | (0.158) |
|     |     | L3            | 0.039   | 0.019   |
|     |     |               | (0.117) | (0.152) |
|     |     | L4            | 0.075   | 0.097   |
|     |     |               | (0.113) | (0.151) |
|     |     | L5            | 0.029   | 0.188   |
|     |     |               | (0.100) | (0.126) |
|     |     | N             | 29,634  | 24,626  |
Source: LIAB and Statistical Offices of the Laender. Notes: The table shows the
estimatesofthedistributedlagmodelwhosecumulativeeffectsareplottedinFigure
| D.3. Please | refer to figure | note for further | information. |     |
| ----------- | --------------- | ---------------- | ------------ | --- |
76

| Table D.15:   | Event study | estimates: | GDP       |
| ------------- | ----------- | ---------- | --------- |
|               | (1)         | (2)        | (3)       |
| Specification | Increases   | Large Inc  | Decreases |
| F4            | -0.146      | 0.134      | 2.310     |
|               | (0.164)     | (0.241)    | (1.080)   |
| F3            | 0.019       | 0.152      | 2.420     |
|               | (0.137)     | (0.196)    | (0.770)   |
| F2            | 0.119       | 0.016      | 0.773     |
|               | (0.099)     | (0.132)    | (0.671)   |
| L0            | 0.033       | 0.006      | -0.597    |
|               | (0.093)     | (0.128)    | (0.977)   |
| L1            | -0.011      | -0.229     | -0.733    |
|               | (0.118)     | (0.172)    | (0.972)   |
| L2            | 0.066       | -0.231     | 0.492     |
|               | (0.137)     | (0.202)    | (1.150)   |
| L3            | -0.085      | -0.425     | 0.341     |
|               | (0.162)     | (0.228)    | (0.818)   |
| L4            | 0.050       | -0.240     | 0.875     |
|               | (0.180)     | (0.254)    | (0.954)   |
| L5            | 0.115       | -0.450     | 0.048     |
|               | (0.197)     | (0.278)    | (1.030)   |
| N             | 31,023      | 31,023     | 6,479     |
Source: LIAB and Statistical Offices of the Laender. Notes: The table shows the
event study estimates plotted in Panel A of Figure 4. Please refer to figure note for
further information.
77

Table D.16: Event study estimates: unemployment
(1) (2) (3)
Specification Increases Large Inc Decreases
F4 -0.364 -0.863 -0.112
(0.284) (0.767) (1.640)
F3 -0.174 -0.310 0.231
(0.212) (0.643) (1.440)
F2 0.170 0.234 0.168
(0.143) (0.479) (0.892)
L0 -0.067 -0.010 1.730
(0.125) (0.340) (1.200)
L1 -0.334 0.182 1.810
(0.188) (0.574) (1.330)
L2 -0.241 0.191 3.800
(0.237) (0.692) (1.520)
L3 0.008 0.079 4.880
(0.277) (0.806) (1.470)
L4 0.106 0.751 3.470
(0.315) (0.906) (1.460)
L5 -0.003 1.710 2.250
(0.337) (0.975) (2.320)
N 31,023 31,023 6,479
Source: LIAB and Statistical Offices of the Laender. Notes: The table shows the
event study estimates plotted in Panel B of Figure 4. Please refer to figure note for
further information.
78

| Table | D.17:         | Event | study     | estimates: | municipal |           | revenues |
| ----- | ------------- | ----- | --------- | ---------- | --------- | --------- | -------- |
|       |               |       |           | (1)        | (2)       | (3)       |          |
|       | Specification |       | Increases |            | Large Inc | Decreases |          |
|       | F4            |       | 1.150     |            | 0.659     | -8.820    |          |
|       |               |       | (0.663)   |            | (1.910)   | (4.470)   |          |
|       | F3            |       | 0.949     |            | -2.200    | -8.030    |          |
|       |               |       | (0.627)   |            | (1.640)   | (3.900)   |          |
|       | F2            |       | 1.460     |            | 1.390     | -5.350    |          |
|       |               |       | (0.509)   |            | (1.730)   | (3.480)   |          |
|       | L0            |       | -0.008    |            | 0.980     | 0.288     |          |
|       |               |       | (0.506)   |            | (1.400)   | (3.110)   |          |
|       | L1            |       | 1.320     |            | 1.850     | -3.540    |          |
|       |               |       | (0.624)   |            | (1.930)   | (3.820)   |          |
|       | L2            |       | 1.360     |            | -0.148    | -0.851    |          |
|       |               |       | (0.647)   |            | (1.920)   | (4.800)   |          |
|       | L3            |       | 0.421     |            | -0.629    | -4.700    |          |
|       |               |       | (0.676)   |            | (2.070)   | (5.490)   |          |
|       | L4            |       | 1.120     |            | 0.102     | 4.970     |          |
|       |               |       | (0.722)   |            | (1.920)   | (5.010)   |          |
|       | L5            |       | 1.830     |            | 1.660     | -3.090    |          |
|       |               |       | (0.748)   |            | (2.040)   | (3.900)   |          |
|       | N             |       | 30,984    |            | 30,984    | 6,477     |          |
Source: LIAB and Statistical Offices of the Laender. Notes: The table shows the
event study estimates plotted in Panel A of Figure D.5. Please refer to figure note
for further information.
79

| Table | D.18:         | Event | study     | estimates: | municipal |           | spending |
| ----- | ------------- | ----- | --------- | ---------- | --------- | --------- | -------- |
|       |               |       |           | (1)        | (2)       | (3)       |          |
|       | Specification |       | Increases |            | Large Inc | Decreases |          |
|       | F4            |       | -0.169    |            | -0.255    | -6.010    |          |
|       |               |       | (0.689)   |            | (2.040)   | (2.930)   |          |
|       | F3            |       | -0.313    |            | -2.910    | -7.080    |          |
|       |               |       | (0.623)   |            | (1.770)   | (3.370)   |          |
|       | F2            |       | 0.682     |            | 0.720     | -0.251    |          |
|       |               |       | (0.501)   |            | (1.810)   | (3.310)   |          |
|       | L0            |       | -1.460    |            | -2.630    | 0.421     |          |
|       |               |       | (0.515)   |            | (1.580)   | (3.100)   |          |
|       | L1            |       | -0.178    |            | -1.870    | 2.320     |          |
|       |               |       | (0.629)   |            | (1.850)   | (3.610)   |          |
|       | L2            |       | 0.246     |            | -1.820    | -1.170    |          |
|       |               |       | (0.667)   |            | (2.010)   | (3.980)   |          |
|       | L3            |       | -0.692    |            | -1.180    | 4.270     |          |
|       |               |       | (0.709)   |            | (2.240)   | (4.090)   |          |
|       | L4            |       | -0.203    |            | -2.500    | 7.040     |          |
|       |               |       | (0.765)   |            | (2.100)   | (4.270)   |          |
|       | L5            |       | 0.046     |            | 0.547     | -2.520    |          |
|       |               |       | (0.798)   |            | (2.240)   | (3.610)   |          |
|       | N             |       | 30,982    |            | 30,982    | 6,476     |          |
Source: LIAB and Statistical Offices of the Laender. Notes: The table shows the
event study estimates plotted in Panel B of Figure D.5. Please refer to figure note
for further information.
80

| Table | D.19: Event   | study estimates: | municipal | fiscal surplus |
| ----- | ------------- | ---------------- | --------- | -------------- |
|       |               | (1)              | (2)       | (3)            |
|       | Specification | Increases        | Large Inc | Decreases      |
|       | F4            | 0.169            | 0.110     | -1.330         |
|       |               | (0.090)          | (0.263)   | (1.310)        |
|       | F3            | 0.121            | -0.156    | -1.050         |
|       |               | (0.091)          | (0.278)   | (1.400)        |
|       | F2            | 0.086            | 0.027     | -2.050         |
|       |               | (0.081)          | (0.251)   | (1.150)        |
|       | L0            | 0.230            | 0.442     | 0.604          |
|       |               | (0.078)          | (0.294)   | (1.100)        |
|       | L1            | 0.228            | 0.383     | -2.780         |
|       |               | (0.079)          | (0.194)   | (1.880)        |
|       | L2            | 0.192            | 0.246     | 1.030          |
|       |               | (0.085)          | (0.262)   | (1.890)        |
|       | L3            | 0.153            | -0.089    | -2.680         |
|       |               | (0.088)          | (0.231)   | (1.370)        |
|       | L4            | 0.141            | 0.150     | -0.336         |
|       |               | (0.100)          | (0.332)   | (1.900)        |
|       | L5            | 0.255            | -0.081    | -0.080         |
|       |               | (0.095)          | (0.252)   | (1.200)        |
|       | N             | 30,983           | 30,983    | 6,477          |
Source: LIAB and Statistical Offices of the Laender. Notes: The table shows the
event study estimates plotted in Panel C of Figure D.5. Please refer to figure note
for further information.
81

ifo Working Papers
No. 240 Ochsner, C., Dismantled once, diverged forever? A quasi-natural experiment of Red
Army misdeeds in post-WWII Europe, August 2017.
No. 239 Drometer, M. and R. Méango, Electoral Cycles, Effects and U.S. Naturalization Policies,
August 2017.
No. 238 Sen, S. and M.-T. von Schickfus, Will Assets be Stranded or Bailed Out? Expectations of
Investors in the Face of Climate Policy, August 2017.
No. 237 Giesing, Y. and A. Music, Household behaviour in times of political change: Evidence
from Egypt, July 2017.
No. 236 Hayo, B. and F. Neumeier, Explaining Central Bank Trust in an Inflation Targeting
Country: The Case of the Reserve Bank of New Zealand, June 2017.
No. 235 Buettner, T. und M. Krause, Föderalismus im Wunderland: Zur Steuerautonomie bei
der Grunderwerbsteuer, März 2017.
No. 234 Blesse, S. und F. Rösel, Gebietsreformen: Hoffnungen, Risiken und Alternativen,
Januar 2017.
No. 233 Hayo, B. and F. Neumeier, The (In)Validity of the Ricardian Equivalence Theorem –
Findings from a Representative German Population Survey, December 2016.
No. 232 Fritzsche, C. and L. Vandrei, The German Real Estate Transfer Tax: Evidence for Single-
Family Home Transactions, November 2016.
No. 231 Nagl, W. and M. Weber, Stuck in a trap? Long-term unemployment under two-tier
unemployment compensation schemes, November 2016.
No. 230 Neumeier, F., Do Businessmen Make Good Governors?, November 2016.

No. 229 Gutmann, J., M. Neuenkirch and F. Neumeier, Precision-Guided or Blunt? The Effects
of US Economic Sanctions on Human Rights, November 2016.
No. 228 Felbermayr, G., R. Aichele, I. Heiland, A. Melchior and M. Steininger, TTIP – Potential
Effects on Norway, (November 2016) revised version December 2016.
No. 227 Schueler, R., Educational inputs and economic development in end-of-nineteenth-
century Prussia, October 2016.
No. 226 Riem, M., Does political uncertainty influence firm owners‘ business perceptions?,
October 2016.
No. 225 Enzi, B. and B. Siegler, The Impact of the Bologna Reform on Student Outcomes –
Evidence from Exogenous Variation in Regional Supply of Bachelor Programs in
Germany, October 2016.
No. 224 Roesel, F., Do mergers of large local governments reduce expenditures? – Evidence
from Germany using the synthetic control method, October 2016.
No. 223 Schueler, R., Centralized Monitoring, Resistance, and Reform Outcomes: Evidence from
School Inspections in Prussia, October 2016.
No. 222 Battisti, M., R. Michaels and C. Park, Labor supply within the firm, October 2016.
No. 221 Riem, M., Corporate investment decisions under political uncertainty, October 2016.
No. 220 Aichele, R., I. Heiland and G. Felbermayr, TTIP and intra-European trade: boon or
bane?, September 2016.
No. 219 Aichele, R., G. Felbermayr and I. Heiland, Going Deep: The Trade and Welfare Effects of
TTIP Revised, July 2016.
No. 218 Fischer, M., B. Kauder, N. Potrafke and H.W. Ursprung, Support for free-market policies
and reforms: Does the field of study influence students’ political attitudes?, July 2016.
No. 217 Battisti, M., G. Felbermayr and S. Lehwald, Inequality in Germany: Myths, Facts, and
Policy Implications, June 2016.
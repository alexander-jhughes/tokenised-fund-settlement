# Sources

Full citation list for this project, with what each source actually supports.

**Bindseil, U. and Pantelopoulos, G. (2022), "Towards the Holy Grail of Cross-Border Payments," ECB Working Paper No. 2693.** ([PDF](https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2693~8d4e580438.en.pdf)) Argues stablecoins are among the most promising routes to straight-through cross-border processing, contingent on resolving AML/CFT, financial stability, and monetary sovereignty concerns. Underpins the problem statement.

**Monetary Authority of Singapore, Project Guardian: "Operationalising Tokenised Funds."** ([PDF](https://www.mas.gov.sg/-/media/mas-media-library/development/fintech/guardian/guardian-funds-framework.pdf)) Defines the three tokenised fund register models, Digital Mirror, Digital Twin, and Digital Native, each with different technical and legal requirements. Used in `docs/architecture.md` for the settlement and compliance model design.

**Aldasoro, I., Doerr, S., Gambacorta, L., Garratt, R. and Koo Wilkens, P. (2023), "The Tokenisation Continuum," BIS Bulletin No. 72.** ([PDF](https://www.bis.org/publ/bisbull72.pdf)) Frames tokenisation as a core asset/ownership layer plus a service layer of platform rules, and notes intermediaries tend to persist through tokenisation rather than disappear. Used in `docs/architecture.md`.

**International Monetary Fund, "Tokenized Finance," IMF Notes No. 26/01 (April 2026).** ([PDF](https://www.imf.org/-/media/files/publications/imf-notes/2026/english/insea2026001.pdf)) Identifies cross-border payments as a leading tokenisation use case given long-standing correspondent banking inefficiencies and fragmented liquidity. Used in `docs/case-study.md` for framing.

**Central Bank of the UAE, in collaboration with the BIS Innovation Hub, the People's Bank of China, the Bank of Thailand, and the Hong Kong Monetary Authority, "Project mBridge: Connecting Economies Through CBDC."** ([PDF](https://www.centralbank.ae/media/lnchuury/project-mbridge-connecting-economies-through-cbdc-final.pdf)) Describes correspondent banking's fragmented, time-zone-dependent intermediary chain, and the rationale for restricting foreign holdings of the Digital Dirham to protect monetary sovereignty. Used in `docs/case-study.md`.

**Central Bank of the UAE, CBDC Strategy (long report, July 2026).** ([PDF](https://centralbank.ae/media/qw1ex32h/cbdc-long-report_july.pdf)) Models the effect of a non-interest-bearing CBDC on money demand, adapted from Jobst and Lin (2016). Used in `docs/case-study.md` and `model/cbdc_money_demand.py`.

**Bank for International Settlements, Committee on Payments and Market Infrastructures, "Delivery versus Payment in Securities Settlement Systems" (1992).** ([PDF](https://www.bis.org/cpmi/publ/d06.pdf)) Defines Herstatt (principal) risk, the loss exposure created when one side of a trade settles before the other, and how DvP eliminates it. Basis for the settlement risk exposure formula in `model/settlement_simulation.py`.

**Glasserman, P. (2004), Monte Carlo Methods in Financial Engineering. Springer, New York.** Standard reference for Monte Carlo estimator efficiency, standard error, and confidence intervals. Basis for the simulation methodology in `model/settlement_simulation.py`.

**Global Credit Data, "Large Corporates PD and Default Rate Report 2025."** ([PDF](https://globalcreditdata.org/wp-content/uploads/2025/12/pd-reports-2025-dm-lc-v8.pdf)) Reports a 0.22% through-the-cycle default probability for investment-grade exposures, used as a general counterparty risk proxy in `model/settlement_simulation.py`.
# Case Study: Tokenised Fund Settlement Between Singapore and the UAE
## 1. Context

Tokenised settlement infrastructure is changing cross-border capital movement: quicker liquidity pools, tracked transactions, lower operational risk and cost vs correspondent banking.

Risk: faster rails could enable large, rapid capital in/outflows, a financial stability concern.

Response, by design:
- **Project mBridge**: settlement controlled through participating central banks, not open commercial rails
- **Digital Dirham**: non-interest-bearing, foreign holdings restricted, so it doesn't compete with bank deposits or affect remittance flow scale, illustrated using a money-demand framework CBUAE's CBDC strategy report adapts from Jobst and Lin (2016)

This tension (efficiency vs monetary stability) is why SG-UAE sovereign capital can't just adopt tokenised rails without the policy safeguards Guardian and mBridge are built around.

## 2. The Problem: Cross-Border Settlement Friction

Correspondent banking: chain of intermediary banks via nostro/vostro accounts. Fund's bank has no direct account in investor's jurisdiction, routes via correspondent (nostro to fund's bank, vostro to correspondent). FX conversion happens at this stage.

T+2 (roughly 48hrs) breakdown ([model/settlement_simulation.py](../model/settlement_simulation.py)):

1. **Fund → Fund's Bank**: instruction/processing
2. **Fund's Bank → Correspondent Bank**: AML/KYC screening
3. **Correspondent Bank → Investor's Bank**: receiving-side compliance (largest delay, less visibility into originating counterparty)
4. **Investor's Bank → Investor**: final crediting

Cost layers (Bech et al., 2022):
- Operational, compliance, network, correspondent, FX, liquidity cost

One of these, the opportunity cost of capital sitting idle during settlement, is modelled here using SOFR (Secured Overnight Financing Rate), published daily by the Federal Reserve Bank of New York ([newyorkfed.org/markets/reference-rates/sofr](https://www.newyorkfed.org/markets/reference-rates/sofr)). SOFR is used as a baseline riskless benchmark for what the capital could otherwise earn, rather than any specific bank's funding rate, since the comparison is meant to isolate the cost of time, not the cost of any one institution's balance sheet.

**Key formulas**

Opportunity cost of idle capital:

$$C_{opp} = V \cdot \frac{r}{8760} \cdot \Delta h$$

where V is the transaction size, r is the annual SOFR, Δh is the hours of settlement time saved, and 8760 is hours per year.

Settlement (Herstatt) exposure:

$$E = V \cdot \frac{h}{8760} \cdot p$$

where h is settlement time in hours and p is the annual counterparty default probability. This assumes default risk accrues linearly with exposure time, a simplification appropriate for an illustrative comparison, not a regulatory capital model.

Monte Carlo estimate precision, used for the 95% confidence interval on simulated settlement time:

$$SE = \frac{s}{\sqrt{n}}, \quad CI_{95} = \bar{x} \pm 1.96 \cdot SE$$

where s is the sample standard deviation across trials (Glasserman, 2004, Section 1.1) and n = 10,000. This is valid even though each hop is drawn from a triangular distribution, not a normal one: each trial sums several independent hops, and the Central Limit Theorem means that sum tends toward normal regardless of the shape of the individual pieces.

Each intermediary means more counterparty risk, operational risk, failure points. Structural, not incidental. The settlement model runs a Monte Carlo simulation (10,000 trials, triangular distribution per hop) and estimates the counterparty (Herstatt) risk exposure this friction creates, following BIS's DvP framework.

## 3. Singapore: Project Guardian

MAS-run, multilateral (Policymaker Group includes IMF, World Bank, ECB, Banque de France, Bundesbank).

**Tokenisation models** (Guardian Funds Framework):
1. **Digital Mirror**: token reflects off-chain register (legal source of truth stays off-chain)
2. **Digital Twin**: partial on-chain register (Distributor / Feeder Fund variants)
3. **Digital Native**: full on-chain register

**Compliance:** ERC-3643, "Permissioned Asset on Permissionless Rails." Transfers only between KYC-passed wallets.

**Bridging** (MAS Interlinking Networks Whitepaper, 2023):
- **Lock and Mint**: lock source token, mint wrapped token on destination
- **Burn and Mint**: burn source token, mint new token on destination

**Framing:** BIS Bulletin 72 (Aldasoro et al., 2023): tokens combine a core layer (asset/ownership) with a service layer (platform rules). Tech alone doesn't remove intermediaries. Biggest gains come from assets hardest to tokenise, traded at volume, which fits institutional fund settlement.

## 4. UAE: Digital Dirham, ADX, and ADGM

**Digital Dirham / mBridge:** CBUAE, under the FIT programme. Cross-border rail is mBridge, a multi-CBDC platform with the BIS Innovation Hub, China, Thailand, and Hong Kong. Targets correspondent banking's fragmented, time-zone-dependent chain. First cross-border payment: January 2024, UAE to China.

Design choice: non-interest-bearing, foreign holdings restricted. No competition with bank deposits, no material effect on remittance flow scale or speed. See [model/cbdc_money_demand.py](../model/cbdc_money_demand.py) for an illustration of this mechanism, adapted from CBUAE's CBDC strategy report.

**ADX:** MENA's first digital bond (ADX, HSBC, FAB, via HSBC Orion), plus a fully digitally-native bond. UAE's closest parallel to Guardian, at exchange level.

**ADGM:** first regional digital assets framework covering tokenised funds, securities, custodians. Legal basis for ADX's tokenised issuances.

The UAE is building both the payment-rail side (Digital Dirham/mBridge) and the securities side (ADX/ADGM), parallel to Guardian, independently, not yet interoperable.

## 5. The Opportunity: Connecting the Two

Singapore and the UAE built tokenisation infrastructure independently. No direct interoperability exists.

The gap is the opportunity. SWF capital moving between the two still relies on correspondent banking for the cash leg, even where the underlying asset is tokenised.

To connect them, roughly requires:
1. **Bridging mechanism** between Guardian-compatible tokens and UAE infrastructure (Lock-and-Mint / Burn-and-Mint, depending on EVM compatibility)
2. **Shared settlement asset** for the cash leg: stablecoin, tokenised bank liability, or Digital Dirham linked to an SG wholesale CBDC equivalent
3. **Aligned compliance**: ERC-3643-gated tokens satisfying UAE KYC/AML without duplicate onboarding

If solved, SWF capital could move at the speed and cost modelled here (an estimated 133x median-to-median speedup, per Monte Carlo simulation), while keeping each jurisdiction's monetary sovereignty safeguards intact.

## 6. Limitations and Open Questions

1. **Capital treatment**: stablecoin exposure under Basel III/IV remains unsettled, a real adoption blocker for banks
2. **Issuer risk**: stablecoin credibility depends on provable reserves, audits, full backing; de-peg risk otherwise
3. **Bridging complexity**: EVM vs non-EVM networks need custom bridging (Lock-and-Mint / Burn-and-Mint), each with its own risk
4. **Operational risk**: private key loss, ledger manipulation risk (Guardian Funds Framework)
5. **Intermediaries persist**: technology alone doesn't remove them (Aldasoro et al., 2023); their role changes, it doesn't disappear
6. **This project's scope**: time and cost figures are estimates from published research, not measured system performance


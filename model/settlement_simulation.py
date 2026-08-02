# settlement_simulation.py
# Monte Carlo simulation of total settlement time for traditional
# correspondent banking vs tokenised DvP settlement, plus the resulting
# opportunity cost and counterparty (Herstatt) risk exposure implications.

import matplotlib.pyplot as plt
import numpy as np
import os
import requests

N_TRIALS = 10_000
RNG_SEED = 42

traditional_settlement = [
    ("Fund -> Fund's Bank", 2, 6),
    ("Fund's Bank -> Correspondent Bank (AML/KYC)", 8, 24),
    ("Correspondent Bank -> Investor's Bank", 10, 30),
    ("Investor's Bank -> Investor", 4, 12),
]

tokenised_settlement = [
    ("Fund -> Tokenised Fund Share", 0.02, 0.1),
    ("Compliance Check (ERC-3643)", 0.02, 0.25),
    ("Block confirmation + stablecoin settlement", 0.03, 0.3),
]

SOFR_FALLBACK = 0.0364


def fetch_live_sofr(timeout=5):
    url = "https://markets.newyorkfed.org/api/rates/secured/all/latest.json"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        rates = response.json()["refRates"]
        sofr = next(r for r in rates if r["type"] == "SOFR")
        return sofr["percentRate"] / 100, sofr["effectiveDate"]
    except Exception as e:
        print(f"Live SOFR pull failed ({e}), using fallback {SOFR_FALLBACK*100:.2f}%.")
        return SOFR_FALLBACK, "fallback (23 Jul 2026)"


SOFR_ANNUAL, SOFR_DATE = fetch_live_sofr()
HOURLY_RATE = SOFR_ANNUAL / (24 * 365)

TRANSACTION_SIZE = 10_000_000
DEFAULT_PROBABILITY_ANNUAL = 0.0022


def opportunity_cost(hours_delta):
    return TRANSACTION_SIZE * HOURLY_RATE * hours_delta


def print_flow(name, flow):
    print(f"\n{name}")
    for step, low, high in flow:
        print(f"  {step}: {low}-{high} hours")


def monte_carlo_hours(flow, n=N_TRIALS, rng=None):
    if rng is None:
        rng = np.random.default_rng(RNG_SEED)
    totals = np.zeros(n)
    for _, low, high in flow:
        mode = (low + high) / 2
        totals += rng.triangular(low, mode, high, n)
    return totals


def monte_carlo_standard_error(samples):
    return np.std(samples, ddof=1) / np.sqrt(len(samples))


def settlement_exposure(hours, default_probability=DEFAULT_PROBABILITY_ANNUAL):
    time_years = hours / 8760
    return TRANSACTION_SIZE * time_years * default_probability


def generate_distribution_chart(trad_samples, tok_samples):
    """
    Histogram of the Monte Carlo settlement time distributions, styled to
    academic finance-paper convention: serif type, boxed axes with inward
    ticks, a navy/slate two-tone palette, legend placed in the empty middle
    of the plot rather than over the data, caption below.
    """
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]

    TRAD_FILL = "#aebfce"
    TRAD_EDGE = "#3d4f5c"
    TOK_FILL = "#0f2f4f"
    TOK_EDGE = "#081b2e"

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bins = np.logspace(np.log10(0.05), np.log10(100), 50)
    counts_trad, _, _ = ax.hist(trad_samples, bins=bins, facecolor=TRAD_FILL,
                                 edgecolor=TRAD_EDGE, linewidth=0.7,
                                 label="Traditional (correspondent banking)")
    counts_tok, _, _ = ax.hist(tok_samples, bins=bins, facecolor=TOK_FILL,
                                edgecolor=TOK_EDGE, linewidth=0.7,
                                label="Tokenised (DvP)")

    ax.set_xscale("log")
    ymax = max(counts_trad.max(), counts_tok.max())
    ax.set_ylim(0, ymax * 1.35)

    ax.set_xlabel("Total settlement time, hours (log scale)", fontsize=10.5)
    ax.set_ylabel(f"Frequency (of {N_TRIALS:,} simulated trials)", fontsize=10.5)

    ax.tick_params(axis="both", direction="in", length=4, labelsize=9.5)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(0.8)

    ax.grid(axis="y", linestyle=":", linewidth=0.5, color="gray", alpha=0.45)
    ax.set_axisbelow(True)

    legend = ax.legend(frameon=True, fontsize=9.5, loc="upper center", edgecolor="black")
    legend.get_frame().set_linewidth(0.7)

    ax.set_title("Figure 1. Monte Carlo distribution of settlement time",
                 fontsize=11.5, loc="left", pad=12)

    fig.text(0.5, -0.04,
              "Note: each hop's duration drawn from a triangular distribution (low, midpoint, high); "
              "10,000 trials summed per flow. Illustrative estimate, not measured system performance.",
              ha="center", fontsize=8, color="#333333")

    os.makedirs("model/output", exist_ok=True)
    plt.tight_layout()
    plt.savefig("model/output/settlement_distribution.png", dpi=200, bbox_inches="tight")
    print("Chart saved to model/output/settlement_distribution.png")


print_flow("Traditional Settlement (Correspondent Banking)", traditional_settlement)
print_flow("Tokenised Settlement (DvP)", tokenised_settlement)

rng = np.random.default_rng(RNG_SEED)
trad_samples = monte_carlo_hours(traditional_settlement, rng=rng)
tok_samples = monte_carlo_hours(tokenised_settlement, rng=rng)

trad_p5, trad_p50, trad_p95 = np.percentile(trad_samples, [5, 50, 95])
tok_p5, tok_p50, tok_p95 = np.percentile(tok_samples, [5, 50, 95])

speedup_p50 = trad_p50 / tok_p50

print(f"\nMonte Carlo simulation ({N_TRIALS:,} trials, triangular distribution per hop):")
print(f"  Traditional: P5={trad_p5:.2f}h, median={trad_p50:.2f}h, P95={trad_p95:.2f}h")
print(f"  Tokenised:   P5={tok_p5:.2f}h, median={tok_p50:.2f}h, P95={tok_p95:.2f}h")
print(f"  Median-to-median speedup: {speedup_p50:.0f}x")

trad_se = monte_carlo_standard_error(trad_samples)
tok_se = monte_carlo_standard_error(tok_samples)

print(f"\nMonte Carlo estimate precision (95% CI on the mean, {N_TRIALS:,} trials):")
print(f"  Traditional: {trad_samples.mean():.2f}h \u00b1 {1.96 * trad_se:.3f}h")
print(f"  Tokenised:   {tok_samples.mean():.2f}h \u00b1 {1.96 * tok_se:.3f}h")

print(f"\nNote: these are illustrative estimates based on published research, not measured system performance.")

hours_saved_median = trad_p50 - tok_p50
cost_median = opportunity_cost(hours_saved_median)

print(f"\nOn a $10,000,000 subscription, tokenised settlement saves an estimated")
print(f"${cost_median:,.0f} in opportunity cost of capital at the median settlement time,")
print(f"at an annualised SOFR of {SOFR_ANNUAL*100:.2f}% (as of {SOFR_DATE}).")

trad_exposure = settlement_exposure(trad_p50)
tok_exposure = settlement_exposure(tok_p50)
exposure_reduction = trad_exposure - tok_exposure

print(f"\nSettlement risk exposure (median settlement time, at a {DEFAULT_PROBABILITY_ANNUAL*100:.2f}%")
print(f"annual investment-grade default probability, Global Credit Data, 2025):")
print(f"  Traditional: ${trad_exposure:,.2f}")
print(f"  Tokenised:   ${tok_exposure:,.2f}")
print(f"  Reduction:   ${exposure_reduction:,.2f}")

generate_distribution_chart(trad_samples, tok_samples)
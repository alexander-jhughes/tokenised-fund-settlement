# cbdc_money_demand.py
# Illustrates the theoretical effect of a non-interest-bearing, transaction-only
# CBDC on real money demand, following the framework in Jobst and Lin (2016),
# as adapted in CBUAE's CBDC strategy report.
# This is a conceptual illustration, not a fitted or empirically estimated curve.
#
# Logic: a CBDC that pays no interest is a substitute for cash balances (the
# transactional component of money demand), not for interest-bearing bank
# deposits (the savings component). Introducing it is modelled as an inward
# shift of the money demand curve at a given real interest rate, rather than
# a shift in the money supply itself.

import matplotlib.pyplot as plt
import numpy as np
import os

def generate_chart():
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10.5

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    m = np.linspace(0.5, 10, 200)

    md_before = 10 / m
    md_after = 7 / m

    ax.plot(m, md_before, color="#9a9a9a", linewidth=1.8, linestyle="--", label="$M_D(Y)$: before")
    ax.plot(m, md_after, color="#0f2f4f", linewidth=2.2, label="$M'_D(Y)$: after")

    ms_level = 3.3
    ax.axvline(ms_level, color="#333333", linewidth=1.3)
    ax.text(ms_level, 3.15, "$M_S$", ha="center", fontsize=10, color="#333333")

    r_before = 10 / ms_level
    r_after = 7 / ms_level
    ax.plot([0, ms_level], [r_before, r_before], color="#9a9a9a", linewidth=0.9, linestyle=":")
    ax.plot([0, ms_level], [r_after, r_after], color="#0f2f4f", linewidth=0.9, linestyle=":")
    ax.annotate("", xy=(ms_level * 0.55, r_after), xytext=(ms_level * 0.55, r_before),
                arrowprops=dict(arrowstyle="->", color="#555555", linewidth=1.2))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_xlabel("Real money demand ($m = P/M$)", fontsize=9.5, color="#444444")
    ax.set_ylabel("Real interest rate ($r$)", fontsize=9.5, color="#444444")
    ax.set_title("Illustrative effect of a non-interest-bearing CBDC on real money demand",
                 fontsize=12, loc="left", pad=16, fontweight="bold", color="#111111")
    ax.legend(frameon=False, fontsize=9, loc="upper right")

    ax.grid(axis="both", which="major", linestyle="-", linewidth=0.4, alpha=0.15)
    ax.set_axisbelow(True)
    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#888888")
    ax.spines["bottom"].set_color("#888888")

    fig.text(0.5, -0.02,
              "Illustrative only, adapting the money-demand framework used in CBUAE's CBDC strategy "
              "report, attributed there to Jobst and Lin (2016). Not a fitted or empirically estimated relationship.",
              ha="center", fontsize=7.5, style="italic", color="#777777")

    os.makedirs("model/output", exist_ok=True)
    plt.tight_layout()
    plt.savefig("model/output/cbdc_money_demand.png", dpi=200, bbox_inches="tight")
    print("Chart saved to model/output/cbdc_money_demand.png")

generate_chart()
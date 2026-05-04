"""
=============================================================
  Epidemic Simulator — SIR / SEIR Models
  Author: Claude (Anthropic)
  Description: Models infectious disease spread using
               differential equations. Supports SIR and SEIR
               compartmental models with interactive CLI and
               multi-scenario comparison.
=============================================================
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from dataclasses import dataclass, field
from typing import Optional
import argparse
import sys


# ──────────────────────────────────────────────────────────────
# Data classes for model parameters and results
# ──────────────────────────────────────────────────────────────

@dataclass
class EpidemicParams:
    """Holds all parameters for a single simulation run."""
    N: int            = 100_000   # Total population size
    beta: float       = 0.30      # Transmission rate (contacts × prob. of transmission)
    gamma: float      = 0.10      # Recovery rate (1/gamma = mean infectious period in days)
    sigma: float      = 0.20      # SEIR only: incubation rate (1/sigma = mean latent period)
    I0: int           = 10        # Initial infected individuals
    E0: int           = 0         # SEIR only: initial exposed individuals
    days: int         = 180       # Simulation duration in days
    label: str        = "Scenario"# Label used in plots
    model: str        = "SIR"     # "SIR" or "SEIR"

    @property
    def R0(self) -> float:
        """Basic reproduction number: average secondary cases from one infective."""
        return self.beta / self.gamma

    @property
    def herd_immunity_threshold(self) -> float:
        """Fraction of population that must be immune to halt spread."""
        return 1.0 - 1.0 / self.R0 if self.R0 > 1 else 0.0


@dataclass
class SimulationResult:
    """Stores time-series output of a simulation."""
    t: np.ndarray
    S: np.ndarray
    I: np.ndarray
    R: np.ndarray
    E: Optional[np.ndarray]       # None for SIR
    params: EpidemicParams

    @property
    def peak_infected(self) -> int:
        return int(np.max(self.I))

    @property
    def peak_day(self) -> int:
        return int(np.argmax(self.I))

    @property
    def total_recovered(self) -> int:
        return int(self.R[-1])

    @property
    def attack_rate(self) -> float:
        """Fraction of population ever infected."""
        return self.total_recovered / self.params.N

    @property
    def daily_new_cases(self) -> np.ndarray:
        """Approximate daily incidence from change in S."""
        return np.maximum(0, -np.diff(self.S, prepend=self.S[0]))


# ──────────────────────────────────────────────────────────────
# ODE definitions
# ──────────────────────────────────────────────────────────────

def sir_odes(y, t, N, beta, gamma):
    """
    SIR differential equations.

    dS/dt = -β·S·I / N
    dI/dt =  β·S·I / N − γ·I
    dR/dt =  γ·I
    """
    S, I, R = y
    dS = -beta * S * I / N
    dI =  beta * S * I / N - gamma * I
    dR =  gamma * I
    return [dS, dI, dR]


def seir_odes(y, t, N, beta, sigma, gamma):
    """
    SEIR differential equations (adds Exposed compartment).

    dS/dt = -β·S·I / N
    dE/dt =  β·S·I / N − σ·E
    dI/dt =  σ·E       − γ·I
    dR/dt =  γ·I
    """
    S, E, I, R = y
    dS = -beta * S * I / N
    dE =  beta * S * I / N - sigma * E
    dI =  sigma * E - gamma * I
    dR =  gamma * I
    return [dS, dE, dI, dR]


# ──────────────────────────────────────────────────────────────
# Simulation runner
# ──────────────────────────────────────────────────────────────

def run_simulation(params: EpidemicParams) -> SimulationResult:
    """
    Integrate the ODE system for the given parameters.
    Returns a SimulationResult with full time-series data.
    """
    t = np.linspace(0, params.days, params.days * 10 + 1)  # 10 points/day for smooth curves
    N = params.N

    if params.model.upper() == "SIR":
        S0 = N - params.I0
        I0 = params.I0
        R0 = 0
        y0 = [S0, I0, R0]
        sol = odeint(sir_odes, y0, t, args=(N, params.beta, params.gamma))
        S, I, R = sol[:, 0], sol[:, 1], sol[:, 2]
        E = None

    elif params.model.upper() == "SEIR":
        S0 = N - params.I0 - params.E0
        E0 = params.E0
        I0 = params.I0
        R0 = 0
        y0 = [S0, E0, I0, R0]
        sol = odeint(seir_odes, y0, t, args=(N, params.beta, params.sigma, params.gamma))
        S, E, I, R = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3]

    else:
        raise ValueError(f"Unknown model '{params.model}'. Choose 'SIR' or 'SEIR'.")

    return SimulationResult(t=t, S=S, I=I, R=R, E=E, params=params)


# ──────────────────────────────────────────────────────────────
# Visualization
# ──────────────────────────────────────────────────────────────

COLORS = {
    "S": "#3266ad",
    "E": "#BA7517",
    "I": "#E24B4A",
    "R": "#3B6D11",
}

SCENARIO_PALETTE = [
    "#3266ad", "#E24B4A", "#3B6D11", "#BA7517",
    "#7F77DD", "#D4537E", "#378ADD", "#639922",
]


def plot_single(result: SimulationResult, save_path: Optional[str] = None):
    """
    Full dashboard plot for a single simulation:
    - Main epidemic curve (S, E, I, R)
    - Daily new cases bar chart
    - Stacked area (population breakdown)
    - Summary text box
    """
    p = result.params
    fig = plt.figure(figsize=(14, 9), facecolor="#fafafa")
    fig.suptitle(
        f"{p.model} Epidemic Simulation — {p.label}",
        fontsize=15, fontweight="bold", y=0.98, color="#222"
    )

    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.40, wspace=0.30)
    ax_main   = fig.add_subplot(gs[0, :])   # full-width top panel
    ax_daily  = fig.add_subplot(gs[1, 0])
    ax_stack  = fig.add_subplot(gs[1, 1])

    t, N = result.t, p.N

    # ── Main epidemic curve ──────────────────────────────────
    ax_main.plot(t, result.S / N * 100, color=COLORS["S"], lw=2.2, label="Susceptible (S)")
    if result.E is not None:
        ax_main.plot(t, result.E / N * 100, color=COLORS["E"], lw=2, ls="--", label="Exposed (E)")
    ax_main.plot(t, result.I / N * 100, color=COLORS["I"], lw=2.5, label="Infected (I)")
    ax_main.plot(t, result.R / N * 100, color=COLORS["R"], lw=2.2, label="Recovered (R)")

    # Mark peak
    ax_main.axvline(result.peak_day / 10, color=COLORS["I"], lw=1, ls=":", alpha=0.7)
    ax_main.annotate(
        f"Peak day {result.peak_day}",
        xy=(result.peak_day / 10, result.peak_infected / N * 100),
        xytext=(result.peak_day / 10 + p.days * 0.03, result.peak_infected / N * 100 + 3),
        fontsize=9, color=COLORS["I"],
        arrowprops=dict(arrowstyle="->", color=COLORS["I"], lw=1),
    )

    ax_main.set_xlabel("Days", fontsize=11)
    ax_main.set_ylabel("% of population", fontsize=11)
    ax_main.set_ylim(0, 105)
    ax_main.set_xlim(0, p.days)
    ax_main.legend(loc="center right", fontsize=10, framealpha=0.9)
    ax_main.grid(axis="y", color="gray", alpha=0.12, lw=0.7)
    ax_main.spines[["top", "right"]].set_visible(False)

    # Summary textbox
    summary = (
        f"R₀ = {p.R0:.2f}   |   β = {p.beta}   γ = {p.gamma}"
        + (f"   σ = {p.sigma}" if p.model == "SEIR" else "")
        + f"\nPeak infected: {result.peak_infected:,} ({result.peak_infected/N*100:.1f}%)"
        f"   on day {result.peak_day}"
        f"\nTotal ever infected: {result.total_recovered:,} ({result.attack_rate*100:.1f}%)"
        f"\nHerd immunity threshold: {p.herd_immunity_threshold*100:.1f}%"
    )
    ax_main.text(
        0.02, 0.97, summary,
        transform=ax_main.transAxes, fontsize=9, va="top", ha="left",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.85)
    )

    # ── Daily new cases ──────────────────────────────────────
    daily = result.daily_new_cases
    t_daily = np.arange(len(daily))
    ax_daily.bar(t_daily, daily, color=COLORS["I"], alpha=0.65, width=0.9, label="New cases/day")
    ax_daily.set_xlabel("Days", fontsize=10)
    ax_daily.set_ylabel("New infections", fontsize=10)
    ax_daily.set_title("Daily new infections", fontsize=11)
    ax_daily.set_xlim(0, p.days)
    ax_daily.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax_daily.grid(axis="y", color="gray", alpha=0.10, lw=0.7)
    ax_daily.spines[["top", "right"]].set_visible(False)

    # ── Stacked area ─────────────────────────────────────────
    pct_S = result.S / N * 100
    pct_I = result.I / N * 100
    pct_R = result.R / N * 100

    if result.E is not None:
        pct_E = result.E / N * 100
        ax_stack.stackplot(
            t, pct_S, pct_E, pct_I, pct_R,
            colors=[COLORS["S"], COLORS["E"], COLORS["I"], COLORS["R"]],
            labels=["S", "E", "I", "R"], alpha=0.75
        )
    else:
        ax_stack.stackplot(
            t, pct_S, pct_I, pct_R,
            colors=[COLORS["S"], COLORS["I"], COLORS["R"]],
            labels=["S", "I", "R"], alpha=0.75
        )

    ax_stack.set_xlabel("Days", fontsize=10)
    ax_stack.set_ylabel("% of population", fontsize=10)
    ax_stack.set_title("Population breakdown", fontsize=11)
    ax_stack.set_ylim(0, 100)
    ax_stack.set_xlim(0, p.days)
    ax_stack.legend(loc="lower left", fontsize=9, framealpha=0.9)
    ax_stack.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  Saved to: {save_path}")
    plt.show()


def plot_comparison(results: list[SimulationResult], save_path: Optional[str] = None):
    """
    Compare multiple simulation scenarios side-by-side.
    Overlays infected curves and shows summary table.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor="#fafafa")
    fig.suptitle("Scenario Comparison — Infected Population", fontsize=14, fontweight="bold", y=1.01)

    ax_abs, ax_pct = axes

    for i, res in enumerate(results):
        color = SCENARIO_PALETTE[i % len(SCENARIO_PALETTE)]
        t = res.t
        N = res.params.N
        lbl = f"{res.params.label} (R₀={res.params.R0:.2f})"

        ax_abs.plot(t, res.I, color=color, lw=2.2, label=lbl)
        ax_pct.plot(t, res.I / N * 100, color=color, lw=2.2, label=lbl)

    for ax, ylabel, title in [
        (ax_abs, "Infected individuals", "Absolute infected count"),
        (ax_pct, "% of population", "Infected as % of population"),
    ]:
        ax.set_xlabel("Days", fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_title(title, fontsize=11)
        ax.legend(fontsize=9, framealpha=0.9)
        ax.grid(axis="y", color="gray", alpha=0.12, lw=0.7)
        ax.spines[["top", "right"]].set_visible(False)

    # Print comparison table
    print("\n" + "="*72)
    print(f"{'Scenario':<22} {'Model':<6} {'R₀':>5} {'Peak I':>10} {'Peak day':>9} {'Attack%':>8}")
    print("-"*72)
    for res in results:
        p = res.params
        print(f"{p.label:<22} {p.model:<6} {p.R0:>5.2f} "
              f"{res.peak_infected:>10,} {res.peak_day:>9} "
              f"{res.attack_rate*100:>7.1f}%")
    print("="*72)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"\n  Saved comparison to: {save_path}")
    plt.show()


# ──────────────────────────────────────────────────────────────
# Interactive CLI
# ──────────────────────────────────────────────────────────────

def prompt_float(msg: str, default: float, lo: float, hi: float) -> float:
    while True:
        raw = input(f"  {msg} [{default}]: ").strip()
        val = float(raw) if raw else default
        if lo <= val <= hi:
            return val
        print(f"  ⚠  Please enter a value between {lo} and {hi}.")


def prompt_int(msg: str, default: int, lo: int, hi: int) -> int:
    while True:
        raw = input(f"  {msg} [{default}]: ").strip()
        val = int(raw) if raw else default
        if lo <= val <= hi:
            return val
        print(f"  ⚠  Please enter a value between {lo} and {hi}.")


def prompt_choice(msg: str, options: list, default: str) -> str:
    opts = "/".join(options)
    while True:
        raw = input(f"  {msg} ({opts}) [{default}]: ").strip().upper()
        val = raw if raw else default.upper()
        if val in [o.upper() for o in options]:
            return val
        print(f"  ⚠  Choose one of: {opts}")


def interactive_mode():
    """Run interactive CLI to configure and launch simulations."""
    print("\n" + "╔" + "═"*58 + "╗")
    print("║          EPIDEMIC SIMULATOR  —  SIR / SEIR              ║")
    print("╚" + "═"*58 + "╝\n")

    results = []
    while True:
        print(f"─── Scenario {len(results)+1} ─────────────────────────────────────")
        label   = input(  "  Scenario label [Scenario]: ").strip() or "Scenario"
        model   = prompt_choice("Model", ["SIR", "SEIR"], "SIR")
        N       = prompt_int  ("Population size",         100_000,  1_000, 10_000_000)
        beta    = prompt_float("Infection rate β",         0.30,    0.01,  2.0)
        gamma   = prompt_float("Recovery rate γ",          0.10,    0.01,  1.0)
        sigma   = prompt_float("Incubation rate σ (SEIR)", 0.20,    0.01,  1.0) if model == "SEIR" else 0.20
        I0      = prompt_int  ("Initial infected (I₀)",   10,       1,     N)
        days    = prompt_int  ("Simulation days",          180,      10,    3650)

        p = EpidemicParams(
            N=N, beta=beta, gamma=gamma, sigma=sigma,
            I0=I0, days=days, label=label, model=model
        )
        print(f"\n  ✓ R₀ = {p.R0:.3f}  |  "
              f"Herd immunity threshold: {p.herd_immunity_threshold*100:.1f}%\n")

        results.append(run_simulation(p))

        again = input("  Add another scenario? (y/n) [n]: ").strip().lower()
        if again != "y":
            break

    # Display results
    for res in results:
        plot_single(res)

    if len(results) > 1:
        plot_comparison(results)


# ──────────────────────────────────────────────────────────────
# CLI argument parser (non-interactive mode)
# ──────────────────────────────────────────────────────────────

def build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="SIR/SEIR Epidemic Simulator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--model",  default="SIR",    choices=["SIR","SEIR"], help="Compartmental model")
    parser.add_argument("--N",      type=int,   default=100_000, help="Population size")
    parser.add_argument("--beta",   type=float, default=0.30,    help="Transmission rate β")
    parser.add_argument("--gamma",  type=float, default=0.10,    help="Recovery rate γ")
    parser.add_argument("--sigma",  type=float, default=0.20,    help="Incubation rate σ (SEIR only)")
    parser.add_argument("--I0",     type=int,   default=10,      help="Initial infected count")
    parser.add_argument("--days",   type=int,   default=180,     help="Simulation duration in days")
    parser.add_argument("--label",  type=str,   default="Run 1", help="Scenario label")
    parser.add_argument("--compare",action="store_true",          help="Run built-in multi-scenario comparison")
    parser.add_argument("--save",   type=str,   default=None,    help="Save plot to this file path")
    return parser


def run_builtin_comparison(save_path: Optional[str] = None):
    """
    Demonstrates 4 scenarios: baseline, high-beta, interventions, SEIR.
    Useful for understanding how parameters shape the epidemic curve.
    """
    scenarios = [
        EpidemicParams(N=100_000, beta=0.30, gamma=0.10, days=300, label="Baseline (β=0.30)", model="SIR"),
        EpidemicParams(N=100_000, beta=0.50, gamma=0.10, days=300, label="High spread (β=0.50)", model="SIR"),
        EpidemicParams(N=100_000, beta=0.15, gamma=0.10, days=300, label="Intervention (β=0.15)", model="SIR"),
        EpidemicParams(N=100_000, beta=0.30, gamma=0.10, sigma=0.20, days=300, label="SEIR (σ=0.20)", model="SEIR"),
    ]
    results = [run_simulation(p) for p in scenarios]
    for r in results:
        plot_single(r)
    plot_comparison(results, save_path=save_path)


# ──────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────

def main():
    # No arguments → interactive mode
    if len(sys.argv) == 1:
        interactive_mode()
        return

    parser = build_cli_parser()
    args = parser.parse_args()

    if args.compare:
        run_builtin_comparison(save_path=args.save)
        return

    p = EpidemicParams(
        N=args.N, beta=args.beta, gamma=args.gamma, sigma=args.sigma,
        I0=args.I0, days=args.days, label=args.label, model=args.model,
    )
    print(f"\n{'='*50}")
    print(f"  Model: {p.model}  |  N={p.N:,}  |  β={p.beta}  γ={p.gamma}"
          + (f"  σ={p.sigma}" if p.model == "SEIR" else ""))
    print(f"  R₀ = {p.R0:.3f}  |  Herd immunity threshold: {p.herd_immunity_threshold*100:.1f}%")
    print(f"{'='*50}")

    result = run_simulation(p)

    print(f"\n  Peak infected : {result.peak_infected:,} on day {result.peak_day}")
    print(f"  Total infected: {result.total_recovered:,} ({result.attack_rate*100:.1f}% attack rate)")
    plot_single(result, save_path=args.save)


if __name__ == "__main__":
    main()

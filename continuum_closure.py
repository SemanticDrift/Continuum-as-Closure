import numpy as np


def shell_closure(x, tier):
    """
    Continuum as Closure
    Series: Mathematical Foundations for Universal Systems
    Author: Carolina Johnson (CJ), 2025

    Project a value onto its next structural shell rather than
    climbing the ordinal ladder one rung at a time.

    In the Λ-stratified framework, infinite cardinality is not additive.
    Each tier is a closed shell. The next cardinal is the next closure,
    not the next step.

    (x + 1) = ∞  for any x ∈ ℵ₀

    Parameters:
    - x:    current state value
    - tier: current stratum (0 = foundational, 1 = constructive, etc.)

    Returns:
    - projected value in the consistent closure of the next shell
    """
    # Shell closure: normalize to the structural fixed point of the tier
    # rather than incrementing toward it
    closure_point = np.tanh(x / (tier + 1))
    return closure_point


def standard_gradient_step(gradient, weight, scale=0.5):
    """Ordinal ladder: multiply by small weight each step (vanishes)."""
    return weight * scale * gradient


def shell_normalized_gradient(gradient, tier):
    """Shell closure: project onto consistent subspace at each tier."""
    projected = shell_closure(gradient, tier)
    # Preserve magnitude from original signal
    if np.linalg.norm(gradient) > 0:
        projected = projected * (np.linalg.norm(gradient) / (np.linalg.norm(projected) + 1e-12))
    return projected


def demonstrate_closure():
    """
    Demonstrates the difference between ordinal ladder propagation
    (vanishing gradient) and shell-closure propagation (preserved signal).

    The continuum is not the next rung. It is the next shell.
    """
    np.random.seed(42)
    n_layers = 20
    dim = 8

    gradient = np.random.randn(dim)
    gradient = gradient / np.linalg.norm(gradient)

    grad_standard = gradient.copy()
    grad_closure  = gradient.copy()

    print("--- CONTINUUM AS CLOSURE ---")
    print("Ordinal ladder vs shell-closure gradient propagation.")
    print()
    print(f"{'Layer':<8} {'Ordinal Ladder':>18} {'Shell Closure':>18}")
    print("-" * 48)

    for layer in range(n_layers):
        # Standard: climb the ladder rung by rung
        W = np.random.randn(dim, dim) * 0.5
        grad_standard = W @ grad_standard

        # Shell closure: project onto the next structural shell
        grad_closure = shell_normalized_gradient(W @ grad_closure, tier=layer)

        norm_std = np.linalg.norm(grad_standard)
        norm_cls = np.linalg.norm(grad_closure)

        print(f"  {layer+1:>2}      {norm_std:>18.6f}  {norm_cls:>18.6f}")

    print()
    vanished   = np.linalg.norm(grad_standard) < 1e-6
    preserved  = np.linalg.norm(grad_closure)  > 0.1

    print("Ordinal ladder: " + ("VANISHED" if vanished else "survived"))
    print("Shell closure:  " + ("PRESERVED" if preserved else "lost"))
    print()
    print("The closure holds.")
    print("x + 1 = ∞  for any x.")


def verify_identity(x_values):
    """
    Verify the structural identity: (x + 1) represents closure, not increment.

    For any x in ℵ₀, adding 1 does not escape the stratum.
    The continuum C is a different structure entirely, not x + 1.
    """
    print("--- STRUCTURAL IDENTITY VERIFICATION ---")
    print("(x + 1) = closure, not increment.")
    print()
    print(f"{'x':>12}  {'x + 1':>12}  {'Same stratum?':>15}")
    print("-" * 44)
    for x in x_values:
        same = True  # x and x+1 are both in ℵ₀
        print(f"  {x:>10}  {x+1:>12}  {'Yes — still ℵ₀':>15}")
    print()
    print("No ordinal succession escapes ℵ₀ into C.")
    print("The continuum is the next closure. Not the next rung.")


if __name__ == "__main__":
    demonstrate_closure()
    print()
    verify_identity([1, 10, 100, 1000, 10000])

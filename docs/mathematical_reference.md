# Mathematical reference

This reference explains the analytical models in the demonstrations. Measured errors and tested ranges belong to the [validation report](phase2_validation.md); plotting corrections belong to [Phase 3A](phase3a_review.md). These are ideal, two-dimensional incompressible flows, locally irrotational away from singularities, not numerical solutions of viscous flow equations.

## Coordinates and conventions

Cartesian coordinates are $(x,y)$ in meters; velocity components $(u,v)$ are in m/s. Polar coordinates relative to each model's center are $r$ and counterclockwise angle $\theta$ measured from $+x$. $U$ is freestream speed, $\alpha$ its angle, $R$ cylinder radius, $m$ source strength per unit depth, $\Gamma$ circulation, and $\rho$ density. $m$ and $\Gamma$ have units $\mathrm{m^2/s}$; potential $\phi$ and stream function $\psi$ have the same units.

$$
u=\phi_x=\psi_y,\qquad v=\phi_y=-\psi_x,
\qquad u_x+v_y=0,\qquad \omega_z=v_x-u_y=0.
$$

Subscripts indicate partial derivatives. The stream-function convention ensures continuity for smooth fields; a velocity potential additionally requires local irrotationality. Both scalar functions satisfy Laplace's equation in smooth potential-flow regions. Streamlines are constant-$\psi$ curves. An impermeable stationary boundary has zero normal velocity, hence constant $\psi$ along it.

## Elementary fields and superposition

**Uniform flow** (`uniform.py`):

$$
u=U\cos\alpha,\quad v=U\sin\alpha,\quad
\phi=U(x\cos\alpha+y\sin\alpha),\quad
\psi=U(y\cos\alpha-x\sin\alpha).
$$

**Point source/sink** (`source_or_sink`): for $\Delta x=x-x_r$, $\Delta y=y-y_r$, $r=\sqrt{\Delta x^2+\Delta y^2}$ and $\theta=\operatorname{atan2}(\Delta y,\Delta x)$,

$$
\phi=\frac{m}{2\pi}\ln\frac r{r_{ref}},\quad
\psi=\frac{m}{2\pi}\theta,\quad
(u,v)=\frac{m}{2\pi r^2}(\Delta x,\Delta y),\quad
u_r=\frac{m}{2\pi r}.
$$

$r_{ref}$ is one coordinate unit (1 m for these examples). Positive $m$ creates outward flux, negative $m$ a sink. The center is singular; the principal angular stream function has a branch cut. The helper returns NaNs at exactly $r=0$.

**Superposition** (`uniform_source_sink.py`, `rankine.py`): add each component's potential, stream function and velocities. Linearity preserves continuity and local irrotationality where the constituent solutions are smooth. Boundary geometry is determined by the resulting streamlines, not by arbitrary additions to the equations.

**Free vortex** (`vortex.py`):

$$
(u,v)=\frac{\Gamma}{2\pi r^2}(-\Delta y,\Delta x),\quad
V_\theta=\frac{\Gamma}{2\pi r},\quad
\psi=-\frac{\Gamma}{2\pi}\ln\frac r{r_{ref}},\quad
\oint\mathbf V\cdot d\mathbf l=\Gamma.
$$

Positive circulation is counterclockwise. Local vorticity is zero outside the singular center despite nonzero circulation on loops enclosing it. A local potential is $\Gamma\theta/(2\pi)$, but the vortex demo does not evaluate it. Its excluded central disk is for plotting, not a viscous-core model. Finite-difference vorticity residuals are discretization effects.

## Rankine oval

`rankine.py` combines uniform flow along $+x$, a source of strength $m>0$ at $(-a,0)$ and a sink of strength $-m$ at $(a,0)$:

$$
\psi=Uy+\frac m{2\pi}\left[\operatorname{atan2}(y,x+a)-\operatorname{atan2}(y,x-a)\right].
$$

The closed part of $\psi=0$ defines the oval. Along the axis outside the centers,

$$
u(x,0)=U-\frac{ma}{\pi(x^2-a^2)},\qquad
x_{stag}=\pm\sqrt{a^2+\frac{ma}{\pi U}}.
$$

The half-height $H>0$ satisfies $UH=(m/\pi)\arctan(a/H)$. The zero level also contains axis branches, so it cannot be treated indiscriminately as one body boundary. The corrected contour mask excludes the source-sink angular cut at grid resolution, with `corner_mask=False`; a resolution check rejects inadequately sampled thin shapes.

The featured exterior-flow asset additionally masks grid points inside a path assembled from the actual upper/lower contour arcs and analytical stagnation tips. Its gray fill depicts the equivalent excluded body region. This is an export-only visualization step; `rankine.py` retains the complete analytical superposition. See the [asset report](phase4a_assets.md).

## Doublet and cylinder flow

`cylinder_flow.py` uses uniform flow plus a doublet of strength $\mu=UR^2$. With $\beta=\theta-\alpha$,

$$
\phi=U\left(r+\frac{R^2}{r}\right)\cos\beta,\quad
\psi=U\left(r-\frac{R^2}{r}\right)\sin\beta,
$$

$$
V_r=U\left(1-\frac{R^2}{r^2}\right)\cos\beta,\quad
V_\theta=-U\left(1+\frac{R^2}{r^2}\right)\sin\beta.
$$

At $r=R$, $V_r=0$: the circular surface is impermeable. Interior samples are excluded. Cartesian components are $u=V_r\cos\theta-V_\theta\sin\theta$ and $v=V_r\sin\theta+V_\theta\cos\theta$.

`lift_cyl.py` adds $\Gamma/(2\pi r)$ to $V_\theta$ and $-\Gamma\ln(r/R)/(2\pi)$ to $\psi$. The normal boundary condition is unchanged; surface speed becomes asymmetric.

## Pressure and forces

Steady Bernoulli flow with a common freestream pressure gives

$$
C_p=\frac{p-p_\infty}{\tfrac12\rho U^2}=1-\frac{|\mathbf V|^2}{U^2}.
$$

For the surface, $V_r=0$, so $C_p=1-(V_\theta/U)^2$. Without circulation, $C_p=1-4\sin^2(\theta-\alpha)$. `lift_cyl.py` evaluates the exterior pressure field; `cyl_pressure_plot.py` evaluates surface curves for several circulations with $\alpha=0$.

Pressure acts opposite the outward normal. The latter script integrates gauge pressure $p_g=\tfrac12\rho U^2 C_p$:

$$
F_x'=-R\int_0^{2\pi}p_g\cos\theta\,d\theta,\qquad
F_y'=-R\int_0^{2\pi}p_g\sin\theta\,d\theta.
$$

Primes denote force per unit span in N/m. Kutta-Joukowski gives $(F_x',F_y')=\rho U\Gamma(\sin\alpha,-\cos\alpha)$. Thus for flow along $+x$, $L_y'=-\rho U\Gamma$ and ideal drag is zero. The numerical integrals use `np.trapezoid`; they do not model viscous drag.

## Joukowski airfoil

`joukowski_airfoil.py` uses complex cylinder-plane coordinate $z$, center $z_c$, $w=z-z_c$ and radius $R=|a-z_c|$, placing $z=a$ on the circle. Here $a$ is the mapping parameter, distinct from the Rankine half-separation.

$$
\zeta=z+\frac{a^2}{z},\qquad
W=U\left(e^{-i\alpha}w+\frac{R^2e^{i\alpha}}w\right)+\frac{\Gamma}{2\pi i}\ln\frac wR,
\qquad \psi=\operatorname{Im}W.
$$

The imaginary part defines mapped streamlines. The circle transforms to an airfoil with a sharp trailing edge at $\zeta=2a$. With $\theta_{te}=\arg(a-z_c)$, the script chooses

$$
\Gamma=4\pi RU\sin(\theta_{te}-\alpha).
$$

This Kutta condition sets $W'(a)=0$ where $J'(a)=0$. In validation, mapped velocity $u-iv=W'(z)/J'(z)$ approaches the removable limit $W''(a)/J''(a)$ rather than an infinite speed. This is an imposed trailing-edge condition, not a viscous simulation. The demonstration itself plots contours and geometry, not mapped velocity, airfoil pressure or lift.

## Analytical fields versus plotting

Equations are evaluated on sampled grids; contour interpolation, numerical streamline tracing and optional finite differences are visualization/diagnostic procedures. Singular masks and percentile color limits do not change analytical velocities. No boundary-layer, separation, stall or real-drag prediction is implemented. Rotational scratchpads `fun.py` and `test.py` are outside these potential-flow claims.

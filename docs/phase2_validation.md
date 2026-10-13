# Phase 2 mathematical validation - 2026-10-12

## Result and scope

The active flow equations and circulation signs passed the checks below. No active physics-equation error was found in the tested parameter ranges. A reproducible Rankine mask limitation was confirmed; it can hide the correct dividing streamline for thin ovals. No plotting module or demonstration script was modified.

This pass evaluated 225 parameter/check cases using Python 3.14.7, NumPy 2.5.3, and Matplotlib 3.11.2 with Agg. Script calculation statements were executed in memory from their actual syntax trees, with parameter assignments overridden and display calls omitted. Supplementary analytical calculations independently checked derivatives, surface conditions, circulation, roots, and forces. Selected contours were generated and checked numerically; this was not a manual visual review or a repeat of Phase 1's full interactive-script runs.

## Validation table

Errors are maximum absolute errors over the stated safe region or tested parameter set. Velocities are m/s, flux/circulation/stream-function values m^2/s, force per span N/m, and divergence/vorticity 1/s. Relative velocity errors use a characteristic speed, not pointwise division near stagnation.

| Model | Independent check | Numerical result | Assessment |
| --- | --- | --- | --- |
| Uniform flow | Both potential and stream-function derivatives; continuity and curl | Velocity error <= 1.803e-13; divergence/curl <= 2.132e-14 | Pass, roundoff |
| Sources/sinks | Derivatives, radial direction, closed-circle flux = m | Finest velocity error 2.331e-04; sampled flux error 0.000e+00 | Pass outside center/cut |
| Free vortex | Local potential/stream-function derivatives; CCW circulation = Gamma | Finest velocity error 5.226e-04; grid-loop circulation error 9.103e-06 | Pass, second-order residuals |
| Angled source/sink superposition | Independent Cartesian component sum and derivatives | Sum error 3.553e-15; finest derivative error 6.558e-04 | Pass |
| Rankine oval | Stagnation roots, upper dividing streamline, height equation | Stagnation speed 1.332e-15; exact boundary psi residual 3.553e-15; finest contour psi residual 2.453e-04 | Equations pass; fixed mask limitation |
| Rankine half-body | Elementary uniform+source combination, supplementary only | Stagnation speed 4.441e-16; boundary psi residual 1.776e-15 | No dedicated demo implemented |
| Doublet/cylinder velocity | Source/sink doublet limit; derivatives of cylinder fields | Cylinder finest velocity error 6.389e-04; pair-limit errors decrease about 4x per halving separation | Pass |
| Cylinder surface/pressure/lift | Normal/tangential velocity, stagnation, Bernoulli, pressure integration | Normal velocity 0 analytically (fluid-side derivative residual 1.205e-09); stagnation speed 5.329e-15; force error 1.705e-13; drag 8.527e-14 | Pass for both circulation signs |
| Joukowski airfoil | Geometry, Kutta numerator, complex derivative, chain rule, mapped boundary/circulation | Potential derivative error 2.052e-10; mapped derivative error 1.268e-10; normal error 7.658e-13 | Pass for tested valid circles |
| Rotational experiments | Polynomial stream function, divergence=0, curl=-1 | Velocity error 1.137e-12; curl residual 2.842e-13 | Correctly rotational; no potential |

## Equations, parameters, and exclusions

- Convention: u=psi_y=phi_x, v=-psi_x=phi_y. Uniform flow used U={1.2,2,3.5} and angles {-66,0,30} degrees on 101^2, 201^2, 401^2 grids.
- Source/sink: k=m/(2*pi), phi=k*log(r/r_ref), with r_ref=1 m, psi=k*atan2(dy,dx), (u,v)=k*(dx,dy)/r^2. Strengths +/-2 and +/-10, center (0.13,-0.17), and circle radii 0.5,1,2 were tested. Outward/inward radial directions and zero tangential components agree with the sign of m.
- Vortex: (u,v)=Gamma*(-dy,dx)/(2*pi*r^2), psi=-Gamma*log(r)/(2*pi); local phi=Gamma*theta/(2*pi) was supplied only for validation. Gamma={-7,7,15}; 151^2, 301^2, 601^2 grids; closed circles and an actual Cartesian-grid square loop were checked. Positive Gamma is counterclockwise. Local curl is zero outside the core despite nonzero circulation around it.
- Derivative comparisons use second-order NumPy gradients, omit two outer grid rows/columns, and exclude centers/masks plus unsafe branch-cut stencils. Source/sink cores are excluded to r>0.8 m; vortex comparisons use r>0.75 m; cylinder comparisons use r>R+0.4 m. Angular cuts are excluded with a 3-grid-spacing buffer. These distances are validation regions, not changes to the physical model.
- Relative speed scales are U for uniform/superposed/cylinder flows, |m|/(2*pi*0.8) for isolated sources, and |Gamma|/(2*pi*0.75) for vortices. Finest-grid errors were below 5e-4 of these scales; all five nonlinear derivative groups improved by more than 3.5x per halving spacing. Exact identities used 1e-10 absolute tolerances in the units above. Complex finite-difference velocity checks used 1e-8 m/s tolerance with step 1e-5 m. These bounds apply only to the tested ranges.

### Rankine and doublet checks

For a source at (-a,0) and sink at (+a,0), u(x,0)=U-m*a/[pi*(x^2-a^2)], giving stagnation x=+/-sqrt(a^2+m*a/(pi*U)). The upper/lower dividing boundaries have psi=0 away from the segment cut. Independently bisected upper-boundary roots also satisfy H=a*cot(pi*U*H/m) at x=0. These are the same defining checks posed in [MIT's Rankine-body exercise](https://ocw.mit.edu/courses/2-25-advanced-fluid-mechanics-fall-2013/aac01df13a68b0ab7838ae459dfc1a14_MIT2_25F13_Problem6.4.pdf).

Tested (U,m,a)=(2,10,3), (1.5,4,1), (3,20,2), each at three resolutions with domain extent 1.5 times the stagnation distance. Default stagnation x=+/-3.711421 m (rounded). Actual linearly interpolated contour vertices were evaluated against the analytical psi; only vertices outside the cut strip and axis were compared. The zero level also contains exterior x-axis branches; it should not be treated as a single closed polygon automatically.

The half-body is supplementary, not a feature claim: x_stag=-m/(2*pi*U), upper boundary psi=m/2, lower boundary psi=-m/2 on the principal-angle branches, and downstream half-width m/(2*U). Cases (U,m)=(2,4),(3,10) passed.

The doublet limit holds with mu=m*a/pi fixed. Using mu=2 and a={0.1,0.05,0.025} m, the maximum velocity differences from (u,v)=mu*(y^2-x^2,-2xy)/r^4 outside r>=1 m were 1.946e-2, 4.842e-3, 1.209e-3 m/s. The cylinder uses mu=U*R^2.

### Cylinder boundary, pressure, and signs

At r=R, vr=0 and vt=-2*U*sin(theta-alpha)+Gamma/(2*pi*R). Surface stagnation angles satisfy sin(theta-alpha)=Gamma/(4*pi*U*R). When the magnitude of that ratio exceeds 1, surface stagnation points disappear; the exterior point lies at r/R=|k|+sqrt(k^2-1), theta=alpha+sign(k)*pi/2. Both regimes were checked.

Bernoulli gives Cp=1-(vt/U)^2 and, without circulation, Cp=1-4*sin^2(theta-alpha). Pressure forces were integrated against outward normal components over closed angle intervals. With positive circulation counterclockwise, the force per span is (Fx,Fy)=rho*U*Gamma*(sin(alpha),-cos(alpha)); projection along freestream is zero. The lift/circulation principle is summarized in [MIT's potential-flow lecture](https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec1011/node45.html); the vector sign here was independently derived and integrated for this repository's convention.

Tested (U,R)=(2,1),(4.5,1.4), alpha={-66,0,30} degrees, Gamma/(4*pi*U*R)={-1.2,-1,-0.5,0,0.5,1,1.2}, rho=1.225, and 181/721 angular points. Cartesian derivative checks also evaluated the actual lifting script with Gamma=-20,0,+20. Tangential velocities independently differentiated from surface phi converge: worst errors are 1.828e-3 and 1.142e-4 m/s at the two angular resolutions. Actual cyl_pressure_plot.py final-case lift and drag were checked too. Direct boundary-limit evaluation of the lifting script gives a maximum Cartesian normal residual of 8.882e-16 m/s, with tangential velocity and Cp matching the independent surface equations for Gamma=-20,0,+20. The physical interior masks were bypassed only in memory to evaluate the analytic limit at R. Default lift_cyl.py lift is +119.970 N/m in y. The nearly exact periodic trapezoidal force results reflect smooth trigonometric integrands; they are not a general accuracy guarantee for arbitrary pressure data.

### Joukowski geometry and velocity

Tested a=1 m, U=3 m/s, circle centers -0.05, -0.05+0.10i, -0.08-0.08i m, and alpha={-15,-5,0,10,20} degrees. R=|a-zc| places +a on the circle; zero and -a lie strictly inside all tested circles. J(z)=z+a^2/z, J'(z)=1-a^2/z^2, and J'(a)=0. Locally J(z)-2a ~ (z-a)^2/a, producing the sharp trailing edge. A user-selected circle that leaves zero or -a in the exterior needs separate review.

With w=z-zc, W=U*(exp(-i*alpha)*w+R^2*exp(i*alpha)/w)+Gamma*log(w/R)/(2*pi*i). Its derivative is Q=dW/dz=U*(exp(-i*alpha)-R^2*exp(i*alpha)/w^2)+Gamma/(2*pi*i*w)=u-i*v. Independent polar velocities and finite differences in both Cartesian directions agree. The mapped velocity is dW/dzeta=Q/J'(z), verified using local inverse-map finite differences, mapped boundary normals, and circulation integrals. The chain-rule construction is described in [the university-hosted Joukowski teaching notes](https://www-mdp.eng.cam.ac.uk/web/library/enginfo/aerothermal_dvd_only/aero/jouk/jouk.html); no pressure or airfoil lift model was added.

Gamma=4*pi*R*U*sin(theta_te-alpha), theta_te=arg(a-zc), makes Q(a)=0. The finite mapped limit is W''(a)/J''(a)=a*W''(a)/2; mapped velocity need not be zero at the trailing edge. Exterior radial and slightly oblique approaches converged to this limit. For the default geometry, radial errors at epsilon={1e-3,1e-5,1e-7} were 8.155e-4, 8.162e-6, 8.233e-8 m/s. A deliberately incorrect 1% circulation perturbation instead produced speeds approximately proportional to 1/epsilon.

## Numerical convergence and limitations

| Smooth field | Grids | Max velocity error, coarse -> middle -> fine (m/s) | Finest max divergence / curl (1/s) |
| --- | --- | --- | --- |
| Source/sink | 101^2, 201^2, 401^2 | 3.699e-03 -> 9.325e-04 -> 2.331e-04 | 1.748e-03 / 1.745e-03 |
| Vortex | 151^2, 301^2, 601^2 | 8.036e-03 -> 2.005e-03 -> 5.226e-04 | 4.076e-03 / 4.171e-03 |
| Superposition | 101^2, 201^2, 401^2 | 1.058e-02 -> 2.628e-03 -> 6.558e-04 | 4.847e-03 / 4.705e-03 |
| Rankine oval | 101^2, 201^2, 401^2 | 1.532e-02 -> 3.823e-03 -> 9.554e-04 | 7.023e-03 / 7.126e-03 |
| Cylinders | 101^2, 201^2, 401^2 | 1.025e-02 -> 2.557e-03 -> 6.389e-04 | 2.694e-03 / 2.713e-03 |

Nonzero smooth-field divergence/curl are truncation residuals and shrink roughly as spacing squared. Exclusions must include a stencil buffer: in the default vortex, 44 cells outside the 0.25 m mask still have NaN numerical vorticity because adjacent derivative samples are masked, reaching r=0.27487 m. They are not physical vorticity. The existing r>0.75 m diagnostic avoids that halo.

Actual vortex-grid closed-loop circulation errors decrease from 1.456e-4 to 3.641e-5 to 9.103e-6 m^2/s. Supplementary float32/float64 source calculations on a 201^2 grid give maximum velocity errors 9.072e-4/9.040e-4 m/s: spatial truncation dominates there. The shared helper converts coordinate arrays to float64; float32 input precision already lost before conversion cannot be recovered.

Exact source centers return NaN in all five helper outputs. However, linspace(-5,5,301) represents the point intended as x=0.1 by 0.09999999999999964. Relative to a center at 0.1, that is a nonzero 3.608e-16 m offset and gives 4.411e15 m/s for m=10. This is a floating-point sampling artifact on top of the true 1/r singularity, not a sign or source-strength error. Percentile colors do not regularize those velocities.

The Joukowski angular seam agrees to <4e-15 in coordinates/psi, and no folded triangles were detected in the tested default grids for the 15 geometry/angle cases. Its logarithmic branch jump is in phi, not psi, so it does not introduce a jump in the plotted stream function. Default-grid geometry avoids the circle by starting at 1.002 R and the sampled polygon may miss the exact cusp. Closest polygon distances from the exact trailing edge were at most 3.323e-7 m for the tested geometries.

Mapped contour psi residuals for (radial,angular) sizes (110,250), (220,500), (440,1000) were 2.610e-4, 6.682e-5, 1.634e-5 m^2/s at levels {-6,-3,0,3,6}. One interpolated vertex on the coarse grid mapped slightly inside the source circle and was excluded from the exterior comparison; none did at default/fine resolution. This is a mesh/interpolation limitation, not an equation error. These tests do not prove that arbitrary grids cannot produce visual artifacts.

Directly evaluating Q/J' extremely close to the Kutta point subtracts nearly equal numbers. Default-case error improves to 8.233e-8 m/s at epsilon=1e-7, then worsens to 6.183e-7, 5.680e-5, 5.948e-3 at epsilon=1e-9,1e-11,1e-13. At the exact point the quotient is 0/0. A future mapped-velocity implementation should evaluate the removable limit explicitly rather than sample at machine precision. The current script plots psi and does not evaluate this quotient.

## Discrepancies and recommended next actions

1. **Confirmed plotting limitation - Rankine cut mask:** at U=2, m=0.2, a=1, the independently computed maximum half-height is 0.0484587 m. The script masks |y|<0.06 m for |x|<a, so true upper/lower boundary points at x=0 are hidden even on a resolved 401^2 grid. Necessary before claiming robust parameter changes: use a cut mask tied to grid spacing, verify it does not obscure the body, and refine when body height approaches stencil width. This changes plotting exclusions, not the equations; no correction was made in this pass.
2. **Numerical limitations:** exact-point source masking can miss representational near-centers; derivative stencils cross mask edges; contour interpolation and trailing-edge cancellation require resolution checks. If robust near-center visualizations are needed, exclude an explicitly documented grid-sized unresolved core without changing the analytical fields. Retain characteristic-scale error checks rather than relative errors at zero velocity.
3. **Confirmed incomplete experiment:** test.py's unused phi returns None. The active u=3y,v=2x has curl=-1, so adding an irrotational potential for that field would be mathematically incorrect. Its active stream-function and velocity plots are consistent; keep the placeholder out of potential-flow claims.
4. **Optional improvements:** resolve/specially sample the Joukowski cusp, add lightweight repeatable numerical checks later, and only then consider mapped pressure or airfoil lift. A half-body demonstration remains optional. No speculative flow equations, assumptions, or circulation signs need correction based on this pass.

All Python source-file hashes matched before and after the validation. No deletion, dependency installation, commit, push, history rewrite, remote change, or publication was performed.

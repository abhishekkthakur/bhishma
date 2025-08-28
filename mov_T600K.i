[Mesh]
    type = GeneratedMesh
    dim = 2
    #elem_type = HEX8
    elem_type = QUAD4
    #distribution = DEFAULT
    nx = 128
    ny = 128
    nz = 0
    xmin = 0
    xmax = 128
    ymin = 0
    ymax = 128
    zmin = 0
    zmax = 0
    #uniform_refine = 2
[]

[Variables]
    [./c]
        order = FIRST
        family = LAGRANGE
        scaling = 1e+04
    [../]
    [./w]
        order = FIRST
        family = LAGRANGE
    [../]
[]

[ICs]
    [./concentrationIC]
        type = RandomIC
        variable = c
        #min = 0.44774
        #max = 0.48774
        min = 0.48000
        max = 0.52000
    [../]
[]

[BCs]
    [./Periodic]
        [./c_bcs]
            auto_direction = 'x y'
        [../]
    [../]
[]

[Kernels]
  [./w_dot]
    variable = w
    v = c
    type = CoupledTimeDerivative
  [../]
  [./coupled_res]
    variable = w
    type = SplitCHWRes
    mob_name = M
  [../]
  [./coupled_parsed]
    variable = c
    type = SplitCHParsed
    f_name = f_loc
    kappa_name = kappa_c
    w = w
  [../]
[]

[Materials]
  [./constants]
    type = GenericFunctionMaterial
    block = 0
    prop_names = 'kappa_c M'
    prop_values = '1.3832e-15*6.24150934e+18*1e+09^2*1e-27 2.2841e-26*1e+09^2/6.24150934e+18/1e-27'
  [../]
  [./local_energy]
    type = DerivativeParsedMaterial
    block = 0
    f_name = f_loc
    args = c
    constant_names = 'T   R  eV_J  d'
    constant_expressions = '600.0 8.314 6.24150934e+18 1e-27'
    function = 'eV_J*d*((-7930.43+133.346053*T-24.134*T*log(T)-3.098*0.001*T*T+0.12175*0.000001*T*T*T+69460/T)*c+(-7746.302+131.9197*T-23.56414*T*log(T)-3.443396*0.001*T*T+0.566283*0.000001*T*T*T+65812/T-0.130927*0.000000001*T*T*T*T)*(1-c)+R*T*(c*log(c)+(1-c)*log(1-c))+c*(1-c)*(-14800.01+13.0712*T+9*(1-2*c)+(-33315+12.9*T)*(1-2*c)*(1-2*c)))'
    derivative_order = 2
  [../]
  [./precipitate_indicator]  # Returns 1/2500 if precipitate
      type = ParsedMaterial
      f_name = prec_indic
      args = c
      function = if(c>0.6,0.000061035,0)
  [../]
  [./precipitate_indicator2]  # Returns 1/2500 if precipitate
      type = ParsedMaterial
      f_name = prec_indic2
      args = c
      function = if(c<0.4,0.000061035,0)
  [../]
[]

[GlobalParams]
  block = 0           # The generated mesh is used for all materials and kernels
[]

[Preconditioning]
  [./coupled]
    type = SMP
    full = true
  [../]
[]

[Executioner]
  type = Transient
  solve_type = NEWTON
  l_max_its = 30
  l_tol = 1e-6
  nl_max_its = 50
  nl_abs_tol = 1e-9
  end_time = 8640000
  petsc_options_iname = '-pc_type -ksp_grmres_restart -sub_ksp_type -sub_pc_type -pc_asm_overlap'
  petsc_options_value = 'asm      31                  preonly ilu          1'
  [./TimeStepper]
    type = IterationAdaptiveDT
    dt = 10
    cutback_factor = 0.8
    growth_factor = 1.5
    optimal_iterations = 7
  [../]
  #[./Adaptivity]
  #  coarsen_fraction = 0.1
  #  refine_fraction = 0.7
  #  max_h_level = 2
  #[../]
[]

[AuxVariables]
  [./f_density]   # Local energy density (eV/mol)
    order = CONSTANT
    family = MONOMIAL
  [../]
[]

[AuxKernels]
  # Calculates the energy density by combining the local and gradient energies
  [./f_density]   # (eV/mol/nm^2)
    type = TotalFreeEnergy
    variable = f_density
    f_name = 'f_loc'
    kappa_names = 'kappa_c'
    interfacial_vars = c
  [../]
[]

[Postprocessors]
  [./step_size]             # Size of the time step
    type = TimestepSize
  [../]
  #[./iterations]            # Number of iterations needed to converge timestep
  #  type = NumNonlinearIterations
  #[../]
  [./nodes]                 # Number of nodes in mesh
    type = NumNodes
  [../]
  #[./evaluations]           # Cumulative residual calculations for simulation
  #  type = NumResidualEvaluations
  #[../]
  [./precipitate_area]      # Fraction of surface devoted to precipitates
    type = ElementIntegralMaterialProperty
    mat_prop = prec_indic
  [../]
  [./precipitate_area2]      # Fraction of surface devoted to precipitates
    type = ElementIntegralMaterialProperty
    mat_prop = prec_indic2
  [../]
  [./total_energy]          # Total free energy at each timestep
    type = ElementIntegralVariablePostprocessor
    variable = f_density
  [../]
  #[./precipitate_area_two]      # Fraction of surface devoted to precipitates
  #type = ElementIntegralMaterialProperty
  #mat_prop = prec_indic_two
  #[../]
  [./minConc]
    type = ElementExtremeValue
    variable = c
    value_type = min
  [../]
  [./maxConc]
    type = ElementExtremeValue
    variable = c
    value_type = max
  [../]
[]

[Outputs]
  exodus = true
  console = true
  csv = true
  perf_graph = true
  #output_initial = true
  #[./console]
  #  type = Console
  #  max_rows = 10
  #[../]
[]

[Debug]
  show_var_residual_norms = true
[]

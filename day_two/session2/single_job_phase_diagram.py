
import numpy as np
import freud
import hoomd
import gsd.hoomd

for pressure in np.arange(1.0,10.0):

    #choose here which device to run on
    # device = hoomd.device.CPU()
    device = hoomd.device.GPU()

    seed = np.random.randint(1,1e4)
    print('random seed is ', seed)

    simulation = hoomd.Simulation(device = device, seed = seed)

    #Here we'll set how fast the temperature changes
    #We can set the system to equilibrate pressure first, then temperature
    kT = hoomd.variant.Ramp(A=0.5, B=2.0, t_start=int(1e4), t_ramp=int(1e5))

    pressure = pressure

    #Change these to change the interparticle forces
    epsilon = 1.0
    sigma = 1.0

    num_replicas = 6

    #We have to change the number of particles to reflect the FCC lattice
    N_particles = 4*num_replicas**3

    #We will directly load from one initial FCC lattice file
    simulation.create_state_from_gsd(filename='initial_state.gsd')


    #We will need to choose an integrator and thermostat which can be used with a box
    #that is changing in volume to hold pressure constant
    integrator = hoomd.md.Integrator(dt = 0.005)
    thermostat = hoomd.md.methods.thermostats.Bussi(kT=kT)

    #HOOMD takes in a stress tensor S but we can assume simple isotropic pressure
    npt = hoomd.md.methods.ConstantPressure(filter = hoomd.filter.All(),thermostat=thermostat,
    										S = pressure, tauS = 1.0, couple="xyz")
    integrator.methods.append(npt)


    #hoomd uses a Neighbor List (nlist) to speed up computation
    #by only checking forces for particles that are near each other
    cell = hoomd.md.nlist.Cell(buffer=0.4)

    #Define the force for different particles
    lj = hoomd.md.pair.LJ(nlist=cell)

    lj.params[('A', 'A')] = {"epsilon":epsilon, "sigma":sigma}

    lj.r_cut[('A', 'A')] = 2.7*sigma

    integrator.forces.append(lj)
    simulation.operations.integrator = integrator

    simulation.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=0.5)


    #Set up writers to save data
    thermodynamic_properties = hoomd.md.compute.ThermodynamicQuantities(
        filter=hoomd.filter.All())

    simulation.operations.computes.append(thermodynamic_properties)

    logger = hoomd.logging.Logger(categories=['scalar', 'sequence'])
    logger.add(simulation)
    logger.add(thermodynamic_properties)

    hdf5_writer = hoomd.write.HDF5Log(
        trigger=hoomd.trigger.Periodic(int(1e3)), 
        filename='log_{}.h5'.format(pressure), mode='x', logger=logger
    )

    simulation.operations.writers.append(hdf5_writer)

    gsd_writer = hoomd.write.GSD(
        filename='trajectory_{}.gsd'.format(pressure),
        trigger=hoomd.trigger.Periodic(int(1e3)),
        mode='xb',
        filter=hoomd.filter.All(),
    )

    simulation.operations.writers.append(gsd_writer)

    #Use this code if you want to save a DCD file for VMD visualization
    # dcd = hoomd.write.DCD(trigger=hoomd.trigger.Periodic(int(1e3)),
    #                       filename='trajectory_{}.dcd'.format(pressure))
    # simulation.operations.writers.append(dcd)

    tps_tracking = hoomd.logging.Logger(categories=['scalar', 'string'])
    tps_tracking.add(simulation, quantities=['timestep', 'tps'])

    table = hoomd.write.Table(trigger=hoomd.trigger.Periodic(period=int(1e4)), logger=tps_tracking)
    simulation.operations.writers.append(table)


    #finally, run the simulation
    timesteps = int(1e4+1e5)
    simulation.run(timesteps)

    simulation.operations.writers.remove(hdf5_writer)
    gsd_writer.flush()
    simulation.operations.writers.remove(gsd_writer)




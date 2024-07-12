Files for running and analyzing a rough melting study of the phase coexistence of the Lennard-Jones fluid.

There are multiple ways to do this, including on the CPU (slow), the GPU (fast but expensive), and the route we're going to take, CPU array jobs.

To submit the melting run simulations, choose a set of pressures (it will default to integers like a python range) and run the following command:

```
sbatch --array=Pinit-Pfinal array-cpu.slurm
```

See the SLURM array documentation for more detailed control of the pressure IDs.
https://slurm.schedmd.com/job_array.html

def check_power_requirements(gpu_power, cpu_power, psu_watts):
    """Check if PSU can handle the system power requirements"""
    total_power = (gpu_power + cpu_power) * 1.5  # Adding 50% overhead for other components
    return psu_watts >= total_power

def check_case_compatibility(gpu_length, case_max_length):
    """Check if GPU fits in the case"""
    return gpu_length <= case_max_length

def check_cpu_motherboard_compatibility(cpu_socket, motherboard_socket):
    """Check if CPU and motherboard sockets match"""
    return cpu_socket == motherboard_socket

def check_motherboard_case_compatibility(motherboard_form_factor, case_supported_form_factors):
    """Check if motherboard form factor is supported by the case"""
    return motherboard_form_factor in case_supported_form_factors

def get_compatible_components(selected_gpu, components):
    """Get all compatible components based on selected GPU"""
    compatible_components = {
        'motherboards': [],
        'cpus': [],
        'ram': [],
        'psus': [],
        'cases': [],
        'coolers': []
    }
    
    # Filter PSUs based on power requirements
    for psu in components['psus']:
        if psu['watts'] >= selected_gpu['power'] * 1.5:
            compatible_components['psus'].append(psu)
            
    # Filter cases based on GPU length
    for case in components['cases']:
        if case['max_gpu_length'] >= selected_gpu['length']:
            compatible_components['cases'].append(case)
            
    # Add all RAM and coolers (assumed compatible)
    compatible_components['ram'] = components['ram']
    compatible_components['coolers'] = components['coolers']
    
    # Filter motherboards and CPUs based on socket compatibility
    for motherboard in components['motherboards']:
        for cpu in components['cpus']:
            if cpu['socket'] == motherboard['socket']:
                if motherboard not in compatible_components['motherboards']:
                    compatible_components['motherboards'].append(motherboard)
                if cpu not in compatible_components['cpus']:
                    compatible_components['cpus'].append(cpu)
                    
    return compatible_components

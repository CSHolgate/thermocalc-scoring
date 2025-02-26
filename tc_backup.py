import numpy as np 
import pandas as pd 
from tc_python import *
import argparse
import json

class calc():
    """
    My goal is to somehow accept an argument from shell (command line) that looks
    and functions like a dictionary. Not sure how to do that now, but I will move forward
    assuming that it is possible. 

    INPUTS:
      - The global composition (given as a dictionary with the element as the key and
        the concentration as the value). This global composition represents the 
        mixed composition of the BCC and the B2 predicted by the language model
        and also captures the relative proportion of each.

    For outputs, I am envisioning this class wrapping a few different functions each with their own output.
    Functions and outputs:
      - Thermo-Calc: This will output a table in long-form with the calculation results.
      - Thermo-Calc Confidence Score: This will output some number(s) that detail how much faith
                                      we should put into the Thermo-Calc results
      - Reward function: This would reference the TC results and the confidence score to assign some
                         reward to the model.
    """

    def __init__(self, globalcomp):
        """
        INPUT: globalcomp should be a dictionary, with element symbol as the key and concentration as the value.
        """

        self.globalcomp = globalcomp
        pass

    def ThermoCalc(self, database='TCHEA7'):
        # Create an array of temperatures. I'm setting this up to be non-uniformly spaced because we'll care more
        # about high temperatures than low (to calculate when BCC and B2 lose their stability).
        Temps = np.append(np.array([100, 500, 800, 900, 1000])+273.15, np.arange(1100,2050,50)+273.15)
        phaselist = [] # Create a new empty list to append to.

        with TCPython() as session:
            elements = list(self.globalcomp.keys()) # Extract out the elements from the global composition dictionary
            system = session.select_database_and_elements(database, elements).get_system() # Set the data base and elements present
            calc = system.with_single_equilibrium_calculation(False, elements) # Create a single equilibrium calculation
            
            for temp in Temps: # Run a calculation for each temperature we care about
                try: # sometimes an individual calculation fails. If this happens we don't want to kill everything
                    (calc.
                     set_condition('P', 100000).
                     set_condition('T', temp)
                    )

                    for element in elements: # Set the concentration of each element from the global composition
                        calc.set_condition(f"N({element})", self.globalcomp[element])
                    
                    calc_result = calc.calculate() # This actually runs the TC calculation

                    # Get a list of all the stable phases for this condition
                    stablephases = calc_result.get_stable_phases()

                    # Check if BCC_B2 is ordered or not
                    is_ordered = np.nan # reset the "is ordered" flag for each calculation wrt temperature
                    for phase in stablephases:
                        if 'BCC_B2' in phase:
                            # If the two sites have a concentration difference of > 0.05, change order flag to 1
                            if np.abs(calc_result.get_value_of(f"Y({phase}, {elements[0]}#1)") - 
                                    calc_result.get_value_of(f"Y({phase}, {elements[0]}#2)")) > 0.05:
                                is_ordered = 1
                            # If the two sites are close to eachother, set the order flag to 0
                            elif np.abs(calc_result.get_value_of(f"Y({phase}, {elements[0]}#1)") - 
                                    calc_result.get_value_of(f"Y({phase}, {elements[0]}#2)")) < 0.05:
                                is_ordered = 0

                    for phase in stablephases:
                        a = np.nan # reset lattice parameter
                        phasequantity = calc_result.get_value_of(ThermodynamicQuantity.mole_fraction_of_a_phase(phase))
                        
                        if "BCC_B2" in phase:
                            # BCC has 2 atoms per unit cell, so given a molar volume, we can
                                # convert to a lattice parameter via (Vm * 2 / 6.022e23)
                            molar_volume = calc_result.get_value_of(f"VM({phase})")
                            a = ((molar_volume * 2 / 6.022e23)**(1/3)) * 1e10 # Value in Å


                        phaselist.append({"Global Composition": self.globalcomp, 
                                          "Temperature": temp,
                                          'Phase': phase,
                                          'Quantity': phasequantity,
                                          'IsOrdered': is_ordered,
                                          'LatticeParameter': a
                                          })
                    print(temp) # For testing only
                    
                except:
                    phaselist.append({"Global Composition": self.globalcomp, 
                                      "Temperature": temp,
                                      'Phase': np.nan,
                                      'Quantity': np.nan,
                                      'IsOrdered': np.nan,
                                      'LatticeParameter': np.nan
                                      })
                    pass
        
        self.phaselist = phaselist
        self.df = pd.DataFrame(phaselist)




def main():
    parser = argparse.ArgumentParser(description="Run Thermo-Calc calculations with a given global composition.")
    parser.add_argument("globalcomp", type=str, help="JSON string representing the global composition dictionary.")

    args = parser.parse_args()

    try:
        # Parse JSON input
        globalcomp_dict = json.loads(args.globalcomp)

        # Ensure it is a dictionary
        if not isinstance(globalcomp_dict, dict):
            raise ValueError("Provided global composition must be a dictionary.")

        # Run calculation
        results = calc(globalcomp_dict)
        results.ThermoCalc()

        # Print results (or save them as needed)
        print(results.df)

    except json.JSONDecodeError:
        print("Error: globalcomp must be a valid JSON string. Example: '{\"Fe\": 0.5, \"Ni\": 0.5}'")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
    ### EXAMPLE USE from Command Prompt:
    ### python tc.py "{""Nb"":25, ""Al"":75}"
    ### Note: double quotes are (annoyingly) important apparently.
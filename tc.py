import numpy as np 
import pandas as pd 
from tc_python import *
import argparse
import json
from itertools import combinations

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
        self.Temps = np.append(np.array([100, 500, 800, 900, 1000])+273.15, np.arange(1100,2050,50)+273.15)
        phaselist = [] # Create a new empty list to append to.

        with TCPython() as session:
            elements = list(self.globalcomp.keys()) # Extract out the elements from the global composition dictionary
            system = session.select_database_and_elements(database, elements).get_system() # Set the data base and elements present
            calc = system.with_single_equilibrium_calculation(False, elements) # Create a single equilibrium calculation
            
            for temp in self.Temps: # Run a calculation for each temperature we care about
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

                    for phase in stablephases:
                        is_ordered = np.nan # reset the "is ordered" flag for each phase
                        a = np.nan # reset lattice parameter

                        # Measure how much of the phase we have
                        phasequantity = calc_result.get_value_of(ThermodynamicQuantity.mole_fraction_of_a_phase(phase)) 

                        if 'BCC_B2' in phase:
                            # Extract the lattice parameter of the phase
                            # BCC has 2 atoms per unit cell, so given a molar volume, we can
                            # convert to a lattice parameter via (Vm * 2 / 6.022e23)
                            molar_volume = calc_result.get_value_of(f"VM({phase})")
                            a = ((molar_volume * 2 / 6.022e23)**(1/3)) * 1e10 # Value in Å

                            # Check if the phase is ordered
                            # If the two sites have a concentration difference of > 0.05, change order flag to 1
                            if np.abs(calc_result.get_value_of(f"Y({phase}, {elements[0]}#1)") - 
                                    calc_result.get_value_of(f"Y({phase}, {elements[0]}#2)")) > 0.05:
                                is_ordered = int(1)
                            # If the two sites are close to eachother, set the order flag to 0
                            elif np.abs(calc_result.get_value_of(f"Y({phase}, {elements[0]}#1)") - 
                                    calc_result.get_value_of(f"Y({phase}, {elements[0]}#2)")) < 0.05:
                                is_ordered = int(0)

                        # Save the results
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

    def confidence(self):
        # Note that this function is currently only written to handle the refractories. If we want to do
        # FCC+L12 we can also implement that.

        # First lets import the list of critically and tentatively assessed ternaries
        crit = pd.read_csv('./tchea7-criticalassessedternaries.csv') # these ternaries are the most accurate
        tent = pd.read_csv('./tchea7-tentativeassessedternaries.csv') # these are less accurate
        all_ternaries = pd.concat([crit, tent]).reset_index() # This combines both in case we don't care to distinguish.
        tchea_elements = ['Al', 'B', 'C', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Ir', 
                          'Mn', 'Mo', 'N', 'Nb', 'Ni', 'Re', 'Rh', 'Ru', 'Si', 
                          'Sn', 'Ta', 'Ti', 'V', 'W', 'Y', 'Zn', 'Zr'] # This is a list of all elements in the database
        
        elements = list(self.globalcomp.keys()) # Gather the list of elements in the candidate alloy

        # Define a function to count how many ternaries are exist in a predifined list
        def check_elements_in_df(df, elements_tuple):
            elements_set = set(elements_tuple)
            for idx, row in df.iterrows():
                row_elements = set([row['Element1'], row['Element2'], row['Element3']])
                if row_elements == elements_set:
                    return True
            return False

        # First check if we are only dealing with two elements. 
        # If so, we'll just assume a perfect score.
        if len(elements) <=2:
            self.confidence_score = 1 # assign a perfect score
        
        # Otherwise we will deal with the ternaries
        else:
            # Generate a list of ternaries 
            alloy_ternaries = list(combinations(elements, 3))
            tent_assessed_bool = [] # Create an empty list for the number of tentatively assessed systems
            crit_assessed_bool = [] # Create an empty list for the number of critically assessed systmes
            for ternary in alloy_ternaries:
                tent_assessed_bool.append(check_elements_in_df(tent, ternary))
                crit_assessed_bool.append(check_elements_in_df(crit, ternary))
            tent_assessed = sum(tent_assessed_bool)
            crit_assessed = sum(crit_assessed_bool)

        """
        Neal: This would be the place I think to build in some confidence score as a result
        of the assessed ternaries. One thought is to take some function like:

        confidence_score = frac_critically_assessed + 0.5 * frac_tentatively_assessed

        This would effectively count tentatively assessed systems less. A completely unassessed system
        would receive a score of 0, whereas a perfect system would get 1.

        An issues with this approach:
        We will probably run into cases (like Nb-Ti-Ru) where there is no assessed ternaries.
        This would receive a score of 0. But so would something like (Nb-Ti-Ru-Y). But in the
        first case there would only be one missing ternary, whereas in the second there is four
        missing ternaries. This may mean that we would want to add in negative score for missed
        ternaries. But this would require the scoring metric to be able to handle negative values.
        Neal and I talked about this issue for a bit, but I think we need to think about this some
        more. A negative score could be implemented as:

        confidence_score = frac_critically_assessed + 0.5 * frac_tent_assessed - frac_not_assessed

        Then the score would be bounded by -1 to 1. The key point here (I think) would be what prefactor
        do tentatively assessed systems get?
        """
        
        ### TESTING REGION TKTK ###
        print('Number of Critically Assessed Ternaries: ', crit_assessed)
        print('Fraction of Critically Assessed Ternaries: ', crit_assessed/len(alloy_ternaries))
        print()
        print('Number of Tentatively Assessed Ternaries: ', tent_assessed)
        print('Fraction of Tentatviely Assessed Ternaries: ', tent_assessed/len(alloy_ternaries))
        print()
        print('Total Number of Assessed Ternaries: ', crit_assessed + tent_assessed)
        print('Fraction of Assessed Ternaries: ', (crit_assessed + tent_assessed)/len(alloy_ternaries))
        ### END TESTING REGION ###

        

    def scoring(self):
        # Goal is to take some TC results and check whether or not the alloy forms BCC and B2 together.
        # Should also check for any other phases that we don't want.
        # Should ideally check how long BCC and B2 are stable for (i.e., what temp they disappear at)
        # Should check for misfit between the phases
        # Then somehow we need to do the scoring for this.

        # Filter the datasets to extract just the rows with BCC and B2s
        bccs = self.df[(self.df['Phase'].str.contains('BCC_B2'))&(self.df['IsOrdered']==0)]
        b2s = self.df[(self.df['Phase'].str.contains('BCC_B2'))&(self.df['IsOrdered']==1)]

        # Check whether BCC or B2 form at all:
        # One issue with the if... else... below is that it doesn't account for both phases forming at the same temperature.
        # Should we check this for each temperature? If so we can build up a total score or something?
        bcc_forms = len(bccs) > 0
        b2_forms = len(b2s) > 0
        
        ### TESTING REGION TKTK ###
        if bcc_forms and b2_forms:
            print('Alloy forms BCC and B2')
        ### END TESTING REGION ###
            
        # Create a new dataframe with metrics for scoring
        scoring_list = []
        
        # We don't want to iterate over temperatures that didn't converge. So lets get rid of those
        temps_that_worked = self.df.dropna(subset=['Phase']).Temperature.unique()

        for temp in temps_that_worked:
            # reset flags
            phase_status = np.nan
            amount_bcc = np.nan
            amount_b2 = np.nan
            bccb2_quant = np.nan
            a_bcc = np.nan
            a_b2 = np.nan
            a_mismatch = np.nan

            # Check if there is BCC, B2, both, or neither at the temperature
            # and quantify each phase
            is_bcc = len(bccs[bccs.Temperature == temp]) > 0
            is_b2 = len(b2s[b2s.Temperature == temp]) > 0
            if is_bcc and is_b2:
                phase_status = 'BCC+B2'
                amount_bcc = sum(bccs[bccs.Temperature == temp].Quantity)
                amount_b2 = sum(b2s[b2s.Temperature == temp].Quantity)
                bccb2_quant = amount_bcc + amount_b2
            elif is_bcc:
                phase_status = 'BCC'
                amount_bcc = sum(bccs[bccs.Temperature == temp].Quantity)
                bccb2_quant = amount_bcc
            elif is_b2:
                phase_status = 'B2'
                amount_b2 = sum(b2s[b2s.Temperature == temp].Quantity)
                bccb2_quant = amount_b2
            else:
                phase_status = 'No BCC or B2'
                bccb2_quant = 0

            # Check for lattice mismatch
            if is_bcc:
                a_bcc = np.mean(bccs[bccs.Temperature == temp].LatticeParameter)
            if is_b2:
                a_b2 = np.mean(b2s[b2s.Temperature == temp].LatticeParameter)
            # else should be np.nan, which is set at the start of the loop
            a_mismatch = (2*(a_b2 - a_bcc))/(a_b2 + a_bcc)



            scoring_list.append({'Temperature':temp, 'Phases':phase_status, 
                               'QuantBCC': amount_bcc, 'QuantB2': amount_b2,'TotalBCCandB2': bccb2_quant, 
                               'LatticeMismatch':a_mismatch})
        
        self.scoring_df = pd.DataFrame(scoring_list)
            


        # Extract out the maximum temperature of each phase:
        max_bcc_temp = bccs.Temperature.max()
        max_b2_temp = b2s.Temperature.max()
        # Function to score this TKTK
        ### TESTING REGION ###
        print("We want the BCC to be more stable than the B2 phase")
        print("Temperature difference between BCC and B2: ", max_bcc_temp - max_b2_temp)
        ### END TESTING REGION ###






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
        
        # Run scoring function
        results.scoring()
        print(results.scoring_df)

        # Run Confidence function
        results.confidence()

    except json.JSONDecodeError:
        print("Error: globalcomp must be a valid JSON string. Example: '{\"Fe\": 0.5, \"Ni\": 0.5}'")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
    ### EXAMPLE USE from Command Prompt:
    ### python tc.py "{""Nb"":25, ""Al"":75}"
    ### Note: double quotes are (annoyingly) important apparently.
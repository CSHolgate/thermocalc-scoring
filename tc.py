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
        """
        The ThermoCalc function is here to actually run the Thermo-Calc
        calculations and create a dataframe of results, which is written to a
        object.

        INPUTS:
            - The user can optionally input a database. By default, this is set
              to the state-of-the-art database for high entropy alloys (TCHEA7).
              If we go down the route of Ni-superalloys this could be set to
              'TCNi12'.

        OUTPUTS:
            - self.df: A pandas dataframe (in long form) with the key results
              from the equilibrium calculation. Right now this contains columns
              on:
                - The global alloy composition (for future reference)
                - The calculation temperature (in K)
                - The predicted equilibrium phase(s)
                - The predicted phase quantity (in mole fraction)
                - If the phase is BCC or B2, the following columns get non-nan
                  values:
                    - Is the phase ordered {0: Disordered BCC, 1: Ordered B2}
                    - The lattice parameter of the phase (in Å)
        """

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
                     set_condition('P', 100000). # Set pressure
                     set_condition('T', temp) # Set temperature
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

                        # Extract the phase composition
                        phasecomposition = {} # Create an empty dictionary to append to
                        for element in elements:
                            phasecomposition[element] = calc_result.get_value_of(ThermodynamicQuantity.composition_of_phase_as_mole_fraction(phase, element))
                        # phasecomposition = calc_result.get_value_of(ThermodynamicQuantity.composition_of_phase_as_mole_fraction('All'))
                        # phasecomposition = calc_result.get_value_of(ThermodynamicQuantity.composition_of_phase_as_mole_fraction(phase, "All"))


                        # ThermoCalc annoying does not clearly output whether a phase is truly BCC or B2
                        # but rather uses a combined name for each. We need to extract whether this
                        # phase is BCC or B2. 
                        if 'BCC_B2' in phase:
                            # Extract the lattice parameter of the phase
                            # BCC has 2 atoms per unit cell, so given a molar volume, we can
                            # convert to a lattice parameter via:  a = (Vm * 2 / 6.022e23)
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
                                          'LatticeParameter': a,
                                          'PhaseComposition': phasecomposition
                                          })
                    print(temp) # For testing only, just to get an idea of how fast the calculations run
                    
                except Exception as e:
                    print('Exception:', e)
                    phaselist.append({"Global Composition": self.globalcomp, 
                                      "Temperature": temp,
                                      'Phase': np.nan,
                                      'Quantity': np.nan,
                                      'IsOrdered': np.nan,
                                      'LatticeParameter': np.nan,
                                      'PhaseComposition': np.nan
                                      })
                    pass
        
        self.df = pd.DataFrame(phaselist) # Save the results as a pandas dataframe object

    def confidence(self):
        """
        The confidence function will provide some quantified amount of "trust"
        we should place in the Thermo-Calc results based on how many of the
        systems are assessed (critically or tentatively) in the database.

        INPUTS:
            - The global composition dictionary object is called from __init__

        OUTPUTS:
            - self.confidence_score: a float bounded by (-inf, 1). This idea is
              a work in progress. We should discuss the best way to handle this
              score.
        """
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
            for _, row in df.iterrows():
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
            self.alloy_ternaries = alloy_ternaries
            tent_assessed_bool = [] # Create an empty list for the number of tentatively assessed systems
            crit_assessed_bool = [] # Create an empty list for the number of critically assessed systmes
            for ternary in alloy_ternaries:
                tent_assessed_bool.append(check_elements_in_df(tent, ternary))
                crit_assessed_bool.append(check_elements_in_df(crit, ternary))
            self.tent_assessed = sum(tent_assessed_bool)
            self.crit_assessed = sum(crit_assessed_bool)

            # Assign a confidence score
            ### WE NEED TO WORK ON THIS (SEE BELOW)
            self.confidence_score = ((self.crit_assessed/len(alloy_ternaries)) 
                                     + (0.5 * self.tent_assessed/len(alloy_ternaries)) 
                                     - (len(alloy_ternaries)-self.crit_assessed-self.tent_assessed))

        """
        Neal: We should talk more (probably with Sam and Satanu) about how to do
        this scoring.

        The key issue is that we will probably run into cases (like Nb-Ti-Ru)
        where there are no assessed ternaries in the database. A simple approach
        of just counting the positive hits, weighing the tentatively assessed
        systems worse, like:
        
        confidence_score = frac_critically_assessed + 0.5 * frac_tentatively_assessed
        
        would assign a score of 0. A perfect system would get 1. This sounds
        good, but consider something like (Nb-Ti-Ru-Y). This system has four
        ternaries and all are unassessed. So in the previous case there is one
        missing ternary but here there are four. With the above equation both
        would receive the same score (of 0) which doesn't feel right. There is a
        lot more extrapolation happening for the case with four missing
        ternaries.
         
        This may mean that we would want to add in a **not normalized** negative
        score for missed ternaries. But this would require the scoring metric to
        be able to handle (potentially arbitrary) negative values. And
        realistically, given how incomplete the databases are, I suspect it
        would make most of the scores negative. Another option is to just go
        unbounded in the score, but I would guess that would also cause issues.
        Anyway, this now obnoxiously long comment will serve as a marker for
        discussion!
        """
        
        ### TESTING REGION TKTK ###
        print('Number of Critically Assessed Ternaries: ', self.crit_assessed)
        print('Fraction of Critically Assessed Ternaries: ', self.crit_assessed/len(alloy_ternaries))
        print()
        print('Number of Tentatively Assessed Ternaries: ', self.tent_assessed)
        print('Fraction of Tentatviely Assessed Ternaries: ', self.tent_assessed/len(alloy_ternaries))
        print()
        print('Total Number of Assessed Ternaries: ', self.crit_assessed + self.tent_assessed)
        print('Fraction of Assessed Ternaries: ', (self.crit_assessed + self.tent_assessed)/len(alloy_ternaries))
        ### END TESTING REGION ###

        

    def scoring(self):
        """
        The scoring function will take in Thermo-Calc results for a candidate
        alloy and calculate a score that can be used for preference learning. To
        do this, a decent amount of post-processing must take place.

        Note: The scoring function is TKTK.

        INPUTS:
            - self.df (The pandas dataframe containing the output from
              Thermo-Calc)

        OUTPUTS:
            - self.scoring_df: A dataframe of processed data for scoring. This
              probably does not need to be an object eventually, but for now I
              am keeping this output for any troubleshooting.
            - self.score: TKTK. The score used to rank the LM's alloy
              prediction.
        """

        # Filter the datasets to extract just the rows with BCC and B2s
        bccs = self.df[(self.df['Phase'].str.contains('BCC_B2'))&(self.df['IsOrdered']==0)]
        b2s = self.df[(self.df['Phase'].str.contains('BCC_B2'))&(self.df['IsOrdered']==1)]

        # Check whether BCC or B2 form at all: One issue with the two code lines
        #below is that it doesn't account for both phases forming at the same
        # temperature. Should we check this for each temperature? If so we can
        # build up a total score or something?
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
            # Check if any conditions form multiple bccs or b2s at a single temp
            # is_multiple_bcc = len(bccs[bccs.Temperature == temp]) > 1
            # is_multiple_b2 = len(b2s[b2s.Temperature == temp]) > 1
            if is_bcc and is_b2:
                phase_status = 'BCC+B2'
                amount_bcc = sum(bccs[bccs.Temperature == temp].Quantity)
                amount_b2 = sum(b2s[b2s.Temperature == temp].Quantity)
                bccb2_quant = amount_bcc + amount_b2
                bcc_output = bccs.loc[bccs.Temperature==temp, 'PhaseComposition'].to_list()
                b2_output = b2s.loc[b2s.Temperature==temp, 'PhaseComposition'].to_list()
            elif is_bcc:
                phase_status = 'BCC'
                amount_bcc = sum(bccs[bccs.Temperature == temp].Quantity)
                bccb2_quant = amount_bcc
                bcc_output = bccs.loc[bccs.Temperature==temp, 'PhaseComposition'].to_list()
                b2_output = np.nan
            elif is_b2:
                phase_status = 'B2'
                amount_b2 = sum(b2s[b2s.Temperature == temp].Quantity)
                bccb2_quant = amount_b2
                bcc_output = np.nan
                b2_output = b2s.loc[b2s.Temperature==temp, 'PhaseComposition'].to_list()
            else:
                phase_status = 'No BCC or B2'
                bccb2_quant = 0
                bcc_output = np.nan
                b2_output = np.nan

            # Check for lattice mismatch
            if is_bcc:
                a_bcc = np.mean(bccs[bccs.Temperature == temp].LatticeParameter)
            if is_b2:
                a_b2 = np.mean(b2s[b2s.Temperature == temp].LatticeParameter)
            # else should be np.nan, which is set at the start of the loop
            a_mismatch = (2*(a_b2 - a_bcc))/(a_b2 + a_bcc)



            scoring_list.append({'Temperature':temp, 'Phases':phase_status, 
                               'QuantBCC': amount_bcc, 'QuantB2': amount_b2,'TotalBCCandB2': bccb2_quant, 
                               'LatticeMismatch':a_mismatch,
                               'BCC_Output':bcc_output, 'B2_Output':b2_output})
        
        self.scoring_df = pd.DataFrame(scoring_list)
        
        # self.score TKTK


        ### TESTING REGION ###
        # Extract out the maximum temperature of each phase:
        max_bcc_temp = bccs.Temperature.max()
        max_b2_temp = b2s.Temperature.max()
        print("We want the BCC to be more stable than the B2 phase")
        print("Temperature difference between BCC and B2: ", max_bcc_temp - max_b2_temp)
        ### END TESTING REGION ###


        """
        Neal: Let me know how you want to continue with the scoring dataframe. I think you'd be the best
        person to build the actually scoring function—hopefully the info above is everything that you need to put that
        together. It captures whether or not BCC and/or B2 forms, their stable temperatures, the amount of each phase (and
        therefore the amount of non-BCC/B2 phases) and it gives the coherency between the BCC and B2 phase. 

        Let me know if you need any other information though!
        """






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
        print('Thermo-Calc Confidence Score is: ', results.confidence_score)

    except json.JSONDecodeError:
        print("Error: globalcomp must be a valid JSON string. Example: '{\"Fe\": 0.5, \"Ni\": 0.5}'")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    # To print to file, uncomment block below
    # import sys
    # sys.stdout.reconfigure(encoding='utf-8')
    # with open('sample_output.txt', 'w', encoding='utf-8') as f:
    #     sys.stdout = f
    #     main()
    
    # To print to terminal, uncomment this:
    main()
    
    ### EXAMPLE USE from Command Prompt:
    ### python tc.py "{""Nb"":25, ""Al"":75}"
    ### Note: double quotes are (annoyingly) important apparently.
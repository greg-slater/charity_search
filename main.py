
import pymatch.keyword_matching as keyword_matching
import pydash.dashboard as dashboard

# STEP ONE ------------------------------------------------------------------------//

answer = input('If you would like to run the keyword matching please enter "y":  ')

if answer.lower() == 'y':

    print('run matching')

    keyword_matching.run()

    print('matching complete')


# STEP TWO ------------------------------------------------------------------------//

answer2 = input('If you would like to run the dashboard please enter "y":  ')

if answer2.lower() == 'y':

    print('run dashboard')

    dashboard.run()
